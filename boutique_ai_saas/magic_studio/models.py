from __future__ import annotations

from django.db import models


class ProductBase(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    primary_color = models.CharField(max_length=32, default="#db2777")
    tags = models.CharField(max_length=300, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Saree(ProductBase):
    layer_body_png = models.CharField(max_length=500, blank=True, default="")
    layer_pallu_png = models.CharField(max_length=500, blank=True, default="")
    layer_border_png = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


class Blouse(ProductBase):
    template_png = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


class Accessory(ProductBase):
    image_png = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


class SavedLook(models.Model):
    user_name = models.CharField(max_length=120, default="Guest")
    saree_id = models.IntegerField(blank=True, null=True)
    blouse_id = models.IntegerField(blank=True, null=True)
    accessories_json = models.TextField(default="[]")
    image_card_png = models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Look {self.pk}"


class Moodboard(models.Model):
    user_name = models.CharField(max_length=120, unique=True, default="Guest")
    mood_key = models.CharField(max_length=40, default="festive")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.user_name}: {self.mood_key}"


class FestivalTheme(models.Model):
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    theme_color = models.CharField(max_length=32, default="#db2777")
    banner_text = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return self.name


class UXFlag(models.Model):
    key = models.CharField(max_length=80, unique=True, db_index=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["key"]

    def __str__(self) -> str:
        return f"{self.key}={self.enabled}"

