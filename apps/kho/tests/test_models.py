"""Tests for Inventory (Kho) models."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.danh_muc.models import HangHoa
from apps.kho.models import Kho, KhoEntry, KhoLot, TonKho, VatTuHangHoa


@pytest.fixture
def kho():
    """Create a test warehouse."""
    return Kho.objects.create(
        ma_kho="KHO01",
        ten_kho="Kho chính",
        dia_chi="123 Test St",
        nguoi_phu_trach="Nguyễn Văn A",
    )


@pytest.fixture
def hang_hoa():
    """Create a test goods item."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH001",
        ten_hang_hoa="Hàng test",
        don_vi_tinh="cái",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
        don_vi_tinh="cái",
        ton_toi_thieu=Decimal("10"),
        ton_toi_da=Decimal("1000"),
    )


@pytest.fixture
def kho_lot(hang_hoa):
    """Create a test inventory lot."""
    return KhoLot.objects.create(
        ma_lot="LOT001",
        hang_hoa=hang_hoa,
        ngay_nhap=date(2026, 1, 1),
        so_luong_nhap=Decimal("100"),
        so_luong_ton=Decimal("100"),
        don_gia_nhap=Decimal("10000"),
    )


@pytest.mark.django_db
class TestKhoModel:
    """Test Kho (Warehouse) model."""

    def test_kho_creation(self):
        """Test basic Kho creation."""
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho test",
        )
        assert kho.ma_kho == "KHO001"
        assert kho.ten_kho == "Kho test"
        assert kho.is_active is True

    def test_kho_str(self):
        """Test Kho string representation."""
        kho = Kho.objects.create(
            ma_kho="KHO001",
            ten_kho="Kho test",
        )
        assert str(kho) == "KHO001 - Kho test"

    def test_kho_unique_ma_kho(self):
        """Test that ma_kho must be unique."""
        Kho.objects.create(ma_kho="KHO001", ten_kho="Kho 1")
        with pytest.raises(IntegrityError):
            Kho.objects.create(ma_kho="KHO001", ten_kho="Kho 2")


@pytest.mark.django_db
class TestVatTuHangHoaModel:
    """Test VatTuHangHoa model."""

    def test_vat_tu_creation(self, hang_hoa):
        """Test basic VatTuHangHoa creation."""
        assert hang_hoa.phuong_phap_tinh_gia == "FIFO"
        assert hang_hoa.don_vi_tinh == "cái"
        assert hang_hoa.ton_toi_thieu == Decimal("10")

    def test_vat_tu_str(self, hang_hoa):
        """Test VatTuHangHoa string representation."""
        assert "FIFO" in str(hang_hoa)

    def test_vat_tu_different_methods(self):
        """Test VatTuHangHoa with different valuation methods."""
        hh = HangHoa.objects.create(
            ma_hang_hoa="HH002",
            ten_hang_hoa="Hàng FIFO",
        )
        vat_tu_fifo = VatTuHangHoa.objects.create(
            hang_hoa=hh,
            phuong_phap_tinh_gia="FIFO",
        )
        assert vat_tu_fifo.phuong_phap_tinh_gia == "FIFO"

        hh2 = HangHoa.objects.create(
            ma_hang_hoa="HH003",
            ten_hang_hoa="Hàng BINH_QUAN",
        )
        vat_tu_bq = VatTuHangHoa.objects.create(
            hang_hoa=hh2,
            phuong_phap_tinh_gia="BINH_QUAN",
        )
        assert vat_tu_bq.phuong_phap_tinh_gia == "BINH_QUAN"

        hh3 = HangHoa.objects.create(
            ma_hang_hoa="HH004",
            ten_hang_hoa="Hàng DICH_DANH",
        )
        vat_tu_dd = VatTuHangHoa.objects.create(
            hang_hoa=hh3,
            phuong_phap_tinh_gia="DICH_DANH",
        )
        assert vat_tu_dd.phuong_phap_tinh_gia == "DICH_DANH"


@pytest.mark.django_db
class TestKhoLotModel:
    """Test KhoLot model."""

    def test_kho_lot_creation(self, kho_lot):
        """Test basic KhoLot creation."""
        assert kho_lot.ma_lot == "LOT001"
        assert kho_lot.so_luong_nhap == Decimal("100")
        assert kho_lot.so_luong_ton == Decimal("100")
        assert kho_lot.don_gia_nhap == Decimal("10000")

    def test_kho_lot_str(self, kho_lot):
        """Test KhoLot string representation."""
        assert "LOT001" in str(kho_lot)

    def test_kho_lot_unique_ma_lot(self, hang_hoa):
        """Test that ma_lot must be unique."""
        KhoLot.objects.create(
            ma_lot="LOT001",
            hang_hoa=hang_hoa,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )
        with pytest.raises(IntegrityError):
            KhoLot.objects.create(
                ma_lot="LOT001",
                hang_hoa=hang_hoa,
                ngay_nhap=date(2026, 1, 2),
                so_luong_nhap=Decimal("50"),
                so_luong_ton=Decimal("50"),
                don_gia_nhap=Decimal("10000"),
            )

    def test_kho_lot_negative_ton_validation(self, hang_hoa):
        """Test that so_luong_ton cannot be negative."""
        lot = KhoLot(
            ma_lot="LOT002",
            hang_hoa=hang_hoa,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("-10"),
            don_gia_nhap=Decimal("10000"),
        )
        with pytest.raises(ValidationError):
            lot.full_clean()

    def test_kho_lot_ton_greater_than_nhap(self, hang_hoa):
        """Test that so_luong_ton cannot exceed so_luong_nhap."""
        lot = KhoLot(
            ma_lot="LOT003",
            hang_hoa=hang_hoa,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("150"),
            don_gia_nhap=Decimal("10000"),
        )
        with pytest.raises(ValidationError):
            lot.full_clean()

    def test_kho_lot_decimal_precision(self, hang_hoa):
        """Test KhoLot decimal precision (4 decimal places)."""
        lot = KhoLot.objects.create(
            ma_lot="LOT004",
            hang_hoa=hang_hoa,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100.1234"),
            so_luong_ton=Decimal("100.1234"),
            don_gia_nhap=Decimal("10000.5678"),
        )
        assert lot.so_luong_nhap == Decimal("100.1234")
        assert lot.don_gia_nhap == Decimal("10000.5678")


