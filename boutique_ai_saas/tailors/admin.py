from django.contrib import admin

from .models import TailorProfile, TailorTask


@admin.register(TailorProfile)
class TailorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor", "speciality", "daily_capacity")
    list_filter = ("vendor",)
    search_fields = ("user__username", "vendor__subdomain")


@admin.register(TailorTask)
class TailorTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "tailor", "order", "task_type", "status", "deadline")
    list_filter = ("status", "task_type", "tailor__vendor")
    search_fields = ("id", "order__id", "tailor__user__username")

