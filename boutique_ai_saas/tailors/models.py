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
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

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
    piece_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.task_type} ({self.order_id})"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"


class TailorPayment(models.Model):
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name="payments")
    period_start = models.DateField()
    period_end = models.DateField()
    pieces_done = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment#{self.pk} ({self.tailor_id})"


class TailorReview(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="tailor_review")
    tailor = models.ForeignKey(TailorProfile, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"TailorReview#{self.order_id} ({self.rating}/5)"
