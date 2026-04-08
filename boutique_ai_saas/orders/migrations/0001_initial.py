from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vendors", "0001_initial"),
        ("boutique", "0001_initial"),
        ("tryon_ai", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(default="Pending", max_length=30)),
                ("tracking_stage", models.CharField(choices=[("Received", "Received"), ("Cutting", "Cutting"), ("Stitching", "Stitching"), ("Finishing", "Finishing"), ("Packaging", "Packaging"), ("Out for delivery", "Out for delivery"), ("Completed", "Completed")], default="Received", max_length=40)),
                ("invoice_pdf", models.FileField(blank=True, null=True, upload_to="invoices/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="boutique.product")),
                ("tryon_session", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="tryon_ai.tryonsession")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

