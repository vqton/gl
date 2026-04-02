"""Tests for nghiep_vu services."""

import pytest
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

from apps.danh_muc.models import (
    HangHoa,
    KhachHang,
    NhaCungCap,
    TaiKhoanKeToan,
)
from apps.nghiep_vu.models import Kho
from apps.nghiep_vu.models import (
    ButToan,
    ButToanChiTiet,
    HoaDon,
    HoaDonChiTiet,
    NhapKho,
    NhapKhoChiTiet,
    XuatKho,
    XuatKhoChiTiet,
)
from apps.nghiep_vu.services import (
    doi_tu_nguyen_te,
    tao_but_toan,
    tao_hoa_don,
    tao_nhap_kho,
    tao_xuat_kho,
    tinh_thue_gtgt,
    tinh_thue_tndn,
    tinh_thue_tndn_sme,
)


class TestTinhThueGtgt:
    """Tests for VAT calculation."""

    def test_10_percent_rate(self):
        """Test 10% VAT rate."""
        result = tinh_thue_gtgt(Decimal("1000000"), "10")
        assert result == Decimal("100000.00")

    def test_5_percent_rate(self):
        """Test 5% VAT rate."""
        result = tinh_thue_gtgt(Decimal("1000000"), "5")
        assert result == Decimal("50000.00")

    def test_8_percent_rate(self):
        """Test 8% VAT rate."""
        result = tinh_thue_gtgt(Decimal("1000000"), "8")
        assert result == Decimal("80000.00")

    def test_0_percent_rate(self):
        """Test 0% VAT rate."""
        result = tinh_thue_gtgt(Decimal("1000000"), "0")
        assert result == Decimal("0.00")

    def test_zero_amount(self):
        """Test zero amount."""
        result = tinh_thue_gtgt(Decimal("0"), "10")
        assert result == Decimal("0.00")

    def test_invalid_rate(self):
        """Test invalid VAT rate."""
        with pytest.raises(ValidationError):
            tinh_thue_gtgt(Decimal("1000000"), "15")

    def test_negative_amount(self):
        """Test negative amount raises error."""
        with pytest.raises(ValidationError):
            tinh_thue_gtgt(Decimal("-1000000"), "10")

    def test_default_rate(self):
        """Test default rate is 10%."""
        result = tinh_thue_gtgt(Decimal("1000000"))
        assert result == Decimal("100000.00")

    def test_precision(self):
        """Test decimal precision."""
        result = tinh_thue_gtgt(Decimal("1234567"), "10")
        assert result == Decimal("123456.70")


class TestTinhThueTndnSme:
    """Tests for corporate income tax calculation."""

    def test_positive_profit(self):
        """Test tax on positive profit."""
        result = tinh_thue_tndn_sme(Decimal("100000000"))
        assert result == Decimal("15000000.00")

    def test_zero_profit(self):
        """Test tax on zero profit."""
        result = tinh_thue_tndn_sme(Decimal("0"))
        assert result == Decimal("0.00")

    def test_negative_profit(self):
        """Test negative profit returns zero tax."""
        result = tinh_thue_tndn_sme(Decimal("-50000000"))
        assert result == Decimal("0.00")

    def test_15_percent_rate(self):
        """Test 15% SME rate."""
        result = tinh_thue_tndn_sme(Decimal("200000000"))
        assert result == Decimal("30000000.00")


class TestTinhThueTndn:
    """Tests for corporate income tax with revenue threshold."""

    def test_sme_rate_under_3b(self):
        """Test SME rate for revenue under 3 billion."""
        result = tinh_thue_tndn(
            Decimal("2500000000"),
            Decimal("100000000"),
        )
        assert result == Decimal("15000000.00")

    def test_standard_rate_over_3b(self):
        """Test standard rate for revenue over 3 billion."""
        result = tinh_thue_tndn(
            Decimal("3500000000"),
            Decimal("100000000"),
        )
        assert result == Decimal("20000000.00")

    def test_negative_profit(self):
        """Test negative profit returns zero."""
        result = tinh_thue_tndn(
            Decimal("1000000000"),
            Decimal("-50000000"),
        )
        assert result == Decimal("0.00")


