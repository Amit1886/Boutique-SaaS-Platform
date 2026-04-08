from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .ai import generate_virtual_tryon, remove_background
from .forms import OrderConfirmForm, TryOnUploadForm
from .models import Category, Order, Product, TemplateDesign, TryOnRequest


def _processed_user_path(tryon: TryOnRequest) -> Path:
    return Path(settings.MEDIA_ROOT) / "tryon" / "processed" / f"processed_{tryon.pk}.png"


def _processed_user_url(tryon: TryOnRequest) -> str:
    return f"{settings.MEDIA_URL}tryon/processed/processed_{tryon.pk}.png"


def home(request: HttpRequest) -> HttpResponse:
    featured = Product.objects.all().order_by("-id")[:8]
    categories = [
        (Category.SAREE, "Sarees"),
        (Category.BLOUSE, "Blouses"),
        (Category.FALL, "Fall-Pico"),
        (Category.LEHENGA, "Lehengas"),
        (Category.CUSTOM, "Custom"),
    ]
    return render(request, "home.html", {"featured": featured, "categories": categories})


def product_list(request: HttpRequest, category: str) -> HttpResponse:
    if category not in Category.values:
        return redirect("home")
    products = Product.objects.filter(category=category).order_by("-id")
    return render(
        request,
        "product_list.html",
        {"products": products, "category": category, "category_label": Category(category).label},
    )


@require_http_methods(["GET", "POST"])
def upload_image(request: HttpRequest) -> HttpResponse:
    product_id = request.GET.get("product") or request.POST.get("product_id")
    selected_product = None
    if product_id:
        selected_product = Product.objects.filter(pk=product_id).first()

    if request.method == "POST":
        form = TryOnUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tryon = form.save()
            messages.success(request, "Photo uploaded. Choose a template to preview and generate your try-on.")
            url = reverse("tryon_templates", args=[tryon.pk])
            if selected_product:
                url += f"?product={selected_product.pk}"
            return redirect(url)
    else:
        form = TryOnUploadForm()

    return render(
        request,
        "tryon_upload.html",
        {"form": form, "selected_product": selected_product},
    )


def show_templates(request: HttpRequest, id: int) -> HttpResponse:
    tryon = get_object_or_404(TryOnRequest, pk=id)
    product_id = request.GET.get("product")

    processed_path = _processed_user_path(tryon)
    if not processed_path.exists():
        remove_background(Path(tryon.user_image.path), processed_path)

    templates = TemplateDesign.objects.all().order_by("-id")[:20]
    return render(
        request,
        "tryon_templates.html",
        {
            "tryon": tryon,
            "product_id": product_id,
            "templates": templates,
            "processed_user_url": _processed_user_url(tryon),
        },
    )


@require_http_methods(["POST"])
def generate_tryon(request: HttpRequest) -> HttpResponse:
    tryon_id = request.POST.get("tryon_id")
    template_id = request.POST.get("template_id")
    product_id = request.POST.get("product_id")
    if not tryon_id or not template_id:
        messages.error(request, "Please select a template first.")
        return redirect("home")

    tryon = get_object_or_404(TryOnRequest, pk=tryon_id)
    template = get_object_or_404(TemplateDesign, pk=template_id)

    processed_path = _processed_user_path(tryon)
    if not processed_path.exists():
        remove_background(Path(tryon.user_image.path), processed_path)

    out_path = Path(settings.MEDIA_ROOT) / "tryon" / "generated" / f"tryon_{tryon.pk}.png"
    generate_virtual_tryon(processed_path, Path(template.image.path), out_path)

    relative = out_path.relative_to(settings.MEDIA_ROOT).as_posix()
    tryon.selected_template = template
    tryon.auto_generated_image.name = relative
    tryon.save(update_fields=["selected_template", "auto_generated_image"])

    confirm_url = reverse("confirm_order")
    confirm_url += f"?tryon={tryon.pk}"
    if product_id:
        confirm_url += f"&product={product_id}"

    return render(
        request,
        "tryon_result.html",
        {"tryon": tryon, "product_id": product_id, "confirm_url": confirm_url},
    )


@require_http_methods(["GET", "POST"])
def confirm_order(request: HttpRequest) -> HttpResponse:
    tryon_id = request.GET.get("tryon") or request.POST.get("tryon_id")
    if not tryon_id:
        return redirect("home")
    tryon = get_object_or_404(TryOnRequest, pk=tryon_id)
    if not tryon.selected_template or not tryon.auto_generated_image:
        messages.error(request, "Please generate your try-on result first.")
        return redirect("tryon_templates", id=tryon.pk)

    initial = {}
    product_id = request.GET.get("product") or request.POST.get("product")
    if product_id:
        initial["product"] = Product.objects.filter(pk=product_id).first()

    if request.method == "POST":
        form = OrderConfirmForm(request.POST, initial=initial)
        if form.is_valid():
            product = form.cleaned_data["product"]
            order = Order.objects.create(
                tryon_request=tryon,
                product=product,
                amount=product.price,
            )
            messages.success(request, "Order placed successfully!")
            return redirect("order_success", id=order.pk)
    else:
        form = OrderConfirmForm(initial=initial)

    return render(
        request,
        "order_confirm.html",
        {"tryon": tryon, "form": form},
    )


def order_success(request: HttpRequest, id: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=id)
    return render(request, "order_success.html", {"order": order})


@staff_member_required
@require_http_methods(["GET", "POST"])
def admin_order_list(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        if order_id and new_status:
            order = (
                Order.objects.filter(pk=order_id)
                .select_related("tryon_request", "product", "tryon_request__selected_template")
                .first()
            )
            valid_statuses = {k for k, _ in Order._meta.get_field("status").choices}
            if order and new_status in valid_statuses:
                order.status = new_status
                order.save(update_fields=["status"])
                messages.success(request, f"Order #{order.pk} updated to {new_status}.")
            else:
                messages.error(request, "Invalid order/status.")
        return redirect("admin_order_list")

    orders = (
        Order.objects.select_related("product", "tryon_request", "tryon_request__selected_template")
        .order_by("-id")
    )
    return render(request, "admin_order_list.html", {"orders": orders})

