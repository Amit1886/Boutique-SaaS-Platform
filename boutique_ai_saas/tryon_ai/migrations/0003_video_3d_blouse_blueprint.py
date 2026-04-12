from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("boutique", "0001_initial"),
        ("vendors", "0001_initial"),
        ("tryon_ai", "0002_aitaskhistory"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlouseDesign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("options", models.JSONField(blank=True, default=dict)),
                ("image", models.ImageField(blank=True, null=True, upload_to="blouse/designs/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="BodyModel3D",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("created", "Created"), ("processing", "Processing"), ("succeeded", "Succeeded"), ("failed", "Failed")], default="created", max_length=20)),
                ("mesh_file", models.FileField(blank=True, null=True, upload_to="tryon/3d/")),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("session", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="body_3d", to="tryon_ai.tryonsession")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="CuttingBlueprint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("measurements", models.JSONField(blank=True, default=dict)),
                ("pdf", models.FileField(blank=True, null=True, upload_to="blueprints/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="VideoTryOnJob",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("input_video", models.FileField(upload_to="tryon/video/input/")),
                ("output_video", models.FileField(blank=True, null=True, upload_to="tryon/video/output/")),
                ("status", models.CharField(choices=[("created", "Created"), ("processing", "Processing"), ("succeeded", "Succeeded"), ("failed", "Failed")], default="created", max_length=20)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("session", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="video_jobs", to="tryon_ai.tryonsession")),
                ("template", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="boutique.templatedesign")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

