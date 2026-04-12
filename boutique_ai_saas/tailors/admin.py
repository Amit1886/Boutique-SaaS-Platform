from django.contrib import admin

from .models import TailorPayment, TailorProfile, TailorTask


@admin.register(TailorProfile)
class TailorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor", "speciality", "daily_capacity")
    list_filter = ("vendor",)
    search_fields = ("user__username", "vendor__subdomain")


@admin.register(TailorTask)
class TailorTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "tailor", "order", "task_type", "status", "piece_rate", "completed_at", "deadline")
    list_filter = ("status", "task_type", "tailor__vendor")
    search_fields = ("id", "order__id", "tailor__user__username")


@admin.register(TailorPayment)
class TailorPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "tailor", "period_start", "period_end", "pieces_done", "amount", "status", "paid_at")
    list_filter = ("status", "tailor__vendor", "period_start")
    search_fields = ("id", "tailor__user__username", "tailor__vendor__subdomain")
