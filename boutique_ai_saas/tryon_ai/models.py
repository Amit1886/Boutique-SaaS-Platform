from __future__ import annotations

from django.conf import settings
from django.db import models

from boutique.models import TemplateDesign
from vendors.models import VendorProfile


class TryOnType(models.TextChoices):
    TWO_D = "2D", "2D"
    THREE_D = "3D", "3D"
    AR = "AR", "AR"


class TryOnSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to="tryon/original/")
    bg_removed_image = models.ImageField(upload_to="tryon/bg_removed/", null=True, blank=True)
    measurement_data = models.JSONField(default=dict, blank=True)
    selected_template = models.ForeignKey(TemplateDesign, on_delete=models.SET_NULL, null=True, blank=True)
    ai_result = models.ImageField(upload_to="tryon/result/", null=True, blank=True)
    type = models.CharField(max_length=5, choices=TryOnType.choices, default=TryOnType.TWO_D)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Session #{self.pk} ({self.vendor.subdomain})"


class AITaskHistory(models.Model):
    session = models.ForeignKey(TryOnSession, on_delete=models.CASCADE, related_name="ai_tasks", null=True, blank=True)
    provider = models.CharField(max_length=40, default="dummy")
    task_type = models.CharField(max_length=60)
    status = models.CharField(max_length=30, default="created")
    request_meta = models.JSONField(default=dict, blank=True)
    response_meta = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    duration_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.task_type} ({self.provider})"
