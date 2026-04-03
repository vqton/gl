"""Seed predefined roles for RBAC system."""

from django.core.management.base import BaseCommand

from apps.he_thong.models import VaiTro

PREDEFINED_ROLES = [
    {
        "ma": "ke_toan_truong",
        "ten": "Kế toán trưởng",
        "mo_ta": "Toàn quyền truy cập hệ thống kế toán",
    },
    {
        "ma": "ke_toan_vien",
        "ten": "Kế toán viên",
        "mo_ta": "Đọc/Ghi, không được xóa chứng từ đã ghi sổ",
    },
    {
        "ma": "thu_quy",
        "ten": "Thủ quỹ",
        "mo_ta": "Chỉ được truy cập module Tiền mặt/Ngân hàng",
    },
    {
        "ma": "giam_doc",
        "ten": "Giám đốc",
        "mo_ta": "Chỉ xem báo cáo, không được chỉnh sửa",
    },
]


class Command(BaseCommand):
    help = "Seed predefined roles for the RBAC system"

    def handle(self, *args, **options):
        """Create or update predefined roles."""
        for role_data in PREDEFINED_ROLES:
            role, created = VaiTro.objects.update_or_create(
                ma=role_data["ma"],
                defaults={
                    "ten": role_data["ten"],
                    "mo_ta": role_data["mo_ta"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role.ten}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated role: {role.ten}"))

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {len(PREDEFINED_ROLES)} roles successfully")
        )
