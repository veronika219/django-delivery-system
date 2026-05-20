from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "paid", "created_at")

    list_filter = ("status", "paid")
    inlines = [OrderItemInline]
