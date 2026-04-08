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

