from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpRequest, HttpResponse
from .cart import Cart
from core.decorators import role_required, customer_or_guest_required


@customer_or_guest_required
def cart_detail(request: HttpRequest) -> HttpResponse:

    cart = Cart(request)

    products = []

    for product in cart.get_products():
        quantity = cart.get_quantity(product.id)

        products.append(
            {"product": product, "quantity": quantity, "total": product.price * quantity}
        )

    return render(
        request,
        "cart/cart.html",
        {
            "products": products,
            "total_price": cart.get_total_price(),
            "cart_total_item": cart.get_total_items(),
        },
    )

@customer_or_guest_required
def ajax_increase(request, product_id):

    cart = Cart(request)

    cart.add(product_id)

    quantity = cart.get_quantity(product_id)

    cart_total_price = float(cart.get_total_price())

    item_total= float(cart.get_item_total(product_id))

    return JsonResponse(
        {
            "success": True,
            "product_id": product_id,
            "quantity": quantity,
            "item_total": item_total ,
            "cart_total_price": cart_total_price,
            "cart_total_items": cart.get_total_items(),
        }
    )

@customer_or_guest_required
def ajax_decrease(request, product_id):

    cart = Cart(request)

    product_id = str(product_id)

    if product_id not in cart.cart:
        return JsonResponse({"success": False})

    quantity = cart.get_quantity(product_id) - 1

    # DELETE PRODUCT
    if quantity <= 0:

        cart.remove(product_id)

        # EMPTY CART
        if cart.get_total_items() == 0:
            return JsonResponse(
                {
                    "success": True,
                    "empty_cart": True,
                    "redirect_url": reverse("menu"),
                    "cart_total_items": 0,
                    "cart_total_price": 0,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "removed": True,
                "product_id": product_id,
                "cart_total_items": cart.get_total_items(),
                "cart_total_price": float(cart.get_total_price()),
            }
        )

    # UPDATE PRODUCT
    cart.update(product_id, quantity)
    item_total = float(cart.get_item_total(product_id))
    return JsonResponse(
        {
            "success": True,
            "product_id": product_id,
            "quantity": quantity,
            "item_total": item_total,
            "cart_total_items": cart.get_total_items(),
            "cart_total_price": float(cart.get_total_price()),
        }
    )

@customer_or_guest_required
def ajax_remove(request, product_id):

    cart = Cart(request)
    cart.remove(product_id)
    total_items = cart.get_total_items()

    return JsonResponse(
        {
            "removed": True,
            "product_id": product_id,
            "cart_total_items": total_items,
            "cart_total_price": float(cart.get_total_price()),
            "empty_cart": total_items == 0,
            "redirect_url": reverse("menu") if total_items == 0 else None,
        }
    )
