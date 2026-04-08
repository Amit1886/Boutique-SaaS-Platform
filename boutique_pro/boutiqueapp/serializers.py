from rest_framework import serializers

from .models import Order, Product, TemplateDesign, TryOnRequest


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "price", "image", "description"]


class TemplateDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateDesign
        fields = ["id", "name", "category", "image"]


class TryOnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TryOnRequest
        fields = [
            "id",
            "user_image",
            "selected_template",
            "auto_generated_image",
            "bust_size",
            "waist_size",
            "height",
            "status",
            "created_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "tryon_request", "product", "amount", "status"]

