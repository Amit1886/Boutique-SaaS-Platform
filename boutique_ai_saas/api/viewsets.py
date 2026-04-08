from rest_framework import permissions, viewsets

from boutique.models import Product, TemplateDesign
from orders.models import Order
from tryon_ai.models import TryOnSession
from vendors.models import Plan, VendorProfile

from .serializers import (
    OrderSerializer,
    PlanSerializer,
    ProductSerializer,
    TemplateDesignSerializer,
    TryOnSessionSerializer,
    VendorSerializer,
)


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all().order_by("price")
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VendorProfile.objects.select_related("plan").all().order_by("business_name")
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("vendor").all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TemplateDesignViewSet(viewsets.ModelViewSet):
    queryset = TemplateDesign.objects.select_related("vendor").all().order_by("-default_flag", "-id")
    serializer_class = TemplateDesignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TryOnSessionViewSet(viewsets.ModelViewSet):
    queryset = TryOnSession.objects.select_related("vendor", "selected_template").all().order_by("-id")
    serializer_class = TryOnSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("vendor", "product", "tryon_session").all().order_by("-id")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
