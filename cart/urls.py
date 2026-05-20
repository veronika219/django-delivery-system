from django.urls import path
from .views import cart_detail, ajax_remove, ajax_increase, ajax_decrease

urlpatterns = [
    path("", cart_detail, name="cart"),
    path("ajax/increase/<int:product_id>/", ajax_increase, name="ajax_increase"),
    path("ajax/decrease/<int:product_id>/", ajax_decrease, name="ajax_decrease"),
    path("ajax/remove/<int:product_id>/", ajax_remove, name="ajax_remove"),
]
