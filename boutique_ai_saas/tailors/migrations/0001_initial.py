from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vendors", "0001_initial"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TailorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("speciality", models.CharField(blank=True, max_length=120)),
                ("daily_capacity", models.PositiveIntegerField(default=5)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
        migrations.CreateModel(
            name="TailorTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("task_type", models.CharField(default="Cutting", max_length=80)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("In progress", "In progress"), ("Done", "Done")], default="Pending", max_length=30)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tailor_tasks", to="orders.order")),
                ("tailor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="tailors.tailorprofile")),
            ],
        ),
    ]

