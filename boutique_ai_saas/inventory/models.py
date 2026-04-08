from __future__ import annotations

from django.db import models

from vendors.models import VendorProfile


class FabricStock(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    fabric_type = models.CharField(max_length=120)
    meter_available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    meter_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.vendor.subdomain} - {self.fabric_type}"

