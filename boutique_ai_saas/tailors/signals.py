from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order, TrackingStage

from .models import TailorProfile, TailorTask


@receiver(post_save, sender=Order)
def create_tailor_task(sender, instance: Order, created: bool, **kwargs) -> None:
    # Auto create a first task on new order (dummy workflow).
    if not created:
        return

    tailor = TailorProfile.objects.filter(vendor=instance.vendor).order_by("id").first()
    if not tailor:
        return

    TailorTask.objects.create(tailor=tailor, order=instance, task_type="Cutting")

