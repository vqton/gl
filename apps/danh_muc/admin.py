"""Admin configuration for danh_muc app."""

from django.contrib import admin

from apps.danh_muc.models import (
    DonVi,
    HangHoa,
    KhachHang,
    NganHang,
    NhaCungCap,
    TaiKhoanKeToan,
    TaiKhoanNganHang,
)


@admin.register(TaiKhoanKeToan)
class TaiKhoanKeToanAdmin(admin.ModelAdmin):
    list_display = [
        "ma_tai_khoan",
        "ten_tai_khoan",
        "cap_do",
        "loai_tai_khoan",
        "is_active",
        "is_immutable",
    ]
    list_filter = ["cap_do", "loai_tai_khoan", "is_active", "is_immutable"]
    search_fields = ["ma_tai_khoan", "ten_tai_khoan"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    fieldsets = [
        (
            "Thông tin tài khoản",
            {
                "fields": [
                    "ma_tai_khoan",
                    "ten_tai_khoan",
                    "cap_do",
                    "tai_khoan_me",
                    "loai_tai_khoan",
                ]
            },
        ),
        (
            "Mô tả",
            {"fields": ["mo_ta"], "classes": ["collapse"]},
        ),
        (
            "Trạng thái",
            {"fields": ["is_active", "is_immutable"]},
        ),
        (
            "Audit",
            {
                "fields": ["created_at", "updated_at", "created_by", "updated_by"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(DonVi)
class DonViAdmin(admin.ModelAdmin):
    list_display = [
        "ten_don_vi",
        "ma_so_thue",
        "loai_don_vi",
        "is_active",
    ]
    list_filter = ["loai_don_vi", "is_active"]
    search_fields = ["ten_don_vi", "ma_so_thue"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(NhaCungCap)
class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = [
        "ma_ncc",
        "ten_ncc",
        "ma_so_thue",
        "dien_thoai",
        "is_active",
    ]
    list_filter = ["is_active"]
    search_fields = ["ma_ncc", "ten_ncc", "ma_so_thue"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = [
        "ma_kh",
        "ten_kh",
        "ma_so_thue",
        "dien_thoai",
        "is_active",
    ]
    list_filter = ["is_active"]
    search_fields = ["ma_kh", "ten_kh", "ma_so_thue"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(NganHang)
class NganHangAdmin(admin.ModelAdmin):
    list_display = [
        "ma_ngan_hang",
        "ten_ngan_hang",
        "ma_dien_toan",
    ]
    search_fields = ["ma_ngan_hang", "ten_ngan_hang"]


@admin.register(TaiKhoanNganHang)
class TaiKhoanNganHangAdmin(admin.ModelAdmin):
    list_display = [
        "so_tai_khoan",
        "ten_chu_tai_khoan",
        "ngan_hang",
        "tien_te",
        "is_active",
    ]
    list_filter = ["tien_te", "is_active"]
    search_fields = ["so_tai_khoan", "ten_chu_tai_khoan"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(HangHoa)
class HangHoaAdmin(admin.ModelAdmin):
    list_display = [
        "ma_hang_hoa",
        "ten_hang_hoa",
        "don_vi_tinh",
        "gia_ban",
        "thue_suat_gtgt",
        "is_active",
    ]
    list_filter = ["thue_suat_gtgt", "is_active"]
    search_fields = ["ma_hang_hoa", "ten_hang_hoa"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
