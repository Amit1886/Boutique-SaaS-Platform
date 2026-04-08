from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/vendor/", views.signup_vendor, name="signup_vendor"),
    path("language/", views.language_settings, name="language_settings"),
    path("dashboard/", views.customer_dashboard, name="customer_dashboard"),
]
