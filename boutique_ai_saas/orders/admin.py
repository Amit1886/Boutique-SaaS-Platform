from django.contrib import admin

from .models import Order, OrderFeedback


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "product", "amount", "status", "tracking_stage", "created_at")
    list_filter = ("vendor", "status", "tracking_stage", "created_at")
    search_fields = ("id", "vendor__subdomain", "product__name")


@admin.register(OrderFeedback)
class OrderFeedbackAdmin(admin.ModelAdmin):
    list_display = ("order", "rating", "created_at")
    search_fields = ("order__id",)