@pytest.mark.django_db
class TestKhoEntryModel:
    """Test KhoEntry model."""

    def test_kho_entry_creation(self, hang_hoa, kho):
        """Test basic KhoEntry creation."""
        entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            loai="NHAP",
            ngay_chung_tu=date(2026, 1, 1),
            so_chung_tu="NK001",
            loai_chung_tu="NK",
            so_luong=Decimal("100"),
            don_gia=Decimal("10000"),
            thanh_tien=Decimal("1000000"),
        )
        assert entry.loai == "NHAP"
        assert entry.so_luong == Decimal("100")
        assert entry.don_gia == Decimal("10000")

    def test_kho_entry_str(self, hang_hoa, kho):
        """Test KhoEntry string representation."""
        entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            loai="NHAP",
            ngay_chung_tu=date(2026, 1, 1),
            so_chung_tu="NK001",
            loai_chung_tu="NK",
            so_luong=Decimal("100"),
            don_gia=Decimal("10000"),
            thanh_tien=Decimal("1000000"),
        )
        assert "NK001" in str(entry)

    def test_kho_entry_auto_thanh_tien(self, hang_hoa, kho):
        """Test that thanh_tien is auto-calculated on save."""
        entry = KhoEntry(
            hang_hoa=hang_hoa,
            kho=kho,
            loai="NHAP",
            ngay_chung_tu=date(2026, 1, 1),
            so_chung_tu="NK002",
            loai_chung_tu="NK",
            so_luong=Decimal("50"),
            don_gia=Decimal("20000"),
        )
        entry.save()
        assert entry.thanh_tien == Decimal("1000000")

    def test_kho_entry_decimal_precision(self, hang_hoa, kho):
        """Test KhoEntry decimal precision."""
        entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            loai="NHAP",
            ngay_chung_tu=date(2026, 1, 1),
            so_chung_tu="NK003",
            loai_chung_tu="NK",
            so_luong=Decimal("100.1234"),
            don_gia=Decimal("10000.5678"),
            thanh_tien=Decimal("1001234.56"),
        )
        assert entry.so_luong == Decimal("100.1234")
        assert entry.don_gia == Decimal("10000.5678")

    def test_kho_entry_gia_von_fields(self, hang_hoa, kho):
        """Test gia_von_tam_tinh and gia_von_chinh_thuc fields."""
        entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            loai="XUAT",
            ngay_chung_tu=date(2026, 1, 5),
            so_chung_tu="XK001",
            loai_chung_tu="XK",
            so_luong=Decimal("50"),
            don_gia=Decimal("10000"),
            thanh_tien=Decimal("500000"),
            gia_von_tam_tinh=Decimal("500000"),
            gia_von_chinh_thuc=Decimal("500000"),
        )
        assert entry.gia_von_tam_tinh == Decimal("500000")
        assert entry.gia_von_chinh_thuc == Decimal("500000")
        assert entry.da_dong_bo is False


@pytest.mark.django_db
class TestTonKhoModel:
    """Test TonKho model."""

    def test_ton_kho_creation(self, hang_hoa, kho):
        """Test basic TonKho creation."""
        ton = TonKho.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            so_luong_ton=Decimal("100"),
            gia_tri_ton=Decimal("1000000"),
        )
        assert ton.so_luong_ton == Decimal("100")
        assert ton.gia_tri_ton == Decimal("1000000")

    def test_ton_kho_str(self, hang_hoa, kho):
        """Test TonKho string representation."""
        ton = TonKho.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            so_luong_ton=Decimal("100"),
            gia_tri_ton=Decimal("1000000"),
        )
        assert "100" in str(ton)

    def test_ton_kho_unique_constraint(self, hang_hoa, kho):
        """Test unique constraint on (hang_hoa, kho)."""
        TonKho.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            so_luong_ton=Decimal("100"),
            gia_tri_ton=Decimal("1000000"),
        )
        with pytest.raises(IntegrityError):
            TonKho.objects.create(
                hang_hoa=hang_hoa,
                kho=kho,
                so_luong_ton=Decimal("200"),
                gia_tri_ton=Decimal("2000000"),
            )

    def test_ton_kho_default_values(self, hang_hoa, kho):
        """Test TonKho default values."""
        ton = TonKho.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
        )
        assert ton.so_luong_ton == Decimal("0")
        assert ton.gia_tri_ton == Decimal("0")
