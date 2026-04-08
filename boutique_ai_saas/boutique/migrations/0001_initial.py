from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("category", models.CharField(choices=[("saree", "Saree"), ("blouse", "Blouse"), ("lehenga", "Lehenga"), ("fall_pico", "Fall-Pico"), ("custom", "Custom")], max_length=20)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image", models.ImageField(upload_to="products/")),
                ("description", models.TextField(blank=True)),
                ("stock_meter", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("is_tailoring_service", models.BooleanField(default=False)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="TemplateDesign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.CharField(choices=[("saree", "Saree"), ("blouse", "Blouse"), ("lehenga", "Lehenga"), ("fall_pico", "Fall-Pico"), ("custom", "Custom")], max_length=20)),
                ("image", models.ImageField(upload_to="templates/")),
                ("default_flag", models.BooleanField(default=False)),
                ("name", models.CharField(default="Template", max_length=200)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="templates", to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="SavedLook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="My Look", max_length=200)),
                ("snapshot", models.ImageField(blank=True, null=True, upload_to="saved_looks/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

