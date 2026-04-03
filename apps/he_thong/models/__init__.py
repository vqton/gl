"""He thong (System) models for configuration and audit."""

import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class ThongTinCongTy(models.Model):
    """
    Singleton model for company information.

    Only one instance is allowed (pk=1). Cannot be deleted.
    """

    HINH_THUC_KE_TOAN_CHOICES = [
        ("nhat_ky_chung", "Nhật ký chung"),
        ("nhat_ky_so_cai", "Nhật ký - Sổ cái"),
        ("chung_tu_ghi_so", "Chứng từ ghi sổ"),
        ("nhat_ky_chung_tu", "Nhật ký chứng từ"),
    ]

    PHUONG_PHAP_GTGT_CHOICES = [
        ("khau_tru", "Khấu trừ"),
        ("truc_tiep", "Trực tiếp"),
    ]

    PHUONG_PHAP_TON_KHO_CHOICES = [
        ("nhap_truoc_xuat_truoc", "Nhập trước xuất trước (FIFO)"),
        ("nhap_sau_xuat_truoc", "Nhập sau xuất trước (LIFO)"),
        ("binh_quan_lien_hoan", "Bình quân liên hoàn"),
        ("binh_quan_cuoi_ky", "Bình quân cuối kỳ"),
        ("thuc_te_lich_trinh", "Thực tế đích danh"),
    ]

    ten_cong_ty = models.CharField(
        max_length=255,
        verbose_name="Tên công ty",
    )
    ma_so_thue = models.CharField(
        max_length=20,
        verbose_name="Mã số thuế",
    )
    dia_chi = models.TextField(
        blank=True,
        default="",
        verbose_name="Địa chỉ",
    )
    dien_thoai = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Điện thoại",
    )
    email = models.EmailField(
        blank=True,
        default="",
        verbose_name="Email",
    )
    nguoi_dai_dien = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Người đại diện",
    )
    chuc_vu_ndd = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Chức vụ người đại diện",
    )
    ke_toan_truong = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Kế toán trưởng",
    )
    hinh_thuc_ke_toan = models.CharField(
        max_length=30,
        choices=HINH_THUC_KE_TOAN_CHOICES,
        default="nhat_ky_chung",
        verbose_name="Hình thức kế toán",
    )
    phuong_phap_gtgt = models.CharField(
        max_length=20,
        choices=PHUONG_PHAP_GTGT_CHOICES,
        default="khau_tru",
        verbose_name="Phương pháp GTGT",
    )
    phuong_phap_ton_kho = models.CharField(
        max_length=30,
        choices=PHUONG_PHAP_TON_KHO_CHOICES,
        default="binh_quan_lien_hoan",
        verbose_name="Phương pháp tồn kho",
    )
    logo = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True,
        verbose_name="Logo",
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
        verbose_name = "Thông tin công ty"
        verbose_name_plural = "Thông tin công ty"

    def __str__(self):
        return self.ten_cong_ty

    def save(self, *args, **kwargs):
        """Force singleton pattern with pk=1."""
        self.pk = 1
        existing = ThongTinCongTy.objects.filter(pk=1).first()
        if existing:
            ThongTinCongTy.objects.filter(pk=1).update(
                ten_cong_ty=self.ten_cong_ty,
                ma_so_thue=self.ma_so_thue,
                dia_chi=self.dia_chi,
                dien_thoai=self.dien_thoai,
                email=self.email,
                nguoi_dai_dien=self.nguoi_dai_dien,
                chuc_vu_ndd=self.chuc_vu_ndd,
                ke_toan_truong=self.ke_toan_truong,
                hinh_thuc_ke_toan=self.hinh_thuc_ke_toan,
                phuong_phap_gtgt=self.phuong_phap_gtgt,
                phuong_phap_ton_kho=self.phuong_phap_ton_kho,
                logo=self.logo,
                updated_at=timezone.now(),
            )
            return
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of singleton."""
        raise ValidationError("Không được xóa thông tin công ty.")

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class KyKeToan(models.Model):
    """
    Accounting period model.

    Prevents posting to locked/closed periods.
    """

    TRANG_THAI_CHOICES = [
        ("open", "Mở"),
        ("locked", "Khóa"),
        ("closed", "Đóng"),
    ]

    nam = models.IntegerField(
        verbose_name="Năm",
    )
    ngay_bat_dau = models.DateField(
        verbose_name="Ngày bắt đầu",
    )
    ngay_ket_thuc = models.DateField(
        verbose_name="Ngày kết thúc",
    )
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default="open",
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
        ordering = ["-nam", "ngay_bat_dau"]
        verbose_name = "Kỳ kế toán"
        verbose_name_plural = "Kỳ kế toán"

    def __str__(self):
        return f"Kỳ {self.nam}: {self.ngay_bat_dau} - {self.ngay_ket_thuc}"

    def clean(self):
        """Validate period dates."""
        super().clean()
        if self.ngay_ket_thuc <= self.ngay_bat_dau:
            raise ValidationError(
                {"ngay_ket_thuc": "Ngày kết thúc phải sau ngày bắt đầu."}
            )

    def is_postable(self):
        """Check if posting is allowed in this period."""
        return self.trang_thai == "open"

    def lock(self):
        """Lock the period."""
        self.trang_thai = "locked"
        self.save(update_fields=["trang_thai", "updated_at"])

    def unlock(self):
        """Unlock the period."""
        self.trang_thai = "open"
        self.save(update_fields=["trang_thai", "updated_at"])

    @classmethod
    def get_open_periods(cls):
        """Get all open accounting periods."""
        return cls.objects.filter(trang_thai="open")

    @classmethod
    def can_post_on_date(cls, date):
        """Check if posting is allowed on a given date."""
        period = cls.objects.filter(
            ngay_bat_dau__lte=date,
            ngay_ket_thuc__gte=date,
        ).first()
        if period is None:
            return False
        return period.is_postable()


class CauHinhHeThong(models.Model):
    """
    System configuration for tax rates and defaults.

    Singleton model (pk=1).
    """

    tien_te_mac_dinh = models.CharField(
        max_length=10,
        default="VND",
        verbose_name="Tiền tệ mặc định",
    )
    ty_gia = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=Decimal("1.0000"),
        verbose_name="Tỷ giá",
    )
    thue_tndn_15 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("15.00"),
        verbose_name="Thuế TNDN 15%",
    )
    thue_tndn_20 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("20.00"),
        verbose_name="Thuế TNDN 20%",
    )
    thue_vat_0 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Thuế VAT 0%",
    )
    thue_vat_5 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("5.00"),
        verbose_name="Thuế VAT 5%",
    )
    thue_vat_8 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("8.00"),
        verbose_name="Thuế VAT 8%",
    )
    thue_vat_10 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
        verbose_name="Thuế VAT 10%",
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
        verbose_name = "Cấu hình hệ thống"
        verbose_name_plural = "Cấu hình hệ thống"

    def __str__(self):
        return "Cấu hình hệ thống"

    def save(self, *args, **kwargs):
        """Force singleton pattern with pk=1."""
        self.pk = 1
        existing = CauHinhHeThong.objects.filter(pk=1).first()
        if existing:
            CauHinhHeThong.objects.filter(pk=1).update(
                tien_te_mac_dinh=self.tien_te_mac_dinh,
                ty_gia=self.ty_gia,
                thue_tndn_15=self.thue_tndn_15,
                thue_tndn_20=self.thue_tndn_20,
                thue_vat_0=self.thue_vat_0,
                thue_vat_5=self.thue_vat_5,
                thue_vat_8=self.thue_vat_8,
                thue_vat_10=self.thue_vat_10,
                updated_at=timezone.now(),
            )
            return
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of singleton."""
        raise ValidationError("Không được xóa cấu hình hệ thống.")

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class AuditLog(models.Model):
    """
    Audit log for tracking system changes.

    Written to audit.sqlite3 via AuditQueue for performance.
    """

    user = models.CharField(
        max_length=150,
        verbose_name="Người dùng",
    )
    action = models.CharField(
        max_length=50,
        verbose_name="Hành động",
    )
    url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="URL",
    )
    ip_address = models.CharField(
        max_length=45,
        blank=True,
        default="",
        verbose_name="Địa chỉ IP",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Thời gian",
    )
    model_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Tên model",
    )
    object_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="ID đối tượng",
    )
    old_value = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Giá trị cũ",
    )
    new_value = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Giá trị mới",
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Nhật ký kiểm tra"
        verbose_name_plural = "Nhật ký kiểm tra"

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
