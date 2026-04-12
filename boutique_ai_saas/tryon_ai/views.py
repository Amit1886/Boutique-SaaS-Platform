from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import OperationalError, ProgrammingError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from analytics.models import TemplateUsageEvent
from boutique.models import Product, TemplateDesign
from boutique.models import SavedLook
from orders.models import Order, TrackingStage
from vendors.models import VendorProfile

from .ai import ai_face_shape, ai_measurement_extract, ai_skin_tone, generate_3d_body
from .forms import BlouseDesignerForm, BlueprintForm, OrderConfirmForm, VideoTryOnForm, VirtualUploadForm
from .models import BlouseDesign, CuttingBlueprint, TryOnSession, TryOnType, VideoTryOnJob
from .services import (
    ai_fitting_recommend,
    change_background,
    generate_3d_body_model,
    generate_blouse_design,
    generate_cutting_pdf,
    generate_tryon_image,
    generate_video_tryon,
    log_task,
    remove_background,
)


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
    generate_tryon_image(Path(session.bg_removed_image.path), Path(template.image.path), out_img, session=session)
    session.ai_result.name = _save_relative(Path(settings.MEDIA_ROOT), out_img)
    session.save(update_fields=["selected_template", "ai_result", "type"])

    try:
        TemplateUsageEvent.objects.create(
            vendor=vendor_obj,
            template=template,
            user_id=request.user.id if request.user.is_authenticated else None,
            event_type=TemplateUsageEvent.EventType.TRYON,
            meta={"session_id": session.pk, "source": "virtual_generate"},
        )
    except (OperationalError, ProgrammingError):
        # Migrations might not be applied yet on a fresh DB.
        pass

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
    meas = ai_measurement_extract(temp_path)
    from .services import ai_measurement_detect as ai_measurement_detect_service

    detected = ai_measurement_detect_service(temp_path, session=None)
    fitting = ai_fitting_recommend(detected, session=None)
    return JsonResponse({"ok": True, "data": {"measurements": detected, "fitting": fitting, "raw": meas}})


@require_http_methods(["POST"])
def tryon_preview_api(request: HttpRequest, vendor: str) -> JsonResponse:
    """
    AJAX: generate try-on preview without full page reload.
    Expects: session_id, template_id
    """
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session_id = request.POST.get("session_id")
    template_id = request.POST.get("template_id")
    if not session_id or not template_id:
        return JsonResponse({"ok": False, "error": "session_id and template_id required"}, status=400)

    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    template = get_object_or_404(TemplateDesign, pk=template_id, vendor=vendor_obj)

    def _opt_float(name: str) -> float | None:
        raw = request.POST.get(name, "")
        if raw is None or str(raw).strip() == "":
            return None
        try:
            return float(raw)
        except Exception:
            return None

    # Use per-template defaults when available, otherwise auto-fit.
    defaults = (template.fit_meta or {}) if hasattr(template, "fit_meta") else {}

    scale = _opt_float("scale")
    x_offset_frac = _opt_float("x_offset_frac")
    y_offset_frac = _opt_float("y_offset_frac")
    rotation_deg = _opt_float("rotation_deg")
    if scale is None and "scale" in defaults:
        scale = float(defaults.get("scale"))
    if x_offset_frac is None and "x_offset_frac" in defaults:
        x_offset_frac = float(defaults.get("x_offset_frac"))
    if y_offset_frac is None and "y_offset_frac" in defaults:
        y_offset_frac = float(defaults.get("y_offset_frac"))
    if rotation_deg is None and "rotation_deg" in defaults:
        rotation_deg = float(defaults.get("rotation_deg"))

    out_img = Path(settings.MEDIA_ROOT) / "tryon" / "result" / f"preview_{session.pk}_{template.pk}.png"
    generate_tryon_image(
        Path(session.bg_removed_image.path),
        Path(template.image.path),
        out_img,
        scale=scale,
        x_offset_frac=x_offset_frac,
        y_offset_frac=y_offset_frac,
        rotation_deg=rotation_deg,
        session=session,
    )
    session.selected_template = template
    session.ai_result.name = _save_relative(Path(settings.MEDIA_ROOT), out_img)
    session.save(update_fields=["selected_template", "ai_result"])

    try:
        TemplateUsageEvent.objects.create(
            vendor=vendor_obj,
            template=template,
            user_id=request.user.id if request.user.is_authenticated else None,
            event_type=TemplateUsageEvent.EventType.TRYON,
            meta={"session_id": session.pk, "source": "preview"},
        )
    except (OperationalError, ProgrammingError):
        pass

    rec = ai_fitting_recommend((session.measurement_data or {}).get("measurements", {}), session=session)

    # Optional: save fit defaults on the template (vendor users only).
    if request.user.is_authenticated and request.POST.get("save_fit") == "1":
        try:
            from accounts.models import UserProfile, UserRole

            profile = UserProfile.objects.filter(user=request.user).first()
            if profile and profile.role == UserRole.VENDOR and template.vendor_id == vendor_obj.id:
                template.fit_meta = {
                    "scale": scale,
                    "x_offset_frac": x_offset_frac,
                    "y_offset_frac": y_offset_frac,
                    "rotation_deg": rotation_deg,
                }
                template.save(update_fields=["fit_meta"])
        except Exception:
            pass

    return JsonResponse(
        {
            "ok": True,
            "result_url": session.ai_result.url,
            "fitting": rec,
            "applied": {
                "scale": scale,
                "x_offset_frac": x_offset_frac,
                "y_offset_frac": y_offset_frac,
                "rotation_deg": rotation_deg,
            },
        }
    )


