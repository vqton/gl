"""Thuế models - Tax declarations."""

from django.db import models

from apps.nghiep_vu.models import HoaDon


class BangKeHoaDonMuaVao(models.Model):
    """
    Purchase invoice register (Bảng kê hóa đơn mua vào).
    """

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    hoa_don = models.ForeignKey(
        HoaDon,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bang_ke_mua_vao",
        verbose_name="Hóa đơn",
    )
    ma_so_thue_ncc = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="MST nhà cung cấp",
    )
    tien_chua_thue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tiền chưa thuế",
    )
    thue_gtgt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế GTGT",
    )
    tong_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng tiền",
    )
    loai_hang_hoa = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Loại hàng hóa",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        ordering = ["-nam", "-thang"]
        verbose_name = "Bảng kê hóa đơn mua vào"
        verbose_name_plural = "Bảng kê hóa đơn mua vào"

    def __str__(self):
        return f"Mua vào - {self.thang}/{self.nam}"

    def save(self, *args, **kwargs):
        self.tong_tien = self.tien_chua_thue + self.thue_gtgt
        super().save(*args, **kwargs)


class BangKeHoaDonBanRa(models.Model):
    """
    Sales invoice register (Bảng kê hóa đơn bán ra).
    """

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    hoa_don = models.ForeignKey(
        HoaDon,
        on_delete=models.PROTECT,
        related_name="bang_ke_ban_ra",
        verbose_name="Hóa đơn",
    )
    ma_so_thue_kh = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="MST khách hàng",
    )
    tien_chua_thue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tiền chưa thuế",
    )
    thue_gtgt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế GTGT",
    )
    tong_tien = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng tiền",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        ordering = ["-nam", "-thang"]
        verbose_name = "Bảng kê hóa đơn bán ra"
        verbose_name_plural = "Bảng kê hóa đơn bán ra"

    def __str__(self):
        return f"Bán ra - {self.thang}/{self.nam}"

    def save(self, *args, **kwargs):
        self.tong_tien = self.tien_chua_thue + self.thue_gtgt
        super().save(*args, **kwargs)


class ToKhaiGTGT(models.Model):
    """
    VAT declaration (Tờ khai GTGT - Mẫu 01/GTGT).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("da_nop", "Đã nộp"),
    ]

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    tong_doanh_so_ban = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng doanh số bán",
    )
    thue_gtgt_dau_ra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế GTGT đầu ra",
    )
    tong_gia_tri_mua_vao = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng giá trị mua vào",
    )
    thue_gtgt_dau_vao = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế GTGT đầu vào",
    )
    thue_gtgt_phai_nop = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế GTGT phải nộp",
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
        unique_together = ["thang", "nam"]
        ordering = ["-nam", "-thang"]
        verbose_name = "Tờ khai GTGT"
        verbose_name_plural = "Tờ khai GTGT"

    def __str__(self):
        return f"GTGT - {self.thang}/{self.nam}"

    def save(self, *args, **kwargs):
        self.thue_gtgt_phai_nop = self.thue_gtgt_dau_ra - self.thue_gtgt_dau_vao
        if self.thue_gtgt_phai_nop < 0:
            self.thue_gtgt_phai_nop = 0
        super().save(*args, **kwargs)


class ToKhaiTNDNTamTinh(models.Model):
    """
    Corporate income tax quarterly (Tờ khai TNDN tạm tính).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("da_nop", "Đã nộp"),
    ]

    quy = models.IntegerField(
        verbose_name="Quý",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    doanh_thu = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Doanh thu",
    )
    chi_phi_duoc_tru = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Chi phí được trừ",
    )
    loi_nhuan = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Lợi nhuận",
    )
    thue_phai_nop = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Thuế phải nộp",
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
        unique_together = ["quy", "nam"]
        ordering = ["-nam", "-quy"]
        verbose_name = "Tờ khai TNDN tạm tính"
        verbose_name_plural = "Tờ khai TNDN tạm tính"

    def __str__(self):
        return f"TNDN Q{self.quy}/{self.nam}"


class ToKhaiTNCN(models.Model):
    """
    Personal income tax monthly (Tờ khai TNCN).
    """

    TRANG_THAI_CHOICES = [
        ("draft", "Nháp"),
        ("da_nop", "Đã nộp"),
    ]

    thang = models.IntegerField(
        verbose_name="Tháng",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    tong_thu_nhap = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng thu nhập",
    )
    tong_thue_tncn = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Tổng thuế TNCN",
    )
    so_nhan_vien = models.IntegerField(
        default=0,
        verbose_name="Số nhân viên",
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
        unique_together = ["thang", "nam"]
        ordering = ["-nam", "-thang"]
        verbose_name = "Tờ khai TNCN"
        verbose_name_plural = "Tờ khai TNCN"

    def __str__(self):
        return f"TNCN - {self.thang}/{self.nam}"
