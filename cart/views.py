from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import ProductVariant
from django.http import HttpResponse
from django.template.loader  import render_to_string
from django.views.decorators.http import require_POST

def add_to_cart(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        quantity   = int(request.POST.get("quantity", 1))

        if not variant_id:
            return redirect("view_cart")  # don't crash on blank

        variant = get_object_or_404(ProductVariant, id=variant_id)

        # create session key if needed
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # get or create the user's Cart
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

        # get or create CartItem
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=variant.product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect("view_cart")

    return redirect("view_cart")


def view_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart = Cart.objects.filter(session_key=session_key).first()
    cart_items = cart.items.all() if cart else []
    total = sum(item.get_total_price() for item in cart_items)

    return render(request, "view_cart.html", {
        "cart_items": cart_items,
        "total": total
    })

def view_cart_total(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(cart__session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)
    html = render_to_string("cart_total.html", {"total": total})
    return HttpResponse(html)


def htmx_remove_from_cart(request, item_id):
    if request.method == "DELETE":
        try:
            item = CartItem.objects.get(id=item_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass

        # Calculate new total
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(cart__session_key=session_key)
        total = sum(item.get_total_price() for item in cart_items)

        # Return empty response, but trigger the event for JS to update the total
        response = HttpResponse("")
        response["HX-Trigger"] = f'{{"cartTotalUpdated": {{"total": "{total:.2f}"}}}}'
        response["Content-Type"] = "text/html"
        return response
    


@require_POST
@require_POST
def htmx_update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    try:
        new_quantity = int(request.POST.get("quantity", 1))
        item.quantity = max(new_quantity, 1)
        item.save()
    except ValueError:
        pass

    # Recalculate grand total
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(cart__session_key=session_key)
    total = sum(i.get_total_price() for i in cart_items)

    html = render_to_string("cart_row.html", {"item": item}, request=request)

    response = HttpResponse(html)
    response["HX-Trigger"] = f'{{"cartTotalUpdated": {{"total": "{total:.2f}"}}}}'
    return response
