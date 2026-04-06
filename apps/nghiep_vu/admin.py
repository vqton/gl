"""Admin configuration for nghiep_vu app."""

from django.contrib import admin

from apps.nghiep_vu.models import (
    BangPhanBoNVLCCDC,
    BangThanhToanTienLuong,
    BienBanGiaoNhanTSCD,
    BienBanThanhLyTSCD,
    ButToan,
    ButToanChiTiet,
    GiayDeNghiTamUng,
    GiayThanhToanTamUng,
    HoaDon,
    HoaDonChiTiet,
    Kho,
    NhapKho,
    NhapKhoChiTiet,
    PhieuChi,
    PhieuThu,
    XuatKho,
    XuatKhoChiTiet,
)


class HoaDonChiTietInline(admin.TabularInline):
    model = HoaDonChiTiet
    extra = 0
    readonly_fields = ["tien_thue", "tong_tien"]


@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    list_display = [
        "so_hoa_don",
        "ngay_hoa_don",
        "khach_hang",
        "tong_tien_truoc_thue",
        "tien_thue_gtgt",
        "tong_cong_thanh_toan",
        "trang_thai",
    ]
    list_filter = ["trang_thai", "hinh_thuc_thanh_toan", "ngay_hoa_don"]
    search_fields = ["so_hoa_don", "khach_hang__ten_kh"]
    readonly_fields = [
        "tong_tien_truoc_thue",
        "tien_thue_gtgt",
        "tong_cong_thanh_toan",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "ngay_hoa_don"
    inlines = [HoaDonChiTietInline]


class ButToanChiTietInline(admin.TabularInline):
    model = ButToanChiTiet
    extra = 0


@admin.register(ButToan)
class ButToanAdmin(admin.ModelAdmin):
    list_display = [
        "so_but_toan",
        "ngay_hach_toan",
        "dien_giai",
        "trang_thai",
        "nguoi_tao",
    ]
    list_filter = ["trang_thai", "ngay_hach_toan"]
    search_fields = ["so_but_toan", "dien_giai"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "ngay_hach_toan"
    inlines = [ButToanChiTietInline]


class NhapKhoChiTietInline(admin.TabularInline):
    model = NhapKhoChiTiet
    extra = 0
    readonly_fields = ["thanh_tien"]


@admin.register(NhapKho)
class NhapKhoAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay",
        "kho",
        "nha_cung_cap",
        "tong_tien",
        "trang_thai",
    ]
    list_filter = ["trang_thai", "ngay", "kho"]
    search_fields = ["so_chung_tu", "nha_cung_cap__ten_ncc"]
    readonly_fields = ["tong_tien", "created_at", "updated_at"]
    date_hierarchy = "ngay"
    inlines = [NhapKhoChiTietInline]


class XuatKhoChiTietInline(admin.TabularInline):
    model = XuatKhoChiTiet
    extra = 0
    readonly_fields = ["thanh_tien"]


@admin.register(XuatKho)
class XuatKhoAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay",
        "kho",
        "khach_hang",
        "tong_tien",
        "trang_thai",
    ]
    list_filter = ["trang_thai", "ngay", "kho"]
    search_fields = ["so_chung_tu", "khach_hang__ten_kh"]
    readonly_fields = ["tong_tien", "created_at", "updated_at"]
    date_hierarchy = "ngay"
    inlines = [XuatKhoChiTietInline]


@admin.register(Kho)
class KhoAdmin(admin.ModelAdmin):
    list_display = [
        "ma_kho",
        "ten_kho",
        "nguoi_phu_trach",
        "is_active",
    ]
    list_filter = ["is_active"]
    search_fields = ["ma_kho", "ten_kho"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]


@admin.register(PhieuThu)
class PhieuThuAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_chung_tu",
        "so_tien",
        "so_tien_vnd",
        "tk_no",
        "tk_co",
        "hinh_thuc_thanh_toan",
        "trang_thai",
        "khach_hang",
    ]
    list_filter = ["trang_thai", "hinh_thuc_thanh_toan", "ngay_chung_tu"]
    search_fields = ["so_chung_tu", "khach_hang__ten_kh", "dien_giai"]
    readonly_fields = ["so_tien_vnd", "created_at", "updated_at"]
    date_hierarchy = "ngay_chung_tu"


