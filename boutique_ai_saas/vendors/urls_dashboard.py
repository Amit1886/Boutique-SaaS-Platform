from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("settings/", views.vendor_settings_update, name="vendor_settings_update"),
    path("tailors/tasks/", views.vendor_tailor_tasks, name="vendor_tailor_tasks"),
]
