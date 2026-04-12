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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet_summary_api(request):
    from wallet.services import get_or_create_wallet
    from wallet.models import WalletTransaction

    wallet = get_or_create_wallet(request.user)
    txs = WalletTransaction.objects.filter(wallet=wallet).order_by("-id")[:50]
    return Response(
        {
            "ok": True,
            "balance": str(wallet.balance),
            "ref_code": getattr(getattr(request.user, "referral_code", None), "code", ""),
            "transactions": [
                {
                    "id": t.id,
                    "type": t.tx_type,
                    "status": t.status,
                    "amount": str(t.amount),
                    "order_id": t.order_id,
                    "note": t.note,
                    "created_at": t.created_at.isoformat(),
                }
                for t in txs
            ],
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def tailor_reviews_api(request, tailor_id: int):
    from tailors.models import TailorReview

    qs = TailorReview.objects.filter(tailor_id=tailor_id).select_related("tailor", "tailor__user")[:100]
    return Response(
        {
            "ok": True,
            "reviews": [
                {"id": r.id, "rating": r.rating, "comment": r.comment, "created_at": r.created_at.isoformat()}
                for r in qs
            ],
        }
    )
