"""Management command to create default user groups and permissions."""

import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction


class Command(BaseCommand):
    help = "Create default user groups and permissions for accounting system"

    PERMISSIONS = {
        "Quan tri vien": {
            "danh_muc": [
                "taikhoanketoan",
                "donvi",
                "khachhang",
                "nhacungcap",
                "nganhang",
                "taikhoannganhang",
                "hanghoa",
            ],
            "nghiep_vu": [
                "buttoan",
                "hoadon",
                "nhapkho",
                "xuatkho",
                "kho",
                "phieuthu",
                "phieuchi",
            ],
            "kho": ["kho", "vattuhanghoa", "kholot", "khoentry", "tonkho"],
            "tai_san": ["taisancodinh", "bangkhauhao"],
            "luong": ["nhanvien", "bangluong"],
            "users": ["nguoidung"],
        },
        "Ke toan vien": {
            "danh_muc": [
                "taikhoanketoan",
                "donvi",
                "khachhang",
                "nhacungcap",
                "nganhang",
                "taikhoannganhang",
                "hanghoa",
            ],
            "nghiep_vu": [
                "buttoan",
                "hoadon",
                "nhapkho",
                "xuatkho",
                "kho",
                "phieuthu",
                "phieuchi",
            ],
            "kho": ["kho", "vattuhanghoa", "kholot", "khoentry", "tonkho"],
            "tai_san": ["taisancodinh", "bangkhauhao"],
            "luong": ["nhanvien", "bangluong"],
        },
    }

    GROUP_DISPLAY_NAMES = {
        "Quan tri vien": "System Admin",
        "Ke toan vien": "Accountant",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete and recreate groups if they exist",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get("force", False)

        for group_name, app_perms in self.PERMISSIONS.items():
            display_name = self.GROUP_DISPLAY_NAMES.get(group_name, group_name)
            group, created = Group.objects.get_or_create(name=group_name)

            if not created and force:
                group.permissions.clear()
                self.stdout.write(
                    f"[WARNING] Cleared permissions for group: {display_name}"
                )

            perms_to_add = []

            for app_label, model_names in app_perms.items():
                for model_name in model_names:
                    for codename in ["view", "add", "change", "delete"]:
                        try:
                            perm = Permission.objects.get(
                                codename=f"{codename}_{model_name}",
                                content_type__app_label=app_label,
                            )
                            perms_to_add.append(perm)
                        except Permission.DoesNotExist:
                            pass

            group.permissions.add(*perms_to_add)

            if created:
                self.stdout.write(f"[SUCCESS] Created group: {display_name}")
            else:
                self.stdout.write(f"[SUCCESS] Updated group: {display_name}")

            self.stdout.write(f"  - Permissions count: {group.permissions.count()}")

        self.stdout.write("\n[SUCCESS] User groups created successfully!")
