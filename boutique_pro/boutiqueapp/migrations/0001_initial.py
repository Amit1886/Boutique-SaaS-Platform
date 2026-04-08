from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("category", models.CharField(choices=[("saree", "Saree"), ("blouse", "Blouse"), ("fall", "Fall-Pico"), ("lehenga", "Lehenga"), ("custom", "Custom")], max_length=20)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image", models.ImageField(upload_to="products/")),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="TemplateDesign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="templates/")),
                ("name", models.CharField(max_length=200)),
                ("category", models.CharField(choices=[("saree", "Saree"), ("blouse", "Blouse"), ("fall", "Fall-Pico"), ("lehenga", "Lehenga"), ("custom", "Custom")], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="TryOnRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_image", models.ImageField(upload_to="tryon/user/")),
                ("auto_generated_image", models.ImageField(blank=True, null=True, upload_to="tryon/generated/")),
                ("bust_size", models.DecimalField(decimal_places=2, max_digits=6)),
                ("waist_size", models.DecimalField(decimal_places=2, max_digits=6)),
                ("height", models.DecimalField(decimal_places=2, max_digits=6)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("selected_template", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="boutiqueapp.templatedesign")),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("Processing", "Processing"), ("Completed", "Completed"), ("Canceled", "Canceled")], default="Pending", max_length=20)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="boutiqueapp.product")),
                ("tryon_request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="boutiqueapp.tryonrequest")),
            ],
        ),
    ]

