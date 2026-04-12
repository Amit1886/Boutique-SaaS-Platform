# Generated manually for this repo.
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
            name="WalletAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("balance", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="wallet", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ReferralCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="referral_code", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ReferralInvite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20)),
                ("status", models.CharField(choices=[("applied", "Applied"), ("rewarded", "Rewarded")], default="applied", max_length=20)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("referrer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="referrals_sent", to=settings.AUTH_USER_MODEL)),
                ("referred_user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="referral_used", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="WalletTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tx_type", models.CharField(choices=[("credit", "Credit"), ("debit", "Debit"), ("cashback", "Cashback"), ("referral", "Referral"), ("adjustment", "Adjustment")], max_length=30)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("succeeded", "Succeeded"), ("void", "Void")], default="succeeded", max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("order_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("ref_code", models.CharField(blank=True, max_length=32)),
                ("note", models.CharField(blank=True, max_length=200)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("wallet", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="transactions", to="wallet.walletaccount")),
            ],
            options={"ordering": ["-id"]},
        ),
    ]

