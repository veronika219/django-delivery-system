from django import template

register = template.Library()


@register.filter
def get_item(cart, product_id):

    product_id = str(product_id)

    if product_id in cart:
        return cart[product_id]['quantity']

    return 0