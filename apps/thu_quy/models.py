"""Thủ Quỹ (Cashier Reconciliation) models."""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.nghiep_vu.models import ButToan

from .constants import (
    LOAI_CHENH_LECH,
    TRANG_THAI_KIEM_KE,
    XU_LY_CHENH_LECH,
)


class KiemKeQuy(models.Model):
    """
    Cash count/verification record.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Quy định về quản lý tiền mặt
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    so_kiem_ke = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số kiểm kê",
    )
    ngay_kiem_ke = models.DateField(
        verbose_name="Ngày kiểm kê",
    )
    ky_quy = models.CharField(
        max_length=20,
        verbose_name="Kỳ quỹ",
        help_text="VD: Q1/2026, T01/2026",
    )
    so_du_so_sach = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số dư sổ sách",
    )
    so_thuc_te = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số thực tế",
    )
    chen_lech = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Chênh lệch",
        help_text="Auto: thực tế - sổ sách",
    )
    ly_do = models.TextField(
        blank=True,
        default="",
        verbose_name="Lý do",
    )
    nguoi_kiem_ke = models.CharField(
        max_length=200,
        verbose_name="Người kiểm kê",
    )
    thu_quy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="kiem_ke_quy",
        verbose_name="Thủ quỹ",
    )
    trang_thai = models.CharField(
        max_length=15,
        choices=TRANG_THAI_KIEM_KE,
        default="draft",
        verbose_name="Trạng thái",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )

    class Meta:
        ordering = ["-ngay_kiem_ke"]
        verbose_name = "Kiểm kê quỹ"
        verbose_name_plural = "Kiểm kê quỹ"

    def __str__(self):
        return f"{self.so_kiem_ke} - {self.ky_quy}"

    def clean(self):
        super().clean()
        if self.so_thuc_te < Decimal("0"):
            raise ValidationError(
                {"so_thuc_te": ["Số thực tế không được âm"]}
            )
        if self.nguoi_kiem_ke and self.thu_quy_id:
            if self.nguoi_kiem_ke.lower() == self.thu_quy.username.lower():
                raise ValidationError(
                    {
                        "nguoi_kiem_ke": [
                            "Người kiểm kê và thủ quỹ phải là người khác nhau "
                            "(segregation of duties)."
                        ]
                    }
                )

    def save(self, *args, **kwargs):
        """Auto-calculate chen_lech = so_thuc_te - so_du_so_sach."""
        self.chen_lech = (self.so_thuc_te - self.so_du_so_sach).quantize(
            Decimal("0.01")
        )
        super().save(*args, **kwargs)


class XuLyChenhLechQuy(models.Model):
    """
    Cash over/short resolution.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Quy định về xử lý chênh lệch quỹ
    """

    kiem_ke = models.ForeignKey(
        KiemKeQuy,
        on_delete=models.PROTECT,
        related_name="xu_ly_chenh_lech",
        verbose_name="Kiểm kê",
    )
    loai = models.CharField(
        max_length=10,
        choices=LOAI_CHENH_LECH,
        verbose_name="Loại chênh lệch",
    )
    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    nguyen_nhan = models.TextField(
        verbose_name="Nguyên nhân",
    )
    xu_ly = models.CharField(
        max_length=30,
        choices=XU_LY_CHENH_LECH,
        verbose_name="Hình thức xử lý",
    )
    but_toan = models.ForeignKey(
        ButToan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="xu_ly_chenh_lech",
        verbose_name="Bút toán xử lý",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Xử lý chênh lệch quỹ"
        verbose_name_plural = "Xử lý chênh lệch quỹ"

    def __str__(self):
        return f"{self.kiem_ke} - {self.get_loai_display()}: {self.so_tien}"

    def clean(self):
        super().clean()
        if self.so_tien <= Decimal("0"):
            raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})
        if self.kiem_ke_id:
            abs_chen_lech = abs(self.kiem_ke.chen_lech)
            if abs(self.so_tien - abs_chen_lech) > Decimal("0.01"):
                raise ValidationError(
                    {
                        "so_tien": [
                            f"Số tiền xử lý ({self.so_tien}) phải bằng "
                            f"giá trị chênh lệch ({abs_chen_lech})."
                        ]
                    }
                )
