from __future__ import annotations

from .models import FeatureAccess, VendorProfile


def vendor_feature_enabled(vendor: VendorProfile | None, feature_key: str) -> bool:
    if not vendor or not vendor.plan:
        return False

    # 1) explicit FeatureAccess (recommended for enterprise feature toggles)
    fa = FeatureAccess.objects.filter(plan=vendor.plan, feature_key=feature_key).first()
    if fa is not None:
        return bool(fa.enabled)

    # 2) fallback to Plan.features JSON
    features = vendor.plan.features or {}
    return bool(features.get(feature_key))


def feature_required(feature_key: str):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            vendor = getattr(request, "vendor_profile", None)
            if not vendor_feature_enabled(vendor, feature_key):
                from django.contrib import messages
                from django.shortcuts import redirect

                messages.error(request, f"Feature not enabled for your plan: {feature_key}")
                return redirect("pricing")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

