from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Category, Product, TemplateDesign


def _copy_static_to_media(static_rel: str, media_rel: str) -> str:
    src = Path(settings.BASE_DIR) / static_rel
    dst = Path(settings.MEDIA_ROOT) / media_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copyfile(src, dst)
    return media_rel.replace("\\", "/")


@receiver(post_migrate)
def seed_demo_data(sender, **kwargs) -> None:
    if sender.name != "boutiqueapp":
        return

    template_src_dir = Path(settings.BASE_DIR) / "static" / "images" / "templates"
    if not template_src_dir.exists():
        return

    if TemplateDesign.objects.count() < 20:
        existing = TemplateDesign.objects.count()
        need = 20 - existing
        images = sorted(template_src_dir.glob("template*.png"))
        if images:
            for i in range(need):
                img = images[i % len(images)]
                media_rel = f"templates/{img.name}"
                saved_rel = _copy_static_to_media(
                    f"static/images/templates/{img.name}", media_rel
                )
                TemplateDesign.objects.create(
                    name=f"Template {existing + i + 1}",
                    category=Category.SAREE,
                    image=saved_rel,
                )

    if Product.objects.count() == 0:
        sample_img = sorted(template_src_dir.glob("template*.png"))[:1]
        if not sample_img:
            return
        img_name = sample_img[0].name
        saved_rel = _copy_static_to_media(
            f"static/images/templates/{img_name}", f"products/{img_name}"
        )
        Product.objects.bulk_create(
            [
                Product(
                    name="Royal Silk Saree",
                    category=Category.SAREE,
                    price="2499.00",
                    image=saved_rel,
                    description="Elegant silk saree for festive occasions.",
                ),
                Product(
                    name="Designer Blouse Stitching",
                    category=Category.BLOUSE,
                    price="799.00",
                    image=saved_rel,
                    description="Premium blouse stitching with modern fit.",
                ),
                Product(
                    name="Fall-Pico Stitching",
                    category=Category.FALL,
                    price="399.00",
                    image=saved_rel,
                    description="Neat fall and pico finishing service.",
                ),
                Product(
                    name="Bridal Lehenga Set",
                    category=Category.LEHENGA,
                    price="8999.00",
                    image=saved_rel,
                    description="Heavy bridal lehenga with rich embroidery.",
                ),
                Product(
                    name="Custom Boutique Design",
                    category=Category.CUSTOM,
                    price="4999.00",
                    image=saved_rel,
                    description="Work with our designer for a custom outfit.",
                ),
            ]
        )

