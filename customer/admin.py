from django.contrib import admin
from customer.models import OrderModel, Category, MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ("image_preview",)
    fields = ("name", "description", "price", "category", "image", "image_preview",)


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
