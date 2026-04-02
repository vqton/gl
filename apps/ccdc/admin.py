"""CCDC admin."""

from django.contrib import admin

from apps.ccdc.models import BangPhanBoCCDC, CongCuDungCu


@admin.register(CongCuDungCu)
class CongCuDungCuAdmin(admin.ModelAdmin):
    list_display = ["ma_ccdc", "ten_ccdc", "ngay_mua", "tong_gia_tri", "phuong_phap_phan_bo", "so_ky_phan_bo", "trang_thai"]
    list_filter = ["trang_thai", "phuong_phap_phan_bo"]
    search_fields = ["ma_ccdc", "ten_ccdc"]


@admin.register(BangPhanBoCCDC)
class BangPhanBoCCDCAdmin(admin.ModelAdmin):
    list_display = ["ccdc", "thang", "nam", "so_tien_phan_bo", "trang_thai"]
    list_filter = ["trang_thai", "nam", "thang"]
