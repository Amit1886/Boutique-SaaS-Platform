from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import VendorAnalytics

from .models import Order, TrackingStage
from .notifications import send_email_sms, send_whatsapp_update


@receiver(post_save, sender=Order)
def on_order_created(sender, instance: Order, created: bool, **kwargs) -> None:
    # Wallet cashback: create pending on new order; settle when completed/canceled.
    try:
        from wallet.services import create_cashback_pending, settle_cashback

        if created:
            create_cashback_pending(user=instance.user, order_id=instance.pk, order_amount=instance.amount)
        else:
            if instance.user and instance.tracking_stage == TrackingStage.COMPLETED:
                settle_cashback(user=instance.user, order_id=instance.pk, succeed=True)
            if instance.user and (instance.status or "").lower() in {"canceled", "cancelled"}:
                settle_cashback(user=instance.user, order_id=instance.pk, succeed=False)
    except Exception:
        pass

    if not created:
        return

    analytics, _ = VendorAnalytics.objects.get_or_create(vendor=instance.vendor)
    analytics.total_orders = int(analytics.total_orders or 0) + 1
    analytics.revenue = (analytics.revenue or 0) + instance.amount

    trending = analytics.trending_items or []
    trending.append({"product": instance.product.name, "amount": str(instance.amount)})
    analytics.trending_items = trending[-50:]
    analytics.save(update_fields=["total_orders", "revenue", "trending_items"])

    # Dummy notification hooks
    if instance.user and hasattr(instance.user, "email") and instance.user.email:
        send_email_sms(instance.user.email, f"Your order #{instance.pk} has been received.")
    if instance.user:
        phone = getattr(getattr(instance.user, "userprofile", None), "phone", "") if hasattr(instance.user, "userprofile") else ""
        if phone:
            send_whatsapp_update(phone, f"Order #{instance.pk} received. Tracking stage: {instance.tracking_stage}")