@pytest.mark.django_db
class TestTaoButToan:
    """Tests for journal entry creation."""

    def _create_account(self, code, name):
        return TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan=code,
            defaults={"ten_tai_khoan": name, "cap_do": 1},
        )[0]

    def test_create_balanced_entry(self):
        """Test creating a balanced journal entry."""
        tk_no = self._create_account("111", "Tiền mặt")
        tk_co = self._create_account("131", "Phải thu khách hàng")

        bt = tao_but_toan(
            ngay=date(2026, 1, 15),
            dien_giai="Thu tiền khách hàng",
            chi_tiet=[
                {
                    "tai_khoan": tk_no,
                    "loai_no_co": "no",
                    "so_tien": Decimal("1000000"),
                },
                {
                    "tai_khoan": tk_co,
                    "loai_no_co": "co",
                    "so_tien": Decimal("1000000"),
                },
            ],
        )

        assert bt.so_but_toan.startswith("BT20260115")
        assert bt.dien_giai == "Thu tiền khách hàng"
        assert bt.chi_tiet.count() == 2

    def test_unbalanced_entry_raises_error(self):
        """Test unbalanced entry raises ValidationError."""
        tk_no = self._create_account("111", "Tiền mặt")
        tk_co = self._create_account("131", "Phải thu")

        with pytest.raises(ValidationError):
            tao_but_toan(
                ngay=date(2026, 1, 15),
                dien_giai="Test",
                chi_tiet=[
                    {
                        "tai_khoan": tk_no,
                        "loai_no_co": "no",
                        "so_tien": Decimal("1000000"),
                    },
                    {
                        "tai_khoan": tk_co,
                        "loai_no_co": "co",
                        "so_tien": Decimal("500000"),
                    },
                ],
            )

    def test_empty_details_raises_error(self):
        """Test empty details raises ValidationError."""
        with pytest.raises(ValidationError):
            tao_but_toan(
                ngay=date(2026, 1, 15),
                dien_giai="Test",
                chi_tiet=[],
            )

    def test_negative_amount_raises_error(self):
        """Test negative amount raises ValidationError."""
        tk = self._create_account("111", "Tiền mặt")

        with pytest.raises(ValidationError):
            tao_but_toan(
                ngay=date(2026, 1, 15),
                dien_giai="Test",
                chi_tiet=[
                    {
                        "tai_khoan": tk,
                        "loai_no_co": "no",
                        "so_tien": Decimal("-1000000"),
                    },
                ],
            )

    def test_custom_so_but_toan(self):
        """Test custom voucher number."""
        tk = self._create_account("111", "Tiền mặt")

        bt = tao_but_toan(
            ngay=date(2026, 1, 15),
            dien_giai="Test",
            chi_tiet=[
                {
                    "tai_khoan": tk,
                    "loai_no_co": "no",
                    "so_tien": Decimal("1000000"),
                },
                {
                    "tai_khoan": tk,
                    "loai_no_co": "co",
                    "so_tien": Decimal("1000000"),
                },
            ],
            so_but_toan="BT-CUSTOM-001",
        )

        assert bt.so_but_toan == "BT-CUSTOM-001"

    def test_multiple_lines(self):
        """Test journal entry with multiple debit/credit lines."""
        tk1 = self._create_account("111", "Tiền mặt")
        tk2 = self._create_account("112", "Ngân hàng")
        tk3 = self._create_account("131", "Phải thu")

        bt = tao_but_toan(
            ngay=date(2026, 1, 15),
            dien_giai="Multi-line entry",
            chi_tiet=[
                {
                    "tai_khoan": tk1,
                    "loai_no_co": "no",
                    "so_tien": Decimal("500000"),
                },
                {
                    "tai_khoan": tk2,
                    "loai_no_co": "no",
                    "so_tien": Decimal("500000"),
                },
                {
                    "tai_khoan": tk3,
                    "loai_no_co": "co",
                    "so_tien": Decimal("1000000"),
                },
            ],
        )

        assert bt.chi_tiet.count() == 3

    def test_future_date_raises_error(self):
        """Test future date raises ValidationError."""
        tk = self._create_account("111", "Tiền mặt")

        with pytest.raises(ValidationError):
            tao_but_toan(
                ngay=date(2099, 1, 1),
                dien_giai="Test",
                chi_tiet=[
                    {
                        "tai_khoan": tk,
                        "loai_no_co": "no",
                        "so_tien": Decimal("1000000"),
                    },
                    {
                        "tai_khoan": tk,
                        "loai_no_co": "co",
                        "so_tien": Decimal("1000000"),
                    },
                ],
            )


