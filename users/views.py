from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, EmailLoginForm, ProfileUpdateForm


def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("profile")

    else:

        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")

    else:
        form = EmailLoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def profile_view(request):

    orders = request.user.orders.all().order_by("-created_at")

    return render(request, "users/profile.html", {
        "orders": orders
    })
