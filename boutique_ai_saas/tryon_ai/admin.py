from django.contrib import admin
from django.utils.html import format_html

from .models import AITaskHistory, TryOnSession


@admin.register(TryOnSession)
class TryOnSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "vendor", "user", "type", "orig_thumb", "template", "result_thumb", "created_at")
    list_filter = ("vendor", "type", "created_at")
    search_fields = ("id", "vendor__subdomain", "user__username")

    def orig_thumb(self, obj: TryOnSession) -> str:
        if not obj.original_image:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:8px;" />',
            obj.original_image.url,
        )

    def result_thumb(self, obj: TryOnSession) -> str:
        if not obj.ai_result:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:8px;" />',
            obj.ai_result.url,
        )

    def template(self, obj: TryOnSession) -> str:
        return obj.selected_template.name if obj.selected_template else "—"

    orig_thumb.short_description = "Original"
    result_thumb.short_description = "Result"


@admin.register(AITaskHistory)
class AITaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "provider", "task_type", "status", "duration_ms", "created_at")
    list_filter = ("provider", "task_type", "status", "created_at")
    search_fields = ("id", "session__id", "task_type", "provider")
