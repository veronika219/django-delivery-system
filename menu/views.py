from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.cart import Cart
from django.db.models import Q

def menu(request):
    query = request.GET.get('q')
    cart = Cart(request)

    categories = Category.objects.prefetch_related('products')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(name__icontains=query.capitalize())
        )

    return render(request, 'menu/menu.html', {
        'categories': categories,
        'products': products,
        'active_category': None,
        'cart': cart.get_cart(),
        'cart_total_item': cart.get_total_items()
    })


def category_view(request, category_id):

    cart = Cart(request)

    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(category=category)

    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(name__icontains=query.capitalize())
        )

    return render(request, 'menu/menu.html', {
        'categories': categories,
        'products': products,
        'active_category': category,
        'cart_ids': list(cart.get_cart().keys()),
        'cart_total_item': cart.get_total_items()
    })