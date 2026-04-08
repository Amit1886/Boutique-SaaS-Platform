from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RazorpayTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("Created", "Created"), ("Paid", "Paid"), ("Failed", "Failed")], default="Created", max_length=20)),
                ("razorpay_order_id", models.CharField(blank=True, max_length=120)),
                ("razorpay_payment_id", models.CharField(blank=True, max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("plan", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="vendors.plan")),
                ("vendor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vendors.vendorprofile")),
            ],
        ),
    ]

