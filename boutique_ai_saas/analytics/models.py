from __future__ import annotations

from django.db import models

from vendors.models import VendorProfile


class VendorAnalytics(models.Model):
    vendor = models.OneToOneField(VendorProfile, on_delete=models.CASCADE)
    total_orders = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    daily_stats = models.JSONField(default=dict, blank=True)
    trending_items = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return f"Analytics ({self.vendor.subdomain})"


class TemplateUsageEvent(models.Model):
    class EventType(models.TextChoices):
        VIEW = "view", "View"
        TRYON = "tryon", "Try-on"
        FAVORITE = "favorite", "Favorite"

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    template = models.ForeignKey("boutique.TemplateDesign", on_delete=models.CASCADE)
    user_id = models.PositiveBigIntegerField(null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.VIEW)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["vendor", "template", "event_type", "-created_at"]),
            models.Index(fields=["user_id", "event_type", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.vendor_id}:{self.template_id}:{self.event_type}"
