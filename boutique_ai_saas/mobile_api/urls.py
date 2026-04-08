from django.urls import path

from . import views

urlpatterns = [
    path("vendors/", views.vendors_list, name="mobile_vendors"),
    path("feed/<slug:vendor>/", views.vendor_feed, name="mobile_vendor_feed"),
]

