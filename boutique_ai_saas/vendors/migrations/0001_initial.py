from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
                ("price", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("features", models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="VendorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(max_length=200)),
                ("subdomain", models.SlugField(max_length=50, unique=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="vendor_logos/")),
                ("theme_color", models.CharField(default="#db2777", max_length=20)),
                ("plan", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="vendors.plan")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="FeatureAccess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("feature_key", models.CharField(max_length=80)),
                ("enabled", models.BooleanField(default=False)),
                ("plan", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feature_access", to="vendors.plan")),
            ],
            options={
                "unique_together": {("plan", "feature_key")},
            },
        ),
    ]

