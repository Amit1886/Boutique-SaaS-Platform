from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.tailor_dashboard, name="tailor_dashboard"),
    path("tasks/update/", views.update_task_status, name="tailor_task_update"),
]

