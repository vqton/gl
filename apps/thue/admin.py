"""Thuế admin."""

from django.contrib import admin

from apps.thue.models import BangKeHoaDonBanRa, BangKeHoaDonMuaVao, ToKhaiGTGT, ToKhaiTNCN, ToKhaiTNDNTamTinh


@admin.register(BangKeHoaDonMuaVao)
class BangKeHoaDonMuaVaoAdmin(admin.ModelAdmin):
    list_display = ["thang", "nam", "hoa_don", "tien_chua_thue", "thue_gtgt", "tong_tien"]
    list_filter = ["nam", "thang"]


@admin.register(BangKeHoaDonBanRa)
class BangKeHoaDonBanRaAdmin(admin.ModelAdmin):
    list_display = ["thang", "nam", "hoa_don", "tien_chua_thue", "thue_gtgt", "tong_tien"]
    list_filter = ["nam", "thang"]


@admin.register(ToKhaiGTGT)
class ToKhaiGTGTAdmin(admin.ModelAdmin):
    list_display = ["thang", "nam", "thue_gtgt_dau_ra", "thue_gtgt_dau_vao", "thue_gtgt_phai_nop", "trang_thai"]
    list_filter = ["trang_thai", "nam", "thang"]


@admin.register(ToKhaiTNDNTamTinh)
class ToKhaiTNDNTamTinhAdmin(admin.ModelAdmin):
    list_display = ["quy", "nam", "doanh_thu", "loi_nhuan", "thue_phai_nop", "trang_thai"]
    list_filter = ["trang_thai", "nam"]


@admin.register(ToKhaiTNCN)
class ToKhaiTNCNAdmin(admin.ModelAdmin):
    list_display = ["thang", "nam", "tong_thu_nhap", "tong_thue_tncn", "so_nhan_vien", "trang_thai"]
    list_filter = ["trang_thai", "nam", "thang"]
