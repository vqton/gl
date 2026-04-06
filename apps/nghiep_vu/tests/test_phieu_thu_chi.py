"""Tests for M4: Tiền tệ - Phiếu Thu / Phiếu Chi."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import KhachHang, NhaCungCap, TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet, PhieuChi, PhieuThu
from apps.nghiep_vu.services import tao_phieu_chi, tao_phieu_thu


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
        defaults={"ten_tai_khoan": "Phải trả người bán", "cap_do": 1},
    )[0]


@pytest.fixture
def tk_642():
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={"ten_tai_khoan": "Chi phí QLDN", "cap_do": 1},
    )[0]


@pytest.fixture
def khach_hang():
    return KhachHang.objects.create(
        ma_kh="KH_TEST",
        ten_kh="Khách hàng test",
    )


@pytest.fixture
def nha_cung_cap():
    return NhaCungCap.objects.create(
        ma_ncc="NCC_TEST",
        ten_ncc="Nhà cung cấp test",
    )


@pytest.mark.django_db
class TestPhieuThuModel:
    """Test PhieuThu model."""

    def test_create_phieu_thu(self, khach_hang, tk_111, tk_131):
        """Test basic PhieuThu creation."""
        phieu = PhieuThu.objects.create(
            so_chung_tu="PT001",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            dien_giai="Thu tiền khách hàng",
            so_tien=Decimal("10000000"),
            tk_no=tk_111,
            tk_co=tk_131,
            khach_hang=khach_hang,
        )
        assert phieu.so_chung_tu == "PT001"
        assert phieu.so_tien == Decimal("10000000")
        assert phieu.tk_no.ma_tai_khoan == "111"
        assert phieu.tk_co.ma_tai_khoan == "131"
        assert phieu.trang_thai == "draft"
        assert phieu.hinh_thuc_thanh_toan == "tien_mat"

    def test_phieu_thu_auto_vnd(self, khach_hang, tk_112, tk_131):
        """Test auto-calculation of VND amount."""
        phieu = PhieuThu.objects.create(
            so_chung_tu="PT002",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000"),
            ty_gia=Decimal("25000"),
            tk_no=tk_112,
            tk_co=tk_131,
            khach_hang=khach_hang,
            hinh_thuc_thanh_toan="chuyen_khoan",
        )
        assert phieu.so_tien_vnd == Decimal("25000000")

    def test_phieu_thu_default_ty_gia(self, tk_111, tk_131):
        """Test default exchange rate is 1."""
        phieu = PhieuThu.objects.create(
            so_chung_tu="PT003",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("5000000"),
            tk_no=tk_111,
            tk_co=tk_131,
        )
        assert phieu.ty_gia == Decimal("1")
        assert phieu.so_tien_vnd == Decimal("5000000")

    def test_phieu_thu_str(self, khach_hang, tk_111, tk_131):
        """Test PhieuThu string representation."""
        phieu = PhieuThu.objects.create(
            so_chung_tu="PT004",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("1000000"),
            tk_no=tk_111,
            tk_co=tk_131,
            khach_hang=khach_hang,
        )
        assert "PT004" in str(phieu)


@pytest.mark.django_db
class TestPhieuChiModel:
    """Test PhieuChi model."""

    def test_create_phieu_chi(self, nha_cung_cap, tk_331, tk_111):
        """Test basic PhieuChi creation."""
        phieu = PhieuChi.objects.create(
            so_chung_tu="PC001",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            dien_giai="Chi trả nhà cung cấp",
            so_tien=Decimal("20000000"),
            tk_no=tk_331,
            tk_co=tk_111,
            nha_cung_cap=nha_cung_cap,
        )
        assert phieu.so_chung_tu == "PC001"
        assert phieu.so_tien == Decimal("20000000")
        assert phieu.tk_no.ma_tai_khoan == "331"
        assert phieu.tk_co.ma_tai_khoan == "111"
        assert phieu.trang_thai == "draft"

    def test_phieu_chi_auto_vnd(self, nha_cung_cap, tk_331, tk_112):
        """Test auto-calculation of VND amount."""
        phieu = PhieuChi.objects.create(
            so_chung_tu="PC002",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("500"),
            ty_gia=Decimal("25500"),
            tk_no=tk_331,
            tk_co=tk_112,
            nha_cung_cap=nha_cung_cap,
            hinh_thuc_thanh_toan="chuyen_khoan",
        )
        assert phieu.so_tien_vnd == Decimal("12750000")


@pytest.mark.django_db
class TestTaoPhieuThu:
    """Test tao_phieu_thu service."""

    def test_create_phieu_thu_tien_mat(self, khach_hang, tk_111, tk_131):
        """Test cash receipt creation."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang,
            so_tien=Decimal("10000000"),
            tk_co="131",
            hinh_thuc_thanh_toan="tien_mat",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Thu tiền bán hàng",
        )

        assert phieu.so_chung_tu.startswith("PT")
        assert phieu.so_tien == Decimal("10000000")
        assert phieu.tk_no.ma_tai_khoan == "111"
        assert phieu.tk_co.ma_tai_khoan == "131"
        assert phieu.hinh_thuc_thanh_toan == "tien_mat"
        assert phieu.so_tien_vnd == Decimal("10000000")

    def test_create_phieu_thu_chuyen_khoan(self, khach_hang, tk_112, tk_131):
        """Test bank transfer receipt creation."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang,
            so_tien=Decimal("50000000"),
            tk_co="131",
            hinh_thuc_thanh_toan="chuyen_khoan",
            ngay_chung_tu=date(2026, 1, 15),
        )

        assert phieu.tk_no.ma_tai_khoan == "112"
        assert phieu.hinh_thuc_thanh_toan == "chuyen_khoan"

    def test_create_phieu_thu_foreign_currency(self, khach_hang, tk_111, tk_131):
        """Test receipt with foreign currency."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang,
            so_tien=Decimal("1000"),
            tk_co="131",
            ty_gia=Decimal("25000"),
            ngay_chung_tu=date(2026, 1, 15),
        )

        assert phieu.so_tien == Decimal("1000")
        assert phieu.so_tien_vnd == Decimal("25000000")

    def test_create_phieu_thu_auto_journal_entry(self, khach_hang, tk_111, tk_131):
        """Test that receipt auto-creates journal entry."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang,
            so_tien=Decimal("10000000"),
            tk_co="131",
            ngay_chung_tu=date(2026, 1, 15),
        )

        but_toan = ButToan.objects.get(so_but_toan=f"BT-{phieu.so_chung_tu}")
        assert but_toan is not None

        chi_tiet = list(but_toan.chi_tiet.all())
        assert len(chi_tiet) == 2

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")

        assert no_line.tai_khoan.ma_tai_khoan == "111"
        assert co_line.tai_khoan.ma_tai_khoan == "131"
        assert no_line.so_tien == Decimal("10000000")
        assert co_line.so_tien == Decimal("10000000")

    def test_create_phieu_thu_zero_amount_raises_error(self, khach_hang):
        """Test zero amount raises ValidationError."""
        with pytest.raises(ValidationError, match="lớn hơn 0"):
            tao_phieu_thu(
                khach_hang=khach_hang,
                so_tien=Decimal("0"),
                tk_co="131",
                ngay_chung_tu=date(2026, 1, 15),
            )

    def test_create_phieu_thu_negative_amount_raises_error(self, khach_hang):
        """Test negative amount raises ValidationError."""
        with pytest.raises(ValidationError, match="lớn hơn 0"):
            tao_phieu_thu(
                khach_hang=khach_hang,
                so_tien=Decimal("-1000000"),
                tk_co="131",
                ngay_chung_tu=date(2026, 1, 15),
            )

    def test_create_phieu_thu_custom_so_chung_tu(self, khach_hang, tk_111, tk_131):
        """Test custom voucher number."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang,
            so_tien=Decimal("1000000"),
            tk_co="131",
            ngay_chung_tu=date(2026, 1, 15),
            so_chung_tu="PT-CUSTOM-001",
        )
        assert phieu.so_chung_tu == "PT-CUSTOM-001"

    def test_create_phieu_thu_without_customer(self, tk_111):
        """Test receipt without customer (e.g., other income)."""
        phieu = tao_phieu_thu(
            so_tien=Decimal("5000000"),
            tk_co="711",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Thu khác",
        )
        assert phieu.khach_hang is None
        assert phieu.tk_co.ma_tai_khoan == "711"


