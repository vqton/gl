"""Django app config for Inventory (Kho) module."""

from django.apps import AppConfig


class KhoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.kho"
    verbose_name = "Quản lý kho"

    def ready(self):
        """Import signals when app is ready."""
        import apps.kho.signals  # noqa: F401