@pytest.mark.django_db
class TestTaoHoaDon:
    """Tests for invoice creation."""

    def _setup_data(self):
        kh = KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )
        tk_dt, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="511",
            defaults={"ten_tai_khoan": "Doanh thu", "cap_do": 1},
        )
        tk_gv, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="632",
            defaults={"ten_tai_khoan": "Giá vốn", "cap_do": 1},
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
            gia_ban=100000,
            thue_suat_gtgt="10",
            tk_doanh_thu=tk_dt,
            tk_gia_von=tk_gv,
        )
        return kh, hh

    def test_create_invoice_single_item(self):
        """Test creating invoice with single item."""
        kh, hh = self._setup_data()

        hd = tao_hoa_don(
            khach_hang=kh,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("10"),
                    "don_gia": Decimal("100000"),
                },
            ],
            ngay_hoa_don=date(2026, 1, 15),
        )

        assert hd.so_hoa_don.startswith("HD20260115")
        assert hd.tong_tien_truoc_thue == Decimal("1000000.00")
        assert hd.tien_thue_gtgt == Decimal("100000.00")
        assert hd.tong_cong_thanh_toan == Decimal("1100000.00")
        assert hd.chi_tiet.count() == 1

    def test_create_invoice_multiple_items(self):
        """Test creating invoice with multiple items."""
        kh, hh1 = self._setup_data()
        hh2 = HangHoa.objects.create(
            ma_hang_hoa="HH002",
            ten_hang_hoa="Product B",
            gia_ban=200000,
            thue_suat_gtgt="10",
        )

        hd = tao_hoa_don(
            khach_hang=kh,
            items=[
                {
                    "hang_hoa": hh1,
                    "so_luong": Decimal("5"),
                    "don_gia": Decimal("100000"),
                },
                {
                    "hang_hoa": hh2,
                    "so_luong": Decimal("3"),
                    "don_gia": Decimal("200000"),
                },
            ],
            ngay_hoa_don=date(2026, 1, 15),
        )

        assert hd.chi_tiet.count() == 2
        assert hd.tong_tien_truoc_thue == Decimal("1100000.00")

    def test_empty_items_raises_error(self):
        """Test empty items raises ValidationError."""
        kh = KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )

        with pytest.raises(ValidationError):
            tao_hoa_don(
                khach_hang=kh,
                items=[],
            )

    def test_invoice_detail_totals(self):
        """Test invoice line item calculations."""
        kh, hh = self._setup_data()

        hd = tao_hoa_don(
            khach_hang=kh,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("2"),
                    "don_gia": Decimal("500000"),
                    "thue_suat": "10",
                },
            ],
            ngay_hoa_don=date(2026, 1, 15),
        )

        ct = hd.chi_tiet.first()
        assert ct.so_luong == Decimal("2")
        assert ct.don_gia == Decimal("500000")
        assert ct.tien_thue == Decimal("100000.00")
        assert ct.tong_tien == Decimal("1100000.00")

    def test_different_vat_rates(self):
        """Test invoice with different VAT rates."""
        kh, hh1 = self._setup_data()
        hh2 = HangHoa.objects.create(
            ma_hang_hoa="HH002",
            ten_hang_hoa="Product B",
            gia_ban=100000,
            thue_suat_gtgt="5",
        )

        hd = tao_hoa_don(
            khach_hang=kh,
            items=[
                {
                    "hang_hoa": hh1,
                    "so_luong": Decimal("1"),
                    "don_gia": Decimal("100000"),
                    "thue_suat": "10",
                },
                {
                    "hang_hoa": hh2,
                    "so_luong": Decimal("1"),
                    "don_gia": Decimal("100000"),
                    "thue_suat": "5",
                },
            ],
            ngay_hoa_don=date(2026, 1, 15),
        )

        assert hd.tien_thue_gtgt == Decimal("15000.00")


