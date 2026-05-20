from django.urls import path
from .views import driver_dashboard, accept_delivery, complete_delivery

urlpatterns = [
    path("", driver_dashboard, name="driver_dashboard"),
    path("accept/<int:order_id>/", accept_delivery, name="accept_delivery"),
    path("complete/<int:order_id>/", complete_delivery, name="complete_delivery"),
]
