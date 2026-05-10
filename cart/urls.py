from django.urls import path
from cart.views import add_to_cart

path(
    'cart/add/<int:pproduct_id>/', add_to_cart, name="add_to_cart"
)