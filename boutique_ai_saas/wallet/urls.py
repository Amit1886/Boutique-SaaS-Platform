from django.urls import path

from . import views

urlpatterns = [
    path("", views.wallet_dashboard, name="wallet_dashboard"),
    path("apply-referral/", views.wallet_apply_referral, name="wallet_apply_referral"),
    path("admin/adjust/", views.admin_wallet_adjust, name="admin_wallet_adjust"),
]

