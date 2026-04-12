from django.contrib import admin

from .models import TemplateUsageEvent, VendorAnalytics


@admin.register(VendorAnalytics)
class VendorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("vendor", "total_orders", "revenue")
    list_filter = ("vendor",)
    search_fields = ("vendor__subdomain", "vendor__business_name")


@admin.register(TemplateUsageEvent)
class TemplateUsageEventAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "template", "user_id", "event_type", "created_at")
    list_filter = ("vendor", "event_type", "created_at")
    search_fields = ("template__name", "vendor__subdomain", "user_id")
