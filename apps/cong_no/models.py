"""Công nợ models - Receivables/Payables tracking."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.danh_muc.models import KhachHang, NhaCungCap
from apps.nghiep_vu.models import HoaDon, NhapKho


class CongNoPhaiThu(models.Model):
    """
    Receivable tracking (Công nợ phải thu).

    Computed from HoaDon + PhieuThu.
    """

    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.PROTECT,
        related_name="cong_no_phai_thu",
        verbose_name="Khách hàng",
    )
    hoa_don = models.ForeignKey(
        HoaDon,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cong_no_phai_thu",
        verbose_name="Hóa đơn",
    )
    tong_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng nợ",
    )
    da_thu = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Đã thu",
    )
    con_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Còn nợ",
    )
    ngay_den_han = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày đến hạn",
    )
    qua_han = models.BooleanField(
        default=False,
        verbose_name="Quá hạn",
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
        verbose_name = "Công nợ phải thu"
        verbose_name_plural = "Công nợ phải thu"

    def __str__(self):
        return f"{self.khach_hang} - {self.con_no}"

    def save(self, *args, **kwargs):
        """Auto-calculate remaining debt and overdue status."""
        from datetime import date as date_cls

        self.con_no = self.tong_no - self.da_thu
        if self.con_no < 0:
            self.con_no = 0
        if self.ngay_den_han and self.con_no > 0:
            self.qua_han = self.ngay_den_han < date_cls.today()
        super().save(*args, **kwargs)


class CongNoPhaiTra(models.Model):
    """
    Payable tracking (Công nợ phải trả).

    Computed from NhapKho + PhieuChi.
    """

    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        related_name="cong_no_phai_tra",
        verbose_name="Nhà cung cấp",
    )
    chung_tu_goc = models.ForeignKey(
        NhapKho,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cong_no_phai_tra",
        verbose_name="Chứng từ gốc",
    )
    tong_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng nợ",
    )
    da_tra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Đã trả",
    )
    con_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Còn nợ",
    )
    ngay_den_han = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày đến hạn",
    )
    qua_han = models.BooleanField(
        default=False,
        verbose_name="Quá hạn",
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
        verbose_name = "Công nợ phải trả"
        verbose_name_plural = "Công nợ phải trả"

    def __str__(self):
        return f"{self.nha_cung_cap} - {self.con_no}"

    def save(self, *args, **kwargs):
        """Auto-calculate remaining debt and overdue status."""
        from datetime import date as date_cls

        self.con_no = self.tong_no - self.da_tra
        if self.con_no < 0:
            self.con_no = 0
        if self.ngay_den_han and self.con_no > 0:
            self.qua_han = self.ngay_den_han < date_cls.today()
        super().save(*args, **kwargs)


class BienBanDoiChieuCongNo(models.Model):
    """
    Debt confirmation (Biên bản đối chiếu công nợ).
    """

    LOAI_CHOICES = [
        ("phai_thu", "Phải thu"),
        ("phai_tra", "Phải trả"),
    ]

    doi_tuong_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Loại đối tượng",
    )
    doi_tuong_object_id = models.PositiveIntegerField(
        verbose_name="ID đối tượng",
    )
    doi_tuong = GenericForeignKey(
        "doi_tuong_content_type",
        "doi_tuong_object_id",
    )
    loai = models.CharField(
        max_length=10,
        choices=LOAI_CHOICES,
        verbose_name="Loại",
    )
    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    so_dau_ky = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Số dư đầu kỳ",
    )
    phat_sinh_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Phát sinh Nợ",
    )
    phat_sinh_co = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Phát sinh Có",
    )
    so_cuoi_ky = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Số dư cuối kỳ",
    )
    da_xac_nhan = models.BooleanField(
        default=False,
        verbose_name="Đã xác nhận",
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
        ordering = ["-nam", "-thang"]
        verbose_name = "Biên bản đối chiếu công nợ"
        verbose_name_plural = "Biên bản đối chiếu công nợ"

    def __str__(self):
        return f"{self.loai} - {self.thang}/{self.nam}"

    def save(self, *args, **kwargs):
        """Auto-calculate closing balance."""
        self.so_cuoi_ky = self.so_dau_ky + self.phat_sinh_no - self.phat_sinh_co
        super().save(*args, **kwargs)
