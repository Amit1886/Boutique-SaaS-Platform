from django.urls import path

from . import views

urlpatterns = [
    path("", views.pos_billing, name="pos_billing"),
]

