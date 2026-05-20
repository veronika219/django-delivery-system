from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
    )
    ordering = ("role",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": ("role",),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": ("role",),
            },
        ),
    )

