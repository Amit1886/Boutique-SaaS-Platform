from __future__ import annotations

from django.conf import settings
from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=60, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.name


class FeatureAccess(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="feature_access")
    feature_key = models.CharField(max_length=80)
    enabled = models.BooleanField(default=False)

    class Meta:
        unique_together = [("plan", "feature_key")]

    def __str__(self) -> str:
        return f"{self.plan.name}:{self.feature_key}={self.enabled}"


class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    subdomain = models.SlugField(max_length=50, unique=True)
    logo = models.ImageField(upload_to="vendor_logos/", null=True, blank=True)
    theme_color = models.CharField(max_length=20, default="#db2777")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    upi_id = models.CharField(max_length=120, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.business_name} ({self.subdomain})"
