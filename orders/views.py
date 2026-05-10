from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import OrderItem
from cart.cart import Cart
from menu.models import Product

def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save()

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
        request,'orders/checkout.html',
        {
            'form': form,
            'cart': cart
        }
    )