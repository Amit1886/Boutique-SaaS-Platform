from __future__ import annotations

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from analytics.services import get_personal_feed, get_trending_designs

from .serializers import TemplateDesignSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_api(request):
    rows = get_trending_designs(limit=20)
    templates = [row["template"] for row in rows]
    data = TemplateDesignSerializer(templates, many=True, context={"request": request}).data
    return Response({"ok": True, "templates": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def personal_feed_api(request):
    templates = get_personal_feed(request.user, limit=20)
    data = TemplateDesignSerializer(templates, many=True, context={"request": request}).data
    return Response({"ok": True, "templates": data})

