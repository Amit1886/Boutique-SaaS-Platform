from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("hi", "Hindi"), ("ta", "Tamil"), ("gu", "Gujarati")],
                default="en",
                max_length=5,
            ),
        ),
    ]

