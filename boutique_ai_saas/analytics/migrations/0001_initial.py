from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VendorAnalytics",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_orders", models.PositiveIntegerField(default=0)),
                ("revenue", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("daily_stats", models.JSONField(blank=True, default=dict)),
                ("trending_items", models.JSONField(blank=True, default=list)),
                ("vendor", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

