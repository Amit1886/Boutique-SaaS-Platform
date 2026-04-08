from __future__ import annotations

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .feature_keys import FEATURE_KEYS
from .models import FeatureAccess, Plan


def _ensure_featureaccess(plan: Plan, enabled_keys: set[str]) -> None:
    existing = {fa.feature_key for fa in FeatureAccess.objects.filter(plan=plan)}
    for key in FEATURE_KEYS:
        if key not in existing:
            FeatureAccess.objects.create(plan=plan, feature_key=key, enabled=(key in enabled_keys))


@receiver(post_migrate)
def seed_plans(sender, **kwargs) -> None:
    if sender.name != "vendors":
        return

    free, _ = Plan.objects.get_or_create(name="Free", defaults={"price": 0, "features": {}})
    standard, _ = Plan.objects.get_or_create(name="Standard", defaults={"price": 999, "features": {}})
    pro, _ = Plan.objects.get_or_create(name="Pro", defaults={"price": 2499, "features": {}})
    ent, _ = Plan.objects.get_or_create(name="Enterprise", defaults={"price": 9999, "features": {}})

    free_keys = {
        "MULTI_VENDOR_SYSTEM",
        "PRODUCT_LISTING",
        "TEMPLATE_SCROLL_GALLERY",
        "AUTO_TEMPLATE_FIT",
        "AI_VIRTUAL_TRYON_2D",
        "ORDER_TRACKING",
        "INVOICE_GENERATOR",
        "MOBILE_API",
        "MULTI_LANGUAGE",
    }
    standard_keys = set(FEATURE_KEYS) - {"TRYON_3D_BODY_RECON", "VIDEO_TRYON"}  # example
    pro_keys = set(FEATURE_KEYS)
    ent_keys = set(FEATURE_KEYS)

    _ensure_featureaccess(free, free_keys)
    _ensure_featureaccess(standard, standard_keys)
    _ensure_featureaccess(pro, pro_keys)
    _ensure_featureaccess(ent, ent_keys)

