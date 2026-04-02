"""Giá Thành (Product Costing) models - TT 99/2025/TT-BTC compliant."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.danh_muc.models import HangHoa, TaiKhoanKeToan

from .constants import (
    LOAI_DOI_TUONG,
    LOAI_KHOAN_MUC,
    PHUONG_PHAP_PHAN_BO,
    TIEU_THUC_PHAN_BO,
    TRANG_THAI,
)


class DoiTuongTapHopChiPhi(models.Model):
    """
    Cost collection object: product, order, department.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Phụ lục III - Cost accounting
        - Chuẩn mực kế toán VAS 02 - Hàng tồn kho
    """

    ma_doi_tuong = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã đối tượng",
    )
    ten_doi_tuong = models.CharField(
        max_length=200,
        verbose_name="Tên đối tượng",
    )
    loai = models.CharField(
        max_length=20,
        choices=LOAI_DOI_TUONG,
        verbose_name="Loại đối tượng",
    )
    san_pham = models.ForeignKey(
        HangHoa,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="doi_tuong_chi_phi",
        verbose_name="Sản phẩm",
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

    class Meta:
        ordering = ["ma_doi_tuong"]
        verbose_name = "Đối tượng tập hợp chi phí"
        verbose_name_plural = "Đối tượng tập hợp chi phí"

    def __str__(self):
        return f"{self.ma_doi_tuong} - {self.ten_doi_tuong}"


class KhoanMucChiPhi(models.Model):
    """
    Cost item: material, labor, overhead.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Phụ lục III - Cost items
        - TK 621, 622, 627
    """

    ma_khoan_muc = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã khoản mục",
    )
    ten_khoan_muc = models.CharField(
        max_length=200,
        verbose_name="Tên khoản mục",
    )
    loai = models.CharField(
        max_length=30,
        choices=LOAI_KHOAN_MUC,
        verbose_name="Loại khoản mục",
    )
    tk_chi_phi = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="khoan_muc_chi_phi",
        verbose_name="TK chi phí",
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

    class Meta:
        ordering = ["ma_khoan_muc"]
        verbose_name = "Khoản mục chi phí"
        verbose_name_plural = "Khoản mục chi phí"

    def __str__(self):
        return f"{self.ma_khoan_muc} - {self.ten_khoan_muc}"


class PhieuTapHopChiPhi(models.Model):
    """
    Cost collection voucher.

    Records costs incurred for a specific cost object and cost item.
    """

    so_chung_tu = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số chứng từ",
    )
    ngay_chung_tu = models.DateField(
        verbose_name="Ngày chứng từ",
    )
    doi_tuong = models.ForeignKey(
        DoiTuongTapHopChiPhi,
        on_delete=models.PROTECT,
        related_name="phieu_tap_hop",
        verbose_name="Đối tượng",
    )
    khoan_muc = models.ForeignKey(
        KhoanMucChiPhi,
        on_delete=models.PROTECT,
        related_name="phieu_tap_hop",
        verbose_name="Khoản mục",
    )
    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI,
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
        ordering = ["-ngay_chung_tu"]
        verbose_name = "Phiếu tập hợp chi phí"
        verbose_name_plural = "Phiếu tập hợp chi phí"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.doi_tuong}"

    def clean(self):
        super().clean()
        if self.so_tien <= Decimal("0"):
            raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})


class BangPhanBoChiPhi(models.Model):
    """
    Cost allocation table.

    Allocates shared costs across multiple cost objects using
    various allocation methods (direct, coefficient, ratio, standard).
    """

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    phuong_phap = models.CharField(
        max_length=20,
        choices=PHUONG_PHAP_PHAN_BO,
        verbose_name="Phương pháp phân bổ",
    )
    tieu_thuc_phan_bo = models.CharField(
        max_length=30,
        choices=TIEU_THUC_PHAN_BO,
        verbose_name="Tiêu thức phân bổ",
    )
    tong_chi_phi = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Tổng chi phí",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI,
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
        ordering = ["-nam", "-thang"]
        verbose_name = "Bảng phân bổ chi phí"
        verbose_name_plural = "Bảng phân bổ chi phí"

    def __str__(self):
        return f"Phân bổ T{self.thang}/{self.nam} - {self.get_phuong_phap_display()}"

    def clean(self):
        super().clean()
        if self.tong_chi_phi <= Decimal("0"):
            raise ValidationError({"tong_chi_phi": ["Tổng chi phí phải lớn hơn 0"]})

    def tong_da_phan_bo(self):
        """Return total amount already allocated."""
        return sum(ct.muc_phan_bo for ct in self.chi_tiet_phan_bo.all())


class ChiTietPhanBoChiPhi(models.Model):
    """
    Allocation detail per cost object.
    """

    bang_phan_bo = models.ForeignKey(
        BangPhanBoChiPhi,
        on_delete=models.CASCADE,
        related_name="chi_tiet_phan_bo",
        verbose_name="Bảng phân bổ",
    )
    doi_tuong = models.ForeignKey(
        DoiTuongTapHopChiPhi,
        on_delete=models.PROTECT,
        verbose_name="Đối tượng",
    )
    he_so = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("1.0000"),
        verbose_name="Hệ số",
    )
    muc_phan_bo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Mức phân bổ",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )

    class Meta:
        verbose_name = "Chi tiết phân bổ chi phí"
        verbose_name_plural = "Chi tiết phân bổ chi phí"

    def __str__(self):
        return f"{self.bang_phan_bo} - {self.doi_tuong}: {self.muc_phan_bo}"


class BangTinhGiaThanh(models.Model):
    """
    Cost calculation table.

    Formula:
        Giá thành SP hoàn thành = CP dở dang đầu kỳ + CP phát sinh - CP dở dang cuối kỳ
        Giá thành đơn vị = Giá thành SP hoàn thành / Số lượng SP

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Phụ lục III - Cost calculation
        - VAS 02 - Hàng tồn kho
    """

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    doi_tuong = models.ForeignKey(
        DoiTuongTapHopChiPhi,
        on_delete=models.PROTECT,
        related_name="bang_tinh_gia_thanh",
        verbose_name="Đối tượng",
    )
    cp_dở_dang_dau_ky = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="CP dở dang đầu kỳ",
    )
    cp_phat_sinh = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="CP phát sinh trong kỳ",
    )
    cp_dở_dang_cuoi_ky = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="CP dở dang cuối kỳ",
    )
    gia_thanh_sp_hoan_thanh = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Giá thành SP hoàn thành",
    )
    so_luong_sp = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Số lượng SP",
    )
    gia_thanh_don_vi = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=Decimal("0.0000"),
        verbose_name="Giá thành đơn vị",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI,
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
        ordering = ["-nam", "-thang"]
        verbose_name = "Bảng tính giá thành"
        verbose_name_plural = "Bảng tính giá thành"

    def __str__(self):
        return f"GT T{self.thang}/{self.nam} - {self.doi_tuong}"

    def clean(self):
        super().clean()
        tong_cp = self.cp_dở_dang_dau_ky + self.cp_phat_sinh
        if self.cp_dở_dang_cuoi_ky > tong_cp:
            raise ValidationError(
                {
                    "cp_dở_dang_cuoi_ky": [
                        "CP dở dang cuối kỳ không được vượt quá "
                        "tổng CP (đầu kỳ + phát sinh)."
                    ]
                }
            )
        if self.cp_phat_sinh < Decimal("0"):
            raise ValidationError({"cp_phat_sinh": ["CP phát sinh không được âm"]})

    def save(self, *args, **kwargs):
        """Auto-calculate gia_thanh_sp_hoan_thanh and gia_thanh_don_vi."""
        self.gia_thanh_sp_hoan_thanh = (
            self.cp_dở_dang_dau_ky + self.cp_phat_sinh - self.cp_dở_dang_cuoi_ky
        ).quantize(Decimal("0.01"))

        if self.gia_thanh_sp_hoan_thanh < Decimal("0"):
            self.gia_thanh_sp_hoan_thanh = Decimal("0.00")

        if self.so_luong_sp > Decimal("0"):
            self.gia_thanh_don_vi = (
                self.gia_thanh_sp_hoan_thanh / self.so_luong_sp
            ).quantize(Decimal("0.0001"))
        else:
            self.gia_thanh_don_vi = Decimal("0.0000")

        super().save(*args, **kwargs)
