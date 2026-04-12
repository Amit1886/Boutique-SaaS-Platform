from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from vendors.models import VendorProfile

from analytics.services import get_personal_feed, get_trending_designs
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

from tryon_ai.ai import generate_blouse_design_image

from .models import CustomDesignTemplate, Favorite, Product, ProductCategory, SavedLook, TemplateDesign


def home(request: HttpRequest) -> HttpResponse:
    vendors = VendorProfile.objects.select_related("plan").order_by("business_name")[:20]
    trending = get_trending_designs(limit=8)
    personal = get_personal_feed(request.user, limit=8) if request.user.is_authenticated else []
    return render(
        request,
        "home.html",
        {"vendors": vendors, "trending": trending, "personal_feed": personal},
    )


def vendor_home(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_profile = get_object_or_404(VendorProfile, subdomain=vendor)
    products = Product.objects.filter(vendor=vendor_profile).order_by("-id")[:8]
    templates = TemplateDesign.objects.filter(vendor=vendor_profile).order_by("-default_flag", "-id")[:10]
    categories = [(c.value, c.label) for c in ProductCategory]
    return render(
        request,
        "vendor_home.html",
        {
            "vendor_obj": vendor_profile,
            "products": products,
            "templates": templates,
            "categories": categories,
        },
    )


def product_list(request: HttpRequest, vendor: str, category: str) -> HttpResponse:
    vendor_profile = get_object_or_404(VendorProfile, subdomain=vendor)
    if category not in ProductCategory.values:
        return redirect("vendor_home", vendor=vendor)
    products = Product.objects.filter(vendor=vendor_profile, category=category).order_by("-id")
    return render(
        request,
        "product_list.html",
        {
            "vendor_obj": vendor_profile,
            "products": products,
            "category": category,
            "category_label": ProductCategory(category).label,
        },
    )


def trending(request: HttpRequest) -> HttpResponse:
    rows = get_trending_designs(limit=30)
    return render(request, "trending.html", {"rows": rows})


@require_http_methods(["GET"])
def favorites(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    favs = Favorite.objects.filter(user=request.user).select_related("template", "template__vendor").order_by("-created_at")[:200]
    looks = SavedLook.objects.filter(user=request.user).select_related("vendor").order_by("-created_at")[:200]
    return render(request, "favorites.html", {"favorites": favs, "looks": looks})


@require_http_methods(["POST"])
def toggle_favorite(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    template_id = request.POST.get("template_id")
    if not template_id:
        return redirect("favorites")
    t = TemplateDesign.objects.filter(pk=template_id).select_related("vendor").first()
    if not t:
        return redirect("favorites")
    obj = Favorite.objects.filter(user=request.user, template=t).first()
    if obj:
        obj.delete()
    else:
        Favorite.objects.create(user=request.user, vendor=t.vendor, template=t)
    return redirect(request.META.get("HTTP_REFERER") or "favorites")


@require_http_methods(["GET"])
def custom_templates(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_profile = get_object_or_404(VendorProfile, subdomain=vendor)
    templates = CustomDesignTemplate.objects.filter(vendor=vendor_profile).order_by("-id")[:200]
    return render(request, "custom_templates.html", {"vendor_obj": vendor_profile, "templates": templates})


@csrf_protect
@require_http_methods(["POST"])
def save_custom_template(request: HttpRequest, vendor: str) -> HttpResponse:
    vendor_profile = get_object_or_404(VendorProfile, subdomain=vendor)
    name = (request.POST.get("name") or "Custom Template").strip()[:200]
    components = {
        "neck": request.POST.get("neck") or "round",
        "sleeve": request.POST.get("sleeve") or "short",
        "back": request.POST.get("back") or "u-back",
        "pattern": request.POST.get("pattern") or "solid",
        "border": request.POST.get("border") or "none",
        "color": request.POST.get("color") or "#db2777",
    }

    obj = CustomDesignTemplate.objects.create(
        vendor=vendor_profile,
        user=request.user if request.user.is_authenticated else None,
        name=name,
        components=components,
    )
    from pathlib import Path

    out = Path(settings.MEDIA_ROOT) / "custom_templates" / f"custom_{obj.pk}.png"
    generate_blouse_design_image(components, out)
    obj.preview.name = out.relative_to(Path(settings.MEDIA_ROOT)).as_posix()
    obj.save(update_fields=["preview"])
    return redirect("custom_templates", vendor=vendor_profile.subdomain)
