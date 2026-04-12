from __future__ import annotations

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import WalletTransaction
from .services import apply_referral_code, credit, debit, get_or_create_wallet


@login_required
def wallet_dashboard(request: HttpRequest) -> HttpResponse:
    wallet = get_or_create_wallet(request.user)
    txs = WalletTransaction.objects.filter(wallet=wallet).order_by("-id")[:200]
    ref_code = getattr(getattr(request.user, "referral_code", None), "code", "")
    return render(request, "wallet_dashboard.html", {"wallet": wallet, "txs": txs, "ref_code": ref_code})


@login_required
@require_http_methods(["POST"])
def wallet_apply_referral(request: HttpRequest) -> HttpResponse:
    code = request.POST.get("code") or ""
    try:
        apply_referral_code(user=request.user, code=code)
        messages.success(request, "Referral applied. Bonus added to wallet.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect("wallet_dashboard")


@staff_member_required
@require_http_methods(["GET", "POST"])
def admin_wallet_adjust(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        action = (request.POST.get("action") or "credit").strip().lower()
        amount = request.POST.get("amount") or "0"
        note = request.POST.get("note") or ""
        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect("admin_wallet_adjust")
        try:
            if action == "debit":
                debit(user=user, amount=amount, note=note, meta={"by": request.user.username, "source": "admin"})
            else:
                credit(user=user, amount=amount, tx_type="adjustment", note=note, meta={"by": request.user.username, "source": "admin"})
            messages.success(request, "Wallet updated.")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("admin_wallet_adjust")

    return render(request, "admin_wallet.html", {})

