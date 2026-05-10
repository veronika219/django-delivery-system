from django.shortcuts import render
from django.conf import settings
from liqpay import LiqPay

def liqpay(request, order_id):
    liqpay = LiqPay(
        settings.LIQPAY_PUBLIC_KEY,
        settings.LIQPAY_PRIVATE_KEY
    )

    params = {
        'action': 'pay',
        'amount': 100,
        'currency': 'UAN',
        'description': 'Restaurant Order',
        'order_id': str(order_id),
        'version': 3,
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