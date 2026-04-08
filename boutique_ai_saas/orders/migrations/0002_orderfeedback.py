from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="orders.order")),
            ],
        ),
    ]

