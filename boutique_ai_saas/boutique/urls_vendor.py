from django.urls import path

from . import views
from tryon_ai import views as tryon_views

urlpatterns = [
    path("", views.vendor_home, name="vendor_home"),
    path("products/<str:category>/", views.product_list, name="product_list"),
    path("tryon/upload/", tryon_views.virtual_upload, name="virtual_upload"),
    path("tryon/templates/<int:session_id>/", tryon_views.virtual_templates, name="virtual_templates"),
    path("tryon/preview/", tryon_views.tryon_preview_api, name="tryon_preview_api"),
    path("tryon/generate/", tryon_views.virtual_generate, name="virtual_generate"),
    path("tryon/background/", tryon_views.background_change_api, name="background_change_api"),
    path("tryon/video/", tryon_views.tryon_video, name="tryon_video"),
    path("order/confirm/", tryon_views.order_confirm, name="order_confirm"),
    path("look/save/<int:session_id>/", tryon_views.save_look, name="save_look"),
    path("blouse/designer/", tryon_views.blouse_designer, name="blouse_designer"),
    path("blueprint/pdf/", tryon_views.cutting_pdf, name="cutting_pdf"),
]
