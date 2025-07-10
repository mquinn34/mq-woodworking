
from django.urls import path
from . import views
from .views import add_to_cart, view_cart, htmx_remove_from_cart, htmx_update_quantity, create_checkout_session

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('htmx/remove/<int:item_id>/', htmx_remove_from_cart, name='htmx_remove_from_cart'),
    path('htmx/update/<int:item_id>/', htmx_update_quantity, name='htmx_update_quantity'),
    path('cart/total/', views.view_cart_total, name='view_cart_total'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]