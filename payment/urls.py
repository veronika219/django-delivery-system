from django.urls import path
from .views import liqpay, payment_success, payment_callback

urlpatterns = [
    path("liqpay/<int:order_id>/", liqpay, name="liqpay"),
    path("success/", payment_success, name="payment_success"),
    path("callback/", payment_callback, name="payment_callback"),
]
