from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Order, TrackingStage
from .models import OrderFeedback
from .utils import generate_invoice_pdf


def order_track(request: HttpRequest, id: int) -> HttpResponse:
    order = get_object_or_404(Order.objects.select_related("vendor", "product", "tryon_session"), pk=id)
    stages = [s for s, _ in TrackingStage.choices]
    feedback = OrderFeedback.objects.filter(order=order).first()
    return render(request, "order_track.html", {"order": order, "stages": stages, "feedback": feedback})


@require_http_methods(["POST"])
def order_invoice_generate(request: HttpRequest, id: int):
    order = get_object_or_404(Order.objects.select_related("vendor", "product"), pk=id)
    out = Path(settings.MEDIA_ROOT) / "invoices" / f"invoice_{order.pk}.pdf"
    generate_invoice_pdf(order.pk, order.vendor.business_name, order.product.name, str(order.amount), out)
    order.invoice_pdf.name = out.relative_to(settings.MEDIA_ROOT).as_posix()
    order.save(update_fields=["invoice_pdf"])
    return redirect("order_track", id=order.pk)


@require_http_methods(["POST"])
def submit_feedback(request: HttpRequest, id: int):
    order = get_object_or_404(Order, pk=id)
    rating = int(request.POST.get("rating") or 5)
    rating = max(1, min(5, rating))
    comment = request.POST.get("comment") or ""
    OrderFeedback.objects.update_or_create(order=order, defaults={"rating": rating, "comment": comment})
    return redirect("order_track", id=order.pk)
