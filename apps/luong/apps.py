"""Django app config for Payroll (Lương & BHXH)."""

from django.apps import AppConfig


class LuongConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.luong"
    verbose_name = "Lương & BHXH"
