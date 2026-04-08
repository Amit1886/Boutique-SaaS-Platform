from django.apps import AppConfig


class TailorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tailors"

    def ready(self) -> None:
        from . import signals  # noqa: F401

