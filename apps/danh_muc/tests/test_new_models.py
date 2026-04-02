"""Tests for new danh_muc models."""

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import (
    DonVi,
    HangHoa,
    KhachHang,
    NganHang,
    NhaCungCap,
    TaiKhoanKeToan,
    TaiKhoanNganHang,
)


@pytest.mark.django_db
class TestNhaCungCap:
    """Tests for NhaCungCap model."""

    def test_create_nha_cung_cap(self):
        """Test creating a supplier."""
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Công ty TNHH ABC",
            ma_so_thue="0123456789",
            dia_chi="Hà Nội",
            dien_thoai="0901234567",
            email="abc@example.com",
        )
        assert ncc.ma_ncc == "NCC001"
        assert ncc.ten_ncc == "Công ty TNHH ABC"
        assert ncc.is_active is True

    def test_string_representation(self):
        """Test string representation."""
        ncc = NhaCungCap(
            ma_ncc="NCC001",
            ten_ncc="Công ty TNHH ABC",
        )
        assert str(ncc) == "NCC001 - Công ty TNHH ABC"

    def test_unique_ma_ncc(self):
        """Test that supplier codes must be unique."""
        NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Supplier A",
        )
        with pytest.raises(Exception):
            NhaCungCap.objects.create(
                ma_ncc="NCC001",
                ten_ncc="Supplier B",
            )

    def test_bank_fields(self):
        """Test bank account fields."""
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC002",
            ten_ncc="Supplier B",
            tai_khoan_ngan_hang="1234567890",
            ngan_hang="Vietcombank",
        )
        assert ncc.tai_khoan_ngan_hang == "1234567890"
        assert ncc.ngan_hang == "Vietcombank"


@pytest.mark.django_db
class TestKhachHang:
    """Tests for KhachHang model."""

    def test_create_khach_hang(self):
        """Test creating a customer."""
        kh = KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Nguyễn Văn A",
            ma_so_thue="0123456789",
            dia_chi="Hà Nội",
            dien_thoai="0901234567",
            email="a@example.com",
        )
        assert kh.ma_kh == "KH001"
        assert kh.ten_kh == "Nguyễn Văn A"
        assert kh.is_active is True

    def test_string_representation(self):
        """Test string representation."""
        kh = KhachHang(
            ma_kh="KH001",
            ten_kh="Nguyễn Văn A",
        )
        assert str(kh) == "KH001 - Nguyễn Văn A"

    def test_unique_ma_kh(self):
        """Test that customer codes must be unique."""
        KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Customer A",
        )
        with pytest.raises(Exception):
            KhachHang.objects.create(
                ma_kh="KH001",
                ten_kh="Customer B",
            )

    def test_etax_id_field(self):
        """Test eTax ID field."""
        kh = KhachHang.objects.create(
            ma_kh="KH002",
            ten_kh="Customer B",
            so_gioi_thieu_dien_tu="ETAX123456",
        )
        assert kh.so_gioi_thieu_dien_tu == "ETAX123456"


@pytest.mark.django_db
class TestNganHang:
    """Tests for NganHang model."""

    def test_create_ngan_hang(self):
        """Test creating a bank."""
        nb = NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Ngân hàng Vietcombank",
            ma_dien_toan="BFTVVNVX",
            dia_chi="Hà Nội",
        )
        assert nb.ma_ngan_hang == "VCB"
        assert nb.ten_ngan_hang == "Ngân hàng Vietcombank"
        assert nb.ma_dien_toan == "BFTVVNVX"

    def test_string_representation(self):
        """Test string representation."""
        nb = NganHang(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Ngân hàng Vietcombank",
        )
        assert str(nb) == "VCB - Ngân hàng Vietcombank"

    def test_unique_ma_ngan_hang(self):
        """Test that bank codes must be unique."""
        NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Vietcombank",
        )
        with pytest.raises(Exception):
            NganHang.objects.create(
                ma_ngan_hang="VCB",
                ten_ngan_hang="Vietcombank 2",
            )


