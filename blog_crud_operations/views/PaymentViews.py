from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from blog_crud_operations.models import Payment
import json
import traceback

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"})
        
    try:
        # data = request.POST
        data = json.loads(request.body)  # parse JSON body
        amount = int(data.get("amount", 1000))
        currency = data.get("currency", "usd")

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )


        transaction_id = intent.id
        # Save Payment in database
        Payment.objects.create(
            amount = amount,
            currency = currency,
            status = "pending",
            transaction_id = transaction_id,
        )

        # return JsonResponse({"Client_secret": intent.client_secret})
        return JsonResponse({"Client_secret": transaction_id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
            

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sign_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        ## Skip Signature Verification for local testing
        # event  = stripe.Webhook.construct_event(
        #     payload, sign_header, endpoint_secret
        # )
        event = json.loads(request.body)
    except Exception as e:
        print("Webhook error:", str(e))
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)


    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        Payment.objects.filter(transaction_id= intent['id']).update(status='succeeded')
    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        Payment.objects.filter(transaction_id=intent['id']).update(status='failed')

    return JsonResponse({"status": "success"})


@csrf_exempt
def refund_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"})
    
    try:
        data = json.loads(request.body)
        transaction_id = data.get("transaction_id")

        if not transaction_id:
            return JsonResponse({"error": "transaction_id is required"}, status=400)
        
        #Create a Refund
        stripe.Refund.create(payment_intent=transaction_id)

        #Update Payment Record
        Payment.objects.filter(transaction_id=transaction_id).update(status="refunded")

        return JsonResponse({"status": "refunded"})
    except Exception as e:
        return JsonResponse({"error" : str(e)}, status=500)

