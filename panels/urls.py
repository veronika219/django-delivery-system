from django.urls import path
from .views import kitchen_history, kitchen_dashboard, start_cooking, mark_ready, driver_dashboard, take_order, complete_delivered


urlpatterns = [
    path("kitchen/", kitchen_dashboard, name="kitchen_dashboard"),
    path("kitchen/start/<int:order_id>/", start_cooking, name="start_cooking"),
    path("kitchen/ready/<int:order_id>/", mark_ready, name="mark_ready"),
    path("kitchen/history/", kitchen_history, name="kitchen_history"),

    path("driver/", driver_dashboard, name="driver_dashboard"),
    path("driver/take/<int:order_id>/", take_order, name="take_order"),
    path("driver/delivered/<int:order_id>/", complete_delivered, name="complete_delivered")
]
