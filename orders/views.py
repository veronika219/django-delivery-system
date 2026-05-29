from django.shortcuts import render, redirect, get_object_or_404

from .forms import CheckoutForm
from .models import Order
from .services import create_order, send_order_email
from cart.cart import Cart
from core.decorators import role_required, customer_or_guest_required


def get_initial(user):
    if not user.is_authenticated:
        return {}

    return {
        "name": user.full_name,
        "phone": user.phone or "+380",
        "email": user.email,
        "address": user.address,
    }


@customer_or_guest_required
def checkout(request):

    cart = Cart(request)

    if not cart.get_cart():
        return redirect("menu")

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = create_order(request.user, form, cart)
            send_order_email(order)

            # 🔥 PAYMENT FLOW
            if order.payment_method == "ONLINE":
                return redirect("liqpay", order.id)

            return redirect("success")

    else:
        form = CheckoutForm(initial=get_initial(request.user))


    return render(request, "orders/checkout.html", {
        "form": form,
        "cart": cart
    })


@role_required("customer")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    order.cancel(request.user)

    return redirect("profile")

@customer_or_guest_required
def success(request):
    return render(request, "orders/success.html")

