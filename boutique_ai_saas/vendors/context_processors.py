from .models import FeatureAccess


def vendor_context(request):
    vendor = getattr(request, "vendor_profile", None)
    enabled_features = set()
    if vendor and vendor.plan_id:
        enabled_features = set(
            FeatureAccess.objects.filter(plan_id=vendor.plan_id, enabled=True).values_list("feature_key", flat=True)
        )
    return {
        "current_vendor": vendor,
        "vendor_theme_color": getattr(vendor, "theme_color", "#db2777"),
        "enabled_features": enabled_features,
    }
