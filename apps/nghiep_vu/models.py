"""Accounting voucher models for business operations."""

import re
from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.danh_muc.models import (
    HangHoa,
    KhachHang,
    NhaCungCap,
    TaiKhoanKeToan,
)
from apps.nghiep_vu.constants import THUE_SUAT_GTGT_2026


class ChungTu(models.Model):
    """
    Base accounting document model.

    Represents the foundation for all accounting vouchers
    (phiếu thu, phiếu chi, hóa đơn, etc.).
    """

    LOAI_CHUNG_TU_CHOICES = [
        ("phieu_thu", "Phiếu thu"),
        ("phieu_chi", "Phiếu chi"),
        ("hoa_don", "Hóa đơn"),
        ("chung_tu_khac", "Chứng từ khác"),
    ]

    so_chung_tu = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số chứng từ",
    )
    ngay_chung_tu = models.DateField(
        verbose_name="Ngày chứng từ",
    )
    loai_chung_tu = models.CharField(
        max_length=20,
        choices=LOAI_CHUNG_TU_CHOICES,
        verbose_name="Loại chứng từ",
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

    class Meta:
        abstract = True
        ordering = ["-ngay_chung_tu"]

    def __str__(self):
        return f"{self.so_chung_tu} - {self.ngay_chung_tu}"


class PhieuThu(ChungTu):
    """
    Receipt voucher model (Phiếu thu).

    Records cash/bank receipts from customers or other sources.
    Auto-creates journal entries: Nợ 111/112 / Có 131/511/...

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Cash receipt forms
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    HINH_THUC_THANH_TOAN_CHOICES = [
        ("tien_mat", "Tiền mặt (111)"),
        ("chuyen_khoan", "Chuyển khoản (112)"),
    ]

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("posted", "Đã ghi sổ"),
        ("cancelled", "Đã hủy"),
    ]

    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    ty_gia = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=1,
        verbose_name="Tỷ giá",
        help_text="Tỷ giá quy đổi sang VND (mặc định 1)",
    )
    so_tien_vnd = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Số tiền VND",
        help_text="Số tiền quy đổi sang VND",
    )
    hinh_thuc_thanh_toan = models.CharField(
        max_length=20,
        choices=HINH_THUC_THANH_TOAN_CHOICES,
        default="tien_mat",
        verbose_name="Hình thức thanh toán",
    )
    tk_no = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="phieu_thu_no",
        verbose_name="TK Nợ",
        help_text="Tài khoản ghi Nợ (111 hoặc 112)",
    )
    tk_co = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="phieu_thu_co",
        verbose_name="TK Có",
        help_text="Tài khoản ghi Có (131, 511, ...)",
    )
    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="phieu_thu",
        verbose_name="Khách hàng",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
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

    class Meta(ChungTu.Meta):
        verbose_name = "Phiếu thu"
        verbose_name_plural = "Phiếu thu"

    def clean(self):
        super().clean()
        if self.tk_no_id:
            tk_no_code = self.tk_no.ma_tai_khoan
            if tk_no_code not in ("111", "112"):
                raise ValidationError(
                    {"tk_no": f"TK Nợ phải là 111 hoặc 112, hiện tại: {tk_no_code}"}
                )

    def save(self, *args, **kwargs):
        """Auto-calculate VND amount from foreign currency."""
        self.so_tien_vnd = (self.so_tien * self.ty_gia).quantize(
            __import__("decimal", fromlist=["Decimal"]).Decimal("0.01")
        )
        super().save(*args, **kwargs)


class PhieuChi(ChungTu):
    """
    Payment voucher model (Phiếu chi).

    Records cash/bank payments to suppliers or other parties.
    Auto-creates journal entries: Nợ 331/642/... / Có 111/112

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Cash payment forms
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    HINH_THUC_THANH_TOAN_CHOICES = [
        ("tien_mat", "Tiền mặt (111)"),
        ("chuyen_khoan", "Chuyển khoản (112)"),
    ]

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("posted", "Đã ghi sổ"),
        ("cancelled", "Đã hủy"),
    ]

    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    ty_gia = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=1,
        verbose_name="Tỷ giá",
        help_text="Tỷ giá quy đổi sang VND (mặc định 1)",
    )
    so_tien_vnd = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Số tiền VND",
        help_text="Số tiền quy đổi sang VND",
    )
    hinh_thuc_thanh_toan = models.CharField(
        max_length=20,
        choices=HINH_THUC_THANH_TOAN_CHOICES,
        default="tien_mat",
        verbose_name="Hình thức thanh toán",
    )
    tk_no = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="phieu_chi_no",
        verbose_name="TK Nợ",
        help_text="Tài khoản ghi Nợ (331, 642, ...)",
    )
    tk_co = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="phieu_chi_co",
        verbose_name="TK Có",
        help_text="Tài khoản ghi Có (111 hoặc 112)",
    )
    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="phieu_chi",
        verbose_name="Nhà cung cấp",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
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

    class Meta(ChungTu.Meta):
        verbose_name = "Phiếu chi"
        verbose_name_plural = "Phiếu chi"

    def clean(self):
        super().clean()
        if self.tk_co_id:
            tk_co_code = self.tk_co.ma_tai_khoan
            if tk_co_code not in ("111", "112"):
                raise ValidationError(
                    {"tk_co": f"TK Có phải là 111 hoặc 112, hiện tại: {tk_co_code}"}
                )

    def save(self, *args, **kwargs):
        """Auto-calculate VND amount from foreign currency."""
        self.so_tien_vnd = (self.so_tien * self.ty_gia).quantize(
            __import__("decimal", fromlist=["Decimal"]).Decimal("0.01")
        )
        super().save(*args, **kwargs)


