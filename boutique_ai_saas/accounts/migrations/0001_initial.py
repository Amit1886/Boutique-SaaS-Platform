from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("customer", "Customer"), ("vendor", "Vendor"), ("tailor", "Tailor"), ("admin", "Admin")], default="customer", max_length=20)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("profile_img", models.ImageField(blank=True, null=True, upload_to="profiles/")),
                ("language", models.CharField(default="en", max_length=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

