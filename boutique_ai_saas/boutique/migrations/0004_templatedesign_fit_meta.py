from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boutique", "0003_customdesigntemplate"),
    ]

    operations = [
        migrations.AddField(
            model_name="templatedesign",
            name="fit_meta",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]

