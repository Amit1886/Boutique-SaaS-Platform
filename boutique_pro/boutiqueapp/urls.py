from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/<str:category>/", views.product_list, name="product_list"),
    path("tryon/upload/", views.upload_image, name="tryon_upload"),
    path("tryon/templates/<int:id>/", views.show_templates, name="tryon_templates"),
    path("tryon/generate/", views.generate_tryon, name="tryon_generate"),
    path("order/confirm/", views.confirm_order, name="confirm_order"),
    path("order/success/<int:id>/", views.order_success, name="order_success"),
    path("admin/orders/", views.admin_order_list, name="admin_order_list"),
]

