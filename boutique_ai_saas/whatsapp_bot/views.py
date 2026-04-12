from __future__ import annotations

import json
import os

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from vendors.models import VendorProfile
from boutique.models import Product
from orders.models import Order, TrackingStage

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

    reply = "OK"
    text = (msg.text or "").strip().lower()

    if msg.media_url:
        reply = "Image received. Reply with `order <product_id>` to create an order (dummy)."

    if vendor and text.startswith("help"):
        reply = "Commands: `list products`, `order <product_id>`, `status <order_id>`"

    if vendor and "list" in text and "product" in text:
        products = Product.objects.filter(vendor=vendor).order_by("-id")[:10]
        reply = "Products: " + ", ".join([f"{p.id}:{p.name}" for p in products]) if products else "No products."

    if vendor and text.startswith("order"):
        parts = text.split()
        product_id = parts[1] if len(parts) > 1 else ""
        p = Product.objects.filter(vendor=vendor, pk=product_id).first()
        if not p:
            reply = "Invalid product_id. Send `list products`."
        else:
            o = Order.objects.create(
                user=None,
                vendor=vendor,
                product=p,
                tryon_session=None,
                amount=p.price,
                status="Pending",
                tracking_stage=TrackingStage.RECEIVED,
            )
            reply = f"Order created: #{o.id} (Pending)."

    if vendor and text.startswith("status"):
        parts = text.split()
        order_id = parts[1] if len(parts) > 1 else ""
        o = Order.objects.filter(vendor=vendor, pk=order_id).first()
        reply = f"Order #{o.id}: {o.tracking_stage}" if o else "Order not found."

    return JsonResponse({"ok": True, "message_id": msg.pk, "reply": reply})
