"""Django app config for Fixed Assets (Tài sản cố định)."""

from django.apps import AppConfig


class TaiSanConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tai_san"
    verbose_name = "Tài sản cố định"
