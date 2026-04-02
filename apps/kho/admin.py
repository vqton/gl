"""Admin configuration for Inventory (Kho) module."""

from django.contrib import admin

from .models import Kho, KhoEntry, KhoLot, TonKho, VatTuHangHoa


class KhoLotInline(admin.TabularInline):
    model = KhoLot
    extra = 0
    fields = (
        "ma_lot",
        "ngay_nhap",
        "so_luong_nhap",
        "so_luong_ton",
        "don_gia_nhap",
        "han_dung",
    )
    readonly_fields = ("so_luong_ton",)


@admin.register(Kho)
class KhoAdmin(admin.ModelAdmin):
    list_display = ("ma_kho", "ten_kho", "nguoi_phu_trach", "is_active")
    list_filter = ("is_active",)
    search_fields = ("ma_kho", "ten_kho")


@admin.register(VatTuHangHoa)
class VatTuHangHoaAdmin(admin.ModelAdmin):
    list_display = (
        "hang_hoa",
        "phuong_phap_tinh_gia",
        "don_vi_tinh",
        "ton_toi_thieu",
        "ton_toi_da",
    )
    list_filter = ("phuong_phap_tinh_gia",)
    search_fields = ("hang_hoa__ma_hang_hoa", "hang_hoa__ten_hang_hoa")
    inlines = [KhoLotInline]


@admin.register(KhoLot)
class KhoLotAdmin(admin.ModelAdmin):
    list_display = (
        "ma_lot",
        "hang_hoa",
        "ngay_nhap",
        "so_luong_nhap",
        "so_luong_ton",
        "don_gia_nhap",
        "han_dung",
    )
    list_filter = ("ngay_nhap", "hang_hoa__phuong_phap_tinh_gia")
    search_fields = ("ma_lot", "hang_hoa__hang_hoa__ten_hang_hoa")
    readonly_fields = ("so_luong_ton", "created_at", "updated_at")


@admin.register(KhoEntry)
class KhoEntryAdmin(admin.ModelAdmin):
    list_display = (
        "so_chung_tu",
        "hang_hoa",
        "kho",
        "loai",
        "ngay_chung_tu",
        "so_luong",
        "don_gia",
        "thanh_tien",
        "da_dong_bo",
    )
    list_filter = ("loai", "loai_chung_tu", "kho", "da_dong_bo", "ngay_chung_tu")
    search_fields = ("so_chung_tu", "hang_hoa__hang_hoa__ten_hang_hoa")
    readonly_fields = (
        "thanh_tien",
        "gia_von_tam_tinh",
        "gia_von_chinh_thuc",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "ngay_chung_tu"


@admin.register(TonKho)
class TonKhoAdmin(admin.ModelAdmin):
    list_display = (
        "hang_hoa",
        "kho",
        "so_luong_ton",
        "gia_tri_ton",
        "ngay_cap_nhat_cuoi",
    )
    list_filter = ("kho",)
    search_fields = ("hang_hoa__hang_hoa__ten_hang_hoa",)
    readonly_fields = ("ngay_cap_nhat_cuoi",)
