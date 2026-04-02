"""Mua hàng models - Purchasing module."""

from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.danh_muc.models import HangHoa, NhaCungCap


class DeXuatMuaHang(models.Model):
    """
    Purchase request (Đề xuất mua hàng).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("da_duyet", "Đã duyệt"),
        ("tu_choi", "Từ chối"),
        ("da_mua", "Đã mua"),
    ]

    so_de_xuat = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số đề xuất",
    )
    ngay = models.DateField(
        verbose_name="Ngày",
    )
    nguoi_de_xuat = models.CharField(
        max_length=150,
        verbose_name="Người đề xuất",
    )
    ly_do = models.TextField(
        verbose_name="Lý do",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
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
        ordering = ["-ngay"]
        verbose_name = "Đề xuất mua hàng"
        verbose_name_plural = "Đề xuất mua hàng"

    def __str__(self):
        return f"{self.so_de_xuat} - {self.ngay}"


class DonDatHang(models.Model):
    """
    Purchase order (Đơn đặt hàng).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("confirmed", "Đã xác nhận"),
        ("received", "Đã nhận hàng"),
        ("completed", "Hoàn thành"),
        ("cancelled", "Đã hủy"),
    ]

    so_don_hang = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số đơn hàng",
    )
    ngay = models.DateField(
        verbose_name="Ngày",
    )
    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        related_name="don_dat_hang",
        verbose_name="Nhà cung cấp",
    )
    tong_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng tiền",
    )
    ngay_giao_du_kien = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày giao dự kiến",
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
        ordering = ["-ngay"]
        verbose_name = "Đơn đặt hàng"
        verbose_name_plural = "Đơn đặt hàng"

    def __str__(self):
        return f"{self.so_don_hang} - {self.nha_cung_cap}"


class DonDatHangChiTiet(models.Model):
    """
    Purchase order line items.
    """

    don_hang = models.ForeignKey(
        DonDatHang,
        on_delete=models.CASCADE,
        related_name="chi_tiet",
        verbose_name="Đơn hàng",
    )
    hang_hoa = models.ForeignKey(
        HangHoa,
        on_delete=models.PROTECT,
        verbose_name="Hàng hóa",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Số lượng",
    )
    so_luong_da_nhan = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Số lượng đã nhận",
    )
    don_gia = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Đơn giá",
    )
    thanh_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Thành tiền",
    )

    class Meta:
        verbose_name = "Chi tiết đơn đặt hàng"
        verbose_name_plural = "Chi tiết đơn đặt hàng"

    def __str__(self):
        return f"{self.don_hang} - {self.hang_hoa}"

    def save(self, *args, **kwargs):
        self.thanh_tien = (self.so_luong * self.don_gia).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)


class TraHangNCC(models.Model):
    """
    Purchase return (Trả hàng NCC).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("completed", "Hoàn thành"),
        ("cancelled", "Đã hủy"),
    ]

    so_chung_tu = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số chứng từ",
    )
    ngay = models.DateField(
        verbose_name="Ngày",
    )
    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        related_name="tra_hang",
        verbose_name="Nhà cung cấp",
    )
    ly_do_tra = models.TextField(
        verbose_name="Lý do trả",
    )
    tong_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng tiền",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
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
        ordering = ["-ngay"]
        verbose_name = "Trả hàng NCC"
        verbose_name_plural = "Trả hàng NCC"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.nha_cung_cap}"


class BangPhanBoChiPhi(models.Model):
    """
    Cost allocation (Bảng phân bổ chi phí).
    """

    LOAI_CHI_PHI_CHOICES = [
        ("van_chuyen", "Vận chuyển"),
        ("thue_quan", "Thuế quan"),
        ("bao_hiem", "Bảo hiểm"),
        ("khac", "Khác"),
    ]

    chung_tu_goc_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Loại chứng từ gốc",
    )
    chung_tu_goc_object_id = models.PositiveIntegerField(
        verbose_name="ID chứng từ gốc",
    )
    chung_tu_goc = GenericForeignKey(
        "chung_tu_goc_content_type",
        "chung_tu_goc_object_id",
    )
    loai_chi_phi = models.CharField(
        max_length=20,
        choices=LOAI_CHI_PHI_CHOICES,
        verbose_name="Loại chi phí",
    )
    tong_chi_phi = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Tổng chi phí",
    )
    doi_tuong_phan_bo = models.CharField(
        max_length=50,
        verbose_name="Đối tượng phân bổ",
        help_text="Theo giá trị hoặc số lượng",
    )
    so_tien_phan_bo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền phân bổ",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bảng phân bổ chi phí"
        verbose_name_plural = "Bảng phân bổ chi phí"

    def __str__(self):
        return f"{self.loai_chi_phi} - {self.tong_chi_phi}"
