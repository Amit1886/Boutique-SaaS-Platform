from __future__ import annotations

from django.conf import settings
from django.db import models

from boutique.models import Product
from tryon_ai.models import TryOnSession
from vendors.models import VendorProfile


class TrackingStage(models.TextChoices):
    RECEIVED = "Received", "Received"
    CUTTING = "Cutting", "Cutting"
    STITCHING = "Stitching", "Stitching"
    FINISHING = "Finishing", "Finishing"
    PACKAGING = "Packaging", "Packaging"
    OUT_FOR_DELIVERY = "Out for delivery", "Out for delivery"
    COMPLETED = "Completed", "Completed"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    tryon_session = models.ForeignKey(TryOnSession, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, default="Pending")
    tracking_stage = models.CharField(max_length=40, choices=TrackingStage.choices, default=TrackingStage.RECEIVED)
    invoice_pdf = models.FileField(upload_to="invoices/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order #{self.pk} ({self.vendor.subdomain})"


class OrderFeedback(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="feedback")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Feedback #{self.order_id}"
