from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tryon_ai.views import measurement_api

from .viewsets import OrderViewSet, PlanViewSet, ProductViewSet, TemplateDesignViewSet, TryOnSessionViewSet, VendorViewSet

router = DefaultRouter()
router.register("plans", PlanViewSet)
router.register("vendors", VendorViewSet)
router.register("products", ProductViewSet)
router.register("templates", TemplateDesignViewSet)
router.register("tryon-sessions", TryOnSessionViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("measurements/", measurement_api, name="measurement_api"),
]

