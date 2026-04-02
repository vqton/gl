"""Tests for M13: Báo cáo tài chính (Financial Reports) - TT 99/2025/TT-BTC."""

from datetime import date
from decimal import Decimal

import pytest

from apps.bao_cao.services import (
    get_so_du_tai_khoan,
    lap_bang_can_doi_ke_toan,
    lap_bao_cao_kq_kinh_doanh,
    lap_bang_can_doi_so_phat_sinh,
    lap_bao_cao_luu_chuyen_tien_te,
    lap_thuyet_minh_bctc,
)
from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet
from apps.nghiep_vu.services import tao_but_toan


@pytest.fixture
def tk_111():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={"ten_tai_khoan": "Tiền mặt", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_511():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="511",
        defaults={"ten_tai_khoan": "Doanh thu", "cap_do": 1, "loai_tai_khoan": "doanh_thu"},
    )
    return tk


@pytest.fixture
def tk_632():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="632",
        defaults={"ten_tai_khoan": "Giá vốn", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )
    return tk


@pytest.fixture
def tk_642():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={"ten_tai_khoan": "Chi phí QLDN", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )
    return tk


@pytest.fixture
def tk_3331():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="3331",
        defaults={"ten_tai_khoan": "Thuế GTGT", "cap_do": 2, "loai_tai_khoan": "no_phai_tra"},
    )
    return tk


@pytest.fixture
def tk_157():
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="157",
        defaults={"ten_tai_khoan": "Hàng hóa", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def journal_entries(tk_111, tk_511, tk_632, tk_642, tk_3331, tk_157):
    bt1 = tao_but_toan(
        ngay=date(2026, 1, 15),
        dien_giai="Doanh thu bán hàng",
        chi_tiet=[
            {"tai_khoan": "111", "loai_no_co": "no", "so_tien": Decimal("11000000"), "dien_giai": "Thu tiền"},
            {"tai_khoan": "511", "loai_no_co": "co", "so_tien": Decimal("10000000"), "dien_giai": "Doanh thu"},
            {"tai_khoan": "3331", "loai_no_co": "co", "so_tien": Decimal("1000000"), "dien_giai": "Thuế"},
        ],
        so_but_toan="BT-REV-001",
    )
    bt1.trang_thai = "posted"
    bt1.save()

    bt2 = tao_but_toan(
        ngay=date(2026, 1, 15),
        dien_giai="Giá vốn hàng bán",
        chi_tiet=[
            {"tai_khoan": "632", "loai_no_co": "no", "so_tien": Decimal("6000000"), "dien_giai": "Giá vốn"},
            {"tai_khoan": "157", "loai_no_co": "co", "so_tien": Decimal("6000000"), "dien_giai": "Xuất kho"},
        ],
        so_but_toan="BT-COGS-001",
    )
    bt2.trang_thai = "posted"
    bt2.save()

    bt3 = tao_but_toan(
        ngay=date(2026, 1, 20),
        dien_giai="Chi phí quản lý",
        chi_tiet=[
            {"tai_khoan": "642", "loai_no_co": "no", "so_tien": Decimal("2000000"), "dien_giai": "Chi phí"},
            {"tai_khoan": "111", "loai_no_co": "co", "so_tien": Decimal("2000000"), "dien_giai": "Chi tiền"},
        ],
        so_but_toan="BT-EXP-001",
    )
    bt3.trang_thai = "posted"
    bt3.save()


@pytest.mark.django_db
class TestGetSoDuTaiKhoan:
    def test_account_with_debit_balance(self, tk_111, journal_entries):
        result = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 1, 31))
        assert result["no_tong"] == Decimal("11000000")
        assert result["co_tong"] == Decimal("2000000")
        assert result["so_du"] == Decimal("9000000")

    def test_account_with_credit_balance(self, tk_511, journal_entries):
        result = get_so_du_tai_khoan("511", date(2026, 1, 1), date(2026, 1, 31))
        assert result["co_tong"] == Decimal("10000000")
        assert result["so_du"] == Decimal("-10000000")

    def test_account_with_no_entries(self, tk_632):
        result = get_so_du_tai_khoan("632", date(2026, 1, 1), date(2026, 1, 31))
        assert result["no_tong"] == Decimal("0")
        assert result["co_tong"] == Decimal("0")
        assert result["so_du"] == Decimal("0")

    def test_account_outside_period(self, tk_632, journal_entries):
        result = get_so_du_tai_khoan("632", date(2026, 2, 1), date(2026, 2, 28))
        assert result["no_tong"] == Decimal("0")


@pytest.mark.django_db
class TestBangCanDoiKeToan:
    def test_balance_sheet_structure(self, journal_entries):
        result = lap_bang_can_doi_ke_toan(date(2026, 1, 31))
        assert "tai_san" in result
        assert "nguon_von" in result
        assert "ngay_bao_cao" in result
        assert "can_doi" in result

    def test_balance_sheet_sections(self, journal_entries):
        result = lap_bang_can_doi_ke_toan(date(2026, 1, 31))
        assert "A" in result["tai_san"]
        assert "B" in result["tai_san"]
        assert "C" in result["nguon_von"]
        assert "D" in result["nguon_von"]
        assert "E" in result["nguon_von"]

    def test_balance_sheet_totals(self, journal_entries):
        result = lap_bang_can_doi_ke_toan(date(2026, 1, 31))
        assert result["tai_san"]["A"]["tong_cong"] >= Decimal("0")
        assert result["tong_tai_san"] >= Decimal("0")
        assert result["tong_nguon_von"] >= Decimal("0")


@pytest.mark.django_db
class TestBaoCaoKQKD:
    def test_pnl_structure(self, journal_entries):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert "chi_tiet" in result
        assert "01" in result["chi_tiet"]
        assert "10" in result["chi_tiet"]
        assert "20" in result["chi_tiet"]
        assert "80" in result["chi_tiet"]

    def test_pnl_revenue(self, journal_entries):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert result["chi_tiet"]["01"]["so_tien"] == Decimal("10000000")

    def test_pnl_cost(self, journal_entries):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert result["chi_tiet"]["11"]["so_tien"] == Decimal("6000000")

    def test_pnl_gross_profit(self, journal_entries):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert result["chi_tiet"]["20"]["so_tien"] == Decimal("4000000")

    def test_pnl_expenses(self, journal_entries):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert result["chi_tiet"]["41"]["so_tien"] == Decimal("2000000")

    def test_pnl_empty_period(self):
        result = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 1, 31))
        assert result["chi_tiet"]["80"]["so_tien"] == Decimal("0")
