from django.apps import AppConfig


class BoutiqueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boutique"

    def ready(self) -> None:
        from . import signals  # noqa: F401