@pytest.mark.django_db
class TestTaoNhapKho:
    """Tests for goods receipt creation."""

    def _setup_data(self):
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Supplier A",
        )
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
            gia_mua=80000,
        )
        return ncc, kho, hh

    def test_create_nhap_kho(self):
        """Test creating goods receipt."""
        ncc, kho, hh = self._setup_data()

        nk = tao_nhap_kho(
            nha_cung_cap=ncc,
            kho=kho,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("100"),
                    "don_gia": Decimal("80000"),
                },
            ],
            ngay=date(2026, 1, 15),
        )

        assert nk.so_chung_tu.startswith("NK20260115")
        assert nk.tong_tien == Decimal("8000000.00")
        assert nk.chi_tiet.count() == 1

    def test_multiple_items(self):
        """Test goods receipt with multiple items."""
        ncc, kho, hh1 = self._setup_data()
        hh2 = HangHoa.objects.create(
            ma_hang_hoa="HH002",
            ten_hang_hoa="Product B",
            gia_mua=50000,
        )

        nk = tao_nhap_kho(
            nha_cung_cap=ncc,
            kho=kho,
            items=[
                {
                    "hang_hoa": hh1,
                    "so_luong": Decimal("50"),
                    "don_gia": Decimal("80000"),
                },
                {
                    "hang_hoa": hh2,
                    "so_luong": Decimal("100"),
                    "don_gia": Decimal("50000"),
                },
            ],
            ngay=date(2026, 1, 15),
        )

        assert nk.chi_tiet.count() == 2
        assert nk.tong_tien == Decimal("9000000.00")

    def test_empty_items_raises_error(self):
        """Test empty items raises ValidationError."""
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Supplier A",
        )
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )

        with pytest.raises(ValidationError):
            tao_nhap_kho(
                nha_cung_cap=ncc,
                kho=kho,
                items=[],
            )

    def test_detail_line_totals(self):
        """Test detail line total calculations."""
        ncc, kho, hh = self._setup_data()

        nk = tao_nhap_kho(
            nha_cung_cap=ncc,
            kho=kho,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("10"),
                    "don_gia": Decimal("250000"),
                },
            ],
            ngay=date(2026, 1, 15),
        )

        ct = nk.chi_tiet.first()
        assert ct.so_luong == Decimal("10")
        assert ct.don_gia == Decimal("250000")
        assert ct.thanh_tien == Decimal("2500000.00")


@pytest.mark.django_db
class TestTaoXuatKho:
    """Tests for goods issue creation."""

    def _setup_data(self):
        kh = KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
            gia_ban=120000,
        )
        return kh, kho, hh

    def test_create_xuat_kho(self):
        """Test creating goods issue."""
        kh, kho, hh = self._setup_data()

        xk = tao_xuat_kho(
            khach_hang=kh,
            kho=kho,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("50"),
                    "don_gia": Decimal("120000"),
                },
            ],
            ngay=date(2026, 1, 15),
        )

        assert xk.so_chung_tu.startswith("XK20260115")
        assert xk.tong_tien == Decimal("6000000.00")
        assert xk.chi_tiet.count() == 1

    def test_without_customer(self):
        """Test goods issue without customer (internal)."""
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
        )

        xk = tao_xuat_kho(
            khach_hang=None,
            kho=kho,
            items=[
                {
                    "hang_hoa": hh,
                    "so_luong": Decimal("10"),
                    "don_gia": Decimal("100000"),
                },
            ],
            ngay=date(2026, 1, 15),
        )

        assert xk.khach_hang is None

    def test_empty_items_raises_error(self):
        """Test empty items raises ValidationError."""
        kh = KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho chính",
        )

        with pytest.raises(ValidationError):
            tao_xuat_kho(
                khach_hang=kh,
                kho=kho,
                items=[],
            )


class TestDoiTuNguyenTe:
    """Tests for currency conversion."""

    def test_vnd_to_vnd(self):
        """Test VND to VND (rate 1)."""
        result = doi_tu_nguyen_te(Decimal("1000000"))
        assert result == Decimal("1000000.00")

    def test_usd_to_vnd(self):
        """Test USD to VND conversion."""
        result = doi_tu_nguyen_te(
            Decimal("100"),
            Decimal("25000"),
        )
        assert result == Decimal("2500000.00")

    def test_negative_amount_raises_error(self):
        """Test negative amount raises error."""
        with pytest.raises(ValidationError):
            doi_tu_nguyen_te(Decimal("-1000000"))

    def test_zero_rate_raises_error(self):
        """Test zero rate raises error."""
        with pytest.raises(ValidationError):
            doi_tu_nguyen_te(Decimal("1000000"), Decimal("0"))

    def test_negative_rate_raises_error(self):
        """Test negative rate raises error."""
        with pytest.raises(ValidationError):
            doi_tu_nguyen_te(Decimal("1000000"), Decimal("-25000"))
