from __future__ import annotations

from django.conf import settings

from .models import VendorProfile


class VendorRoutingMiddleware:
    """
    Vendor resolver:
    - Subdomain-based (optional): <vendor>.<MAIN_DOMAIN>
    - Path-based (always): /<vendor>/...
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.vendor_profile = None
        request.vendor_slug = None

        host = (request.get_host() or "").split(":")[0].lower()
        main = getattr(settings, "MAIN_DOMAIN", "localhost").lower()

        # Subdomain detection
        if host.endswith(main) and host != main:
            parts = host.split(".")
            if len(parts) >= 2:
                request.vendor_slug = parts[0]

        # Path detection: /<vendor>/...
        if getattr(settings, "VENDOR_PATH_PREFIX_ENABLED", True):
            path = request.path_info.lstrip("/")
            slug = (path.split("/", 1)[0] or "").strip()
            if slug and slug not in {"admin", "api", "mobile_api", "accounts", "vendor", "tailor", "pos", "inventory", "order", "pricing", "static", "media"}:
                # Only set if a vendor exists with this slug.
                if VendorProfile.objects.filter(subdomain=slug).exists():
                    request.vendor_slug = slug

        if request.vendor_slug:
            request.vendor_profile = VendorProfile.objects.select_related("plan", "user").filter(
                subdomain=request.vendor_slug
            ).first()

        return self.get_response(request)