@admin.register(PhieuChi)
class PhieuChiAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_chung_tu",
        "so_tien",
        "so_tien_vnd",
        "tk_no",
        "tk_co",
        "hinh_thuc_thanh_toan",
        "trang_thai",
        "nha_cung_cap",
    ]
    list_filter = ["trang_thai", "hinh_thuc_thanh_toan", "ngay_chung_tu"]
    search_fields = ["so_chung_tu", "nha_cung_cap__ten_ncc", "dien_giai"]
    readonly_fields = ["so_tien_vnd", "created_at", "updated_at"]
    date_hierarchy = "ngay_chung_tu"


@admin.register(GiayDeNghiTamUng)
class GiayDeNghiTamUngAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_chung_tu",
        "nguoi_de_nghi",
        "so_tien",
        "hinh_thuc_chi",
        "trang_thai",
        "but_toan",
    ]
    list_filter = ["trang_thai", "hinh_thuc_chi", "ngay_chung_tu"]
    search_fields = ["so_chung_tu", "nguoi_de_nghi__username", "noi_dung"]
    readonly_fields = ["created_at", "updated_at", "but_toan"]
    date_hierarchy = "ngay_chung_tu"


@admin.register(GiayThanhToanTamUng)
class GiayThanhToanTamUngAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_chung_tu",
        "tam_ung",
        "so_tien_tam_ung",
        "so_tien_chi",
        "so_tien_con_lai",
        "trang_thai",
        "but_toan",
    ]
    list_filter = ["trang_thai", "ngay_chung_tu"]
    search_fields = ["so_chung_tu", "tam_ung__so_chung_tu"]
    readonly_fields = ["so_tien_con_lai", "created_at", "updated_at", "but_toan"]
    date_hierarchy = "ngay_chung_tu"


@admin.register(BienBanGiaoNhanTSCD)
class BienBanGiaoNhanTSCDAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_lap",
        "tai_san",
        "nguoi_giao",
        "nguoi_nhan",
        "nguyen_gia",
        "but_toan",
    ]
    list_filter = ["ngay_lap", "loai"]
    search_fields = ["so_chung_tu", "tai_san__ten_tai_san"]
    readonly_fields = ["created_at", "but_toan"]
    date_hierarchy = "ngay_lap"


@admin.register(BienBanThanhLyTSCD)
class BienBanThanhLyTSCDAdmin(admin.ModelAdmin):
    list_display = [
        "so_chung_tu",
        "ngay_lap",
        "tai_san",
        "loai_xu_ly",
        "nguyen_gia",
        "so_tien_thu",
        "da_hach_toan",
        "but_toan",
    ]
    list_filter = ["loai_xu_ly", "da_hach_toan", "ngay_lap"]
    search_fields = ["so_chung_tu", "tai_san__ten_tai_san"]
    readonly_fields = ["created_at", "but_toan"]
    date_hierarchy = "ngay_lap"


@admin.register(BangPhanBoNVLCCDC)
class BangPhanBoNVLCCDCAdmin(admin.ModelAdmin):
    list_display = [
        "thang",
        "nam",
        "tong_nhap_kho",
        "tong_xuat_kho",
        "tong_chenh_lech",
        "da_hach_toan",
        "but_toan",
    ]
    list_filter = ["da_hach_toan", "nam", "thang"]
    readonly_fields = ["created_at", "but_toan"]


@admin.register(BangThanhToanTienLuong)
class BangThanhToanTienLuongAdmin(admin.ModelAdmin):
    list_display = [
        "thang",
        "nam",
        "so_luong_nhan_vien",
        "tong_tong_thu_nhap",
        "tong_thue_tncn",
        "tong_thuc_linh",
        "da_hach_toan",
        "but_toan",
    ]
    list_filter = ["da_hach_toan", "nam", "thang"]
    readonly_fields = ["created_at", "but_toan"]
