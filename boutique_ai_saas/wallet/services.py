from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import transaction

from .models import (
    ReferralInvite,
    TxStatus,
    TxType,
    WalletAccount,
    WalletTransaction,
)


def _d(value) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value or "0"))


def _q2(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@transaction.atomic
def get_or_create_wallet(user) -> WalletAccount:
    wallet, _ = WalletAccount.objects.select_for_update().get_or_create(user=user)
    return wallet


@transaction.atomic
def credit(
    *,
    user,
    amount,
    tx_type: str = TxType.CREDIT,
    status: str = TxStatus.SUCCEEDED,
    note: str = "",
    order_id: int | None = None,
    ref_code: str = "",
    meta: dict | None = None,
) -> WalletTransaction:
    wallet = get_or_create_wallet(user)
    amt = _q2(_d(amount))
    tx = WalletTransaction.objects.create(
        wallet=wallet,
        tx_type=tx_type,
        status=status,
        amount=amt,
        note=note,
        order_id=order_id,
        ref_code=ref_code,
        meta=meta or {},
    )
    if status == TxStatus.SUCCEEDED:
        wallet.balance = _q2(_d(wallet.balance) + amt)
        wallet.save(update_fields=["balance", "updated_at"])
    return tx


@transaction.atomic
def debit(*, user, amount, note: str = "", meta: dict | None = None) -> WalletTransaction:
    wallet = get_or_create_wallet(user)
    amt = _q2(_d(amount))
    if _d(wallet.balance) < amt:
        raise ValueError("Insufficient wallet balance")
    tx = WalletTransaction.objects.create(
        wallet=wallet,
        tx_type=TxType.DEBIT,
        status=TxStatus.SUCCEEDED,
        amount=amt,
        note=note,
        meta=meta or {},
    )
    wallet.balance = _q2(_d(wallet.balance) - amt)
    wallet.save(update_fields=["balance", "updated_at"])
    return tx


def cashback_amount(order_amount) -> Decimal:
    rate = Decimal(str(getattr(settings, "WALLET_CASHBACK_RATE", "0.02")))
    return _q2(_d(order_amount) * rate)


@transaction.atomic
def create_cashback_pending(*, user, order_id: int, order_amount) -> WalletTransaction | None:
    if not user:
        return None
    amt = cashback_amount(order_amount)
    if amt <= 0:
        return None
    wallet = get_or_create_wallet(user)
    existing = WalletTransaction.objects.filter(wallet=wallet, tx_type=TxType.CASHBACK, order_id=order_id).first()
    if existing:
        return existing
    return WalletTransaction.objects.create(
        wallet=wallet,
        tx_type=TxType.CASHBACK,
        status=TxStatus.PENDING,
        amount=amt,
        order_id=order_id,
        note=f"Cashback for order #{order_id}",
        meta={"rate": str(getattr(settings, "WALLET_CASHBACK_RATE", "0.02"))},
    )


@transaction.atomic
def settle_cashback(*, user, order_id: int, succeed: bool) -> WalletTransaction | None:
    if not user:
        return None
    wallet = get_or_create_wallet(user)
    tx = (
        WalletTransaction.objects.select_for_update()
        .filter(wallet=wallet, tx_type=TxType.CASHBACK, order_id=order_id)
        .first()
    )
    if not tx or tx.status != TxStatus.PENDING:
        return tx
    tx.status = TxStatus.SUCCEEDED if succeed else TxStatus.VOID
    tx.save(update_fields=["status"])
    if succeed:
        wallet.balance = _q2(_d(wallet.balance) + _d(tx.amount))
        wallet.save(update_fields=["balance", "updated_at"])
    return tx


@transaction.atomic
def apply_referral_code(*, user, code: str) -> ReferralInvite:
    code = (code or "").strip()
    if not code:
        raise ValueError("Referral code required")
    if hasattr(user, "referral_used"):
        raise ValueError("Referral already applied")

    from .models import ReferralCode  # local import to avoid cycles

    ref = ReferralCode.objects.select_related("user").filter(code__iexact=code).first()
    if not ref:
        raise ValueError("Invalid referral code")
    if ref.user_id == user.id:
        raise ValueError("You cannot use your own referral code")

    invite = ReferralInvite.objects.create(referrer=ref.user, referred_user=user, code=ref.code)

    bonus = Decimal(str(getattr(settings, "WALLET_REFERRAL_BONUS", "25.00")))
    if bonus > 0:
        credit(user=ref.user, amount=bonus, tx_type=TxType.REFERRAL, note=f"Referral bonus for {user.username}", ref_code=ref.code)
        credit(user=user, amount=bonus, tx_type=TxType.REFERRAL, note="Referral bonus", ref_code=ref.code)
        invite.status = "rewarded"
        invite.save(update_fields=["status"])
    return invite

