from django.core.mail import send_mail
from django.conf import settings

from .models import OrderItem


def send_order_email(order):

    if not order.email:
        return

    items_text = "\n".join([
        f"{i.product.name} × {i.quantity}"
        for i in order.items.all()
    ])

    message = f"""
Дякуємо за замовлення!

№{order.id}
Статус: {order.get_status_display()}

Склад:
{items_text}

Сума: {order.total_price} грн

Час доставки: 40–60 хв
"""

    send_mail(
        subject=f"Замовлення №{order.id}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.email],
        fail_silently=False,
    )

def create_order(user, form, cart):

    order = form.save(commit=False)

    if user.is_authenticated:
        order.customer = user
        order.email = user.email

    order.save()

    for product in cart.get_products():
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart.get_quantity(product.id),
            price=product.price,
        )

    cart.clear()

    return order
