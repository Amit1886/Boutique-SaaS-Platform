from django.contrib import admin
from django.utils.html import format_html

from .models import Order, Product, TemplateDesign, TryOnRequest, TryOnStatus


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name",)

    def thumb(self, obj: Product) -> str:
        if not obj.image:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',
            obj.image.url,
        )

    thumb.short_description = "Image"


@admin.register(TemplateDesign)
class TemplateDesignAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

    def thumb(self, obj: TemplateDesign) -> str:
        if not obj.image:
            return ""
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',
            obj.image.url,
        )

    thumb.short_description = "Image"


@admin.action(description="Mark selected as Approved")
def mark_approved(modeladmin, request, queryset):
    queryset.update(status=TryOnStatus.APPROVED)


@admin.action(description="Mark selected as Rejected")
def mark_rejected(modeladmin, request, queryset):
    queryset.update(status=TryOnStatus.REJECTED)


@admin.register(TryOnRequest)
class TryOnRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_thumb",
        "template_thumb",
        "generated_thumb",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    actions = [mark_approved, mark_rejected]

    def user_thumb(self, obj: TryOnRequest) -> str:
        if not obj.user_image:
            return ""
        return format_html(
            '<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:6px;" />',
            obj.user_image.url,
        )

    def template_thumb(self, obj: TryOnRequest) -> str:
        if not obj.selected_template or not obj.selected_template.image:
            return ""
        return format_html(
            '<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:6px;" />',
            obj.selected_template.image.url,
        )

    def generated_thumb(self, obj: TryOnRequest) -> str:
        if not obj.auto_generated_image:
            return ""
        return format_html(
            '<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:6px;" />',
            obj.auto_generated_image.url,
        )

    user_thumb.short_description = "User"
    template_thumb.short_description = "Template"
    generated_thumb.short_description = "Generated"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "amount", "status", "tryon_status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "product__name")

    def tryon_status(self, obj: Order) -> str:
        return obj.tryon_request.status

    def created_at(self, obj: Order) -> str:
        return obj.tryon_request.created_at.strftime("%Y-%m-%d %H:%M")

    created_at.admin_order_field = "tryon_request__created_at"

