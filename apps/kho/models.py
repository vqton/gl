"""Inventory management models."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.danh_muc.models import HangHoa

from .constants import LOAI_CHUNG_TU_KHO, LOAI_KHO_ENTRY, PHUONG_PHAP_TINH_GIA


class Kho(models.Model):
    """
    Warehouse model for inventory management.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
    """

    ma_kho = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Mã kho",
    )
    ten_kho = models.CharField(
        max_length=255,
        verbose_name="Tên kho",
    )
    dia_chi = models.TextField(
        blank=True,
        default="",
        verbose_name="Địa chỉ",
    )
    nguoi_phu_trach = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Người phụ trách",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Hoạt động",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )
    created_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người tạo",
    )
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người cập nhật",
    )

    class Meta:
        ordering = ["ma_kho"]
        verbose_name = "Kho"
        verbose_name_plural = "Kho"

    def __str__(self):
        return f"{self.ma_kho} - {self.ten_kho}"


class VatTuHangHoa(models.Model):
    """
    Goods/Item configuration for inventory.

    Extends HangHoa from danh_muc with inventory-specific settings.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Inventory valuation
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    hang_hoa = models.OneToOneField(
        HangHoa,
        on_delete=models.PROTECT,
        related_name="vat_tu",
        verbose_name="Hàng hóa",
    )
    phuong_phap_tinh_gia = models.CharField(
        max_length=10,
        choices=PHUONG_PHAP_TINH_GIA,
        default="FIFO",
        verbose_name="Phương pháp tính giá",
    )
    don_vi_tinh = models.CharField(
        max_length=50,
        default="cái",
        verbose_name="Đơn vị tính",
    )
    ton_toi_thieu = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tồn tối thiểu",
    )
    ton_toi_da = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tồn tối đa",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )
    created_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người tạo",
    )
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người cập nhật",
    )

    class Meta:
        ordering = ["hang_hoa__ma_hang_hoa"]
        verbose_name = "Vật tư hàng hóa"
        verbose_name_plural = "Vật tư hàng hóa"

    def __str__(self):
        return f"{self.hang_hoa} ({self.phuong_phap_tinh_gia})"


class KhoLot(models.Model):
    """
    Inventory Lot/Serial tracking for Specific Identification method.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on lot tracking
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    ma_lot = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Mã lô",
    )
    hang_hoa = models.ForeignKey(
        VatTuHangHoa,
        on_delete=models.PROTECT,
        related_name="lots",
        verbose_name="Hàng hóa",
    )
    ngay_nhap = models.DateField(
        verbose_name="Ngày nhập",
    )
    so_luong_nhap = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Số lượng nhập",
    )
    so_luong_ton = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Số lượng tồn",
    )
    don_gia_nhap = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Đơn giá nhập",
    )
    han_dung = models.DateField(
        null=True,
        blank=True,
        verbose_name="Hạn dùng",
    )
    phieu_nhap_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phieu_nhap_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    phieu_nhap = GenericForeignKey(
        "phieu_nhap_content_type",
        "phieu_nhap_object_id",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )
    created_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người tạo",
    )
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người cập nhật",
    )

    class Meta:
        ordering = ["ngay_nhap", "ma_lot"]
        verbose_name = "Lô hàng"
        verbose_name_plural = "Lô hàng"

    def __str__(self):
        return f"{self.ma_lot} - {self.hang_hoa}"

    def clean(self):
        """Validate lot quantities."""
        from django.core.exceptions import ValidationError

        if self.so_luong_ton < 0:
            raise ValidationError({"so_luong_ton": "Số lượng tồn không được âm."})
        if self.so_luong_ton > self.so_luong_nhap:
            raise ValidationError(
                {"so_luong_ton": "Số lượng tồn không được lớn hơn số lượng nhập."}
            )


class KhoEntry(models.Model):
    """
    Traceable inventory log for all in/out movements.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Inventory records
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    hang_hoa = models.ForeignKey(
        VatTuHangHoa,
        on_delete=models.PROTECT,
        related_name="kho_entries",
        verbose_name="Hàng hóa",
    )
    kho = models.ForeignKey(
        Kho,
        on_delete=models.PROTECT,
        related_name="kho_entries",
        verbose_name="Kho",
    )
    loai = models.CharField(
        max_length=4,
        choices=LOAI_KHO_ENTRY,
        verbose_name="Loại",
    )
    ngay_chung_tu = models.DateField(
        verbose_name="Ngày chứng từ",
    )
    so_chung_tu = models.CharField(
        max_length=50,
        verbose_name="Số chứng từ",
    )
    loai_chung_tu = models.CharField(
        max_length=2,
        choices=LOAI_CHUNG_TU_KHO,
        verbose_name="Loại chứng từ",
    )
    so_luong = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Số lượng",
    )
    don_gia = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Đơn giá",
    )
    thanh_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Thành tiền",
    )
    gia_von_tam_tinh = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Giá vốn tạm tính",
    )
    gia_von_chinh_thuc = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Giá vốn chính thức",
    )
    lot = models.ForeignKey(
        KhoLot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kho_entries",
        verbose_name="Lô hàng",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    da_dong_bo = models.BooleanField(
        default=False,
        verbose_name="Đã đồng bộ",
    )
    is_opening = models.BooleanField(
        default=False,
        verbose_name="Số dư đầu kỳ",
        help_text="Đánh dấu đây là số dư đầu kỳ",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )
    created_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người tạo",
    )
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người cập nhật",
    )

    class Meta:
        ordering = ["ngay_chung_tu", "created_at"]
        verbose_name = "Nhật ký kho"
        verbose_name_plural = "Nhật ký kho"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.hang_hoa} ({self.loai})"

    def save(self, *args, **kwargs):
        """Auto-calculate thanh_tien from so_luong * don_gia."""
        if self.so_luong and self.don_gia:
            self.thanh_tien = self.so_luong * self.don_gia
        super().save(*args, **kwargs)


class TonKho(models.Model):
    """
    Current inventory balance snapshot.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory balance
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    hang_hoa = models.ForeignKey(
        VatTuHangHoa,
        on_delete=models.PROTECT,
        related_name="ton_kho",
        verbose_name="Hàng hóa",
    )
    kho = models.ForeignKey(
        Kho,
        on_delete=models.PROTECT,
        related_name="ton_kho",
        verbose_name="Kho",
    )
    so_luong_ton = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=0,
        verbose_name="Số lượng tồn",
    )
    gia_tri_ton = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Giá trị tồn",
    )
    ngay_cap_nhat_cuoi = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật cuối",
    )

    class Meta:
        unique_together = ["hang_hoa", "kho"]
        ordering = ["hang_hoa__hang_hoa__ma_hang_hoa"]
        verbose_name = "Tồn kho"
        verbose_name_plural = "Tồn kho"

    def __str__(self):
        return f"{self.hang_hoa} @ {self.kho}: {self.so_luong_ton}"
