from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image_preview',
        'description',
        'price',
        'available',

    ]
admin.site.register(Category)