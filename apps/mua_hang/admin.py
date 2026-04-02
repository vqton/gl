"""Mua hàng admin."""

from django.contrib import admin

from apps.mua_hang.models import BangPhanBoChiPhi, DeXuatMuaHang, DonDatHang, DonDatHangChiTiet, TraHangNCC


class DonDatHangChiTietInline(admin.TabularInline):
    model = DonDatHangChiTiet
    extra = 1


@admin.register(DeXuatMuaHang)
class DeXuatMuaHangAdmin(admin.ModelAdmin):
    list_display = ["so_de_xuat", "ngay", "nguoi_de_xuat", "trang_thai"]
    list_filter = ["trang_thai"]
    search_fields = ["so_de_xuat", "ly_do"]


@admin.register(DonDatHang)
class DonDatHangAdmin(admin.ModelAdmin):
    list_display = ["so_don_hang", "ngay", "nha_cung_cap", "tong_tien", "trang_thai"]
    list_filter = ["trang_thai"]
    search_fields = ["so_don_hang"]
    inlines = [DonDatHangChiTietInline]


@admin.register(TraHangNCC)
class TraHangNCCAdmin(admin.ModelAdmin):
    list_display = ["so_chung_tu", "ngay", "nha_cung_cap", "tong_tien", "trang_thai"]
    list_filter = ["trang_thai"]


@admin.register(BangPhanBoChiPhi)
class BangPhanBoChiPhiAdmin(admin.ModelAdmin):
    list_display = ["loai_chi_phi", "tong_chi_phi", "doi_tuong_phan_bo", "so_tien_phan_bo"]
    list_filter = ["loai_chi_phi"]
