# Generated manually for this repo.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
        ("tailors", "0002_payroll"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="tailorprofile",
            name="avg_rating",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name="tailorprofile",
            name="rating_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="TailorReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="tailor_review", to="orders.order")),
                ("tailor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="tailors.tailorprofile")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-id"]},
        ),
    ]

