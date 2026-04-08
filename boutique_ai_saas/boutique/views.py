from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from vendors.models import VendorProfile

from .models import Product, ProductCategory, TemplateDesign


def home(request: HttpRequest) -> HttpResponse:
    vendors = VendorProfile.objects.select_related("plan").order_by("business_name")[:20]
    return render(request, "home.html", {"vendors": vendors})


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

