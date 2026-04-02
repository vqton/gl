"""Master data models for Vietnamese SME Accounting System."""

from django.db import models


class TaiKhoanKeToan(models.Model):
    """
    Accounting account model following Thông tư 99/2025/TT-BTC.

    Represents both Tier-1 (cap_do=1) and Tier-2 (cap_do=2) accounts
    from the Vietnamese Chart of Accounts.
    """

    LOAI_TAI_KHOAN_CHOICES = [
        ("tai_san", "Tài sản (Assets)"),
        ("no_phai_tra", "Nợ phải trả (Liabilities)"),
        ("von_chu_so_huu", "Vốn chủ sở hữu (Owner Equity)"),
        ("doanh_thu", "Doanh thu (Revenue)"),
        ("chi_phi", "Chi phí (Expenses)"),
        ("thu_nhap_khac", "Thu nhập khác"),
        ("chi_phi_khac", "Chi phí khác"),
        ("xac_dinh_kq", "Xác định kết quả"),
    ]

    ma_tai_khoan = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Mã tài khoản",
    )
    ten_tai_khoan = models.CharField(
        max_length=255,
        verbose_name="Tên tài khoản",
    )
    cap_do = models.IntegerField(
        choices=[(1, "Cấp 1"), (2, "Cấp 2")],
        verbose_name="Cấp độ",
    )
    tai_khoan_me = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tai_khoan_con",
        verbose_name="Tài khoản mẹ",
    )
    loai_tai_khoan = models.CharField(
        max_length=20,
        choices=LOAI_TAI_KHOAN_CHOICES,
        verbose_name="Loại tài khoản",
    )
    mo_ta = models.TextField(
        blank=True,
        default="",
        verbose_name="Mô tả",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Hoạt động",
    )
    is_immutable = models.BooleanField(
        default=False,
        help_text="Prevents modification of seeded master data",
        verbose_name="Bất biến",
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
        ordering = ["ma_tai_khoan"]
        verbose_name = "Tài khoản kế toán"
        verbose_name_plural = "Tài khoản kế toán"

    def __str__(self):
        return f"{self.ma_tai_khoan} - {self.ten_tai_khoan}"

    def clean(self):
        """Validate account code format and parent-child relationship."""
        from django.core.exceptions import ValidationError

        if self.cap_do == 2 and not self.tai_khoan_me:
            raise ValidationError(
                {"tai_khoan_me": "Tài khoản cấp 2 phải có tài khoản mẹ cấp 1."}
            )

        if self.cap_do == 1 and self.tai_khoan_me:
            raise ValidationError(
                {"tai_khoan_me": "Tài khoản cấp 1 không được có tài khoản mẹ."}
            )

    def save(self, *args, **kwargs):
        """Auto-detect account type from code prefix."""
        if not self.loai_tai_khoan:
            prefix = self.ma_tai_khoan[:1]
            type_map = {
                "1": "tai_san",
                "2": "tai_san",
                "3": "no_phai_tra",
                "4": "von_chu_so_huu",
                "5": "doanh_thu",
                "6": "chi_phi",
                "7": "thu_nhap_khac",
                "8": "chi_phi_khac",
                "9": "xac_dinh_kq",
                "0": "tai_san",
            }
            self.loai_tai_khoan = type_map.get(prefix, "tai_san")
        super().save(*args, **kwargs)


class DonVi(models.Model):
    """
    Company/Entity model for the accounting unit.

    Represents the business entity using the accounting system.
    """

    LOAI_DON_VI_CHOICES = [
        ("tnhh", "Công ty TNHH"),
        ("cp", "Công ty Cổ phần"),
        ("dn_tu_nhan", "Doanh nghiệp tư nhân"),
        ("hop_danh", "Công ty Hợp danh"),
        ("khac", "Loại khác"),
    ]

    ma_so_thue = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã số thuế",
    )
    ten_don_vi = models.CharField(
        max_length=255,
        verbose_name="Tên đơn vị",
    )
    loai_don_vi = models.CharField(
        max_length=20,
        choices=LOAI_DON_VI_CHOICES,
        verbose_name="Loại đơn vị",
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
        verbose_name = "Đơn vị"
        verbose_name_plural = "Đơn vị"

    def __str__(self):
        return f"{self.ten_don_vi} ({self.ma_so_thue})"


class NhaCungCap(models.Model):
    """
    Supplier model for Vietnamese SME Accounting System.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on supplier management
    """

    ma_ncc = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã nhà cung cấp",
    )
    ten_ncc = models.CharField(
        max_length=255,
        verbose_name="Tên nhà cung cấp",
    )
    ma_so_thue = models.CharField(
        max_length=20,
        blank=True,
        default="",
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
    tai_khoan_ngan_hang = models.CharField(
        max_length=30,
        blank=True,
        default="",
        verbose_name="Tài khoản ngân hàng",
    )
    ngan_hang = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Ngân hàng",
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
        ordering = ["ma_ncc"]
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"

    def __str__(self):
        return f"{self.ma_ncc} - {self.ten_ncc}"


class KhachHang(models.Model):
    """
    Customer model for Vietnamese SME Accounting System.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on customer management
        - Nghị định 320/2025/NĐ-CP on e-invoice requirements
    """

    ma_kh = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã khách hàng",
    )
    ten_kh = models.CharField(
        max_length=255,
        verbose_name="Tên khách hàng",
    )
    ma_so_thue = models.CharField(
        max_length=20,
        blank=True,
        default="",
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
    so_gioi_thieu_dien_tu = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Số giới thiệu điện tử (eTax ID)",
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
        ordering = ["ma_kh"]
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"

    def __str__(self):
        return f"{self.ma_kh} - {self.ten_kh}"


class NganHang(models.Model):
    """
    Bank model for Vietnamese banking system.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on bank account management
    """

    ma_ngan_hang = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã ngân hàng",
    )
    ten_ngan_hang = models.CharField(
        max_length=255,
        verbose_name="Tên ngân hàng",
    )
    ma_dien_toan = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mã điện toán (SWIFT)",
    )
    dia_chi = models.TextField(
        blank=True,
        default="",
        verbose_name="Địa chỉ",
    )

    class Meta:
        ordering = ["ma_ngan_hang"]
        verbose_name = "Ngân hàng"
        verbose_name_plural = "Ngân hàng"

    def __str__(self):
        return f"{self.ma_ngan_hang} - {self.ten_ngan_hang}"


