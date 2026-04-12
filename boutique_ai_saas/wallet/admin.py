from django.contrib import admin

from .models import ReferralCode, ReferralInvite, WalletAccount, WalletTransaction


@admin.register(WalletAccount)
class WalletAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "updated_at")
    search_fields = ("user__username", "user__email")


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "tx_type", "status", "amount", "order_id", "ref_code", "created_at")
    list_filter = ("tx_type", "status")
    search_fields = ("id", "wallet__user__username", "order_id", "ref_code")


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "created_at")
    search_fields = ("code", "user__username")


@admin.register(ReferralInvite)
class ReferralInviteAdmin(admin.ModelAdmin):
    list_display = ("id", "referrer", "referred_user", "code", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "referrer__username", "referred_user__username", "code")

