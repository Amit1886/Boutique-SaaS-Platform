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


class VideoTryOnJob(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PROCESSING = "processing", "Processing"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    session = models.ForeignKey(TryOnSession, on_delete=models.SET_NULL, null=True, blank=True, related_name="video_jobs")
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    input_video = models.FileField(upload_to="tryon/video/input/")
    template = models.ForeignKey(TemplateDesign, on_delete=models.SET_NULL, null=True, blank=True)
    output_video = models.FileField(upload_to="tryon/video/output/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    meta = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"VideoJob#{self.pk} {self.status}"


class BodyModel3D(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PROCESSING = "processing", "Processing"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    session = models.OneToOneField(TryOnSession, on_delete=models.CASCADE, related_name="body_3d", null=True, blank=True)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    mesh_file = models.FileField(upload_to="tryon/3d/", null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Body3D#{self.pk} {self.status}"


class BlouseDesign(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    options = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to="blouse/designs/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"BlouseDesign#{self.pk}"


class CuttingBlueprint(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    measurements = models.JSONField(default=dict, blank=True)
    pdf = models.FileField(upload_to="blueprints/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Blueprint#{self.pk}"
