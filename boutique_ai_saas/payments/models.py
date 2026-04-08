from __future__ import annotations

from django.db import models

from vendors.models import Plan, VendorProfile


class PaymentStatus(models.TextChoices):
    CREATED = "Created", "Created"
    PAID = "Paid", "Paid"
    FAILED = "Failed", "Failed"


class RazorpayTransaction(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.CREATED)
    razorpay_order_id = models.CharField(max_length=120, blank=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"RZP #{self.pk} {self.status}"