class HoaDon(models.Model):
    """
    Invoice model for sales transactions.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on invoice requirements
        - Nghị định 320/2025/NĐ-CP on e-invoice implementation
    """

    HINH_THUC_THANH_TOAN_CHOICES = [
        ("tien_mat", "Tiền mặt"),
        ("chuyen_khoan", "Chuyển khoản"),
    ]

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("issued", "Đã xuất"),
        ("cancelled", "Đã hủy"),
    ]

    QUY_SO_CHOICES = [
        ("AA/26E", "AA/26E"),
        ("AB/26E", "AB/26E"),
    ]

    so_hoa_don = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số hóa đơn",
    )
    ky_hieu = models.CharField(
        max_length=10,
        blank=True,
        default="",
        verbose_name="Ký hiệu",
        help_text="Mẫu ký hiệu hóa đơn (VD: AA/26E)",
    )
    quy_so = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Quyển số",
    )
    ma_hang_hoa_gtgt = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Mã hàng hóa GTGT",
    )
    loai_hang_hoa = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Loại hàng hóa",
    )
    ngay_hoa_don = models.DateField(
        verbose_name="Ngày hóa đơn",
    )
    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.PROTECT,
        related_name="hoa_don",
        verbose_name="Khách hàng",
    )
    nguoi_mua_hang = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Người mua hàng",
    )
    ma_so_thue_mua = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mã số thuế người mua",
    )
    dia_chi_mua = models.TextField(
        blank=True,
        default="",
        verbose_name="Địa chỉ người mua",
    )
    hinh_thuc_thanh_toan = models.CharField(
        max_length=20,
        choices=HINH_THUC_THANH_TOAN_CHOICES,
        default="tien_mat",
        verbose_name="Hình thức thanh toán",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
    )
    tong_tien_truoc_thue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng trước thuế",
    )
    tien_thue_gtgt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tiền thuế GTGT",
    )
    tong_cong_thanh_toan = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng thanh toán",
    )
    da_xuat_kho = models.BooleanField(
        default=False,
        verbose_name="Đã xuất kho",
        help_text="Đánh dấu khi phiếu xuất kho đã được tạo tự động",
    )
    da_thanh_toan = models.BooleanField(
        default=False,
        verbose_name="Đã thanh toán",
        help_text="Đánh dấu khi phiếu thu đã được tạo tự động",
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
        ordering = ["-ngay_hoa_don"]
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"

    def __str__(self):
        kh_name = self.khach_hang.ten_kh if self.khach_hang_id else ""
        return f"{self.so_hoa_don} - {self.khach_hang.ma_kh} - {kh_name}"

    def clean(self):
        super().clean()
        if self.ky_hieu:
            pattern = r"^[A-Z]{2}/\d{2}[A-Z]$"
            if not re.match(pattern, self.ky_hieu):
                raise ValidationError(
                    {"ky_hieu": "Ký hiệu phải theo mẫu AA/26E (2 chữ / 2 số + 1 chữ)."}
                )

    def save(self, *args, **kwargs):
        if not self.so_hoa_don:
            date_str = self.ngay_hoa_don.strftime("%Y%m%d")
            count = HoaDon.objects.filter(ngay_hoa_don=self.ngay_hoa_don).count() + 1
            self.so_hoa_don = f"HD-{date_str}-{count:04d}"
        super().save(*args, **kwargs)


class HoaDonChiTiet(models.Model):
    """
    Invoice line item model.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on invoice details
    """

    hoa_don = models.ForeignKey(
        HoaDon,
        on_delete=models.CASCADE,
        related_name="chi_tiet",
        verbose_name="Hóa đơn",
    )
    hang_hoa = models.ForeignKey(
        "danh_muc.HangHoa",
        on_delete=models.PROTECT,
        verbose_name="Hàng hóa",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Số lượng",
    )
    don_gia = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Đơn giá",
    )
    thue_suat = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        choices=[(Decimal(str(v[0])), v[1]) for v in THUE_SUAT_GTGT_2026],
        default=Decimal("10"),
        verbose_name="Thuế suất",
    )
    tien_thue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Tiền thuế",
    )
    tong_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Tổng tiền",
    )

    class Meta:
        verbose_name = "Chi tiết hóa đơn"
        verbose_name_plural = "Chi tiết hóa đơn"

    def __str__(self):
        return f"{self.hoa_don} - {self.hang_hoa}"


