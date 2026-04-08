from django.contrib import admin

from .models import VendorAnalytics


@admin.register(VendorAnalytics)
class VendorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("vendor", "total_orders", "revenue")
    list_filter = ("vendor",)
    search_fields = ("vendor__subdomain", "vendor__business_name")

