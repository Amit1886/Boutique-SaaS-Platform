from __future__ import annotations

from django.db import models

from vendors.models import VendorProfile


class WhatsAppMessage(models.Model):
    """
    Dummy WhatsApp inbox for automation flows.

    This stores incoming webhook payloads so you can build automations without
    coupling to a specific provider (Twilio/Meta Cloud API/etc).
    """

    vendor = models.ForeignKey(VendorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    from_number = models.CharField(max_length=40, blank=True)
    to_number = models.CharField(max_length=40, blank=True)
    text = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    raw = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"WA#{self.pk} {self.from_number}"

