from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("driver", "Driver"),
        ("cook", "Cook")
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
