from django.urls import path

from . import views

urlpatterns = [
    path("", views.inventory_dashboard, name="inventory_dashboard"),
    path("update/<int:id>/", views.inventory_update, name="inventory_update"),
]

