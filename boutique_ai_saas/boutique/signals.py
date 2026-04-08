from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from analytics.models import VendorAnalytics
from vendors.models import Plan, VendorProfile

from .models import Product, ProductCategory, TemplateDesign

User = get_user_model()


def _copy_static_to_media(static_rel: str, media_rel: str) -> str:
    src = Path(settings.BASE_DIR) / static_rel
    dst = Path(settings.MEDIA_ROOT) / media_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists() and not dst.exists():
        shutil.copyfile(src, dst)
    return media_rel.replace("\\", "/")


@receiver(post_migrate)
def seed_demo_boutique(sender, **kwargs) -> None:
    if sender.name != "boutique":
        return

    # Ensure a demo vendor exists so the UI has something to browse.
    demo_user, created = User.objects.get_or_create(username="demo_vendor", defaults={"email": "demo@example.com"})
    if created:
        demo_user.set_password("demo12345")
        demo_user.save()

    free = Plan.objects.filter(name__iexact="Free").first() or Plan.objects.first()
    vendor, _ = VendorProfile.objects.get_or_create(
        user=demo_user,
        defaults={
            "business_name": "Demo Boutique",
            "subdomain": "demo",
            "theme_color": "#db2777",
            "plan": free,
        },
    )

    VendorAnalytics.objects.get_or_create(vendor=vendor)

    template_src_dir = Path(settings.BASE_DIR) / "static" / "images" / "templates"
    images = sorted(template_src_dir.glob("template*.png"))
    if images and TemplateDesign.objects.filter(vendor=vendor).count() < 20:
        existing = TemplateDesign.objects.filter(vendor=vendor).count()
        need = 20 - existing
        for i in range(need):
            img = images[i % len(images)]
            saved_rel = _copy_static_to_media(
                f"static/images/templates/{img.name}", f"templates/{img.name}"
            )
            TemplateDesign.objects.create(
                vendor=vendor,
                category=ProductCategory.SAREE,
                image=saved_rel,
                default_flag=(i < 3),
                name=f"Template {existing + i + 1}",
            )

    if Product.objects.filter(vendor=vendor).count() == 0 and images:
        img_name = images[0].name
        prod_rel = _copy_static_to_media(
            f"static/images/templates/{img_name}", f"products/{img_name}"
        )
        Product.objects.bulk_create(
            [
                Product(
                    vendor=vendor,
                    name="Royal Silk Saree",
                    category=ProductCategory.SAREE,
                    price="2499.00",
                    image=prod_rel,
                    description="Elegant silk saree for festive occasions.",
                    stock_meter="50.0",
                ),
                Product(
                    vendor=vendor,
                    name="Designer Blouse Stitching",
                    category=ProductCategory.BLOUSE,
                    price="799.00",
                    image=prod_rel,
                    description="Premium blouse stitching service.",
                    is_tailoring_service=True,
                ),
                Product(
                    vendor=vendor,
                    name="Fall-Pico Stitching",
                    category=ProductCategory.FALL_PICO,
                    price="399.00",
                    image=prod_rel,
                    description="Neat fall and pico finishing.",
                    is_tailoring_service=True,
                ),
                Product(
                    vendor=vendor,
                    name="Bridal Lehenga Set",
                    category=ProductCategory.LEHENGA,
                    price="8999.00",
                    image=prod_rel,
                    description="Bridal lehenga with rich embroidery.",
                    stock_meter="20.0",
                ),
                Product(
                    vendor=vendor,
                    name="Custom Boutique Design",
                    category=ProductCategory.CUSTOM,
                    price="4999.00",
                    image=prod_rel,
                    description="Work with our designer for a custom outfit.",
                    is_tailoring_service=True,
                ),
            ]
        )

