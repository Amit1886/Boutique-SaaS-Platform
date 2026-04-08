from __future__ import annotations

from django.db import models

from vendors.models import VendorProfile


class POSOrder(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    item_list = models.JSONField(default=list, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"POS #{self.pk} ({self.vendor.subdomain})"

