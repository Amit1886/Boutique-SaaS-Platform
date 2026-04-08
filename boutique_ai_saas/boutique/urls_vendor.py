from django.urls import path

from . import views
from tryon_ai import views as tryon_views

urlpatterns = [
    path("", views.vendor_home, name="vendor_home"),
    path("products/<str:category>/", views.product_list, name="product_list"),
    path("tryon/upload/", tryon_views.virtual_upload, name="virtual_upload"),
    path("tryon/templates/<int:session_id>/", tryon_views.virtual_templates, name="virtual_templates"),
    path("tryon/generate/", tryon_views.virtual_generate, name="virtual_generate"),
    path("order/confirm/", tryon_views.order_confirm, name="order_confirm"),
    path("look/save/<int:session_id>/", tryon_views.save_look, name="save_look"),
]
