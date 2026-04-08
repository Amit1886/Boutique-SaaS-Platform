from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FabricStock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fabric_type", models.CharField(max_length=120)),
                ("meter_available", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("meter_used", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

