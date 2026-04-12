from __future__ import annotations

from django.db.models import Count, Q

from .models import TailorProfile, TaskStatus


def choose_tailor_for_order(*, vendor) -> TailorProfile | None:
    """
    Pick the best tailor for a vendor using a simple load balancer:
    - Prefer higher rating
    - Prefer lower active workload
    - Respect daily_capacity (soft)
    """
    qs = TailorProfile.objects.filter(vendor=vendor)
    if not qs.exists():
        return None

    qs = qs.annotate(
        active_tasks=Count("tasks", filter=~Q(tasks__status=TaskStatus.DONE)),
    ).order_by("-avg_rating", "active_tasks", "id")

    best = qs.first()
    if not best:
        return None

    # Soft capacity check: if best is overloaded, try the next one.
    if best.daily_capacity and best.active_tasks >= best.daily_capacity:
        alt = qs.exclude(id=best.id).first()
        return alt or best
    return best
