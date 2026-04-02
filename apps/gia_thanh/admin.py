"""Admin configuration for Giá Thành."""

from django.contrib import admin

from .models import (
    BangPhanBoChiPhi,
    BangTinhGiaThanh,
    ChiTietPhanBoChiPhi,
    DoiTuongTapHopChiPhi,
    KhoanMucChiPhi,
    PhieuTapHopChiPhi,
)


@admin.register(DoiTuongTapHopChiPhi)
class DoiTuongTapHopChiPhiAdmin(admin.ModelAdmin):
    list_display = ("ma_doi_tuong", "ten_doi_tuong", "loai", "is_active")
    list_filter = ("loai", "is_active")
    search_fields = ("ma_doi_tuong", "ten_doi_tuong")


@admin.register(KhoanMucChiPhi)
class KhoanMucChiPhiAdmin(admin.ModelAdmin):
    list_display = ("ma_khoan_muc", "ten_khoan_muc", "loai", "tk_chi_phi")
    list_filter = ("loai",)
    search_fields = ("ma_khoan_muc", "ten_khoan_muc")


@admin.register(PhieuTapHopChiPhi)
class PhieuTapHopChiPhiAdmin(admin.ModelAdmin):
    list_display = (
        "so_chung_tu",
        "ngay_chung_tu",
        "doi_tuong",
        "khoan_muc",
        "so_tien",
        "trang_thai",
    )
    list_filter = ("trang_thai", "khoan_muc__loai")
    date_hierarchy = "ngay_chung_tu"


@admin.register(BangPhanBoChiPhi)
class BangPhanBoChiPhiAdmin(admin.ModelAdmin):
    list_display = (
        "thang",
        "nam",
        "phuong_phap",
        "tong_chi_phi",
        "trang_thai",
    )
    list_filter = ("phuong_phap", "trang_thai")


@admin.register(ChiTietPhanBoChiPhi)
class ChiTietPhanBoChiPhiAdmin(admin.ModelAdmin):
    list_display = ("bang_phan_bo", "doi_tuong", "he_so", "muc_phan_bo")


@admin.register(BangTinhGiaThanh)
class BangTinhGiaThanhAdmin(admin.ModelAdmin):
    list_display = (
        "thang",
        "nam",
        "doi_tuong",
        "gia_thanh_sp_hoan_thanh",
        "gia_thanh_don_vi",
        "trang_thai",
    )
    list_filter = ("trang_thai",)
