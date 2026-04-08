from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tryon_ai", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AITaskHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(default="dummy", max_length=40)),
                ("task_type", models.CharField(max_length=60)),
                ("status", models.CharField(default="created", max_length=30)),
                ("request_meta", models.JSONField(blank=True, default=dict)),
                ("response_meta", models.JSONField(blank=True, default=dict)),
                ("error", models.TextField(blank=True)),
                ("duration_ms", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("session", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="ai_tasks", to="tryon_ai.tryonsession")),
            ],
        ),
    ]

