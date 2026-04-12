from __future__ import annotations

from datetime import timedelta

from django.db.models import Count
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone

from boutique.models import Favorite, TemplateDesign

from .models import TemplateUsageEvent


def get_trending_designs(*, vendor_id: int | None = None, days: int = 30, limit: int = 20):
    """
    Return a list of {template, uses} for the most used templates.
    """
    try:
        since = timezone.now() - timedelta(days=days)
        qs = TemplateUsageEvent.objects.filter(created_at__gte=since, event_type=TemplateUsageEvent.EventType.TRYON)
        if vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        agg = qs.values("template_id").annotate(uses=Count("id")).order_by("-uses")[:limit]
        template_ids = [row["template_id"] for row in agg]
        templates = {t.id: t for t in TemplateDesign.objects.filter(id__in=template_ids).select_related("vendor")}
        return [{"template": templates.get(row["template_id"]), "uses": row["uses"]} for row in agg if templates.get(row["template_id"])]
    except (OperationalError, ProgrammingError):
        # Most common cause: migrations not applied yet (e.g. new install).
        return []


def get_personal_feed(user, *, limit: int = 20):
    """
    Return a list of TemplateDesign personalized for the user (dummy heuristic).

    Heuristic:
    - Start with user's favorited templates
    - Add templates from vendors/categories they've tried-on recently
    - Fallback to trending
    """
    if not user or not getattr(user, "id", None):
        return [row["template"] for row in get_trending_designs(limit=limit)]

    try:
        favorites = list(
            Favorite.objects.filter(user_id=user.id)
            .select_related("template", "template__vendor")
            .order_by("-created_at")[:limit]
        )
    except (OperationalError, ProgrammingError):
        favorites = []
    fav_templates = [f.template for f in favorites]
    if len(fav_templates) >= limit:
        return fav_templates[:limit]

    # Recent try-ons to infer vendor/category interest
    try:
        recent = (
            TemplateUsageEvent.objects.filter(user_id=user.id, event_type=TemplateUsageEvent.EventType.TRYON)
            .order_by("-created_at")
            .values_list("template_id", flat=True)[:200]
        )
    except (OperationalError, ProgrammingError):
        recent = []
    recent_templates = list(TemplateDesign.objects.filter(id__in=list(recent)).select_related("vendor")[:limit])

    # Combine unique
    seen = set()
    out: list[TemplateDesign] = []
    for t in fav_templates + recent_templates:
        if not t or t.id in seen:
            continue
        seen.add(t.id)
        out.append(t)
        if len(out) >= limit:
            return out

    trending = [row["template"] for row in get_trending_designs(limit=limit)]
    for t in trending:
        if t and t.id not in seen:
            out.append(t)
            seen.add(t.id)
        if len(out) >= limit:
            break
    return out
