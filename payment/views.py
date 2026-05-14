import base64
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from liqpay import LiqPay
from orders.models import Order


def liqpay(request, order_id):

    liqpay = LiqPay(
        settings.LIQPAY_PUBLIC_KEY,
        settings.LIQPAY_PRIVATE_KEY
    )

    params = {
        'action': 'pay',
        'amount': '100',
        'currency': 'UAH',
        'description': 'Restaurant Order',
        'order_id': str(order_id),
        'version': '3',
        'sandbox': 1,
        'server_url': 'http://127.0.0.1:8000/payment/callback/',
        'result_url': 'http://127.0.0.1:8000/payment/success/'
    }

    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)

    return render(
        request,
        'payment/payment.html',
        {
            'signature': signature,
            'data': data
        }
    )


def payment_success(request):
    return redirect('success')


def payment_callback(request):

    data = request.POST.get('data')
    signature = request.POST.get('signature')

    liqpay = LiqPay(
        settings.LIQPAY_PUBLIC_KEY,
        settings.LIQPAY_PRIVATE_KEY
    )

    if liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY) == signature:

        decoded = json.loads(base64.b64decode(data))

        order_id = decoded.get('order_id')

        status = decoded.get('status')

        if status == 'success':

            Order.objects.filter(id=order_id).update(
                paid=True
            )

    return HttpResponse('OK')