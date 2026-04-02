"""Fixed Asset management models (M3)."""

from decimal import Decimal

from django.db import models


class TaiSanCoDinh(models.Model):
    """
    Fixed Asset model (Tài sản cố định).

    Supports straight-line depreciation method (Khấu hao đường thẳng).
    Auto-calculates monthly depreciation amount.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on fixed asset accounting
        - Thông tư 45/2013/TT-BTC on depreciation methods
        - TK 211, 214 (Fixed assets and accumulated depreciation)
    """

    PHUONG_PHAP_KHAU_HAO_CHOICES = [
        ("duong_thang", "Đường thẳng (Straight-line)"),
        ("giam_dan", "Giảm dần (Declining balance)"),
    ]

    TRANG_THAI_CHOICES = [
        ("dang_su_dung", "Đang sử dụng"),
        ("dung_khau_hao", "Đã khấu hao hết"),
        ("thanh_ly", "Đã thanh lý"),
    ]

    ma_tai_san = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã tài sản",
    )
    ten_tai_san = models.CharField(
        max_length=255,
        verbose_name="Tên tài sản",
    )
    nhom_tai_san = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Nhóm tài sản",
    )
    so_luong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
        verbose_name="Số lượng",
    )
    nguyen_gia = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Nguyên giá",
        help_text="Giá trị ban đầu của tài sản",
    )
    gia_tri_con_lai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Giá trị còn lại",
        help_text="Nguyên giá - Khấu hao lũy kế",
    )
    khau_hao_luy_ke = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Khấu hao lũy kế",
    )
    thoi_gian_khau_hao_thang = models.IntegerField(
        verbose_name="Thời gian khấu hao (tháng)",
        help_text="Số tháng khấu hao theo quy định",
    )
    muc_khau_hao_thang = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Mức khấu hao tháng",
        help_text="Tính tự động: Nguyên giá / Thời gian khấu hao",
    )
    phuong_phap_khau_hao = models.CharField(
        max_length=15,
        choices=PHUONG_PHAP_KHAU_HAO_CHOICES,
        default="duong_thang",
        verbose_name="Phương pháp khấu hao",
    )
    ngay_dua_vao_su_dung = models.DateField(
        verbose_name="Ngày đưa vào sử dụng",
    )
    ngay_khau_hao_cuoi = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày khấu hao cuối",
    )
    trang_thai = models.CharField(
        max_length=15,
        choices=TRANG_THAI_CHOICES,
        default="dang_su_dung",
        verbose_name="Trạng thái",
    )
    dia_chi = models.TextField(
        blank=True,
        default="",
        verbose_name="Địa chỉ / Nơi sử dụng",
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
        ordering = ["ma_tai_san"]
        verbose_name = "Tài sản cố định"
        verbose_name_plural = "Tài sản cố định"

    def __str__(self):
        return f"{self.ma_tai_san} - {self.ten_tai_san}"

    def save(self, *args, **kwargs):
        """Auto-calculate monthly depreciation and remaining value."""
        if self.thoi_gian_khau_hao_thang > 0:
            self.muc_khau_hao_thang = (
                self.nguyen_gia / self.thoi_gian_khau_hao_thang
            ).quantize(Decimal("0.01"))
        self.gia_tri_con_lai = self.nguyen_gia - self.khau_hao_luy_ke
        if self.gia_tri_con_lai <= Decimal("0"):
            self.gia_tri_con_lai = Decimal("0")
            if self.trang_thai == "dang_su_dung":
                self.trang_thai = "dung_khau_hao"
        super().save(*args, **kwargs)


class BangKhauHao(models.Model):
    """
    Monthly Depreciation Schedule (Bảng khấu hao tháng).

    Records each month's depreciation for each fixed asset.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on depreciation schedule
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    tai_san = models.ForeignKey(
        TaiSanCoDinh,
        on_delete=models.PROTECT,
        related_name="bang_khau_hao",
        verbose_name="Tài sản",
    )
    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    so_tien_khau_hao = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Số tiền khấu hao",
    )
    khau_hao_luy_ke_dau_thang = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="KH lũy kế đầu tháng",
    )
    khau_hao_luy_ke_cuoi_thang = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="KH lũy kế cuối tháng",
    )
    da_hach_toan = models.BooleanField(
        default=False,
        verbose_name="Đã hạch toán",
        help_text="Đã tạo bút toán khấu hao",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        unique_together = ["tai_san", "thang", "nam"]
        ordering = ["nam", "thang"]
        verbose_name = "Bảng khấu hao"
        verbose_name_plural = "Bảng khấu hao"

    def __str__(self):
        return f"{self.tai_san} - {self.thang}/{self.nam}"
