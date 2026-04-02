"""Bank admin registration."""

from django.contrib import admin

from apps.ngan_hang.models import DoiChieuNganHang, GiayBaoCo, GiayBaoNo, UyNhiemChi


@admin.register(GiayBaoNo)
class GiayBaoNoAdmin(admin.ModelAdmin):
    list_display = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "so_tien", "trang_thai", "da_doi_chieu"]
    list_filter = ["trang_thai", "da_doi_chieu"]
    search_fields = ["so_chung_tu", "dien_giai"]


@admin.register(GiayBaoCo)
class GiayBaoCoAdmin(admin.ModelAdmin):
    list_display = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "so_tien", "trang_thai", "da_doi_chieu"]
    list_filter = ["trang_thai", "da_doi_chieu"]
    search_fields = ["so_chung_tu", "dien_giai"]


@admin.register(UyNhiemChi)
class UyNhiemChiAdmin(admin.ModelAdmin):
    list_display = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "nha_cung_cap", "so_tien", "trang_thai"]
    list_filter = ["trang_thai"]
    search_fields = ["so_chung_tu", "noi_dung"]


@admin.register(DoiChieuNganHang)
class DoiChieuNganHangAdmin(admin.ModelAdmin):
    list_display = ["tai_khoan_ngan_hang", "thang", "nam", "so_du_so_sach", "so_du_ngan_hang", "chenh_lech", "trang_thai"]
    list_filter = ["trang_thai", "nam", "thang"]
