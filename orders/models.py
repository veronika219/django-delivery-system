from django.db import models
from users.models import User
from menu.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("NEW", "New"),
        ("COOKING", "Cooking"),
        ("READY", "Ready"),
        ("ON_THE_WAY", "On the way"),
        ("DELIVERED", "Delivered"),
    )

    DELIVERY_CHOICES = (
        ("DELIVERY", "Delivery"),
        ("PICKUP", "Pickup"),
    )

    PAYMENT_CHOICES = (
        ("ONLINE", "Online"),
        ("CASH", "cash"),
    )

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries",
    )

    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.TextField(blank=True)

    comment = models.TextField(blank=True)

    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price