@require_http_methods(["GET", "POST"])
def tryon_video(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    templates = TemplateDesign.objects.filter(vendor=vendor_obj).order_by("-default_flag", "-id")[:30]
    job = None
    if request.method == "POST":
        form = VideoTryOnForm(request.POST, request.FILES)
        if form.is_valid():
            template = None
            if form.cleaned_data.get("template_id"):
                template = TemplateDesign.objects.filter(pk=form.cleaned_data["template_id"], vendor=vendor_obj).first()
            job = VideoTryOnJob.objects.create(
                vendor=vendor_obj,
                user=request.user if request.user.is_authenticated else None,
                input_video=form.cleaned_data["video"],
                template=template,
                status=VideoTryOnJob.Status.PROCESSING,
                meta={"note": "5s video placeholder pipeline"},
            )
            out = Path(settings.MEDIA_ROOT) / "tryon" / "video" / "output" / f"tryon_video_{job.pk}.mp4"
            generate_video_tryon(Path(job.input_video.path), out, session=None)
            job.output_video.name = _save_relative(Path(settings.MEDIA_ROOT), out)
            job.status = VideoTryOnJob.Status.SUCCEEDED
            job.save(update_fields=["output_video", "status"])
            messages.success(request, "Video try-on generated (placeholder).")
    else:
        form = VideoTryOnForm()
    return render(request, "tryon_video.html", {"vendor_obj": vendor_obj, "form": form, "templates": templates, "job": job})


@require_http_methods(["GET", "POST"])
def blouse_designer(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    design = None
    if request.method == "POST":
        form = BlouseDesignerForm(request.POST)
        if form.is_valid():
            design = BlouseDesign.objects.create(
                vendor=vendor_obj,
                user=request.user if request.user.is_authenticated else None,
                options=form.cleaned_data,
            )
            out = Path(settings.MEDIA_ROOT) / "blouse" / "designs" / f"blouse_{design.pk}.png"
            generate_blouse_design(form.cleaned_data, out, session=None)
            design.image.name = _save_relative(Path(settings.MEDIA_ROOT), out)
            design.save(update_fields=["image"])
            messages.success(request, "Blouse design generated.")
    else:
        form = BlouseDesignerForm()
    recent = BlouseDesign.objects.filter(vendor=vendor_obj).order_by("-id")[:30]
    return render(request, "blouse_designer.html", {"vendor_obj": vendor_obj, "form": form, "design": design, "recent": recent})


@require_http_methods(["GET", "POST"])
def cutting_pdf(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    if request.method == "POST":
        form = BlueprintForm(request.POST)
        if form.is_valid():
            blueprint_type = form.cleaned_data.get("blueprint_type") or "blouse"
            measurements = {
                k: float(v)
                for k, v in form.cleaned_data.items()
                if k != "blueprint_type" and v is not None
            }
            obj = CuttingBlueprint.objects.create(
                vendor=vendor_obj,
                user=request.user if request.user.is_authenticated else None,
                measurements=measurements,
            )
            out = Path(settings.MEDIA_ROOT) / "blueprints" / f"cutting_{obj.pk}.pdf"
            generate_cutting_pdf(measurements, out, blueprint_type=blueprint_type, session=None)
            obj.pdf.name = _save_relative(Path(settings.MEDIA_ROOT), out)
            obj.save(update_fields=["pdf"])
            return redirect(obj.pdf.url)
    else:
        form = BlueprintForm()
    return render(request, "cutting_pdf.html", {"vendor_obj": vendor_obj, "form": form})


@require_http_methods(["POST"])
def background_change_api(request: HttpRequest, vendor: str) -> JsonResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session_id = request.POST.get("session_id")
    background = (request.POST.get("background") or "studio").strip().lower()
    if not session_id:
        return JsonResponse({"ok": False, "error": "session_id required"}, status=400)
    if background not in {"wedding", "party", "studio"}:
        background = "studio"

    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    base_path = Path(session.bg_removed_image.path) if session.bg_removed_image else Path(session.original_image.path)
    out_img = Path(settings.MEDIA_ROOT) / "tryon" / "result" / f"bg_{background}_{session.pk}.png"
    change_background(base_path, out_img, background=background, session=session)
    session.ai_result.name = _save_relative(Path(settings.MEDIA_ROOT), out_img)
    session.save(update_fields=["ai_result"])
    return JsonResponse({"ok": True, "result_url": session.ai_result.url})


@require_http_methods(["GET", "POST"])
def tryon_3d(request: HttpRequest, vendor: str, session_id: int) -> HttpResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)
    body = getattr(session, "body_3d", None)
    return render(request, "tryon_3d.html", {"vendor_obj": vendor_obj, "session": session, "body": body})


@require_http_methods(["POST"])
def generate_3d_api(request: HttpRequest, vendor: str) -> JsonResponse:
    vendor_obj = get_object_or_404(VendorProfile, subdomain=vendor)
    session_id = request.POST.get("session_id")
    if not session_id:
        return JsonResponse({"ok": False, "error": "session_id required"}, status=400)
    session = get_object_or_404(TryOnSession, pk=session_id, vendor=vendor_obj)

    body, _ = BodyModel3D.objects.get_or_create(
        session=session,
        defaults={
            "vendor": vendor_obj,
            "user": request.user if request.user.is_authenticated else None,
            "status": BodyModel3D.Status.PROCESSING,
        },
    )
    body.status = BodyModel3D.Status.PROCESSING
    body.save(update_fields=["status"])

    meta = generate_3d_body_model(Path(session.original_image.path), session=session)
    body.meta = meta or {}
    body.status = BodyModel3D.Status.SUCCEEDED
    body.save(update_fields=["meta", "status"])
    return JsonResponse({"ok": True, "status": body.status, "meta": body.meta})


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
