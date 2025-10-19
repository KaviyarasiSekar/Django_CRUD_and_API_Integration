from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from blog_crud_operations.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"})
        
    try:
        data = request.POST
        amount = int(data.get("amount", 1000))
        currency = data.get("currency", "usd")

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )


        # Save Payment in database
        Payment.objects.create(
            amount = amount,
            currency = currency,
            status = "pending",
            transaction_id = intent.id,
        )

        return JsonResponse({"Client_secret": intent.client_sectet})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
            
