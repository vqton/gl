"""CCDC models - Công cụ dụng cụ (Tools & Equipment)."""

from decimal import Decimal

from django.db import models

from apps.danh_muc.models import TaiKhoanKeToan


class CongCuDungCu(models.Model):
    """
    Tools & Equipment (Công cụ dụng cụ) - tracked on TK 153/242.
    """

    PHUONG_PHAP_PHAN_BO_CHOICES = [
        ("1_lan", "Phân bổ 1 lần"),
        ("nhieu_lan", "Phân bổ nhiều lần"),
    ]

    TRANG_THAI_CHOICES = [
        ("dang_theo_doi", "Đang theo dõi"),
        ("da_phan_bo_het", "Đã phân bổ hết"),
        ("thanh_ly", "Đã thanh lý"),
    ]

    ma_ccdc = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã CCDC",
    )
    ten_ccdc = models.CharField(
        max_length=255,
        verbose_name="Tên CCDC",
    )
    ngay_mua = models.DateField(
        verbose_name="Ngày mua",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
        verbose_name="Số lượng",
    )
    gia_mua = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Giá mua",
    )
    tong_gia_tri = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Tổng giá trị",
        help_text="Giá mua × Số lượng",
    )
    phuong_phap_phan_bo = models.CharField(
        max_length=10,
        choices=PHUONG_PHAP_PHAN_BO_CHOICES,
        default="nhieu_lan",
        verbose_name="Phương pháp phân bổ",
    )
    so_ky_phan_bo = models.IntegerField(
        default=1,
        verbose_name="Số kỳ phân bổ",
    )
    ky_phan_bo_bat_dau = models.DateField(
        verbose_name="Kỳ phân bổ bắt đầu",
    )
    ky_phan_bo_ket_thuc = models.DateField(
        verbose_name="Kỳ phân bổ kết thúc",
    )
    trang_thai = models.CharField(
        max_length=15,
        choices=TRANG_THAI_CHOICES,
        default="dang_theo_doi",
        verbose_name="Trạng thái",
    )
    tk_chi_phi = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="ccdc_chi_phi",
        verbose_name="TK chi phí",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
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
        ordering = ["ma_ccdc"]
        verbose_name = "Công cụ dụng cụ"
        verbose_name_plural = "Công cụ dụng cụ"

    def __str__(self):
        return f"{self.ma_ccdc} - {self.ten_ccdc}"

    def save(self, *args, **kwargs):
        """Auto-calculate total value."""
        self.tong_gia_tri = (self.gia_mua * self.so_luong).quantize(Decimal("0.01"))
        if self.phuong_phap_phan_bo == "1_lan":
            self.so_ky_phan_bo = 1
        super().save(*args, **kwargs)


class BangPhanBoCCDC(models.Model):
    """
    Monthly CCDC allocation (Bảng phân bổ CCDC).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("da_hach_toan", "Đã hạch toán"),
    ]

    ccdc = models.ForeignKey(
        CongCuDungCu,
        on_delete=models.PROTECT,
        related_name="bang_phan_bo",
        verbose_name="CCDC",
    )
    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    so_tien_phan_bo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền phân bổ",
    )
    trang_thai = models.CharField(
        max_length=12,
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        unique_together = ["ccdc", "thang", "nam"]
        ordering = ["nam", "thang"]
        verbose_name = "Bảng phân bổ CCDC"
        verbose_name_plural = "Bảng phân bổ CCDC"

    def __str__(self):
        return f"{self.ccdc} - {self.thang}/{self.nam}"
