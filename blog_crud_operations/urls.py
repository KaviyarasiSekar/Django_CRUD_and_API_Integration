from django.urls import path
from .views import BlogListCreateView, BlogDetailView
from .views import create_payment, stripe_webhook, refund_payment

app_name = "blog_crud_operations"

urlpatterns = [
    path("blog_crud_operations/", BlogListCreateView.as_view(), name="blog_list_create"),
    path("blog_crud_operations/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),

    path("create-payment/", create_payment, name="create_payment"),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('refund-payment/', refund_payment, name='refund-payment'),
]
