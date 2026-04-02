"""Danh muc (Master Data) app configuration."""

from django.apps import AppConfig


class DanhMucConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.danh_muc"
    verbose_name = "Danh mục (Master Data)"

    def ready(self):
        import apps.danh_muc.signals  # noqa: F401
