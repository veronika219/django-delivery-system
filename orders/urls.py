from django.urls import path
from .views import checkout, success, profile_view

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("profile/", profile_view, name="profile"),
    path("success/", success, name="success"),
]
