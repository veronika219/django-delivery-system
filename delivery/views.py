from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order


@login_required
def driver_dashboard(request):
    if request.user.role != "driver":
        return redirect("menu")

    orders = Order.objects.filter(status="READY")

    return render(request, "delivery/dashboard.html", {"orders": orders})


@login_required
def accept_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    order.driver = request.user

    order.status = "ON_THE_WAY"
    order.save()
    return redirect("driver_dashboard")


@login_required
def complete_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = "DELIVERED"
    order.save()

    return redirect("driver_dashboard")