@pytest.mark.django_db
class TestTaiKhoanNganHang:
    """Tests for TaiKhoanNganHang model."""

    def test_create_tai_khoan_ngan_hang(self):
        """Test creating a company bank account."""
        nb = NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Vietcombank",
        )
        tk = TaiKhoanNganHang.objects.create(
            ngan_hang=nb,
            so_tai_khoan="1234567890",
            ten_chu_tai_khoan="Công ty TNHH ABC",
        )
        assert tk.so_tai_khoan == "1234567890"
        assert tk.ngan_hang == nb
        assert tk.tien_te == "VND"

    def test_string_representation(self):
        """Test string representation."""
        nb = NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Vietcombank",
        )
        tk = TaiKhoanNganHang(
            ngan_hang=nb,
            so_tai_khoan="1234567890",
            ten_chu_tai_khoan="Công ty TNHH ABC",
        )
        assert str(tk) == "1234567890 - Công ty TNHH ABC"

    def test_unique_so_tai_khoan(self):
        """Test that account numbers must be unique."""
        nb = NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Vietcombank",
        )
        TaiKhoanNganHang.objects.create(
            ngan_hang=nb,
            so_tai_khoan="1234567890",
            ten_chu_tai_khoan="Company A",
        )
        nb2 = NganHang.objects.create(
            ma_ngan_hang="BIDV",
            ten_ngan_hang="BIDV",
        )
        with pytest.raises(Exception):
            TaiKhoanNganHang.objects.create(
                ngan_hang=nb2,
                so_tai_khoan="1234567890",
                ten_chu_tai_khoan="Company B",
            )

    def test_foreign_currency(self):
        """Test foreign currency account."""
        nb = NganHang.objects.create(
            ma_ngan_hang="VCB",
            ten_ngan_hang="Vietcombank",
        )
        tk = TaiKhoanNganHang.objects.create(
            ngan_hang=nb,
            so_tai_khoan="USD123456",
            ten_chu_tai_khoan="Company A",
            tien_te="USD",
        )
        assert tk.tien_te == "USD"


@pytest.mark.django_db
class TestHangHoa:
    """Tests for HangHoa model."""

    def test_create_hang_hoa(self):
        """Test creating a product."""
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Sản phẩm A",
            don_vi_tinh="cái",
            gia_mua=100000,
            gia_ban=150000,
            thue_suat_gtgt="10",
        )
        assert hh.ma_hang_hoa == "HH001"
        assert hh.gia_mua == 100000
        assert hh.gia_ban == 150000

    def test_string_representation(self):
        """Test string representation."""
        hh = HangHoa(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Sản phẩm A",
        )
        assert str(hh) == "HH001 - Sản phẩm A"

    def test_unique_ma_hang_hoa(self):
        """Test that product codes must be unique."""
        HangHoa.objects.create(
            ma_hang_hoa="HH001",
            ten_hang_hoa="Product A",
        )
        with pytest.raises(Exception):
            HangHoa.objects.create(
                ma_hang_hoa="HH001",
                ten_hang_hoa="Product B",
            )

    def test_vat_rate_choices(self):
        """Test VAT rate choices."""
        for rate in ["0", "5", "8", "10"]:
            hh = HangHoa(
                ma_hang_hoa=f"HH{rate}",
                ten_hang_hoa=f"Product {rate}",
                thue_suat_gtgt=rate,
            )
            assert hh.thue_suat_gtgt == rate

    def test_default_vat_rate(self):
        """Test default VAT rate is 10%."""
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH002",
            ten_hang_hoa="Product B",
        )
        assert hh.thue_suat_gtgt == "10"

    def test_revenue_account_link(self):
        """Test revenue account foreign key."""
        tk_dt, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="511",
            defaults={"ten_tai_khoan": "Doanh thu bán hàng", "cap_do": 1},
        )
        tk_gv, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="632",
            defaults={"ten_tai_khoan": "Giá vốn hàng bán", "cap_do": 1},
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH003",
            ten_hang_hoa="Product C",
            tk_doanh_thu=tk_dt,
            tk_gia_von=tk_gv,
        )
        assert hh.tk_doanh_thu == tk_dt
        assert hh.tk_gia_von == tk_gv
