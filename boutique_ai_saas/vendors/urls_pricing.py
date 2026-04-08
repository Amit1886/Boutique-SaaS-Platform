from django.urls import path

from . import views

urlpatterns = [
    path("", views.pricing, name="pricing"),
    path("upgrade/", views.upgrade_plan, name="upgrade_plan"),
]

