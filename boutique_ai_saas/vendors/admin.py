from django.contrib import admin
from django.utils.html import format_html

from .models import FeatureAccess, Plan, VendorProfile


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


@admin.register(FeatureAccess)
class FeatureAccessAdmin(admin.ModelAdmin):
    list_display = ("plan", "feature_key", "enabled")
    list_filter = ("plan", "enabled")
    search_fields = ("feature_key",)


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ("logo_thumb", "business_name", "subdomain", "plan", "theme_color", "upi_id", "user")
    list_filter = ("plan",)
    search_fields = ("business_name", "subdomain", "user__username")

    def logo_thumb(self, obj: VendorProfile) -> str:
        if not obj.logo:
            return ""
        return format_html(
            '<img src="{}" style="height:36px;width:36px;object-fit:cover;border-radius:8px;" />',
            obj.logo.url,
        )

    logo_thumb.short_description = "Logo"
