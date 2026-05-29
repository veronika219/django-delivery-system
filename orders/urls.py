from django.urls import path
from .views import checkout, success, cancel_order


urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("success/", success, name="success"),
    path("orders/cancel/<int:order_id>/", cancel_order, name="cancel_order"),

]