import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from cart.models import CartItem, Cart
from .models import Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    if not request.session.session_key:
        request.session.create()
        request.session.modified = True
        request.session.save()

    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(cart__session_key=session_key)

    if not cart_items:
        return JsonResponse({"error": "No items in cart"}, status=400)

    order_metadata = []
    line_items = []

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                    'description': f"Wood: {item.variant.wood_type}, Size: {item.variant.size}",
                },
                'unit_amount': int(item.get_total_price() * 100),
            },
            'quantity': item.quantity,
        })

        order_metadata.append({
            'product_name': item.product.name,
            'wood_type': item.variant.wood_type,
            'size': item.variant.size,
            'quantity': item.quantity,
            'price': float(item.get_total_price()),
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
        customer_email="quinnm34@gmail.com",  # Replace with real collected email
        shipping_address_collection={"allowed_countries": ["US"]},
        client_reference_id=session_key,
        metadata={
            'order': json.dumps(order_metadata),
            'session_key': session_key,
        }
    )

    return JsonResponse({'id': checkout_session.id})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            metadata = session.get('metadata', {})
            session_key = metadata.get('session_key')
            order_data = json.loads(metadata.get('order', '[]'))

            customer = session.get('customer_details', {})
            address = customer.get('address', {})
            full_address = f"{address.get('line1', '')}, {address.get('city', '')}, {address.get('state', '')} {address.get('postal_code', '')}"

            # Calculate grand total
            grand_total = sum(item['price'] for item in order_data)

            # Create main order
            order = Order.objects.create(
                customer_name=customer.get('name', ''),
                customer_email=customer.get('email', ''),
                shipping_address=full_address,
                total_price=grand_total,
                stripe_session_id=session.get('id')
            )

            # Create order items
            for item in order_data:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['product_name'],
                    wood_type=item['wood_type'],
                    size=item['size'],
                    quantity=item['quantity'],
                    item_price=item['price']
                )

            # Clear cart
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
                if cart:
                    cart.items.all().delete()

        return HttpResponse(status=200)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order_list.html"
    context_object_name = "orders"
    ordering = ['-created_at']


@login_required
def toggle_order_status(request, pk):
    if request.method == "POST":
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get("status")
        if new_status in ["In Progress", "Completed"]:
            order.status = new_status
            order.save()
    return redirect("order_list")
