from django.shortcuts import render, reverse
from django.http import JsonResponse
from menu.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)

    products = []

    for product in cart.get_products():
        qty = cart.cart[str(product.id)]['quantity']

        products.append({
            'product': product,
            'quantity': qty,
            'total': product.price * qty

        })

    return render(request, 'cart/cart.html', {
        'products': products,
        'total_price': cart.get_total_price(),
        'cart_total_item': cart.get_total_items()
    })


def ajax_increase(request, product_id):

    cart = Cart(request)

    cart.add(product_id)

    product = Product.objects.get(id=product_id)

    quantity = cart.cart[str(product_id)]['quantity']

    return JsonResponse({
        'success': True,

        'product_id': product_id,

        'quantity': quantity,

        'item_total': float(product.price * quantity),

        'cart_total_price': float(cart.get_total_price()),

        'cart_total_items': cart.get_total_items(),
    })


def ajax_decrease(request, product_id):

    cart = Cart(request)

    pid = str(product_id)

    if pid not in cart.cart:

        return JsonResponse({
            'success': False
        })

    quantity = cart.cart[pid]['quantity'] - 1

    # DELETE PRODUCT
    if quantity <= 0:

        cart.remove(product_id)

        # EMPTY CART
        if cart.get_total_items() == 0:

            return JsonResponse({
                'success': True,

                'empty_cart': True,

                'redirect_url': reverse('menu'),

                'cart_total_items': 0,

                'cart_total_price': 0,
            })

        return JsonResponse({
            'success': True,

            'removed': True,

            'product_id': product_id,

            'cart_total_items': cart.get_total_items(),

            'cart_total_price': float(cart.get_total_price()),
        })

    # UPDATE PRODUCT
    cart.update(product_id, quantity)

    product = Product.objects.get(id=product_id)

    return JsonResponse({
        'success': True,

        'product_id': product_id,

        'quantity': quantity,

        'item_total': float(product.price * quantity),

        'cart_total_items': cart.get_total_items(),

        'cart_total_price': float(cart.get_total_price()),
    })

def ajax_remove(request, product_id):

    cart = Cart(request)
    cart.remove(product_id)
    print("REMOVE HIT:", product_id)
    total_items = cart.get_total_items()

    return JsonResponse({
        "removed": True,
        "product_id": product_id,
        "cart_total_items": total_items,
        "cart_total_price": float(cart.get_total_price()),
        "empty_cart": total_items == 0,
        "redirect_url": reverse('menu') if total_items == 0 else None
    })
