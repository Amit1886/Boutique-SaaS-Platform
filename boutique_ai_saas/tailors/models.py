from __future__ import annotations

from django.conf import settings
from django.db import models

from orders.models import Order
from vendors.models import VendorProfile


class TailorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=120, blank=True)
    daily_capacity = models.PositiveIntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.vendor.subdomain})"


class TaskStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    IN_PROGRESS = "In progress", "In progress"
    DONE = "Done", "Done"


class TailorTask(models.Model):
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name="tasks")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tailor_tasks")
    task_type = models.CharField(max_length=80, default="Cutting")
    status = models.CharField(max_length=30, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.task_type} ({self.order_id})"

