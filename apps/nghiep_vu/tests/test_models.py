"""Tests for nghiep_vu models."""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.danh_muc.models import (
    HangHoa,
    KhachHang,
    NganHang,
    NhaCungCap,
    TaiKhoanKeToan,
    TaiKhoanNganHang,
)
from apps.he_thong.models import KyKeToan
from apps.nghiep_vu.models import (
    ButToan,
    ButToanChiTiet,
    HoaDon,
    HoaDonChiTiet,
    Kho,
    NhapKho,
    NhapKhoChiTiet,
    PhieuChi,
    PhieuThu,
    XuatKho,
    XuatKhoChiTiet,
)


@pytest.fixture
def ky_ke_toan_2026():
    return KyKeToan.objects.get_or_create(
        nam=2026,
        defaults={
            "ngay_bat_dau": date(2026, 1, 1),
            "ngay_ket_thuc": date(2026, 12, 31),
            "trang_thai": "open",
        },
    )[0]


@pytest.fixture
def tk_111():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={
            "ten_tai_khoan": "Tiền mặt",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )[0]


@pytest.fixture
def tk_112():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="112",
        defaults={
            "ten_tai_khoan": "Tiền gửi ngân hàng",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )[0]


@pytest.fixture
def tk_131():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={
            "ten_tai_khoan": "Phải thu của khách hàng",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )[0]


@pytest.fixture
def tk_331():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={
            "ten_tai_khoan": "Phải trả người bán",
            "cap_do": 1,
        },
    )[0]


@pytest.fixture
def tk_511():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="511",
        defaults={
            "ten_tai_khoan": "Doanh thu bán hàng",
            "cap_do": 1,
            "loai_tai_khoan": "doanh_thu",
        },
    )[0]


@pytest.fixture
def tk_642():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={
            "ten_tai_khoan": "Chi phí QLDN",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )[0]


@pytest.fixture
def tk_711():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="711",
        defaults={
            "ten_tai_khoan": "Thu nhập khác",
            "cap_do": 1,
            "loai_tai_khoan": "thu_nhap_khac",
        },
    )[0]


@pytest.fixture
def tk_811():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="811",
        defaults={
            "ten_tai_khoan": "Chi phí khác",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi_khac",
        },
    )[0]


@pytest.fixture
def tk_632():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="632",
        defaults={
            "ten_tai_khoan": "Giá vốn hàng bán",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )[0]


@pytest.fixture
def khach_hang():
    return KhachHang.objects.create(
        ma_kh="KH001",
        ten_kh="Customer A",
    )


@pytest.fixture
def hang_hoa():
    return HangHoa.objects.create(
        ma_hang_hoa="HH001",
        ten_hang_hoa="Product A",
    )


