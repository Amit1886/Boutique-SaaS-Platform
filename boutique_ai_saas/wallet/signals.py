from __future__ import annotations

import secrets
import string

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ReferralCode, WalletAccount

User = get_user_model()


def _gen_code(n: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


@receiver(post_save, sender=User)
def ensure_wallet(sender, instance, created: bool, **kwargs) -> None:
    if created:
        WalletAccount.objects.get_or_create(user=instance)
        # Create a unique referral code
        for _ in range(10):
            code = _gen_code(8)
            if not ReferralCode.objects.filter(code=code).exists():
                ReferralCode.objects.get_or_create(user=instance, defaults={"code": code})
                break

