from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vendors", "0001_initial"),
        ("boutique", "0002_favorite"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomDesignTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Custom Template", max_length=200)),
                ("components", models.JSONField(blank=True, default=dict)),
                ("preview", models.ImageField(blank=True, null=True, upload_to="custom_templates/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="custom_templates", to="vendors.vendorprofile")),
            ],
        ),
    ]