class ButToan(models.Model):
    """
    Journal entry model for double-entry bookkeeping.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on journal entries
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("posted", "Đã ghi sổ"),
    ]

    so_but_toan = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số bút toán",
    )
    ngay_hach_toan = models.DateField(
        verbose_name="Ngày hạch toán",
    )
    ngay_dua_vao_su_dung = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày đưa vào sử dụng",
    )
    dien_giai = models.TextField(
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
    )
    nguoi_tao = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="but_toan",
        verbose_name="Người tạo",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật",
    )
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người cập nhật",
    )

    class Meta:
        ordering = ["-ngay_hach_toan"]
        verbose_name = "Bút toán"
        verbose_name_plural = "Bút toán"

    def __str__(self):
        return f"{self.so_but_toan} - {self.ngay_hach_toan}"

    def clean(self):
        super().clean()
        if self.trang_thai == "posted":
            chi_tiet = self.chi_tiet.all()
            if not chi_tiet.exists():
                raise ValidationError("Bút toán phải có ít nhất một chi tiết.")
            tong_no = sum(ct.so_tien for ct in chi_tiet if ct.loai_no_co == "no")
            tong_co = sum(ct.so_tien for ct in chi_tiet if ct.loai_no_co == "co")
            if tong_no != tong_co:
                raise ValidationError(
                    f"Tổng Nợ ({tong_no}) không bằng tổng Có ({tong_co})."
                )


class ButToanChiTiet(models.Model):
    """
    Journal entry line item model.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on double-entry bookkeeping
    """

    LOAI_NO_CO_CHOICES = [
        ("no", "Nợ"),
        ("co", "Có"),
    ]

    but_toan = models.ForeignKey(
        ButToan,
        on_delete=models.CASCADE,
        related_name="chi_tiet",
        verbose_name="Bút toán",
    )
    tai_khoan = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        verbose_name="Tài khoản",
    )
    loai_no_co = models.CharField(
        max_length=2,
        choices=LOAI_NO_CO_CHOICES,
        verbose_name="Loại Nợ/Có",
    )
    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    ma_doi_tuong = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mã đối tượng",
    )
    dien_giai = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Diễn giải",
    )
    so_chung_tu_goc = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Số chứng từ gốc",
    )

    class Meta:
        verbose_name = "Chi tiết bút toán"
        verbose_name_plural = "Chi tiết bút toán"

    def __str__(self):
        return f"{self.but_toan} - {self.tai_khoan} ({self.loai_no_co})"

    def clean(self):
        super().clean()
        if self.tai_khoan_id:
            prefix = self.tai_khoan.ma_tai_khoan[:1]
            account_type = self.tai_khoan.loai_tai_khoan
            if self.loai_no_co == "no":
                if account_type in ("doanh_thu", "thu_nhap_khac"):
                    raise ValidationError(
                        {
                            "loai_no_co": f"Tài khoản {self.tai_khoan.ma_tai_khoan} ({account_type}) "
                            f"không thể ghi Nợ."
                        }
                    )
            elif self.loai_no_co == "co":
                if account_type in ("chi_phi", "chi_phi_khac"):
                    raise ValidationError(
                        {
                            "loai_no_co": f"Tài khoản {self.tai_khoan.ma_tai_khoan} ({account_type}) "
                            f"không thể ghi Có."
                        }
                    )


class Kho(models.Model):
    """
    Warehouse model for inventory management.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
    """

    ma_kho = models.CharField(
        max_length=20,
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


class NhapKho(models.Model):
    """
    Goods receipt model for inventory in.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
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
    kho = models.ForeignKey(
        Kho,
        on_delete=models.PROTECT,
        related_name="nhap_kho",
        verbose_name="Kho",
    )
    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        related_name="nhap_kho",
        verbose_name="Nhà cung cấp",
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
        verbose_name = "Nhập kho"
        verbose_name_plural = "Nhập kho"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.kho}"


