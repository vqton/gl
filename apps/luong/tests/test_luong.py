"""Tests for M7: Lương & BHXH."""

from datetime import date
from decimal import Decimal

import pytest

from apps.luong.constants import (
    BHXT_NLD_BHXH,
    BHXT_NLD_BHTN,
    BHXT_NLD_BHYT,
    BHXT_TONG_NLD,
    GIAM_TRU_BAN_THAN,
    GIAM_TRU_PHU_THUOC,
    MAX_LUONG_BHXH,
    THUE_TNCN_BRACKETS,
)
from apps.luong.models import BangLuong, NhanVien
from apps.luong.services import (
    tao_bang_luong_thang,
    tach_toan_luong,
    tinh_bhxh_dn,
    tinh_bhxh_nld,
    tinh_thue_tncn,
)
from apps.nghiep_vu.models import ButToan


@pytest.fixture
def nhan_vien():
    """Create test employee."""
    return NhanVien.objects.create(
        ma_nhan_vien="NV001",
        ho_ten="Nguyễn Văn A",
        luong_co_ban=Decimal("10000000"),
        he_so_phu_cap=Decimal("0.2"),
        so_nguoi_phu_thuoc=2,
        trang_thai="dang_lam_viec",
        ngay_vao_lam=date(2025, 1, 1),
    )


@pytest.fixture
def nhan_vien_2():
    """Create second test employee."""
    return NhanVien.objects.create(
        ma_nhan_vien="NV002",
        ho_ten="Trần Thị B",
        luong_co_ban=Decimal("15000000"),
        he_so_phu_cap=Decimal("0.3"),
        so_nguoi_phu_thuoc=0,
        trang_thai="dang_lam_viec",
        ngay_vao_lam=date(2025, 6, 1),
    )


