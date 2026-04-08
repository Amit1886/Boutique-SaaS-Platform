from django.contrib import admin

from .models import RazorpayTransaction


@admin.register(RazorpayTransaction)
class RazorpayTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "plan", "amount", "status", "created_at")
    list_filter = ("status", "vendor", "created_at")
    search_fields = ("id", "razorpay_order_id", "vendor__subdomain")

