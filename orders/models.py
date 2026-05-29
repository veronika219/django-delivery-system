from django.db import models
from users.models import User
from menu.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Нове"
        COOKING = "COOKING", "Готується"
        READY = "READY", "Готово"
        ON_THE_WAY = "ON_THE_WAY", "В дорозі"
        DELIVERED = "DELIVERED", "Доставлено"
        CANCELLED = "CANCELLED", "Скасовано"

    class DeliveryType(models.TextChoices):
        DELIVERY = "DELIVERY", "Доставка"
        PICKUP = "PICKUP", "Самовивіз"

    class PaymentMethod(models.TextChoices):
        ONLINE = "ONLINE", "Онлайн"
        CASH = "CASH", "При отриманні"

    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_orders"
    )

    cook = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cook_orders"
    )

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    delivery_type = models.CharField(
        max_length=20,
        choices=DeliveryType.choices
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id}"


    STATUS_LABELS = {
        Status.NEW: "Прийнято",
        Status.COOKING: "Готується",
        Status.READY: "Готується",
        Status.ON_THE_WAY: "В дорозі",
        Status.DELIVERED: "Доставлено",
        Status.CANCELLED: "Скасовано",
    }

    def public_status(self):
        return self.STATUS_LABELS.get(self.status, "Обробляється")


    def start_cooking(self, cook):
        if self.status != self.Status.NEW:
            return False

        self.cook = cook
        self.status = self.Status.COOKING

        self.save(update_fields=["cook", "status"])
        return True

    def mark_ready(self, cook):
        if self.status != self.Status.COOKING:
            return False

        if self.cook != cook:
            return False

        self.status = self.Status.READY

        self.save(update_fields=["status"])
        return True

    def take_delivery(self, driver):
        if self.status != self.Status.READY:
            return False

        if self.driver is not None:
            return False

        self.driver = driver
        self.status = self.Status.ON_THE_WAY

        self.save(update_fields=["driver", "status"])
        return True

    def complete_delivery(self, driver):
        if self.status != self.Status.ON_THE_WAY:
            return False

        if self.driver != driver:
            return False

        self.status = self.Status.DELIVERED

        self.save(update_fields=["status"])
        return True


    def cancel(self, customer):
        if self.customer != customer:
            return False

        if self.status != self.Status.NEW:
            return False

        self.status = self.Status.CANCELLED

        self.save(update_fields=["status"])
        return True


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

