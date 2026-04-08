from django.contrib import admin
from django.utils.html import format_html

from .models import Product, SavedLook, TemplateDesign


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "vendor", "category", "price", "stock_meter", "is_tailoring_service")
    list_filter = ("category", "is_tailoring_service", "vendor")
    search_fields = ("name", "vendor__business_name", "vendor__subdomain")

    def thumb(self, obj: Product) -> str:
        if not obj.image:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:8px;" />',
            obj.image.url,
        )

    thumb.short_description = "Image"


@admin.register(TemplateDesign)
class TemplateDesignAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "vendor", "category", "default_flag")
    list_filter = ("category", "default_flag", "vendor")
    search_fields = ("name", "vendor__subdomain")

    def thumb(self, obj: TemplateDesign) -> str:
        if not obj.image:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:8px;" />',
            obj.image.url,
        )

    thumb.short_description = "Image"


@admin.register(SavedLook)
class SavedLookAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor", "title", "created_at")
    list_filter = ("vendor", "created_at")
    search_fields = ("user__username", "title", "vendor__subdomain")

