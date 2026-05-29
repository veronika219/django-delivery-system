from django.urls import path
from .views import liqpay, payment_callback

urlpatterns = [
    path("liqpay/<int:order_id>/", liqpay, name="liqpay"),
    path("callback/", payment_callback, name="payment_callback"),
]
