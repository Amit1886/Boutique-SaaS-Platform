from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from boutique.models import Product, TemplateDesign
from vendors.models import VendorProfile


@api_view(["GET"])
@permission_classes([AllowAny])
def vendor_feed(request, vendor: str):
    v = VendorProfile.objects.filter(subdomain=vendor).first()
    if not v:
        return Response({"ok": False, "error": "vendor not found"}, status=404)
    products = Product.objects.filter(vendor=v).order_by("-id")[:20]
    templates = TemplateDesign.objects.filter(vendor=v).order_by("-default_flag", "-id")[:20]
    return Response(
        {
            "ok": True,
            "vendor": {"business_name": v.business_name, "subdomain": v.subdomain, "theme_color": v.theme_color},
            "products": [
                {"id": p.id, "name": p.name, "price": str(p.price), "image": p.image.url, "category": p.category}
                for p in products
            ],
            "templates": [{"id": t.id, "name": t.name, "image": t.image.url, "category": t.category} for t in templates],
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def vendors_list(request):
    vendors = VendorProfile.objects.all().order_by("business_name")[:100]
    return Response(
        {
            "ok": True,
            "vendors": [
                {
                    "subdomain": v.subdomain,
                    "business_name": v.business_name,
                    "theme_color": v.theme_color,
                    "logo": v.logo.url if v.logo else None,
                }
                for v in vendors
            ],
        }
    )

