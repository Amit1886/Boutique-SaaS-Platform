from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from boutique import views as boutique_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", boutique_views.home, name="home"),
    path("pricing/", include("vendors.urls_pricing")),
    path("accounts/", include("accounts.urls")),
    path("vendor/", include("vendors.urls_dashboard")),
    path("tailor/", include("tailors.urls_dashboard")),
    path("admin/dashboard/", include("analytics.urls_admin")),
    path("admin/orders/", include("orders.urls_admin")),
    path("pos/", include("pos.urls")),
    path("inventory/", include("inventory.urls")),
    path("order/", include("orders.urls")),
    path("api/", include("api.urls")),
    path("mobile_api/", include("mobile_api.urls")),
    path("deploy/", include("deployhook.urls")),
    path("<slug:vendor>/", include("boutique.urls_vendor")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
