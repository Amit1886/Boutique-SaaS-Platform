# Generated manually for this repo.
from datetime import date

from django.db import migrations


def seed(apps, schema_editor):
    Saree = apps.get_model("magic_studio", "Saree")
    Blouse = apps.get_model("magic_studio", "Blouse")
    Accessory = apps.get_model("magic_studio", "Accessory")
    FestivalTheme = apps.get_model("magic_studio", "FestivalTheme")
    UXFlag = apps.get_model("magic_studio", "UXFlag")

    for key in [
        "magic_mirror",
        "pallu_gravity",
        "tailor_jinn",
        "color_bloom",
        "teleport_anim",
        "shadow_sync",
        "aura_effect",
        "ripple_reveal",
    ]:
        UXFlag.objects.get_or_create(key=key, defaults={"enabled": True})

    if not FestivalTheme.objects.exists():
        y = date.today().year
        FestivalTheme.objects.create(name="Holi", start_date=date(y, 3, 1), end_date=date(y, 3, 31), theme_color="#0ea5e9", banner_text="Holi Color Bloom")
        FestivalTheme.objects.create(name="Navratri", start_date=date(y, 10, 1), end_date=date(y, 10, 15), theme_color="#7c3aed", banner_text="Navratri Nights")
        FestivalTheme.objects.create(name="Diwali", start_date=date(y, 10, 20), end_date=date(y, 11, 10), theme_color="#f59e0b", banner_text="Diwali Glow")
        FestivalTheme.objects.create(name="Wedding Season", start_date=date(y, 11, 1), end_date=date(y, 12, 31), theme_color="#db2777", banner_text="Wedding Season Magic")

    if not Saree.objects.exists():
        Saree.objects.create(name="Rose Silk Saree", price=2999, primary_color="#db2777", tags="wedding,festive")
        Saree.objects.create(name="Ocean Blue Georgette", price=2399, primary_color="#0ea5e9", tags="party")
        Saree.objects.create(name="Royal Purple Banarasi", price=4999, primary_color="#7c3aed", tags="bridal")

    if not Blouse.objects.exists():
        Blouse.objects.create(name="Classic Round Neck", price=799, primary_color="#7c3aed", tags="round,match")
        Blouse.objects.create(name="Sweetheart Neck", price=899, primary_color="#db2777", tags="sweetheart")
        Blouse.objects.create(name="High Neck (Festive)", price=999, primary_color="#f59e0b", tags="highneck")

    if not Accessory.objects.exists():
        Accessory.objects.create(name="Kundan Earrings", price=399, primary_color="#f59e0b", tags="jewelry")
        Accessory.objects.create(name="Pearl Belt", price=499, primary_color="#ffffff", tags="belt")
        Accessory.objects.create(name="Pallu Clip", price=199, primary_color="#0f172a", tags="clip")


class Migration(migrations.Migration):
    dependencies = [("magic_studio", "0001_initial")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]

