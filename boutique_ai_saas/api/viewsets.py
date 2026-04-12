from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from boutique.models import Favorite, Product, TemplateDesign
from orders.models import Order
from tryon_ai.models import BlouseDesign, TryOnSession
from vendors.models import Plan, VendorProfile

from .serializers import (
    BlouseDesignSerializer,
    FavoriteSerializer,
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


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("vendor", "template", "template__vendor").order_by("-id")

    def create(self, request, *args, **kwargs):
        # Expect template_id in payload; vendor is derived from template.
        template_id = self.request.data.get("template") or self.request.data.get("template_id")
        t = TemplateDesign.objects.select_related("vendor").filter(pk=template_id).first()
        if not t:
            raise ValidationError({"template_id": "invalid template"})
        fav, created = Favorite.objects.get_or_create(user=self.request.user, template=t, defaults={"vendor": t.vendor})
        data = self.get_serializer(fav).data
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class BlouseDesignViewSet(viewsets.ModelViewSet):
    serializer_class = BlouseDesignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = BlouseDesign.objects.select_related("vendor", "user").order_by("-id")
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
