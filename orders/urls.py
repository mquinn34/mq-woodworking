from django.urls import path
from .views import StripeWebhookView, OrderListView, toggle_order_status
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("webhook/", csrf_exempt(StripeWebhookView.as_view()), name="stripe_webhook"),
    path("dashboard/", OrderListView.as_view(), name="order_list"),
    path('order/<int:pk>/status/', toggle_order_status, name='toggle_order_status'),
]
