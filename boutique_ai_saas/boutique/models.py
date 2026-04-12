from __future__ import annotations

from django.conf import settings
from django.db import models

from vendors.models import VendorProfile


class ProductCategory(models.TextChoices):
    SAREE = "saree", "Saree"
    BLOUSE = "blouse", "Blouse"
    LEHENGA = "lehenga", "Lehenga"
    FALL_PICO = "fall_pico", "Fall-Pico"
    CUSTOM = "custom", "Custom"


class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=ProductCategory.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    description = models.TextField(blank=True)
    stock_meter = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_tailoring_service = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} ({self.vendor.subdomain})"


class TemplateDesign(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="templates")
    category = models.CharField(max_length=20, choices=ProductCategory.choices)
    image = models.ImageField(upload_to="templates/")
    default_flag = models.BooleanField(default=False)
    name = models.CharField(max_length=200, default="Template")

    def __str__(self) -> str:
        return f"{self.name} ({self.vendor.subdomain})"


class SavedLook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Look")
    snapshot = models.ImageField(upload_to="saved_looks/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.title}"


class Favorite(models.Model):
    """
    Favorites for templates (extendable later to products/looks).
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="favorites")
    template = models.ForeignKey(TemplateDesign, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "template")]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.template_id}"
