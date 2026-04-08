from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendorprofile",
            name="upi_id",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
    ]