@pytest.mark.django_db
class TestHoaDon:
    """Tests for HoaDon model."""

    def test_create_hoa_don(self, khach_hang):
        """Test creating an invoice."""
        hd = HoaDon.objects.create(
            so_hoa_don="HD001",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            tong_tien_truoc_thue=Decimal("1000000"),
            tien_thue_gtgt=Decimal("100000"),
            tong_cong_thanh_toan=Decimal("1100000"),
        )
        assert hd.so_hoa_don == "HD001"
        assert hd.trang_thai == "draft"
        assert hd.hinh_thuc_thanh_toan == "tien_mat"

    def test_string_representation(self, khach_hang):
        """Test string representation."""
        hd = HoaDon(
            so_hoa_don="HD001",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
        )
        assert str(hd) == "HD001 - KH001 - Customer A"

    def test_unique_so_hoa_don(self, khach_hang):
        """Test that invoice numbers must be unique."""
        HoaDon.objects.create(
            so_hoa_don="HD001",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
        )
        with pytest.raises(Exception):
            HoaDon.objects.create(
                so_hoa_don="HD001",
                ngay_hoa_don=date(2026, 1, 16),
                khach_hang=khach_hang,
            )

    def test_cancelled_status(self, khach_hang):
        """Test cancelled status."""
        hd = HoaDon.objects.create(
            so_hoa_don="HD002",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            trang_thai="cancelled",
        )
        assert hd.trang_thai == "cancelled"

    def test_new_fields_exist(self, khach_hang):
        """Test new fields quy_so, ma_hang_hoa_gtgt, loai_hang_hoa."""
        hd = HoaDon.objects.create(
            so_hoa_don="HD003",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            quy_so="AA/26E",
            ma_hang_hoa_gtgt="HH-GTGT-001",
            loai_hang_hoa="hang_hoa_thong_thuong",
        )
        assert hd.quy_so == "AA/26E"
        assert hd.ma_hang_hoa_gtgt == "HH-GTGT-001"
        assert hd.loai_hang_hoa == "hang_hoa_thong_thuong"

    def test_auto_numbering_so_hoa_don(self, khach_hang):
        """Test auto-generation of so_hoa_don when not provided."""
        hd = HoaDon(
            ngay_hoa_don=date(2026, 3, 15),
            khach_hang=khach_hang,
        )
        hd.save()
        assert hd.so_hoa_don == "HD-20260315-0001"

    def test_auto_numbering_sequence(self, khach_hang):
        """Test auto-numbering increments for same date."""
        HoaDon.objects.create(
            so_hoa_don="HD-20260315-0001",
            ngay_hoa_don=date(2026, 3, 15),
            khach_hang=khach_hang,
        )
        hd2 = HoaDon(
            ngay_hoa_don=date(2026, 3, 15),
            khach_hang=khach_hang,
        )
        hd2.save()
        assert hd2.so_hoa_don == "HD-20260315-0002"

    def test_ky_hieu_valid(self, khach_hang):
        """Test valid ky_hieu passes validation."""
        hd = HoaDon(
            so_hoa_don="HD004",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="AA/26E",
        )
        hd.full_clean()

    def test_ky_hieu_invalid_format(self, khach_hang):
        """Test invalid ky_hieu raises ValidationError."""
        hd = HoaDon(
            so_hoa_don="HD005",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="INVALID",
        )
        with pytest.raises(ValidationError):
            hd.full_clean()

    def test_ky_hieu_invalid_pattern_1(self, khach_hang):
        """Test ky_hieu with wrong pattern A/26E."""
        hd = HoaDon(
            so_hoa_don="HD006",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="A/26E",
        )
        with pytest.raises(ValidationError):
            hd.full_clean()

    def test_ky_hieu_invalid_pattern_2(self, khach_hang):
        """Test ky_hieu with wrong pattern AA/2026E."""
        hd = HoaDon(
            so_hoa_don="HD007",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="AA/2026E",
        )
        with pytest.raises(ValidationError):
            hd.full_clean()

    def test_ky_hieu_invalid_pattern_3(self, khach_hang):
        """Test ky_hieu with wrong pattern AA/26."""
        hd = HoaDon(
            so_hoa_don="HD008",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="AA/26",
        )
        with pytest.raises(ValidationError):
            hd.full_clean()

    def test_ky_hieu_empty_allowed(self, khach_hang):
        """Test empty ky_hieu is allowed."""
        hd = HoaDon(
            so_hoa_don="HD009",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            ky_hieu="",
        )
        hd.full_clean()


@pytest.mark.django_db
class TestHoaDonChiTiet:
    """Tests for HoaDonChiTiet model."""

    def _create_invoice(self, khach_hang):
        return HoaDon.objects.create(
            so_hoa_don="HD001",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
        )

    def test_create_line_item(self, khach_hang, hang_hoa):
        """Test creating an invoice line item."""
        hd = self._create_invoice(khach_hang)
        ct = HoaDonChiTiet.objects.create(
            hoa_don=hd,
            hang_hoa=hang_hoa,
            so_luong=Decimal("10"),
            don_gia=Decimal("100000"),
            thue_suat=Decimal("10"),
            tien_thue=Decimal("100000"),
            tong_tien=Decimal("1100000"),
        )
        assert ct.so_luong == Decimal("10")
        assert ct.tong_tien == Decimal("1100000")
        assert ct.thue_suat == Decimal("10")

    def test_thue_suat_is_decimal(self, khach_hang, hang_hoa):
        """Test thue_suat is DecimalField, not CharField."""
        hd = self._create_invoice(khach_hang)
        ct = HoaDonChiTiet.objects.create(
            hoa_don=hd,
            hang_hoa=hang_hoa,
            so_luong=Decimal("1"),
            don_gia=Decimal("100000"),
            thue_suat=Decimal("8"),
            tien_thue=Decimal("8000"),
            tong_tien=Decimal("108000"),
        )
        assert isinstance(ct.thue_suat, Decimal)
        assert ct.thue_suat == Decimal("8")

    def test_thue_suat_choices(self, khach_hang, hang_hoa):
        """Test thue_suat accepts valid choices."""
        hd = self._create_invoice(khach_hang)
        for rate in [Decimal("0"), Decimal("5"), Decimal("8"), Decimal("10")]:
            ct = HoaDonChiTiet(
                hoa_don=hd,
                hang_hoa=hang_hoa,
                so_luong=Decimal("1"),
                don_gia=Decimal("100000"),
                thue_suat=rate,
                tien_thue=Decimal("0"),
                tong_tien=Decimal("100000"),
            )
            ct.full_clean()

    def test_string_representation(self, khach_hang, hang_hoa):
        """Test string representation."""
        hd = self._create_invoice(khach_hang)
        ct = HoaDonChiTiet(
            hoa_don=hd,
            hang_hoa=hang_hoa,
            so_luong=Decimal("10"),
            don_gia=Decimal("100000"),
            thue_suat=Decimal("10"),
            tien_thue=Decimal("100000"),
            tong_tien=Decimal("1100000"),
        )
        assert "HD001" in str(ct)
        assert "HH001" in str(ct)


