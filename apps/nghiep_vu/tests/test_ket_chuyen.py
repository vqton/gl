"""Tests for year-end closing (Kết chuyển TK 911)."""

from datetime import date
from decimal import Decimal

import pytest

from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.ket_chuyen import (
    CHI_PHI_ACCOUNTS,
    DOANH_THU_ACCOUNTS,
    get_tong_phatsinh,
    ket_chuyen_cuoi_ky,
)
from apps.nghiep_vu.models import ButToan, ButToanChiTiet
from apps.nghiep_vu.services import tao_but_toan


@pytest.fixture
def accounts_2026():
    """Create all accounts needed for closing."""
    account_map = {
        "111": "Tiền mặt",
        "3331": "Thuế GTGT phải nộp",
        "511": "Doanh thu bán hàng",
        "515": "Doanh thu tài chính",
        "711": "Thu nhập khác",
        "632": "Giá vốn hàng bán",
        "641": "Chi phí bán hàng",
        "642": "Chi phí QLDN",
        "635": "Chi phí tài chính",
        "811": "Chi phí khác",
        "911": "Xác định KQKD",
        "421": "Lợi nhuận chưa phân phối",
    }
    created = {}
    for code, name in account_map.items():
        loai = "1" if code.startswith(("1", "5", "6", "7", "8")) else "3"
        tk, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan=code,
            defaults={
                "ten_tai_khoan": name,
                "loai_tai_khoan": loai,
                "cap_do": 1,
            },
        )
        created[code] = tk
    return created


@pytest.fixture
def sample_journal_entries(accounts_2026):
    """Create sample journal entries with revenue and expense."""
    # Revenue entry
    tao_but_toan(
        ngay=date(2025, 6, 30),
        dien_giai="Doanh thu 6 tháng",
        chi_tiet=[
            {
                "tai_khoan": "111",
                "loai_no_co": "no",
                "so_tien": Decimal("110000000"),
                "dien_giai": "Thu tiền",
            },
            {
                "tai_khoan": "511",
                "loai_no_co": "co",
                "so_tien": Decimal("100000000"),
                "dien_giai": "Doanh thu",
            },
            {
                "tai_khoan": "3331",
                "loai_no_co": "co",
                "so_tien": Decimal("10000000"),
                "dien_giai": "Thuế",
            },
        ],
        so_but_toan="BT-REV-2025",
    )
    # Expense entry
    tao_but_toan(
        ngay=date(2025, 6, 30),
        dien_giai="Chi phí 6 tháng",
        chi_tiet=[
            {
                "tai_khoan": "632",
                "loai_no_co": "no",
                "so_tien": Decimal("60000000"),
                "dien_giai": "Giá vốn",
            },
            {
                "tai_khoan": "642",
                "loai_no_co": "no",
                "so_tien": Decimal("20000000"),
                "dien_giai": "Chi phí",
            },
            {
                "tai_khoan": "111",
                "loai_no_co": "co",
                "so_tien": Decimal("80000000"),
                "dien_giai": "Chi tiền",
            },
        ],
        so_but_toan="BT-EXP-2025",
    )


@pytest.mark.django_db
class TestGetTongPhatsinh:
    """Test get_tong_phatsinh function."""

    def test_revenue_account_balance(self, accounts_2026, sample_journal_entries):
        """Test revenue account has credit balance."""
        no, co = get_tong_phatsinh("511", date(2025, 1, 1), date(2025, 12, 31))
        assert co == Decimal("100000000")
        assert no == Decimal("0")

    def test_expense_account_balance(self, accounts_2026, sample_journal_entries):
        """Test expense account has debit balance."""
        no, co = get_tong_phatsinh("632", date(2025, 1, 1), date(2025, 12, 31))
        assert no == Decimal("60000000")
        assert co == Decimal("0")

    def test_empty_period(self, accounts_2026):
        """Test account with no entries."""
        no, co = get_tong_phatsinh("511", date(2025, 1, 1), date(2025, 12, 31))
        assert no == Decimal("0")
        assert co == Decimal("0")


