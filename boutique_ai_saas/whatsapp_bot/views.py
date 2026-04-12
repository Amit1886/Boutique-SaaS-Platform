from __future__ import annotations

import json
import os

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from vendors.models import VendorProfile

from .models import WhatsAppMessage


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request: HttpRequest) -> JsonResponse:
    """
    Dummy WhatsApp webhook.

    Expected header (optional):
      X-Webhook-Secret: <WHATSAPP_WEBHOOK_SECRET>

    Payload: any JSON or form-data.
    """
    expected = os.environ.get("WHATSAPP_WEBHOOK_SECRET", "")
    if expected:
        given = request.headers.get("X-Webhook-Secret", "")
        if given != expected:
            return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)

    payload: dict
    try:
        if request.content_type and "application/json" in request.content_type:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        else:
            payload = dict(request.POST.items())
    except Exception:
        payload = {}

    vendor_slug = (payload.get("vendor") or payload.get("vendor_slug") or "").strip()
    vendor = VendorProfile.objects.filter(subdomain=vendor_slug).first() if vendor_slug else None

    msg = WhatsAppMessage.objects.create(
        vendor=vendor,
        from_number=str(payload.get("from") or payload.get("from_number") or ""),
        to_number=str(payload.get("to") or payload.get("to_number") or ""),
        text=str(payload.get("text") or payload.get("body") or ""),
        media_url=str(payload.get("media_url") or ""),
        raw=payload or {},
    )

    # Dummy automation hooks: you can add rules here later.
    return JsonResponse({"ok": True, "message_id": msg.pk})