@pytest.mark.django_db
class TestButToan:
    """Tests for ButToan model."""

    def _create_user(self):
        from apps.users.models import NguoiDung

        return NguoiDung.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_create_but_toan(self):
        """Test creating a journal entry."""
        user = self._create_user()
        bt = ButToan.objects.create(
            so_but_toan="BT001",
            ngay_hach_toan=date(2026, 1, 15),
            dien_giai="Test entry",
            nguoi_tao=user,
        )
        assert bt.so_but_toan == "BT001"
        assert bt.trang_thai == "draft"
        assert bt.nguoi_tao == user

    def test_string_representation(self):
        """Test string representation."""
        bt = ButToan(
            so_but_toan="BT001",
            ngay_hach_toan=date(2026, 1, 15),
        )
        assert str(bt) == "BT001 - 2026-01-15"

    def test_unique_so_but_toan(self):
        """Test that voucher numbers must be unique."""
        ButToan.objects.create(
            so_but_toan="BT001",
            ngay_hach_toan=date(2026, 1, 15),
        )
        with pytest.raises(Exception):
            ButToan.objects.create(
                so_but_toan="BT001",
                ngay_hach_toan=date(2026, 1, 16),
            )

    def test_posted_status(self):
        """Test posted status."""
        bt = ButToan.objects.create(
            so_but_toan="BT002",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="posted",
        )
        assert bt.trang_thai == "posted"

    def test_ngay_dua_vao_su_dung_field(self):
        """Test ngay_dua_vao_su_dung field exists."""
        bt = ButToan.objects.create(
            so_but_toan="BT003",
            ngay_hach_toan=date(2026, 1, 15),
            ngay_dua_vao_su_dung=date(2026, 1, 1),
        )
        assert bt.ngay_dua_vao_su_dung == date(2026, 1, 1)

    def test_ngay_dua_vao_su_dung_nullable(self):
        """Test ngay_dua_vao_su_dung can be null."""
        bt = ButToan.objects.create(
            so_but_toan="BT004",
            ngay_hach_toan=date(2026, 1, 15),
            ngay_dua_vao_su_dung=None,
        )
        assert bt.ngay_dua_vao_su_dung is None

    def test_clean_balanced_posted(self, tk_111, tk_131, ky_ke_toan_2026):
        """Test posted but_toan with balanced Nợ/Có passes."""
        bt = ButToan.objects.create(
            so_but_toan="BT005",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="posted",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        bt.full_clean()

    def test_clean_no_details_posted_raises(self, ky_ke_toan_2026):
        """Test posted but_toan with no details raises error."""
        bt = ButToan.objects.create(
            so_but_toan="BT006",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="posted",
        )
        with pytest.raises(ValidationError, match="ít nhất một chi tiết"):
            bt.full_clean()

    def test_clean_unbalanced_posted_raises(self, tk_111, tk_131, ky_ke_toan_2026):
        """Test posted but_toan with unbalanced Nợ/Có raises error."""
        bt = ButToan.objects.create(
            so_but_toan="BT007",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="posted",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("500000"),
        )
        with pytest.raises(ValidationError, match="không bằng"):
            bt.full_clean()

    def test_clean_balanced_posted_ok(self, tk_111, tk_131, ky_ke_toan_2026):
        """Test posted but_toan with balanced Nợ/Có passes clean."""
        bt = ButToan.objects.create(
            so_but_toan="BT008",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="posted",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        bt.full_clean()

    def test_clean_draft_no_validation(self, tk_111, tk_131, ky_ke_toan_2026):
        """Test draft but_toan skips balance validation."""
        bt = ButToan.objects.create(
            so_but_toan="BT009",
            ngay_hach_toan=date(2026, 1, 15),
            trang_thai="draft",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("500000"),
        )
        bt.full_clean()


@pytest.mark.django_db
class TestButToanChiTiet:
    """Tests for ButToanChiTiet model."""

    def test_create_line_item(self, tk_111):
        """Test creating a journal entry line."""
        bt = ButToan.objects.create(
            so_but_toan="BT001",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        assert ct.loai_no_co == "no"
        assert ct.so_tien == Decimal("1000000")

    def test_string_representation(self, tk_111):
        """Test string representation."""
        bt = ButToan(
            so_but_toan="BT001",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        assert "111" in str(ct)
        assert "no" in str(ct)

    def test_so_chung_tu_goc_field(self, tk_111):
        """Test so_chung_tu_goc field exists and works."""
        bt = ButToan.objects.create(
            so_but_toan="BT010",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
            so_chung_tu_goc="PT-20260115-0001",
        )
        assert ct.so_chung_tu_goc == "PT-20260115-0001"

    def test_so_chung_tu_goc_blank(self, tk_111):
        """Test so_chung_tu_goc can be blank."""
        bt = ButToan.objects.create(
            so_but_toan="BT011",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
            so_chung_tu_goc="",
        )
        assert ct.so_chung_tu_goc == ""

    def test_asset_account_no_allowed(self, tk_111):
        """Test asset account (1xx) can be ghi Nợ."""
        bt = ButToan.objects.create(
            so_but_toan="BT012",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ct.full_clean()

    def test_asset_account_co_allowed(self, tk_111):
        """Test asset account (1xx) can be ghi Có."""
        bt = ButToan.objects.create(
            so_but_toan="BT013",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        ct.full_clean()

    def test_revenue_account_no_raises(self, tk_511):
        """Test revenue account (5xx) cannot be ghi Nợ."""
        bt = ButToan.objects.create(
            so_but_toan="BT014",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_511,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        with pytest.raises(ValidationError, match="không thể ghi Nợ"):
            ct.full_clean()

    def test_revenue_account_co_allowed(self, tk_511):
        """Test revenue account (5xx) can be ghi Có."""
        bt = ButToan.objects.create(
            so_but_toan="BT015",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_511,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        ct.full_clean()

    def test_expense_account_no_allowed(self, tk_642):
        """Test expense account (6xx) can be ghi Nợ."""
        bt = ButToan.objects.create(
            so_but_toan="BT016",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_642,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ct.full_clean()

    def test_expense_account_co_raises(self, tk_642):
        """Test expense account (6xx) cannot be ghi Có."""
        bt = ButToan.objects.create(
            so_but_toan="BT017",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_642,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        with pytest.raises(ValidationError, match="không thể ghi Có"):
            ct.full_clean()

    def test_other_income_no_raises(self, tk_711):
        """Test other income account (7xx) cannot be ghi Nợ."""
        bt = ButToan.objects.create(
            so_but_toan="BT018",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_711,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        with pytest.raises(ValidationError, match="không thể ghi Nợ"):
            ct.full_clean()

    def test_other_expense_no_allowed(self, tk_811):
        """Test other expense account (8xx) can be ghi Nợ."""
        bt = ButToan.objects.create(
            so_but_toan="BT019",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_811,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ct.full_clean()

    def test_other_expense_co_raises(self, tk_811):
        """Test other expense account (8xx) cannot be ghi Có."""
        bt = ButToan.objects.create(
            so_but_toan="BT020",
            ngay_hach_toan=date(2026, 1, 15),
        )
        ct = ButToanChiTiet(
            but_toan=bt,
            tai_khoan=tk_811,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        with pytest.raises(ValidationError, match="không thể ghi Có"):
            ct.full_clean()


@pytest.mark.django_db
class TestPhieuThuForeignKey:
    """Test PhieuThu tk_no/tk_co as ForeignKey."""

    def test_phieu_thu_tk_no_foreign_key(self, tk_111, tk_131):
        """Test tk_no is ForeignKey to TaiKhoanKeToan."""
        pt = PhieuThu.objects.create(
            so_chung_tu="PT010",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_111,
            tk_co=tk_131,
        )
        assert isinstance(pt.tk_no, TaiKhoanKeToan)
        assert pt.tk_no.ma_tai_khoan == "111"

    def test_phieu_thu_tk_co_foreign_key(self, tk_111, tk_131):
        """Test tk_co is ForeignKey to TaiKhoanKeToan."""
        pt = PhieuThu.objects.create(
            so_chung_tu="PT011",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_111,
            tk_co=tk_131,
        )
        assert isinstance(pt.tk_co, TaiKhoanKeToan)
        assert pt.tk_co.ma_tai_khoan == "131"

    def test_phieu_thu_tk_no_must_be_111_or_112(self, tk_131, tk_331):
        """Test tk_no must be 111 or 112."""
        pt = PhieuThu(
            so_chung_tu="PT012",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_131,
        )
        with pytest.raises(ValidationError, match="111 hoặc 112"):
            pt.full_clean()

    def test_phieu_thu_tk_no_111_valid(self, tk_111, tk_131):
        """Test tk_no=111 is valid."""
        pt = PhieuThu(
            so_chung_tu="PT013",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_111,
            tk_co=tk_131,
        )
        pt.full_clean()

    def test_phieu_thu_tk_no_112_valid(self, tk_112, tk_131):
        """Test tk_no=112 is valid."""
        pt = PhieuThu(
            so_chung_tu="PT014",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_112,
            tk_co=tk_131,
        )
        pt.full_clean()


@pytest.mark.django_db
class TestPhieuChiForeignKey:
    """Test PhieuChi tk_no/tk_co as ForeignKey."""

    def test_phieu_chi_tk_no_foreign_key(self, tk_331, tk_111):
        """Test tk_no is ForeignKey to TaiKhoanKeToan."""
        pc = PhieuChi.objects.create(
            so_chung_tu="PC010",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_111,
        )
        assert isinstance(pc.tk_no, TaiKhoanKeToan)
        assert pc.tk_no.ma_tai_khoan == "331"

    def test_phieu_chi_tk_co_foreign_key(self, tk_331, tk_111):
        """Test tk_co is ForeignKey to TaiKhoanKeToan."""
        pc = PhieuChi.objects.create(
            so_chung_tu="PC011",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_111,
        )
        assert isinstance(pc.tk_co, TaiKhoanKeToan)
        assert pc.tk_co.ma_tai_khoan == "111"

    def test_phieu_chi_tk_co_must_be_111_or_112(self, tk_331, tk_131):
        """Test tk_co must be 111 or 112."""
        pc = PhieuChi(
            so_chung_tu="PC012",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_131,
        )
        with pytest.raises(ValidationError, match="111 hoặc 112"):
            pc.full_clean()

    def test_phieu_chi_tk_co_111_valid(self, tk_331, tk_111):
        """Test tk_co=111 is valid."""
        pc = PhieuChi(
            so_chung_tu="PC013",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_111,
        )
        pc.full_clean()

    def test_phieu_chi_tk_co_112_valid(self, tk_331, tk_112):
        """Test tk_co=112 is valid."""
        pc = PhieuChi(
            so_chung_tu="PC014",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("1000000"),
            tk_no=tk_331,
            tk_co=tk_112,
        )
        pc.full_clean()


@pytest.mark.django_db
class TestKho:
    """Tests for Kho model."""

    def test_create_kho(self):
        """Test creating a warehouse."""
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
            dia_chi="Hà Nội",
            nguoi_phu_trach="Nguyễn Văn A",
        )
        assert kho.ma_kho == "KHO001"
        assert kho.is_active is True

    def test_string_representation(self):
        """Test string representation."""
        kho = Kho(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        assert str(kho) == "KHO001 - Kho chính"

    def test_unique_ma_kho(self):
        """Test that warehouse codes must be unique."""
        Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Warehouse A",
        )
        with pytest.raises(Exception):
            Kho.objects.create(
                ma_kho="KHO001",
                ten_kho="Warehouse B",
            )


@pytest.mark.django_db
class TestNhapKho:
    """Tests for NhapKho model."""

    def _create_nha_cung_cap(self):
        return NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Supplier A",
        )

    def _create_kho(self):
        return Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )

    def test_create_nhap_kho(self):
        """Test creating a goods receipt."""
        ncc = self._create_nha_cung_cap()
        kho = self._create_kho()
        nk = NhapKho.objects.create(
            so_chung_tu="NK001",
            ngay=date(2026, 1, 15),
            kho=kho,
            nha_cung_cap=ncc,
            tong_tien=Decimal("10000000"),
        )
        assert nk.so_chung_tu == "NK001"
        assert nk.trang_thai == "draft"

    def test_string_representation(self):
        """Test string representation."""
        kho = self._create_kho()
        ncc = self._create_nha_cung_cap()
        nk = NhapKho(
            so_chung_tu="NK001",
            ngay=date(2026, 1, 15),
            kho=kho,
            nha_cung_cap=ncc,
        )
        assert str(nk) == "NK001 - KHO001 - Kho chính"

    def test_completed_status(self):
        """Test completed status."""
        ncc = self._create_nha_cung_cap()
        kho = self._create_kho()
        nk = NhapKho.objects.create(
            so_chung_tu="NK002",
            ngay=date(2026, 1, 15),
            kho=kho,
            nha_cung_cap=ncc,
            trang_thai="completed",
        )
        assert nk.trang_thai == "completed"


@pytest.mark.django_db
class TestNhapKhoChiTiet:
    """Tests for NhapKhoChiTiet model."""

    def _create_nhap_kho(self):
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Supplier A",
        )
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        return NhapKho.objects.create(
            so_chung_tu="NK001",
            ngay=date(2026, 1, 15),
            kho=kho,
            nha_cung_cap=ncc,
        )

    def _create_hang_hoa(self):
        return HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
        )

    def test_create_line_item(self):
        """Test creating a goods receipt line."""
        nk = self._create_nhap_kho()
        hh = self._create_hang_hoa()
        ct = NhapKhoChiTiet.objects.create(
            nhap_kho=nk,
            hang_hoa=hh,
            so_luong=Decimal("100"),
            don_gia=Decimal("50000"),
            thanh_tien=Decimal("5000000"),
        )
        assert ct.so_luong == Decimal("100")
        assert ct.thanh_tien == Decimal("5000000")


@pytest.mark.django_db
class TestXuatKho:
    """Tests for XuatKho model."""

    def _create_kho(self):
        return Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )

    def _create_khach_hang(self):
        return KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )

    def test_create_xuat_kho(self):
        """Test creating a goods issue."""
        kho = self._create_kho()
        kh = self._create_khach_hang()
        xk = XuatKho.objects.create(
            so_chung_tu="XK001",
            ngay=date(2026, 1, 15),
            kho=kho,
            khach_hang=kh,
            tong_tien=Decimal("5000000"),
        )
        assert xk.so_chung_tu == "XK001"
        assert xk.trang_thai == "draft"

    def test_string_representation(self):
        """Test string representation."""
        kho = self._create_kho()
        xk = XuatKho(
            so_chung_tu="XK001",
            ngay=date(2026, 1, 15),
            kho=kho,
        )
        assert str(xk) == "XK001 - KHO001 - Kho chính"

    def test_without_customer(self):
        """Test goods issue without customer."""
        kho = self._create_kho()
        xk = XuatKho.objects.create(
            so_chung_tu="XK002",
            ngay=date(2026, 1, 15),
            kho=kho,
            khach_hang=None,
        )
        assert xk.khach_hang is None


@pytest.mark.django_db
class TestXuatKhoChiTiet:
    """Tests for XuatKhoChiTiet model."""

    def _create_xuat_kho(self):
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        return XuatKho.objects.create(
            so_chung_tu="XK001",
            ngay=date(2026, 1, 15),
            kho=kho,
        )

    def _create_hang_hoa(self):
        return HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
        )

    def test_create_line_item(self):
        """Test creating a goods issue line."""
        xk = self._create_xuat_kho()
        hh = self._create_hang_hoa()
        ct = XuatKhoChiTiet.objects.create(
            xuat_kho=xk,
            hang_hoa=hh,
            so_luong=Decimal("50"),
            don_gia=Decimal("100000"),
            thanh_tien=Decimal("5000000"),
        )
        assert ct.so_luong == Decimal("50")
        assert ct.thanh_tien == Decimal("5000000")
