from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.cart import Cart


def checkout(request):

    cart = Cart(request)

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.customer = request.user

            order.save()

            for product in cart.get_products():

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart.cart[str(product.id)]['quantity'],
                    price=product.price
                )

            cart.clear()

            return redirect('success')

    else:
        form = CheckoutForm()

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart': cart
        }
    )


def success(request):

    return render(
        request,
        'orders/success.html'
    )

@login_required
def profile_view(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    return render(
        request,
        'users/profile.html',
        {
            'orders': orders
        }
    )
