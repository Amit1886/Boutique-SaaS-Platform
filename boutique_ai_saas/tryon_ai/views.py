from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from boutique.models import Product, TemplateDesign
from boutique.models import SavedLook
from orders.models import Order, TrackingStage
from vendors.models import VendorProfile

from .ai import ai_face_shape, ai_measurement_extract, ai_skin_tone, generate_3d_body
from .forms import OrderConfirmForm, VirtualUploadForm
from .models import TryOnSession, TryOnType
from .services import generate_tryon, log_task, remove_background


def _save_relative(media_root: Path, abs_path: Path) -> str:
    return abs_path.relative_to(media_root).as_posix()


@require_http_methods(["GET", "POST"])
def virtual_upload(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    if request.method == "POST":
        form = VirtualUploadForm(request.POST, request.FILES)
        if form.is_valid():
            session = TryOnSession.objects.create(
                user=request.user if request.user.is_authenticated else None,
                vendor=vendor_obj,
                original_image=form.cleaned_data["photo"],
                type=form.cleaned_data["tryon_type"],
            )

            # Background removal (dummy, but outputs a real PNG)
            out_bg = Path(settings.MEDIA_ROOT) / "tryon" / "bg_removed" / f"bg_removed_{session.pk}.png"
            remove_background(Path(session.original_image.path), out_bg, session=session)
            session.bg_removed_image.name = _save_relative(Path(settings.MEDIA_ROOT), out_bg)

            # AI measurement extraction + face/skin analysis (dummy)
            meas = ai_measurement_extract(Path(session.original_image.path))
            log_task(session, provider="dummy", task_type="ai_measurement_extract", status="succeeded", response_meta=meas)
            if form.cleaned_data.get("manual_bust") is not None:
                meas["bust_in"] = float(form.cleaned_data["manual_bust"])
            if form.cleaned_data.get("manual_waist") is not None:
                meas["waist_in"] = float(form.cleaned_data["manual_waist"])
            if form.cleaned_data.get("manual_height") is not None:
                meas["height_in"] = float(form.cleaned_data["manual_height"])

            session.measurement_data = {
                "measurements": meas,
                "face_shape": ai_face_shape(Path(session.original_image.path)),
                "skin_tone": ai_skin_tone(Path(session.original_image.path)),
            }
            session.save(update_fields=["bg_removed_image", "measurement_data"])

            return redirect("virtual_templates", vendor=vendor, session_id=session.pk)
    else:
        form = VirtualUploadForm()
    return render(request, "virtual_upload.html", {"vendor_obj": vendor_obj, "form": form})


def virtual_templates(request: HttpRequest, vendor: str, session_id: int) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    templates = TemplateDesign.objects.filter(vendor=vendor_obj).order_by("-default_flag", "-id")[:20]
    return render(
        request,
        "virtual_templates.html",
        {"vendor_obj": vendor_obj, "session": session, "templates": templates},
    )


@require_http_methods(["POST"])
def virtual_generate(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session_id = request.POST.get("session_id")
    template_id = request.POST.get("template_id")
    if not session_id or not template_id:
        messages.error(request, "Select a template first.")
        return redirect("vendor_home", vendor=vendor)

    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    template = get_object_or_404(TemplateDesign, pk=template_id, vendor=vendor_obj)
    session.selected_template = template

    if session.type == TryOnType.THREE_D:
        _ = generate_3d_body(Path(session.original_image.path))
        # For 3D we still produce a 2D composite preview image as a placeholder UI asset.
        session.type = TryOnType.THREE_D

    out_img = Path(settings.MEDIA_ROOT) / "tryon" / "result" / f"tryon_{session.pk}.png"
    generate_tryon(Path(session.bg_removed_image.path), Path(template.image.path), out_img, session=session)
    session.ai_result.name = _save_relative(Path(settings.MEDIA_ROOT), out_img)
    session.save(update_fields=["selected_template", "ai_result", "type"])

    return render(request, "virtual_result.html", {"vendor_obj": vendor_obj, "session": session})


@require_http_methods(["GET", "POST"])
def order_confirm(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session_id = request.GET.get("session") or request.POST.get("session_id")
    if not session_id:
        return redirect("vendor_home", vendor=vendor)
    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    if not session.ai_result:
        messages.error(request, "Generate a try-on result first.")
        return redirect("virtual_templates", vendor=vendor, session_id=session.pk)

    products = Product.objects.filter(vendor=vendor_obj).order_by("-id")[:100]
    if request.method == "POST":
        form = OrderConfirmForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=form.cleaned_data["product_id"], vendor=vendor_obj)
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                vendor=vendor_obj,
                product=product,
                tryon_session=session,
                amount=product.price,
                status="Pending",
                tracking_stage=TrackingStage.RECEIVED,
            )
            messages.success(request, "Order created!")
            return redirect("order_track", id=order.pk)
    else:
        form = OrderConfirmForm()

    return render(
        request,
        "order_confirm.html",
        {"vendor_obj": vendor_obj, "session": session, "products": products, "form": form},
    )


@require_http_methods(["POST"])
def measurement_api(request: HttpRequest) -> JsonResponse:
    """
    Measurement auto-detection API (dummy).
    Expects multipart 'photo'.
    """
    photo = request.FILES.get("photo")
    if not photo:
        return JsonResponse({"ok": False, "error": "photo is required"}, status=400)
    temp_path = Path(settings.MEDIA_ROOT) / "tmp" / photo.name
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    with temp_path.open("wb") as f:
        for chunk in photo.chunks():
            f.write(chunk)
    data = ai_measurement_extract(temp_path)
    return JsonResponse({"ok": True, "data": data})


@login_required
def save_look(request: HttpRequest, vendor: str, session_id: int):
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    if not session.ai_result:
        messages.error(request, "Generate a try-on result first.")
        return redirect("virtual_templates", vendor=vendor, session_id=session.pk)
    SavedLook.objects.create(
        user=request.user,
        vendor=vendor_obj,
        title=f"Look #{session.pk}",
        snapshot=session.ai_result.name,
    )
    messages.success(request, "Saved to My Looks.")
    return redirect("customer_dashboard")
