from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from boutique import views as boutique_views

urlpatterns = [
    # Important: keep custom admin pages BEFORE Django admin/, otherwise admin/ will catch them.
    path("admin/dashboard/", include("analytics.urls_admin")),
    path("admin/orders/", include("orders.urls_admin")),
    path("admin/", admin.site.urls),
    path("", boutique_views.home, name="home"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("trending/", boutique_views.trending, name="trending"),
    path("favorites/", boutique_views.favorites, name="favorites"),
    path("favorites/toggle/", boutique_views.toggle_favorite, name="toggle_favorite"),
    path("pricing/", include("vendors.urls_pricing")),
    path("accounts/", include("accounts.urls")),
    path("vendor/", include("vendors.urls_dashboard")),
    path("tailor/", include("tailors.urls_dashboard")),
    path("pos/", include("pos.urls")),
    path("inventory/", include("inventory.urls")),
    path("order/", include("orders.urls")),
    path("wallet/", include("wallet.urls")),
    path("api/", include("api.urls")),
    path("mobile_api/", include("mobile_api.urls")),
    path("deploy/", include("deployhook.urls")),
    path("whatsapp/", include("whatsapp_bot.urls")),
    path("<slug:vendor>/", include("boutique.urls_vendor")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
