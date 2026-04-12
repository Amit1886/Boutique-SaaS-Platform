from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("vendors", "0001_initial"),
        ("boutique", "0001_initial"),
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TemplateUsageEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_id", models.PositiveBigIntegerField(blank=True, null=True)),
                ("event_type", models.CharField(choices=[("view", "View"), ("tryon", "Try-on"), ("favorite", "Favorite")], default="view", max_length=20)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("template", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="boutique.templatedesign")),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
        migrations.AddIndex(
            model_name="templateusageevent",
            index=models.Index(fields=["vendor", "template", "event_type", "-created_at"], name="analytics_te_vend_9dc4d0_idx"),
        ),
        migrations.AddIndex(
            model_name="templateusageevent",
            index=models.Index(fields=["user_id", "event_type", "-created_at"], name="analytics_te_user_i_2b23ea_idx"),
        ),
    ]

