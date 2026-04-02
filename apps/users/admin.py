"""Admin configuration for users app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import NguoiDung


@admin.register(NguoiDung)
class NguoiDungAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "email",
        "user_type",
        "company",
        "is_system_admin",
        "is_active",
    ]
    list_filter = [
        "user_type",
        "is_system_admin",
        "is_active",
        "is_staff",
    ]
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Thông tin bổ sung",
            {
                "fields": (
                    "user_type",
                    "company",
                    "is_system_admin",
                    "phone",
                    "department",
                )
            },
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Thông tin bổ sung",
            {
                "fields": (
                    "user_type",
                    "company",
                    "is_system_admin",
                    "phone",
                    "department",
                )
            },
        ),
    )
