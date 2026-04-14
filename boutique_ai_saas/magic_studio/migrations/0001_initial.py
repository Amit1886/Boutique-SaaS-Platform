# Generated manually for this repo.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Accessory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("price", models.PositiveIntegerField(default=0)),
                ("primary_color", models.CharField(default="#db2777", max_length=32)),
                ("tags", models.CharField(blank=True, default="", max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("image_png", models.CharField(blank=True, default="", max_length=500)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="Blouse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("price", models.PositiveIntegerField(default=0)),
                ("primary_color", models.CharField(default="#db2777", max_length=32)),
                ("tags", models.CharField(blank=True, default="", max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("template_png", models.CharField(blank=True, default="", max_length=500)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="FestivalTheme",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("theme_color", models.CharField(default="#db2777", max_length=32)),
                ("banner_text", models.CharField(blank=True, default="", max_length=200)),
            ],
            options={"ordering": ["-start_date"]},
        ),
        migrations.CreateModel(
            name="Moodboard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_name", models.CharField(default="Guest", max_length=120, unique=True)),
                ("mood_key", models.CharField(default="festive", max_length=40)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="SavedLook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_name", models.CharField(default="Guest", max_length=120)),
                ("saree_id", models.IntegerField(blank=True, null=True)),
                ("blouse_id", models.IntegerField(blank=True, null=True)),
                ("accessories_json", models.TextField(default="[]")),
                ("image_card_png", models.CharField(blank=True, default="", max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="Saree",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("price", models.PositiveIntegerField(default=0)),
                ("primary_color", models.CharField(default="#db2777", max_length=32)),
                ("tags", models.CharField(blank=True, default="", max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("layer_body_png", models.CharField(blank=True, default="", max_length=500)),
                ("layer_pallu_png", models.CharField(blank=True, default="", max_length=500)),
                ("layer_border_png", models.CharField(blank=True, default="", max_length=500)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="UXFlag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(db_index=True, max_length=80, unique=True)),
                ("enabled", models.BooleanField(default=True)),
            ],
            options={"ordering": ["key"]},
        ),
    ]

