from django.contrib import admin

from .models import WhatsAppMessage


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "from_number", "to_number", "created_at")
    search_fields = ("from_number", "to_number", "text")
    list_filter = ("vendor", "created_at")

