from django.urls import path

from . import views

urlpatterns = [
    path("track/<int:id>/", views.order_track, name="order_track"),
    path("invoice/<int:id>/", views.order_invoice_generate, name="order_invoice_generate"),
    path("feedback/<int:id>/", views.submit_feedback, name="order_feedback"),
]
