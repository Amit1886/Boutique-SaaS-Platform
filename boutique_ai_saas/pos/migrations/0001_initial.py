from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="POSOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("item_list", models.JSONField(blank=True, default=list)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

