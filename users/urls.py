from django.urls import path
from .views import login_view, logout_view, register_view, edit_profile, profile_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("edit/", edit_profile, name="edit_profile"),
]
