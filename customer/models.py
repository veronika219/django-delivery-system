from django.db import models
from django.utils.html import format_html


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="menu_images/")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    category = models.ManyToManyField("Category", related_name="items")

    def __str__(self):
        return self.name

    def image_preview(self):
        if self.image:
            return format_html("<img src='{}' width='120' style='border-radius:8px;'/>",
            self.image.url)
        return 'No Image'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField("MenuItem", related_name="order", blank=True)

    # name = models.CharField(max_length=50, blank=True)
    # email = models.CharField(max_length=50, blank=True)
    #
    # city = models.CharField(max_length=50)
    # street = models.CharField(max_length=50)
    # house_number = models.CharField(max_length=10)
    #
    # comment = models.TextField(blank=True)

    def __str__(self):
        return f"Order: {self.created_on.strftime('%b %D %I :%M %p')}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#
#     def __str__(self):
#         return f"{self.menu_item.name} x {self.quantity}"
