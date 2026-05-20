from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    name = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(max_digits=7, decimal_places=2)

    image = models.ImageField(upload_to="products/")
    available = models.BooleanField(default=True)

    def image_preview(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" width=100px height=100px style="object-fit: cover;"/>'
            )
        return "Немає зображення"

    def __str__(self):
        return self.name
