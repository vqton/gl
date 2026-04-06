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


class VaiTro(models.Model):
    """
    Role model for RBAC system.

    Pre-defined roles: ke_toan_truong, ke_toan_vien, thu_quy, giam_doc.
    Seeded via management command.
    """

    ma = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Mã vai trò",
    )
    ten = models.CharField(
        max_length=100,
        verbose_name="Tên vai trò",
    )
    mo_ta = models.TextField(
        blank=True,
        default="",
        verbose_name="Mô tả",
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
        ordering = ["ma"]
        verbose_name = "Vai trò"
        verbose_name_plural = "Vai trò"

    def __str__(self):
        return self.ten


class SoDuDauKy(models.Model):
    """
    Opening balance model (Số dư đầu kỳ).

    Stores opening balances for each account at the start of a fiscal year.
    Supports general ledger and sub-ledger entries (customers, suppliers,
    inventory, fixed assets).

    Legal basis:
        - Thông tư 99/2025/TT-BTC on opening balance requirements
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    tai_khoan = models.ForeignKey(
        "danh_muc.TaiKhoanKeToan",
        on_delete=models.PROTECT,
        related_name="so_du_dau_ky",
        verbose_name="Tài khoản",
    )
    doi_tuong_ma = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mã đối tượng",
        help_text="Mã khách hàng/nhà cung cấp (cho TK 131, 331)",
    )
    kho = models.ForeignKey(
        "kho.Kho",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="so_du_dau_ky",
        verbose_name="Kho",
    )
    hang_hoa = models.ForeignKey(
        "kho.VatTuHangHoa",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="so_du_dau_ky",
        verbose_name="Hàng hóa",
    )
    tai_san = models.ForeignKey(
        "tai_san.TaiSanCoDinh",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="so_du_dau_ky",
        verbose_name="Tài sản cố định",
    )
    so_du_no = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Số dư Nợ",
    )
    so_du_co = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0"),
        verbose_name="Số dư Có",
    )
    nam = models.IntegerField(
        verbose_name="Năm",
    )
    da_khoa = models.BooleanField(
        default=False,
        verbose_name="Đã khóa",
        help_text="Không cho phép chỉnh sửa khi đã khóa",
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
        ordering = ["tai_khoan__ma_tai_khoan", "doi_tuong_ma"]
        verbose_name = "Số dư đầu kỳ"
        verbose_name_plural = "Số dư đầu kỳ"
        constraints = [
            models.UniqueConstraint(
                fields=["tai_khoan", "doi_tuong_ma", "nam"],
                name="unique_so_du_tai_khoan_doi_tuong_nam",
            ),
        ]

    def __str__(self):
        doi_tuong = f" ({self.doi_tuong_ma})" if self.doi_tuong_ma else ""
        return f"{self.tai_khoan}{doi_tuong} - {self.nam}"

    def clean(self):
        """Validate opening balance rules."""
        super().clean()

        if self.so_du_no < Decimal("0"):
            raise ValidationError({"so_du_no": "Số dư Nợ không được âm."})

        if self.so_du_co < Decimal("0"):
            raise ValidationError({"so_du_co": "Số dư Có không được âm."})

        if self.so_du_no > Decimal("0") and self.so_du_co > Decimal("0"):
            raise ValidationError(
                "Một tài khoản không được có cả số dư Nợ và số dư Có. "
                "Vui lòng chỉ nhập một trong hai."
            )

        if self.da_khoa and self.pk:
            try:
                original = SoDuDauKy.objects.get(pk=self.pk)
                if (
                    original.so_du_no != self.so_du_no
                    or original.so_du_co != self.so_du_co
                    or original.doi_tuong_ma != self.doi_tuong_ma
                ):
                    raise ValidationError(
                        "Số dư đã khóa không được chỉnh sửa. "
                        "Vui lòng mở khóa trước khi sửa."
                    )
            except SoDuDauKy.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        """Auto-create/update KhoEntry for inventory opening balances."""
        super().save(*args, **kwargs)

        if self.hang_hoa_id and self.kho_id:
            self._sync_kho_entry()

    def delete(self, *args, **kwargs):
        """Prevent deletion of locked balances."""
        if self.da_khoa:
            raise ValidationError("Không được xóa số dư đã khóa.")
        if self.hang_hoa_id and self.kho_id:
            from apps.kho.models import KhoEntry

            KhoEntry.objects.filter(
                hang_hoa=self.hang_hoa,
                kho=self.kho,
                is_opening=True,
                so_chung_tu=f"SODK-{self.pk}",
            ).delete()
        super().delete(*args, **kwargs)

    def finalize(self):
        """Lock this opening balance record."""
        self.da_khoa = True
        self.save(update_fields=["da_khoa", "updated_at"])

    def _sync_kho_entry(self):
        """Create or update KhoEntry for inventory opening balance."""
        from apps.kho.models import KhoEntry

        entry, created = KhoEntry.objects.get_or_create(
            hang_hoa=self.hang_hoa,
            kho=self.kho,
            is_opening=True,
            so_chung_tu=f"SODK-{self.pk}",
            defaults={
                "loai": "NHAP",
                "ngay_chung_tu": f"{self.nam}-01-01",
                "loai_chung_tu": "NK",
                "so_luong": Decimal("0"),
                "don_gia": Decimal("0"),
                "thanh_tien": self.so_du_no,
                "dien_giai": f"Số dư đầu kỳ {self.nam} - {self.tai_khoan}",
            },
        )
        if not created:
            entry.thanh_tien = self.so_du_no
            entry.dien_giai = f"Số dư đầu kỳ {self.nam} - {self.tai_khoan}"
            entry.save(update_fields=["thanh_tien", "dien_giai", "updated_at"])


class Client(models.Model):
    """
    Client model for accounting firms managing multiple customers.

    Each client has its own database file. Supports lifecycle management:
    active -> suspended -> expired.
    """

    TRANG_THAI_CHOICES = [
        ("active", "Hoạt động"),
        ("suspended", "Tạm khóa"),
        ("expired", "Hết hạn"),
    ]

    ma_khach_hang = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã khách hàng",
        help_text="Tự động sinh (KH001, KH002, ...)",
    )
    ten_cong_ty = models.CharField(
        max_length=255,
        verbose_name="Tên công ty",
    )
    ma_so_thue = models.CharField(
        max_length=20,
        verbose_name="Mã số thuế",
    )
    nganh_nghe = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Ngành nghề",
    )
    db_path = models.CharField(
        max_length=500,
        verbose_name="Đường dẫn CSDL",
        help_text="VD: data/clients/client_001_2026.sqlite3",
    )
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default="active",
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
        ordering = ["ma_khach_hang"]
        verbose_name = "Khách hàng (Dịch vụ kế toán)"
        verbose_name_plural = "Khách hàng (Dịch vụ kế toán)"

    def __str__(self):
        return f"{self.ma_khach_hang} - {self.ten_cong_ty}"

    def save(self, *args, **kwargs):
        """Auto-generate ma_khach_hang if not set."""
        if not self.ma_khach_hang:
            last = Client.objects.order_by("-ma_khach_hang").first()
            if last and last.ma_khach_hang.startswith("KH"):
                try:
                    num = int(last.ma_khach_hang[2:]) + 1
                except ValueError:
                    num = 1
            else:
                num = 1
            self.ma_khach_hang = f"KH{num:03d}"
        super().save(*args, **kwargs)

    def suspend(self):
        """Suspend client access."""
        self.trang_thai = "suspended"
        self.save(update_fields=["trang_thai", "updated_at"])

    def activate(self):
        """Reactivate client."""
        self.trang_thai = "active"
        self.save(update_fields=["trang_thai", "updated_at"])

    def archive(self):
        """Archive client (set to expired)."""
        self.trang_thai = "expired"
        self.save(update_fields=["trang_thai", "updated_at"])

    @classmethod
    def get_active_clients(cls):
        """Get all active clients."""
        return cls.objects.filter(trang_thai="active")


class ClientUserMapping(models.Model):
    """
    Maps users to clients with optional role per client.

    Allows firm accountants to access specific clients with specific roles.
    """

    client = models.ForeignKey(
        "he_thong.Client",
        on_delete=models.CASCADE,
        related_name="user_mappings",
        verbose_name="Khách hàng",
    )
    user = models.ForeignKey(
        "users.NguoiDung",
        on_delete=models.CASCADE,
        related_name="client_mappings",
        verbose_name="Người dùng",
    )
    vai_tro = models.ForeignKey(
        "he_thong.VaiTro",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vai trò (theo khách hàng)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
    )

    class Meta:
        ordering = ["client__ma_khach_hang"]
        verbose_name = "Phân quyền khách hàng"
        verbose_name_plural = "Phân quyền khách hàng"
        constraints = [
            models.UniqueConstraint(
                fields=["client", "user"],
                name="unique_client_user_mapping",
            ),
        ]

    def __str__(self):
        role_str = f" ({self.vai_tro})" if self.vai_tro else ""
        return f"{self.client} → {self.user}{role_str}"
