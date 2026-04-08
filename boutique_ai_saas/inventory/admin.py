from django.contrib import admin

from .models import FabricStock


@admin.register(FabricStock)
class FabricStockAdmin(admin.ModelAdmin):
    list_display = ("vendor", "fabric_type", "meter_available", "meter_used")
    list_filter = ("vendor",)
    search_fields = ("fabric_type", "vendor__subdomain")

