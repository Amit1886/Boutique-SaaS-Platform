from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from payments.upi import upi_payment_link, upi_qr_png

from .models import Order, TrackingStage
from .whatsapp import whatsapp_link


@staff_member_required
@require_http_methods(["GET", "POST"])
def admin_orders(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status") or ""
        stage = request.POST.get("tracking_stage") or ""
        order = get_object_or_404(Order, pk=order_id)
        if status:
            order.status = status
        valid_stages = {k for k, _ in TrackingStage.choices}
        if stage in valid_stages:
            order.tracking_stage = stage
        order.save(update_fields=["status", "tracking_stage"])
        messages.success(request, f"Order #{order.pk} updated.")
        return redirect("admin_orders")

    orders = (
        Order.objects.select_related("vendor", "product", "tryon_session", "user")
        .order_by("-id")[:200]
    )
    stages = [k for k, _ in TrackingStage.choices]
    status_choices = ["Pending", "Processing", "Ready", "Completed", "Canceled"]
    return render(
        request,
        "admin_orders.html",
        {"orders": orders, "stages": stages, "status_choices": status_choices},
    )


@staff_member_required
def admin_order_tools(request: HttpRequest, id: int) -> HttpResponse:
    order = get_object_or_404(Order.objects.select_related("vendor", "product", "user"), pk=id)

    upi_id = getattr(order.vendor, "upi_id", "") or getattr(settings, "DEFAULT_UPI_ID", "")
    upi_link = ""
    qr_url = ""
    if upi_id:
        upi_link = upi_payment_link(
            upi_id=upi_id,
            payee_name=order.vendor.business_name,
            amount=str(order.amount),
            note=f"Order #{order.pk}",
        )
        qr_path = Path(settings.MEDIA_ROOT) / "payment_qr" / f"upi_{order.pk}.png"
        upi_qr_png(upi_link, qr_path)
        qr_url = settings.MEDIA_URL + qr_path.relative_to(settings.MEDIA_ROOT).as_posix()

    phone = ""
    if order.user and hasattr(order.user, "userprofile"):
        phone = order.user.userprofile.phone or ""
    wa = whatsapp_link(phone, f"Order #{order.pk} status: {order.status}. Stage: {order.tracking_stage}")

    return render(
        request,
        "admin_order_tools.html",
        {"order": order, "upi_link": upi_link, "qr_url": qr_url, "whatsapp_url": wa},
    )
