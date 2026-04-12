from rest_framework import serializers

from boutique.models import Favorite, Product, TemplateDesign
from orders.models import Order
from tryon_ai.models import BlouseDesign, TryOnSession
from vendors.models import Plan, VendorProfile


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price"]


class VendorSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = VendorProfile
        fields = ["id", "business_name", "subdomain", "theme_color", "logo", "plan"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "vendor",
            "name",
            "category",
            "price",
            "image",
            "description",
            "stock_meter",
            "is_tailoring_service",
        ]


class TemplateDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateDesign
        fields = ["id", "vendor", "category", "image", "default_flag", "name"]


class TryOnSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TryOnSession
        fields = [
            "id",
            "user",
            "vendor",
            "original_image",
            "bg_removed_image",
            "measurement_data",
            "selected_template",
            "ai_result",
            "type",
            "created_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "vendor",
            "product",
            "tryon_session",
            "amount",
            "status",
            "tracking_stage",
            "invoice_pdf",
            "created_at",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    template = TemplateDesignSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "vendor", "template", "created_at"]


class BlouseDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlouseDesign
        fields = ["id", "vendor", "user", "options", "image", "created_at"]
