from __future__ import annotations

from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order

from .models import TailorReview, TailorTask
from .services import choose_tailor_for_order


@receiver(post_save, sender=Order)
def create_tailor_task(sender, instance: Order, created: bool, **kwargs) -> None:
    # Auto create a first task on new order (dummy workflow).
    if not created:
        return

    tailor = choose_tailor_for_order(vendor=instance.vendor)
    if not tailor:
        return

    TailorTask.objects.create(tailor=tailor, order=instance, task_type="Cutting")


@receiver(post_save, sender=TailorReview)
def update_tailor_rating(sender, instance: TailorReview, created: bool, **kwargs) -> None:
    # Recompute rating aggregates (small scale; acceptable).
    tailor = instance.tailor
    agg = TailorReview.objects.filter(tailor=tailor).aggregate(avg=Avg("rating"), cnt=Count("id"))
    tailor.avg_rating = agg["avg"] or 0
    tailor.rating_count = agg["cnt"] or 0
    tailor.save(update_fields=["avg_rating", "rating_count"])