@pytest.mark.django_db
class TestKetChuyenCuoiKy:
    """Test ket_chuyen_cuoi_ky function."""

    def test_closing_creates_entries(self, accounts_2026, sample_journal_entries):
        """Test closing creates journal entries."""
        result = ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        assert result["doanh_thu"] == Decimal("100000000")
        assert result["chi_phi"] == Decimal("80000000")
        assert result["loi_nhuan"] == Decimal("20000000")
        assert len(result["but_toan_list"]) == 3  # Revenue, Expense, Profit

    def test_closing_revenue_entry(self, accounts_2026, sample_journal_entries):
        """Test revenue closing entry debits revenue, credits 911."""
        ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        bt = ButToan.objects.get(so_but_toan="BT-KC-DT2025")
        chi_tiet = list(bt.chi_tiet.all())

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "511"
        assert no_line.so_tien == Decimal("100000000")

        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")
        assert co_line.tai_khoan.ma_tai_khoan == "911"

    def test_closing_expense_entry(self, accounts_2026, sample_journal_entries):
        """Test expense closing entry credits expenses, debits 911."""
        ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        bt = ButToan.objects.get(so_but_toan="BT-KC-CP2025")
        chi_tiet = list(bt.chi_tiet.all())

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "911"

        co_lines = [c for c in chi_tiet if c.loai_no_co == "co"]
        assert any(c.tai_khoan.ma_tai_khoan == "632" for c in co_lines)
        assert any(c.tai_khoan.ma_tai_khoan == "642" for c in co_lines)

    def test_closing_profit_to_421(self, accounts_2026, sample_journal_entries):
        """Test profit is closed to 421."""
        ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        bt = ButToan.objects.get(so_but_toan="BT-KC-LN2025")
        chi_tiet = list(bt.chi_tiet.all())

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "911"

        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")
        assert co_line.tai_khoan.ma_tai_khoan == "421"
        assert co_line.so_tien == Decimal("20000000")

    def test_closing_loss_to_421(self, accounts_2026):
        """Test loss is closed to 421 (debit 421, credit 911)."""
        # Create entries where expenses > revenue
        tao_but_toan(
            ngay=date(2025, 12, 31),
            dien_giai="Revenue",
            chi_tiet=[
                {
                    "tai_khoan": "111",
                    "loai_no_co": "no",
                    "so_tien": Decimal("50000000"),
                    "dien_giai": "",
                },
                {
                    "tai_khoan": "511",
                    "loai_no_co": "co",
                    "so_tien": Decimal("50000000"),
                    "dien_giai": "",
                },
            ],
            so_but_toan="BT-LOSS-REV",
        )
        tao_but_toan(
            ngay=date(2025, 12, 31),
            dien_giai="Expense",
            chi_tiet=[
                {
                    "tai_khoan": "642",
                    "loai_no_co": "no",
                    "so_tien": Decimal("80000000"),
                    "dien_giai": "",
                },
                {
                    "tai_khoan": "111",
                    "loai_no_co": "co",
                    "so_tien": Decimal("80000000"),
                    "dien_giai": "",
                },
            ],
            so_but_toan="BT-LOSS-EXP",
        )

        result = ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        assert result["loi_nhuan"] == Decimal("-30000000")

        bt = ButToan.objects.get(so_but_toan="BT-KC-LN2025")
        chi_tiet = list(bt.chi_tiet.all())

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "421"

        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")
        assert co_line.tai_khoan.ma_tai_khoan == "911"

    def test_no_entries_no_closing(self, accounts_2026):
        """Test closing with no entries creates nothing."""
        result = ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)

        assert result["doanh_thu"] == Decimal("0")
        assert result["chi_phi"] == Decimal("0")
        assert result["loi_nhuan"] == Decimal("0")
        assert len(result["but_toan_list"]) == 0
