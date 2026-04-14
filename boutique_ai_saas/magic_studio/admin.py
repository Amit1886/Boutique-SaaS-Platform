from django.contrib import admin

from .models import Accessory, Blouse, FestivalTheme, Moodboard, Saree, SavedLook, UXFlag


@admin.register(Saree)
class SareeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "primary_color", "tags", "created_at")
    search_fields = ("name", "tags")


@admin.register(Blouse)
class BlouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "primary_color", "tags", "created_at")
    search_fields = ("name", "tags")


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "primary_color", "tags", "created_at")
    search_fields = ("name", "tags")


@admin.register(SavedLook)
class SavedLookAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "saree_id", "blouse_id", "created_at")
    search_fields = ("user_name",)


@admin.register(Moodboard)
class MoodboardAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "mood_key", "updated_at")
    search_fields = ("user_name", "mood_key")


@admin.register(FestivalTheme)
class FestivalThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date", "theme_color")
    search_fields = ("name",)


@admin.register(UXFlag)
class UXFlagAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "enabled")
    search_fields = ("key",)

