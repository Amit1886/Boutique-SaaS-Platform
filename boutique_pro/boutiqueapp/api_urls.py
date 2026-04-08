from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import OrderViewSet, ProductViewSet, TemplateDesignViewSet, TryOnRequestViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("templates", TemplateDesignViewSet)
router.register("tryon-requests", TryOnRequestViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