class TaiKhoanNganHang(models.Model):
    """
    Company bank account model.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on bank account management
    """

    ngan_hang = models.ForeignKey(
        NganHang,
        on_delete=models.PROTECT,
        related_name="tai_khoan",
        verbose_name="Ngân hàng",
    )
    so_tai_khoan = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Số tài khoản",
    )
    ten_chu_tai_khoan = models.CharField(
        max_length=255,
        verbose_name="Tên chủ tài khoản",
    )
    tien_te = models.CharField(
        max_length=10,
        default="VND",
        verbose_name="Tiền tệ",
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
        ordering = ["so_tai_khoan"]
        verbose_name = "Tài khoản ngân hàng"
        verbose_name_plural = "Tài khoản ngân hàng"

    def __str__(self):
        return f"{self.so_tai_khoan} - {self.ten_chu_tai_khoan}"


class HangHoa(models.Model):
    """
    Goods/Services model for inventory management.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    THUE_SUAT_GTGT_CHOICES = [
        ("0", "0%"),
        ("5", "5%"),
        ("8", "8%"),
        ("10", "10%"),
    ]

    ma_hang_hoa = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã hàng hóa",
    )
    ten_hang_hoa = models.CharField(
        max_length=255,
        verbose_name="Tên hàng hóa",
    )
    don_vi_tinh = models.CharField(
        max_length=20,
        default="cái",
        verbose_name="Đơn vị tính",
    )
    gia_mua = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Giá mua",
    )
    gia_ban = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="Giá bán",
    )
    thue_suat_gtgt = models.CharField(
        max_length=2,
        choices=THUE_SUAT_GTGT_CHOICES,
        default="10",
        verbose_name="Thuế suất GTGT",
    )
    tk_doanh_thu = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="hang_hoa_doanh_thu",
        null=True,
        blank=True,
        verbose_name="TK doanh thu",
    )
    tk_gia_von = models.ForeignKey(
        TaiKhoanKeToan,
        on_delete=models.PROTECT,
        related_name="hang_hoa_gia_von",
        null=True,
        blank=True,
        verbose_name="TK giá vốn",
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
        ordering = ["ma_hang_hoa"]
        verbose_name = "Hàng hóa"
        verbose_name_plural = "Hàng hóa"

    def __str__(self):
        return f"{self.ma_hang_hoa} - {self.ten_hang_hoa}"