@pytest.fixture
def tai_khoan_334():
    """Create account 334."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="334",
        defaults={
            "ten_tai_khoan": "Phải trả NLĐ",
            "loai_tai_khoan": "3",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_111():
    """Create account 111."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={
            "ten_tai_khoan": "Tiền mặt",
            "loai_tai_khoan": "1",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_642():
    """Create account 642."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={
            "ten_tai_khoan": "Chi phí QLDN",
            "loai_tai_khoan": "6",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_3383():
    """Create account 3383."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="3383",
        defaults={
            "ten_tai_khoan": "BHXH phải nộp",
            "loai_tai_khoan": "3",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_3335():
    """Create account 3335."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="3335",
        defaults={
            "ten_tai_khoan": "Thuế TNCN phải nộp",
            "loai_tai_khoan": "3",
            "cap_do": 1,
        },
    )
    return tk


@pytest.mark.django_db
class TestTinhBHXH:
    """Test BHXH calculation functions."""

    def test_bhxh_nld_basic(self):
        """Test employee BHXH calculation."""
        result = tinh_bhxh_nld(Decimal("10000000"))
        assert result["bhxh"] == Decimal("800000")  # 8%
        assert result["bhyt"] == Decimal("150000")  # 1.5%
        assert result["bhtn"] == Decimal("100000")  # 1%
        assert result["tong"] == Decimal("1050000")  # 10.5%

    def test_bhxh_nld_capped(self):
        """Test BHXH capped at 20x base salary."""
        result = tinh_bhxh_nld(Decimal("100000000"))
        base = MAX_LUONG_BHXH
        assert result["bhxh"] == (base * BHXT_NLD_BHXH).quantize(Decimal("0.01"))
        assert result["tong"] == (base * BHXT_TONG_NLD).quantize(Decimal("0.01"))

    def test_bhxh_dn_basic(self):
        """Test employer BHXH calculation."""
        result = tinh_bhxh_dn(Decimal("10000000"))
        assert result["bhxh"] == Decimal("1750000")  # 17.5%
        assert result["bhyt"] == Decimal("300000")  # 3%
        assert result["bhtn"] == Decimal("100000")  # 1%
        assert result["bhtnld_bnn"] == Decimal("50000")  # 0.5%
        assert result["tong"] == Decimal("2200000")  # 22%


@pytest.mark.django_db
class TestTinhThueTNCN:
    """Test personal income tax calculation."""

    def test_no_tax_below_threshold(self):
        """Test no tax when income below deductions."""
        tax = tinh_thue_tncn(Decimal("0"))
        assert tax == Decimal("0")

    def test_tax_bracket_1(self):
        """Test tax for first bracket (5%)."""
        # Income after deductions: 3M
        tax = tinh_thue_tncn(Decimal("3000000"))
        assert tax == Decimal("150000")  # 3M * 5%

    def test_tax_bracket_2(self):
        """Test tax for second bracket (10%)."""
        # Income after deductions: 8M
        tax = tinh_thue_tncn(Decimal("8000000"))
        # 5M * 5% + 3M * 10% = 250K + 300K = 550K
        # Or using formula: 8M * 10% - 250K = 550K
        assert tax == Decimal("550000")

    def test_tax_bracket_3(self):
        """Test tax for third bracket (15%)."""
        tax = tinh_thue_tncn(Decimal("15000000"))
        # 15M * 15% - 750K = 1.5M
        assert tax == Decimal("1500000")

    def test_tax_bracket_7_top(self):
        """Test tax for highest bracket (35%)."""
        tax = tinh_thue_tncn(Decimal("100000000"))
        # 100M * 35% - 9.85M = 25.15M
        assert tax == Decimal("25150000")

    def test_tax_with_dependents(self):
        """Test full calculation with dependents."""
        luong = Decimal("20000000")
        bhxh = Decimal("2100000")  # 10.5%
        giam_tru = GIAM_TRU_BAN_THAN + GIAM_TRU_PHU_THUOC * 2
        # 20M - 2.1M - 19.8M = -1.9M → 0 tax
        thu_nhap = luong - bhxh - giam_tru
        tax = tinh_thue_tncn(max(thu_nhap, Decimal("0")))
        assert tax == Decimal("0")


@pytest.mark.django_db
class TestTaoBangLuongThang:
    """Test tao_bang_luong_thang function."""

    def test_generate_for_single_employee(self, nhan_vien):
        """Test generating payroll for one employee."""
        records = tao_bang_luong_thang(1, 2026)

        assert len(records) == 1
        rec = records[0]
        assert rec.nhan_vien.pk == nhan_vien.pk
        assert rec.luong_co_ban == Decimal("10000000")
        assert rec.phu_cap == Decimal("2000000")  # 20% of base
        assert rec.tong_thu_nhap == Decimal("12000000")

    def test_bhxh_calculations(self, nhan_vien):
        """Test BHXH calculations in payroll record."""
        records = tao_bang_luong_thang(1, 2026)
        rec = records[0]

        assert rec.bhxh_nld == Decimal("800000")  # 8%
        assert rec.bhyt_nld == Decimal("150000")  # 1.5%
        assert rec.bhtn_nld == Decimal("100000")  # 1%
        assert rec.tong_bhxh_nld == Decimal("1050000")

    def test_tax_calculation(self, nhan_vien):
        """Test TNCN tax in payroll record."""
        records = tao_bang_luong_thang(1, 2026)
        rec = records[0]

        # Income: 12M, BHXH: 1.05M, Deductions: 11M + 2*4.4M = 19.8M
        # Taxable: 12M - 1.05M - 19.8M = negative → 0
        assert rec.thue_tncn == Decimal("0")
        assert rec.thuc_linh == Decimal("10950000")  # 12M - 1.05M

    def test_generate_for_multiple_employees(self, nhan_vien, nhan_vien_2):
        """Test generating payroll for multiple employees."""
        records = tao_bang_luong_thang(1, 2026)

        assert len(records) == 2

    def test_no_duplicate_for_same_month(self, nhan_vien):
        """Test that duplicate records are not created."""
        tao_bang_luong_thang(1, 2026)
        records = tao_bang_luong_thang(1, 2026)

        assert len(records) == 1

    def test_filter_by_employee_ids(self, nhan_vien, nhan_vien_2):
        """Test generating payroll for specific employees."""
        records = tao_bang_luong_thang(1, 2026, [nhan_vien.pk])

        assert len(records) == 1
        assert records[0].nhan_vien.pk == nhan_vien.pk

    def test_skips_inactive_employees(self):
        """Test that inactive employees are skipped."""
        NhanVien.objects.create(
            ma_nhan_vien="NV_INACTIVE",
            ho_ten="Inactive",
            luong_co_ban=Decimal("10000000"),
            trang_thai="nghi_viec",
        )
        records = tao_bang_luong_thang(1, 2026)
        assert len(records) == 0

    def test_high_salary_tax(self, nhan_vien_2):
        """Test tax calculation for high salary employee."""
        records = tao_bang_luong_thang(1, 2026, [nhan_vien_2.pk])
        rec = records[0]

        # Income: 15M + 4.5M = 19.5M
        # BHXH: 10.5% of 15M = 1.575M
        # Deductions: 11M (no dependents)
        # Taxable: 19.5M - 1.575M - 11M = 6.925M
        # Tax: 6.925M * 10% - 250K = 442.5K
        assert rec.thue_tncn == Decimal("442500")
        assert rec.thuc_linh == Decimal("17482500")  # 19.5M - 1.575M - 442.5K


@pytest.mark.django_db
class TestTachToanLuong:
    """Test tach_toan_luong function."""

    def test_create_journal_entries(
        self,
        nhan_vien,
        tai_khoan_334,
        tai_khoan_111,
        tai_khoan_642,
        tai_khoan_3383,
        tai_khoan_3335,
    ):
        """Test creating payroll journal entries."""
        tao_bang_luong_thang(1, 2026)

        count = tach_toan_luong(1, 2026)
        assert count == 1

        # Check salary entry
        bt_luong = ButToan.objects.get(so_but_toan="BT-LUONG012026")
        assert bt_luong is not None

        # Check BHXH entry
        bt_bhxh = ButToan.objects.get(so_but_toan="BT-BHXH012026")
        assert bt_bhxh is not None

    def test_marks_records_as_hach_toan(
        self,
        nhan_vien,
        tai_khoan_334,
        tai_khoan_111,
        tai_khoan_642,
        tai_khoan_3383,
        tai_khoan_3335,
    ):
        """Test that records are marked as da_hach_toan."""
        tao_bang_luong_thang(1, 2026)
        tach_toan_luong(1, 2026)

        record = BangLuong.objects.get(nhan_vien=nhan_vien, thang=1, nam=2026)
        assert record.da_hach_toan is True

    def test_no_double_entry(
        self,
        nhan_vien,
        tai_khoan_334,
        tai_khoan_111,
        tai_khoan_642,
        tai_khoan_3383,
        tai_khoan_3335,
    ):
        """Test that running twice doesn't create duplicate entries."""
        tao_bang_luong_thang(1, 2026)
        tach_toan_luong(1, 2026)

        count = tach_toan_luong(1, 2026)
        assert count == 0

    def test_no_records_no_entry(
        self,
        tai_khoan_334,
        tai_khoan_111,
        tai_khoan_642,
        tai_khoan_3383,
        tai_khoan_3335,
    ):
        """Test that no records means no journal entry."""
        count = tach_toan_luong(1, 2026)
        assert count == 0
