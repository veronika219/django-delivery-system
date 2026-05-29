from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from core.decorators import role_required


@role_required('cook')
def kitchen_dashboard(request):

    new_orders = Order.objects.filter(
        status=Order.Status.NEW
    ).prefetch_related("items__product")

    cooking_orders = Order.objects.filter(
        status=Order.Status.COOKING,
        cook=request.user
    ).prefetch_related("items__product")

    ready_orders = Order.objects.filter(
        status=Order.Status.READY
    ).prefetch_related("items__product")

    return render(request, "panels/kitchen.html", {
        "new_orders": new_orders,
        "cooking_orders": cooking_orders,
        "ready_orders": ready_orders,
    })


@role_required('cook')
def start_cooking(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.start_cooking(request.user)

    return redirect("kitchen_dashboard")


@role_required('cook')
def mark_ready(request, order_id):
    order = get_object_or_404(Order, id=order_id, cook=request.user)

    order.mark_ready(request.user)

    return redirect('kitchen_dashboard')


@role_required('driver')
def driver_dashboard(request):

    available_orders = Order.objects.filter(
        status=Order.Status.READY,
        driver__isnull=True
    ).order_by("-created_at")

    my_orders = Order.objects.filter(
        driver=request.user,
        status=Order.Status.ON_THE_WAY
    ).order_by("-created_at")

    return render(request, "panels/driver.html", {
        "available_orders": available_orders,
        "my_orders": my_orders
    })


@role_required('driver')
def take_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.take_delivery(request.user)

    return redirect("driver_dashboard")


@role_required('driver')
def complete_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, driver=request.user)

    order.complete_delivery(request.user)

    return redirect("driver_dashboard")


@role_required('cook')
def kitchen_history(request):

    orders = Order.objects.filter(
        status__in=[Order.Status.DELIVERED, Order.Status.CANCELLED]
    ).order_by("-created_at")[:100]

    return render(request, "panels/kitchen_history.html", {
        "orders": orders
    })
