from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.tailor_dashboard, name="tailor_dashboard"),
    path("tasks/update/", views.update_task_status, name="tailor_task_update"),
    path("payroll/", views.payroll, name="tailor_payroll"),
    path("payroll/mark-paid/", views.mark_paid, name="tailor_payroll_mark_paid"),
]
