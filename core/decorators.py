from functools import wraps
from django.shortcuts import redirect


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.role not in allowed_roles:
                return redirect('menu')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def customer_or_guest_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role != "customer":
                return redirect('menu')
        return view_func(request, *args, **kwargs)
    return wrapper