class NhapKhoChiTiet(models.Model):
    """
    Goods receipt line item model.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory details
    """

    nhap_kho = models.ForeignKey(
        NhapKho,
        on_delete=models.CASCADE,
        related_name="chi_tiet",
        verbose_name="Nhập kho",
    )
    hang_hoa = models.ForeignKey(
        "danh_muc.HangHoa",
        on_delete=models.PROTECT,
        verbose_name="Hàng hóa",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Số lượng",
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
        verbose_name = "Chi tiết nhập kho"
        verbose_name_plural = "Chi tiết nhập kho"

    def __str__(self):
        return f"{self.nhap_kho} - {self.hang_hoa}"


class XuatKho(models.Model):
    """
    Goods issue model for inventory out.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
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
    kho = models.ForeignKey(
        Kho,
        on_delete=models.PROTECT,
        related_name="xuat_kho",
        verbose_name="Kho",
    )
    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.PROTECT,
        related_name="xuat_kho",
        null=True,
        blank=True,
        verbose_name="Khách hàng",
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
        verbose_name = "Xuất kho"
        verbose_name_plural = "Xuất kho"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.kho}"


class XuatKhoChiTiet(models.Model):
    """
    Goods issue line item model.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory details
    """

    xuat_kho = models.ForeignKey(
        XuatKho,
        on_delete=models.CASCADE,
        related_name="chi_tiet",
        verbose_name="Xuất kho",
    )
    hang_hoa = models.ForeignKey(
        "danh_muc.HangHoa",
        on_delete=models.PROTECT,
        verbose_name="Hàng hóa",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Số lượng",
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
        verbose_name = "Chi tiết xuất kho"
        verbose_name_plural = "Chi tiết xuất kho"

    def __str__(self):
        return f"{self.xuat_kho} - {self.hang_hoa}"