@pytest.mark.django_db
class TestTaoPhieuChi:
    """Test tao_phieu_chi service."""

    def test_create_phieu_chi_tien_mat(self, nha_cung_cap, tk_331, tk_111):
        """Test cash payment creation."""
        phieu = tao_phieu_chi(
            nha_cung_cap=nha_cung_cap,
            so_tien=Decimal("20000000"),
            tk_no="331",
            hinh_thuc_thanh_toan="tien_mat",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Chi trả nhà cung cấp",
        )

        assert phieu.so_chung_tu.startswith("PC")
        assert phieu.so_tien == Decimal("20000000")
        assert phieu.tk_no.ma_tai_khoan == "331"
        assert phieu.tk_co.ma_tai_khoan == "111"
        assert phieu.hinh_thuc_thanh_toan == "tien_mat"

    def test_create_phieu_chi_chuyen_khoan(self, nha_cung_cap, tk_331, tk_112):
        """Test bank transfer payment creation."""
        phieu = tao_phieu_chi(
            nha_cung_cap=nha_cung_cap,
            so_tien=Decimal("50000000"),
            tk_no="331",
            hinh_thuc_thanh_toan="chuyen_khoan",
            ngay_chung_tu=date(2026, 1, 15),
        )

        assert phieu.tk_co.ma_tai_khoan == "112"
        assert phieu.hinh_thuc_thanh_toan == "chuyen_khoan"

    def test_create_phieu_chi_auto_journal_entry(self, nha_cung_cap, tk_331, tk_111):
        """Test that payment auto-creates journal entry."""
        phieu = tao_phieu_chi(
            nha_cung_cap=nha_cung_cap,
            so_tien=Decimal("20000000"),
            tk_no="331",
            ngay_chung_tu=date(2026, 1, 15),
        )

        but_toan = ButToan.objects.get(so_but_toan=f"BT-{phieu.so_chung_tu}")
        assert but_toan is not None

        chi_tiet = list(but_toan.chi_tiet.all())
        assert len(chi_tiet) == 2

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")

        assert no_line.tai_khoan.ma_tai_khoan == "331"
        assert co_line.tai_khoan.ma_tai_khoan == "111"
        assert no_line.so_tien == Decimal("20000000")
        assert co_line.so_tien == Decimal("20000000")

    def test_create_phieu_chi_zero_amount_raises_error(self, nha_cung_cap):
        """Test zero amount raises ValidationError."""
        with pytest.raises(ValidationError, match="lớn hơn 0"):
            tao_phieu_chi(
                nha_cung_cap=nha_cung_cap,
                so_tien=Decimal("0"),
                tk_no="331",
                ngay_chung_tu=date(2026, 1, 15),
            )

    def test_create_phieu_chi_negative_amount_raises_error(self, nha_cung_cap):
        """Test negative amount raises ValidationError."""
        with pytest.raises(ValidationError, match="lớn hơn 0"):
            tao_phieu_chi(
                nha_cung_cap=nha_cung_cap,
                so_tien=Decimal("-5000000"),
                tk_no="331",
                ngay_chung_tu=date(2026, 1, 15),
            )

    def test_create_phieu_chi_without_supplier(self, tk_111):
        """Test payment without supplier (e.g., expense)."""
        phieu = tao_phieu_chi(
            so_tien=Decimal("2000000"),
            tk_no="642",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Chi phí quản lý",
        )
        assert phieu.nha_cung_cap is None
        assert phieu.tk_no.ma_tai_khoan == "642"

    def test_create_phieu_chi_custom_so_chung_tu(self, nha_cung_cap, tk_331, tk_111):
        """Test custom voucher number."""
        phieu = tao_phieu_chi(
            nha_cung_cap=nha_cung_cap,
            so_tien=Decimal("1000000"),
            tk_no="331",
            ngay_chung_tu=date(2026, 1, 15),
            so_chung_tu="PC-CUSTOM-001",
        )
        assert phieu.so_chung_tu == "PC-CUSTOM-001"
