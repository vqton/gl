"""Bank models for Vietnamese SME Accounting System."""

from django.db import models

from apps.danh_muc.models import NhaCungCap, TaiKhoanNganHang


class GiayBaoNo(models.Model):
    """
    Bank debit notice (Giấy báo Nợ) - tiền bị trừ khỏi tài khoản.
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("posted", "Đã ghi sổ"),
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
    tai_khoan_ngan_hang = models.ForeignKey(
        TaiKhoanNganHang,
        on_delete=models.PROTECT,
        related_name="giay_bao_no",
        verbose_name="Tài khoản ngân hàng",
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
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
    )
    da_doi_chieu = models.BooleanField(
        default=False,
        verbose_name="Đã đối chiếu",
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
        verbose_name = "Giấy báo Nợ"
        verbose_name_plural = "Giấy báo Nợ"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.ngay} - {self.so_tien}"


class GiayBaoCo(models.Model):
    """
    Bank credit notice (Giấy báo Có) - tiền được cộng vào tài khoản.
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("posted", "Đã ghi sổ"),
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
    tai_khoan_ngan_hang = models.ForeignKey(
        TaiKhoanNganHang,
        on_delete=models.PROTECT,
        related_name="giay_bao_co",
        verbose_name="Tài khoản ngân hàng",
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
        choices=TRANG_THAI_CHOICES,
        default="draft",
        verbose_name="Trạng thái",
    )
    da_doi_chieu = models.BooleanField(
        default=False,
        verbose_name="Đã đối chiếu",
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
        verbose_name = "Giấy báo Có"
        verbose_name_plural = "Giấy báo Có"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.ngay} - {self.so_tien}"


class UyNhiemChi(models.Model):
    """
    Payment order (Ủy nhiệm chi) - lệnh chuyển tiền từ tài khoản ngân hàng.
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("confirmed", "Đã xác nhận"),
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
    tai_khoan_ngan_hang = models.ForeignKey(
        TaiKhoanNganHang,
        on_delete=models.PROTECT,
        related_name="uy_nhiem_chi",
        verbose_name="Tài khoản ngân hàng",
    )
    nha_cung_cap = models.ForeignKey(
        NhaCungCap,
        on_delete=models.PROTECT,
        related_name="uy_nhiem_chi",
        verbose_name="Nhà cung cấp",
    )
    so_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền",
    )
    noi_dung = models.TextField(
        blank=True,
        default="",
        verbose_name="Nội dung thanh toán",
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
        verbose_name = "Ủy nhiệm chi"
        verbose_name_plural = "Ủy nhiệm chi"

    def __str__(self):
        return f"{self.so_chung_tu} - {self.nha_cung_cap}"


class DoiChieuNganHang(models.Model):
    """
    Bank reconciliation (Đối chiếu ngân hàng) - monthly bank statement reconciliation.
    """

    TRANG_THAI_CHOICES = [
        ("cho_doi_chieu", "Chờ đối chiếu"),
        ("da_doi_chieu", "Đã đối chiếu"),
        ("co_chenh_lech", "Có chênh lệch"),
    ]

    tai_khoan_ngan_hang = models.ForeignKey(
        TaiKhoanNganHang,
        on_delete=models.PROTECT,
        related_name="doi_chieu",
        verbose_name="Tài khoản ngân hàng",
    )
    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    so_du_so_sach = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số dư sổ sách",
    )
    so_du_ngan_hang = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số dư ngân hàng",
    )
    chenh_lech = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Chênh lệch",
    )
    trang_thai = models.CharField(
        max_length=15,
        choices=TRANG_THAI_CHOICES,
        default="cho_doi_chieu",
        verbose_name="Trạng thái",
    )
    ghi_chu = models.TextField(
        blank=True,
        default="",
        verbose_name="Ghi chú",
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
        unique_together = ["tai_khoan_ngan_hang", "thang", "nam"]
        ordering = ["-nam", "-thang"]
        verbose_name = "Đối chiếu ngân hàng"
        verbose_name_plural = "Đối chiếu ngân hàng"

    def __str__(self):
        return f"{self.tai_khoan_ngan_hang} - {self.thang}/{self.nam}"

    def save(self, *args, **kwargs):
        """Auto-calculate difference and set status."""
        self.chenh_lech = self.so_du_so_sach - self.so_du_ngan_hang
        if self.chenh_lech == 0:
            self.trang_thai = "da_doi_chieu"
        elif self.trang_thai == "cho_doi_chieu":
            self.trang_thai = "co_chenh_lech"
        super().save(*args, **kwargs)
