from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models


class WalletAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Wallet({self.user_id})"


class TxStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    VOID = "void", "Void"


class TxType(models.TextChoices):
    CREDIT = "credit", "Credit"
    DEBIT = "debit", "Debit"
    CASHBACK = "cashback", "Cashback"
    REFERRAL = "referral", "Referral"
    ADJUSTMENT = "adjustment", "Adjustment"


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(WalletAccount, on_delete=models.CASCADE, related_name="transactions")
    tx_type = models.CharField(max_length=30, choices=TxType.choices)
    status = models.CharField(max_length=20, choices=TxStatus.choices, default=TxStatus.SUCCEEDED)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Optional references
    order_id = models.IntegerField(null=True, blank=True, db_index=True)
    ref_code = models.CharField(max_length=32, blank=True)
    note = models.CharField(max_length=200, blank=True)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Tx#{self.pk} {self.tx_type} {self.amount} ({self.status})"


class ReferralCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_code")
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code


class ReferralStatus(models.TextChoices):
    APPLIED = "applied", "Applied"
    REWARDED = "rewarded", "Rewarded"


class ReferralInvite(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referrals_sent")
    referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_used")
    code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=ReferralStatus.choices, default=ReferralStatus.APPLIED)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.referrer_id} -> {self.referred_user_id} ({self.status})"

