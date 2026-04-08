from django.contrib import admin

from .models import POSOrder


@admin.register(POSOrder)
class POSOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "name", "phone", "total", "created_at")
    list_filter = ("vendor", "created_at")
    search_fields = ("name", "phone", "vendor__subdomain")

