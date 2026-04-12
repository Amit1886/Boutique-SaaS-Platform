from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tryon_ai.views import measurement_api

from . import views
from .viewsets import (
    BlouseDesignViewSet,
    FavoriteViewSet,
    OrderViewSet,
    PlanViewSet,
    ProductViewSet,
    TemplateDesignViewSet,
    TryOnSessionViewSet,
    VendorViewSet,
)

router = DefaultRouter()
router.register("plans", PlanViewSet)
router.register("vendors", VendorViewSet)
router.register("products", ProductViewSet)
router.register("templates", TemplateDesignViewSet)
router.register("tryon-sessions", TryOnSessionViewSet)
router.register("orders", OrderViewSet)
router.register("favorites", FavoriteViewSet, basename="favorites")
router.register("blouse-designs", BlouseDesignViewSet, basename="blouse_designs")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("measurements/", measurement_api, name="measurement_api"),
    path("trending/", views.trending_api, name="trending_api"),
    path("personal-feed/", views.personal_feed_api, name="personal_feed_api"),
    path("wallet/", views.wallet_summary_api, name="wallet_summary_api"),
    path("tailors/<int:tailor_id>/reviews/", views.tailor_reviews_api, name="tailor_reviews_api"),
]
