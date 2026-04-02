"""Tests for Sổ Cái (General Ledger) - TDD approach."""

import pytest
from datetime import date
from decimal import Decimal

from django.test import RequestFactory

from apps.bao_cao.services import get_so_cai_tai_khoan, get_tong_hop_so_cai
from apps.bao_cao.views import SoCaiTaiKhoanView, TongHopSoCaiView
from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet


@pytest.fixture
def tk_111(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={"ten_tai_khoan": "Tiền mặt", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_112(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="112",
        defaults={"ten_tai_khoan": "Tiền gửi NH", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_131(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={"ten_tai_khoan": "Phải thu KH", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_331(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={"ten_tai_khoan": "Phải trả NB", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )[0]


@pytest.fixture
def tk_411(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="411",
        defaults={"ten_tai_khoan": "Vốn đầu tư CSH", "cap_do": 1, "loai_tai_khoan": "von_chu_so_huu"},
    )[0]


@pytest.fixture
def tk_511(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="511",
        defaults={"ten_tai_khoan": "Doanh thu bán hàng", "cap_do": 1, "loai_tai_khoan": "doanh_thu"},
    )[0]


@pytest.fixture
def tk_632(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="632",
        defaults={"ten_tai_khoan": "Giá vốn hàng bán", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )[0]


def _create_journal(so_but_toan, ngay_hach_toan, trang_thai="posted"):
    return ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=ngay_hach_toan,
        trang_thai=trang_thai,
    )


def _add_line(but_toan, tai_khoan, loai_no_co, so_tien, ma_doi_tuong="", dien_giai="", so_chung_tu_goc=""):
    return ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tai_khoan,
        loai_no_co=loai_no_co,
        so_tien=so_tien,
        ma_doi_tuong=ma_doi_tuong,
        dien_giai=dien_giai,
        so_chung_tu_goc=so_chung_tu_goc,
    )


class TestGetSoCaiTaiKhoan:
    """Test detailed general ledger for a single account."""

    def test_empty_account_returns_zero_opening(self, tk_111):
        """Empty account should have zero opening balance and no lines."""
        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert result["so_du_cuoi_ky"] == Decimal("0")
        assert len(result["lines"]) == 0

    def test_single_entry_creates_correct_running_balance(self, tk_111, tk_511):
        """Single debit entry should create correct running balance."""
        bt = _create_journal("BT001", date(2026, 3, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert len(result["lines"]) == 1
        assert result["lines"][0]["so_tien"] == Decimal("10000000")
        assert result["lines"][0]["loai_no_co"] == "no"
        assert result["lines"][0]["so_du_tang_dan"] == Decimal("10000000")
        assert result["so_du_cuoi_ky"] == Decimal("10000000")

    def test_multiple_entries_calculate_running_balance(self, tk_111, tk_131, tk_511):
        """Multiple entries should accumulate running balance correctly."""
        bt1 = _create_journal("BT001", date(2026, 1, 10))
        _add_line(bt1, tk_111, "no", Decimal("50000000"))
        _add_line(bt1, tk_511, "co", Decimal("50000000"))

        bt2 = _create_journal("BT002", date(2026, 2, 5))
        _add_line(bt2, tk_111, "no", Decimal("30000000"))
        _add_line(bt2, tk_131, "co", Decimal("30000000"))

        bt3 = _create_journal("BT003", date(2026, 3, 20))
        _add_line(bt3, tk_131, "no", Decimal("20000000"))
        _add_line(bt3, tk_111, "co", Decimal("20000000"))

        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert len(result["lines"]) == 3

        assert result["lines"][0]["so_du_tang_dan"] == Decimal("50000000")
        assert result["lines"][1]["so_du_tang_dan"] == Decimal("80000000")
        assert result["lines"][2]["so_du_tang_dan"] == Decimal("60000000")
        assert result["so_du_cuoi_ky"] == Decimal("60000000")

    def test_period_filtering_excludes_outside_entries(self, tk_111, tk_511):
        """Entries outside the period should not appear in lines."""
        bt1 = _create_journal("BT001", date(2026, 1, 10))
        _add_line(bt1, tk_111, "no", Decimal("50000000"))
        _add_line(bt1, tk_511, "co", Decimal("50000000"))

        bt2 = _create_journal("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_111, "no", Decimal("20000000"))
        _add_line(bt2, tk_511, "co", Decimal("20000000"))

        result_q1 = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 3, 31))
        assert len(result_q1["lines"]) == 1
        assert result_q1["lines"][0]["so_tien"] == Decimal("50000000")

        result_h1 = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 6, 30))
        assert len(result_h1["lines"]) == 2

    def test_draft_entries_excluded(self, tk_111, tk_511):
        """Draft journal entries should be excluded from ledger."""
        bt = _create_journal("BT001", date(2026, 3, 15), trang_thai="draft")
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert len(result["lines"]) == 0
        assert result["so_du_cuoi_ky"] == Decimal("0")

    def test_opening_balance_from_prior_period(self, tk_111, tk_511):
        """Opening balance should include entries before tu_ngay."""
        bt = _create_journal("BT001", date(2025, 12, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal("BT002", date(2026, 2, 10))
        _add_line(bt2, tk_111, "no", Decimal("20000000"))
        _add_line(bt2, tk_511, "co", Decimal("20000000"))

        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["so_du_dau_ky"] == Decimal("100000000")
        assert len(result["lines"]) == 1
        assert result["so_du_cuoi_ky"] == Decimal("120000000")

    def test_closing_balance_equals_opening_plus_net_activity(self, tk_111, tk_131, tk_511):
        """Closing balance must equal opening + net period activity."""
        bt_prior = _create_journal("BT000", date(2025, 11, 1))
        _add_line(bt_prior, tk_111, "no", Decimal("50000000"))
        _add_line(bt_prior, tk_511, "co", Decimal("50000000"))

        bt1 = _create_journal("BT001", date(2026, 1, 15))
        _add_line(bt1, tk_111, "no", Decimal("30000000"))
        _add_line(bt1, tk_511, "co", Decimal("30000000"))

        bt2 = _create_journal("BT002", date(2026, 2, 20))
        _add_line(bt2, tk_131, "no", Decimal("10000000"))
        _add_line(bt2, tk_111, "co", Decimal("10000000"))

        result = get_so_cai_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        opening = result["so_du_dau_ky"]
        net_activity = sum(
            line["so_tien"] if line["loai_no_co"] == "no" else -line["so_tien"]
            for line in result["lines"]
        )
        assert result["so_du_cuoi_ky"] == opening + net_activity


class TestTongHopSoCai:
    """Test summary general ledger (trial balance style)."""

    def test_returns_only_accounts_with_activity(self, tk_111, tk_511, tk_632):
        """Only accounts with activity in period should appear."""
        bt = _create_journal("BT001", date(2026, 3, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_tong_hop_so_cai(date(2026, 1, 1), date(2026, 12, 31))
        account_codes = [a["ma_tai_khoan"] for a in result["accounts"]]
        assert "111" in account_codes
        assert "511" in account_codes
        assert "632" not in account_codes

    def test_totals_match_sum_of_accounts(self, tk_111, tk_511, tk_331):
        """Totals row must equal sum of individual account values."""
        bt = _create_journal("BT001", date(2026, 3, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("8000000"))
        _add_line(bt, tk_331, "co", Decimal("2000000"))

        result = get_tong_hop_so_cai(date(2026, 1, 1), date(2026, 12, 31))
        sum_no = sum(a["phat_sinh_no"] for a in result["accounts"])
        sum_co = sum(a["phat_sinh_co"] for a in result["accounts"])
        assert result["tong_phat_sinh_no"] == sum_no
        assert result["tong_phat_sinh_co"] == sum_co

    def test_debit_accounts_show_debit_closing(self, tk_111, tk_511):
        """Asset accounts (debit nature) should show closing balance on debit side."""
        bt = _create_journal("BT001", date(2026, 3, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_tong_hop_so_cai(date(2026, 1, 1), date(2026, 12, 31))
        acc_111 = next(a for a in result["accounts"] if a["ma_tai_khoan"] == "111")
        assert acc_111["so_du_cuoi_no"] == Decimal("10000000")
        assert acc_111["so_du_cuoi_co"] == Decimal("0")

    def test_credit_accounts_show_credit_closing(self, tk_331, tk_111):
        """Liability accounts (credit nature) should show closing balance on credit side."""
        bt = _create_journal("BT001", date(2026, 3, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_331, "co", Decimal("10000000"))

        result = get_tong_hop_so_cai(date(2026, 1, 1), date(2026, 12, 31))
        acc_331 = next(a for a in result["accounts"] if a["ma_tai_khoan"] == "331")
        assert acc_331["so_du_cuoi_co"] == Decimal("10000000")
        assert acc_331["so_du_cuoi_no"] == Decimal("0")

    def test_empty_period_returns_no_accounts(self, db):
        """Empty period should return empty accounts list."""
        result = get_tong_hop_so_cai(date(2026, 1, 1), date(2026, 1, 31))
        assert len(result["accounts"]) == 0
        assert result["tong_phat_sinh_no"] == Decimal("0")
        assert result["tong_phat_sinh_co"] == Decimal("0")


class TestSoCaiViews:
    """Test view rendering and access control."""

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    def test_so_cai_chi_tiet_requires_login(self, factory):
        """SoCaiTaiKhoanView should require login."""
        view = SoCaiTaiKhoanView()
        assert hasattr(view, "dispatch")
        from django.contrib.auth.mixins import LoginRequiredMixin
        assert issubclass(SoCaiTaiKhoanView, LoginRequiredMixin)

    def test_so_cai_chi_tiet_returns_200(self, db, factory, tk_111):
        """SoCaiTaiKhoanView should return 200 for authenticated user."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass")

        request = factory.get("/bao-cao/so-cai/111/", {"tu": "2026-01-01", "den": "2026-12-31"})
        request.user = user

        view = SoCaiTaiKhoanView()
        view.setup(request, ma_tai_khoan="111")
        response = view.get(request, ma_tai_khoan="111")
        assert response.status_code == 200

    def test_tong_hop_so_cai_requires_login(self, factory):
        """TongHopSoCaiView should require login."""
        from django.contrib.auth.mixins import LoginRequiredMixin
        assert issubclass(TongHopSoCaiView, LoginRequiredMixin)

    def test_tong_hop_so_cai_returns_200(self, db, factory):
        """TongHopSoCaiView should return 200 for authenticated user."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass")

        request = factory.get("/bao-cao/tong-hop-so-cai/", {"tu": "2026-01-01", "den": "2026-12-31"})
        request.user = user

        view = TongHopSoCaiView()
        view.setup(request)
        response = view.get(request)
        assert response.status_code == 200
