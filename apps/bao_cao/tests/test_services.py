"""Tests for financial report services - TDD approach."""

import pytest
from datetime import date
from decimal import Decimal

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
        defaults={"ten_tai_khoan": "Tiền gửi ngân hàng", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_131(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={"ten_tai_khoan": "Phải thu KH", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_133(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="133",
        defaults={"ten_tai_khoan": "Thuế GTGT khấu trừ", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_152(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="152",
        defaults={"ten_tai_khoan": "Nguyên liệu", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_155(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="155",
        defaults={"ten_tai_khoan": "Thành phẩm", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_157(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="157",
        defaults={"ten_tai_khoan": "Hàng hóa", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_211(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="211",
        defaults={"ten_tai_khoan": "TSCĐ hữu hình", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_214(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="214",
        defaults={"ten_tai_khoan": "Hao mòn TSCĐ", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )[0]


@pytest.fixture
def tk_331(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={"ten_tai_khoan": "Phải trả người bán", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )[0]


@pytest.fixture
def tk_333(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="333",
        defaults={"ten_tai_khoan": "Thuế phải nộp", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )[0]


@pytest.fixture
def tk_334(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="334",
        defaults={"ten_tai_khoan": "Phải trả NLĐ", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )[0]


@pytest.fixture
def tk_338(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="338",
        defaults={"ten_tai_khoan": "Phải trả khác", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )[0]


@pytest.fixture
def tk_411(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="411",
        defaults={"ten_tai_khoan": "Vốn đầu tư CSH", "cap_do": 1, "loai_tai_khoan": "von_chu_so_huu"},
    )[0]


@pytest.fixture
def tk_421(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="421",
        defaults={"ten_tai_khoan": "Lợi nhuận chưa phân phối", "cap_do": 1, "loai_tai_khoan": "von_chu_so_huu"},
    )[0]


@pytest.fixture
def tk_511(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="511",
        defaults={"ten_tai_khoan": "Doanh thu bán hàng", "cap_do": 1, "loai_tai_khoan": "doanh_thu"},
    )[0]


@pytest.fixture
def tk_515(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="515",
        defaults={"ten_tai_khoan": "Doanh thu tài chính", "cap_do": 1, "loai_tai_khoan": "doanh_thu"},
    )[0]


@pytest.fixture
def tk_521(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="521",
        defaults={"ten_tai_khoan": "Giảm trừ doanh thu", "cap_do": 1, "loai_tai_khoan": "doanh_thu"},
    )[0]


@pytest.fixture
def tk_632(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="632",
        defaults={"ten_tai_khoan": "Giá vốn hàng bán", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )[0]


@pytest.fixture
def tk_635(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="635",
        defaults={"ten_tai_khoan": "Chi phí tài chính", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )[0]


@pytest.fixture
def tk_641(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="641",
        defaults={"ten_tai_khoan": "Chi phí bán hàng", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )[0]


@pytest.fixture
def tk_642(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={"ten_tai_khoan": "Chi phí QLDN", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )[0]


@pytest.fixture
def tk_711(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="711",
        defaults={"ten_tai_khoan": "Thu nhập khác", "cap_do": 1, "loai_tai_khoan": "thu_nhap_khac"},
    )[0]


@pytest.fixture
def tk_811(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="811",
        defaults={"ten_tai_khoan": "Chi phí khác", "cap_do": 1, "loai_tai_khoan": "chi_phi_khac"},
    )[0]


@pytest.fixture
def tk_821(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="821",
        defaults={"ten_tai_khoan": "Chi phí thuế TNDN", "cap_do": 1, "loai_tai_khoan": "chi_phi_khac"},
    )[0]


@pytest.fixture
def tk_911(db):
    return TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="911",
        defaults={"ten_tai_khoan": "Xác định KQKD", "cap_do": 1, "loai_tai_khoan": "xac_dinh_kq"},
    )[0]


def _create_journal_entry(so_but_toan, ngay_hach_toan, trang_thai="posted"):
    """Helper to create a posted journal entry."""
    return ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=ngay_hach_toan,
        trang_thai=trang_thai,
    )


def _add_line(but_toan, tai_khoan, loai_no_co, so_tien):
    """Helper to add a journal line."""
    return ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tai_khoan,
        loai_no_co=loai_no_co,
        so_tien=so_tien,
    )


class TestGetSoDuTaiKhoan:
    """Test account balance calculation."""

    def test_empty_account_returns_zero(self, tk_111):
        """Test empty account returns zero balance."""
        result = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["no_tong"] == Decimal("0")
        assert result["co_tong"] == Decimal("0")
        assert result["so_du"] == Decimal("0")

    def test_asset_account_debit_balance(self, tk_111, tk_511):
        """Test asset account shows debit balance (Nợ > Có)."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["no_tong"] == Decimal("10000000")
        assert result["co_tong"] == Decimal("0")
        assert result["so_du"] == Decimal("10000000")

    def test_asset_account_credit_balance(self, tk_111, tk_131):
        """Test asset account shows credit balance when Có > Nợ."""
        bt1 = _create_journal_entry("BT002", date(2026, 1, 10))
        _add_line(bt1, tk_111, "no", Decimal("5000000"))
        _add_line(bt1, tk_131, "co", Decimal("5000000"))

        bt2 = _create_journal_entry("BT003", date(2026, 1, 20))
        _add_line(bt2, tk_131, "no", Decimal("3000000"))
        _add_line(bt2, tk_111, "co", Decimal("3000000"))

        result = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["no_tong"] == Decimal("5000000")
        assert result["co_tong"] == Decimal("3000000")
        assert result["so_du"] == Decimal("2000000")

    def test_revenue_account_credit_balance(self, tk_511, tk_111):
        """Test revenue account shows credit balance (Có > Nợ)."""
        bt = _create_journal_entry("BT004", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_so_du_tai_khoan("511", date(2026, 1, 1), date(2026, 12, 31))
        assert result["no_tong"] == Decimal("0")
        assert result["co_tong"] == Decimal("10000000")
        assert result["so_du"] == Decimal("-10000000")

    def test_period_filtering(self, tk_111, tk_511):
        """Test balance is filtered by period."""
        bt1 = _create_journal_entry("BT005", date(2026, 1, 15))
        _add_line(bt1, tk_111, "no", Decimal("5000000"))
        _add_line(bt1, tk_511, "co", Decimal("5000000"))

        bt2 = _create_journal_entry("BT006", date(2026, 3, 15))
        _add_line(bt2, tk_111, "no", Decimal("3000000"))
        _add_line(bt2, tk_511, "co", Decimal("3000000"))

        result_q1 = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 3, 31))
        assert result_q1["no_tong"] == Decimal("8000000")

        result_jan = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 1, 31))
        assert result_jan["no_tong"] == Decimal("5000000")

    def test_draft_entries_excluded(self, tk_111, tk_511):
        """Test draft journal entries are excluded."""
        bt = _create_journal_entry("BT007", date(2026, 1, 15), trang_thai="draft")
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        result = get_so_du_tai_khoan("111", date(2026, 1, 1), date(2026, 12, 31))
        assert result["no_tong"] == Decimal("0")


class TestLapBangCanDoiKeToan:
    """Test Balance Sheet (B01-DN) report."""

    def test_b01_has_required_sections(self, tk_111, tk_211, tk_331, tk_411):
        """Test B01-DN has all required sections."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        assert "A" in report["tai_san"]
        assert "B" in report["tai_san"]
        assert "C" in report["nguon_von"]
        assert "D" in report["nguon_von"]
        assert "E" in report["nguon_von"]

    def test_b01_tai_san_ngan_han(self, tk_111, tk_112, tk_131, tk_133, tk_152, tk_155, tk_157, tk_411):
        """Test B01-DN tài sản ngắn hạn includes all required accounts."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("50000000"))
        _add_line(bt, tk_112, "no", Decimal("30000000"))
        _add_line(bt, tk_131, "no", Decimal("20000000"))
        _add_line(bt, tk_133, "no", Decimal("10000000"))
        _add_line(bt, tk_152, "no", Decimal("15000000"))
        _add_line(bt, tk_155, "no", Decimal("25000000"))
        _add_line(bt, tk_157, "no", Decimal("35000000"))
        _add_line(bt, tk_411, "co", Decimal("185000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        ts_nh = report["tai_san"]["A"]["chi_tiet"]
        assert "110" in ts_nh  # Tiền và tương đương tiền
        assert "120" in ts_nh  # Đầu tư tài chính ngắn hạn
        assert "130" in ts_nh  # Phải thu ngắn hạn
        assert "140" in ts_nh  # Hàng tồn kho
        assert "150" in ts_nh  # Tài sản ngắn hạn khác

        tong_nh = report["tai_san"]["A"]["tong_cong"]
        assert tong_nh == Decimal("185000000")

    def test_b01_tai_san_dai_han(self, tk_211, tk_214, tk_411):
        """Test B01-DN tài sản dài hạn includes TSCĐ net."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_211, "no", Decimal("200000000"))
        _add_line(bt, tk_214, "co", Decimal("50000000"))
        _add_line(bt, tk_411, "co", Decimal("150000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        ts_dh = report["tai_san"]["B"]["chi_tiet"]
        assert "210" in ts_dh  # TSCĐ
        assert "220" in ts_dh  # BĐS đầu tư
        assert "230" in ts_dh  # Đầu tư tài chính dài hạn
        assert "240" in ts_dh  # Phải thu dài hạn
        assert "250" in ts_dh  # Tài sản dài hạn khác

        tong_dh = report["tai_san"]["B"]["tong_cong"]
        assert tong_dh == Decimal("150000000")  # 200M - 50M hao mon

    def test_b01_no_ngan_han(self, tk_331, tk_333, tk_334, tk_338, tk_111):
        """Test B01-DN nợ ngắn hạn includes all required accounts."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_331, "co", Decimal("40000000"))
        _add_line(bt, tk_333, "co", Decimal("20000000"))
        _add_line(bt, tk_334, "co", Decimal("25000000"))
        _add_line(bt, tk_338, "co", Decimal("15000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        no_nh = report["nguon_von"]["C"]["chi_tiet"]
        assert "310" in no_nh  # Phải trả người bán ngắn hạn
        assert "320" in no_nh  # Người mua trả tiền trước
        assert "330" in no_nh  # Thuế phải nộp
        assert "340" in no_nh  # Phải trả người lao động
        assert "350" in no_nh  # Chi phí phải trả
        assert "360" in no_nh  # Phải trả nội bộ
        assert "370" in no_nh  # Phải trả ngắn hạn khác

        tong_no_nh = report["nguon_von"]["C"]["tong_cong"]
        assert tong_no_nh == Decimal("100000000")

    def test_b01_von_chu_so_huu(self, tk_411, tk_421, tk_111):
        """Test B01-DN vốn chủ sở hữu includes all required accounts."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("200000000"))
        _add_line(bt, tk_411, "co", Decimal("150000000"))
        _add_line(bt, tk_421, "co", Decimal("50000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        vcs = report["nguon_von"]["E"]["chi_tiet"]
        assert "410" in vcs  # Vốn chủ sở hữu
        assert "411" in vcs  # Vốn đầu tư của CSH
        assert "412" in vcs  # Thặng dư vốn cổ phần
        assert "413" in vcs  # Lợi nhuận chưa phân phối

        tong_vcs = report["nguon_von"]["E"]["tong_cong"]
        assert tong_vcs == Decimal("200000000")

    def test_b01_balance_check(self, tk_111, tk_411):
        """Test B01-DN balance check (Tài sản = Nguồn vốn)."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))
        assert report["can_doi"] is True

    def test_b01_has_ma_so_codes(self, tk_111, tk_411):
        """Test B01-DN line items have proper Mã số codes."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_bang_can_doi_ke_toan(date(2026, 12, 31))

        for section in ["A", "B", "C", "D", "E"]:
            if section in report["tai_san"]:
                for ma_so, line in report["tai_san"][section]["chi_tiet"].items():
                    assert "ma_so" in line
                    assert "ten_chi_tieu" in line
                    assert "so_tien" in line
            if section in report["nguon_von"]:
                for ma_so, line in report["nguon_von"][section]["chi_tiet"].items():
                    assert "ma_so" in line
                    assert "ten_chi_tieu" in line
                    assert "so_tien" in line


class TestLapBaoCaoKQKD:
    """Test P&L Report (B02-DN)."""

    def test_b02_has_required_sections(self, tk_511, tk_632, tk_111):
        """Test B02-DN has all required sections."""
        bt = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        report = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 12, 31))

        assert "01" in report["chi_tiet"]
        assert "02" in report["chi_tiet"]
        assert "10" in report["chi_tiet"]
        assert "11" in report["chi_tiet"]
        assert "20" in report["chi_tiet"]
        assert "30" in report["chi_tiet"]
        assert "31" in report["chi_tiet"]
        assert "40" in report["chi_tiet"]
        assert "50" in report["chi_tiet"]
        assert "51" in report["chi_tiet"]
        assert "60" in report["chi_tiet"]

    def test_b02_doanh_thu_thuan(self, tk_511, tk_521, tk_111, tk_333):
        """Test B02-DN doanh thu thuần calculation."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("110000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))
        _add_line(bt1, tk_333, "co", Decimal("10000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 20))
        _add_line(bt2, tk_521, "no", Decimal("5000000"))
        _add_line(bt2, tk_111, "co", Decimal("5000000"))

        report = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 12, 31))

        assert report["chi_tiet"]["01"]["so_tien"] == Decimal("100000000")
        assert report["chi_tiet"]["02"]["so_tien"] == Decimal("5000000")
        assert report["chi_tiet"]["10"]["so_tien"] == Decimal("95000000")

    def test_b02_loi_nhuan_gop(self, tk_511, tk_632, tk_111):
        """Test B02-DN lợi nhuận gộp calculation."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        report = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 12, 31))

        assert report["chi_tiet"]["11"]["so_tien"] == Decimal("60000000")
        assert report["chi_tiet"]["20"]["so_tien"] == Decimal("40000000")

    def test_b02_loi_nhuan_thuan(self, tk_511, tk_515, tk_632, tk_635, tk_641, tk_642, tk_111):
        """Test B02-DN lợi nhuận thuần calculation."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        bt3 = _create_journal_entry("BT003", date(2026, 6, 15))
        _add_line(bt3, tk_641, "no", Decimal("5000000"))
        _add_line(bt3, tk_111, "co", Decimal("5000000"))

        bt4 = _create_journal_entry("BT004", date(2026, 6, 15))
        _add_line(bt4, tk_642, "no", Decimal("10000000"))
        _add_line(bt4, tk_111, "co", Decimal("10000000"))

        bt5 = _create_journal_entry("BT005", date(2026, 6, 15))
        _add_line(bt5, tk_111, "no", Decimal("2000000"))
        _add_line(bt5, tk_515, "co", Decimal("2000000"))

        bt6 = _create_journal_entry("BT006", date(2026, 6, 15))
        _add_line(bt6, tk_635, "no", Decimal("3000000"))
        _add_line(bt6, tk_111, "co", Decimal("3000000"))

        report = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 12, 31))

        # gross profit = 100M - 60M = 40M
        assert report["chi_tiet"]["20"]["so_tien"] == Decimal("40000000")
        # net operating = 40M + 2M - 3M - 5M - 10M = 24M
        assert report["chi_tiet"]["50"]["so_tien"] == Decimal("24000000")

    def test_b02_loi_nhuan_rong(self, tk_511, tk_632, tk_711, tk_811, tk_821, tk_111, tk_333):
        """Test B02-DN lợi nhuận ròng includes tax."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        bt3 = _create_journal_entry("BT003", date(2026, 6, 15))
        _add_line(bt3, tk_111, "no", Decimal("5000000"))
        _add_line(bt3, tk_711, "co", Decimal("5000000"))

        bt4 = _create_journal_entry("BT004", date(2026, 6, 15))
        _add_line(bt4, tk_811, "no", Decimal("2000000"))
        _add_line(bt4, tk_111, "co", Decimal("2000000"))

        bt5 = _create_journal_entry("BT005", date(2026, 6, 15))
        _add_line(bt5, tk_821, "no", Decimal("6000000"))
        _add_line(bt5, tk_333, "co", Decimal("6000000"))

        report = lap_bao_cao_kq_kinh_doanh(date(2026, 1, 1), date(2026, 12, 31))

        # net operating = 100M - 60M = 40M
        assert report["chi_tiet"]["50"]["so_tien"] == Decimal("40000000")
        # net profit = 40M + 5M - 2M - 6M = 37M
        assert report["chi_tiet"]["80"]["so_tien"] == Decimal("37000000")


class TestLapBangCanDoiSoPhatSinh:
    """Test Trial Balance (Bảng cân đối số phát sinh)."""

    def test_trial_balance_has_all_accounts(self, tk_111, tk_511):
        """Test trial balance shows all accounts with activity."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        report = lap_bang_can_doi_so_phat_sinh(date(2026, 1, 1), date(2026, 12, 31))

        assert len(report["accounts"]) >= 2
        account_codes = [a["ma_tai_khoan"] for a in report["accounts"]]
        assert "111" in account_codes
        assert "511" in account_codes

    def test_trial_balance_totals_match(self, tk_111, tk_511):
        """Test trial balance total debit = total credit."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        report = lap_bang_can_doi_so_phat_sinh(date(2026, 1, 1), date(2026, 12, 31))

        assert report["tong_phat_sinh_no"] == report["tong_phat_sinh_co"]

    def test_trial_balance_has_required_columns(self, tk_111, tk_511):
        """Test trial balance has all required columns."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("10000000"))
        _add_line(bt, tk_511, "co", Decimal("10000000"))

        report = lap_bang_can_doi_so_phat_sinh(date(2026, 1, 1), date(2026, 12, 31))

        for acc in report["accounts"]:
            assert "ma_tai_khoan" in acc
            assert "ten_tai_khoan" in acc
            assert "so_du_dau_no" in acc
            assert "so_du_dau_co" in acc
            assert "phat_sinh_no" in acc
            assert "phat_sinh_co" in acc
            assert "so_du_cuoi_no" in acc
            assert "so_du_cuoi_co" in acc


class TestLapBaoCaoLuuChuyenTienTe:
    """Test Cash Flow Statement (B03-DN)."""

    def test_b03_has_required_sections(self, tk_111, tk_511, tk_632):
        """Test B03-DN has all 4 required sections."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        report = lap_bao_cao_luu_chuyen_tien_te(date(2026, 1, 1), date(2026, 12, 31))

        assert "I" in report
        assert "II" in report
        assert "III" in report
        assert "IV" in report

    def test_b03_luu_chuyen_tu_kinh_doanh(self, tk_111, tk_511, tk_632):
        """Test B03-DN cash from operating activities."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        report = lap_bao_cao_luu_chuyen_tien_te(date(2026, 1, 1), date(2026, 12, 31))

        assert "01" in report["I"]["chi_tiet"]
        assert "02" in report["I"]["chi_tiet"]
        assert "03" in report["I"]["chi_tiet"]
        assert "04" in report["I"]["chi_tiet"]
        assert "05" in report["I"]["chi_tiet"]
        assert "06" in report["I"]["chi_tiet"]
        assert "07" in report["I"]["chi_tiet"]
        assert "08" in report["I"]["chi_tiet"]
        assert "09" in report["I"]["chi_tiet"]
        assert "10" in report["I"]["chi_tiet"]
        assert "20" in report["I"]["chi_tiet"]

    def test_b03_tong_luu_chuyen(self, tk_111, tk_511, tk_632):
        """Test B03-DN total cash flow calculation."""
        bt1 = _create_journal_entry("BT001", date(2026, 6, 15))
        _add_line(bt1, tk_111, "no", Decimal("100000000"))
        _add_line(bt1, tk_511, "co", Decimal("100000000"))

        bt2 = _create_journal_entry("BT002", date(2026, 6, 15))
        _add_line(bt2, tk_632, "no", Decimal("60000000"))
        _add_line(bt2, tk_111, "co", Decimal("60000000"))

        report = lap_bao_cao_luu_chuyen_tien_te(date(2026, 1, 1), date(2026, 12, 31))

        tong = report["IV"]["tong_luu_chuyen"]
        assert tong == Decimal("40000000")  # 100M thu - 60M chi


class TestLapThuyetMinhBCTC:
    """Test Notes to Financial Statements (B09-DN)."""

    def test_b09_has_required_sections(self, tk_111, tk_411):
        """Test B09-DN has all required sections."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_thuyet_minh_bctc(date(2026, 12, 31))

        assert "thong_tin_chung" in report
        assert "chinh_sach_ke_toan" in report
        assert "thuyet_minh_chi_tieu" in report

    def test_b09_thong_tin_chung(self, tk_111, tk_411):
        """Test B09-DN company information section."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_thuyet_minh_bctc(date(2026, 12, 31))

        info = report["thong_tin_chung"]
        assert "ngay_bao_cao" in info
        assert "ky_bao_cao" in info

    def test_b09_chinh_sach_ke_toan(self, tk_111, tk_411):
        """Test B09-DN accounting policies section."""
        bt = _create_journal_entry("BT001", date(2026, 1, 15))
        _add_line(bt, tk_111, "no", Decimal("100000000"))
        _add_line(bt, tk_411, "co", Decimal("100000000"))

        report = lap_thuyet_minh_bctc(date(2026, 12, 31))

        policies = report["chinh_sach_ke_toan"]
        assert "co_so_lap" in policies
        assert "nguyen_tac_gia_goc" in policies
        assert "phuong_phap_khau_hao" in policies
        assert "phuong_phap_ton_kho" in policies
