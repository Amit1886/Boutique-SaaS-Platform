from rest_framework import viewsets

from .models import Order, Product, TemplateDesign, TryOnRequest
from .serializers import (
    OrderSerializer,
    ProductSerializer,
    TemplateDesignSerializer,
    TryOnRequestSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer


class TemplateDesignViewSet(viewsets.ModelViewSet):
    queryset = TemplateDesign.objects.all().order_by("-id")
    serializer_class = TemplateDesignSerializer


class TryOnRequestViewSet(viewsets.ModelViewSet):
    queryset = TryOnRequest.objects.select_related("selected_template").order_by("-id")
    serializer_class = TryOnRequestSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("tryon_request", "product").order_by("-id")
    serializer_class = OrderSerializer

