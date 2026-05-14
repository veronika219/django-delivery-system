from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),

    # категорія (як якір / фільтр)
    path('category/<int:category_id>/', views.category_view, name='category_view'),
]