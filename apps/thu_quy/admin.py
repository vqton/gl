"""Admin configuration for Thủ Quỹ."""

from django.contrib import admin

from .models import KiemKeQuy, XuLyChenhLechQuy


@admin.register(KiemKeQuy)
class KiemKeQuyAdmin(admin.ModelAdmin):
    list_display = (
        "so_kiem_ke",
        "ngay_kiem_ke",
        "ky_quy",
        "so_du_so_sach",
        "so_thuc_te",
        "chen_lech",
        "trang_thai",
    )
    list_filter = ("trang_thai",)
    date_hierarchy = "ngay_kiem_ke"
    search_fields = ("so_kiem_ke", "ky_quy")


@admin.register(XuLyChenhLechQuy)
class XuLyChenhLechQuyAdmin(admin.ModelAdmin):
    list_display = (
        "kiem_ke",
        "loai",
        "so_tien",
        "xu_ly",
        "but_toan",
    )
    list_filter = ("loai", "xu_ly")
