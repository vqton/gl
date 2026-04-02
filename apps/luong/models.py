"""Payroll models (M7: Lương & BHXH)."""

from decimal import Decimal

from django.db import models

from apps.luong.constants import (
    BHXT_NLD_BHXH,
    BHXT_NLD_BHTN,
    BHXT_NLD_BHYT,
    BHXT_TONG_DN,
    BHXT_TONG_NLD,
    GIAM_TRU_BAN_THAN,
    GIAM_TRU_PHU_THUOC,
    MAX_LUONG_BHXH,
    THUE_TNCN_BRACKETS,
)


class NhanVien(models.Model):
    """
    Employee model with encrypted sensitive data.

    Legal basis:
        - Nghị định 13/2023/NĐ-CP on personal data protection
        - Thông tư 99/2025/TT-BTC on payroll accounting
    """

    TRANG_THAI_CHOICES = [
        ("dang_lam_viec", "Đang làm việc"),
        ("nghi_viec", "Đã nghỉ việc"),
        ("tam_ngung", "Tạm ngừng"),
    ]

    ma_nhan_vien = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã nhân viên",
    )
    ho_ten = models.CharField(
        max_length=255,
        verbose_name="Họ tên",
    )
    ngay_sinh = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày sinh",
    )
    cmnd_ccc = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="CMND/CCCD",
    )
    ma_so_thue = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mã số thuế",
    )
    so_dien_thoai = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Số điện thoại",
    )
    so_tai_khoan = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Số tài khoản ngân hàng",
    )
    luong_co_ban = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Lương cơ bản",
    )
    he_so_phu_cap = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Hệ số phụ cấp",
    )
    so_nguoi_phu_thuoc = models.IntegerField(
        default=0,
        verbose_name="Số người phụ thuộc",
    )
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default="dang_lam_viec",
        verbose_name="Trạng thái",
    )
    ngay_vao_lam = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày vào làm",
    )
    ngay_nghi = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày nghỉ",
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
        ordering = ["ma_nhan_vien"]
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"

    def __str__(self):
        return f"{self.ma_nhan_vien} - {self.ho_ten}"


class BangLuong(models.Model):
    """
    Monthly payroll record for an employee.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on payroll accounting
        - Nghị định 58/2020/NĐ-CP on social insurance
    """

    nhan_vien = models.ForeignKey(
        NhanVien,
        on_delete=models.PROTECT,
        related_name="bang_luong",
        verbose_name="Nhân viên",
    )
    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    # Income
    luong_co_ban = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Lương cơ bản",
    )
    phu_cap = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Phụ cấp",
    )
    tong_thu_nhap = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Tổng thu nhập",
    )
    # Deductions - Employee portion
    bhxh_nld = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHXH NLĐ (8%)",
    )
    bhyt_nld = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHYT NLĐ (1.5%)",
    )
    bhtn_nld = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHTN NLĐ (1%)",
    )
    tong_bhxh_nld = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Tổng BHXH NLĐ",
    )
    # Tax
    thu_nhap_tinh_thue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Thu nhập tính thuế",
    )
    thue_tncn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Thuế TNCN",
    )
    # Net
    thuc_linh = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Thực lĩnh",
    )
    # Employer portion
    bhxh_dn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHXH DN (17.5%)",
    )
    bhyt_dn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHYT DN (3%)",
    )
    bhtn_dn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHTN DN (1%)",
    )
    bhtnld_bnn_dn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="BHTNLĐ-BNN DN (0.5%)",
    )
    tong_bhxh_dn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Tổng BHXH DN",
    )
    da_hach_toan = models.BooleanField(
        default=False,
        verbose_name="Đã hạch toán",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        unique_together = ["nhan_vien", "thang", "nam"]
        ordering = ["nam", "thang", "nhan_vien__ma_nhan_vien"]
        verbose_name = "Bảng lương"
        verbose_name_plural = "Bảng lương"

    def __str__(self):
        return f"{self.nhan_vien} - {self.thang}/{self.nam}"
