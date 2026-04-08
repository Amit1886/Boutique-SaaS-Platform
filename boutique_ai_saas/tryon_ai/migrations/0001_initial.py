from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vendors", "0001_initial"),
        ("boutique", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TryOnSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("original_image", models.ImageField(upload_to="tryon/original/")),
                ("bg_removed_image", models.ImageField(blank=True, null=True, upload_to="tryon/bg_removed/")),
                ("measurement_data", models.JSONField(blank=True, default=dict)),
                ("ai_result", models.ImageField(blank=True, null=True, upload_to="tryon/result/")),
                ("type", models.CharField(choices=[("2D", "2D"), ("3D", "3D"), ("AR", "AR")], default="2D", max_length=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("selected_template", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="boutique.templatedesign")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

