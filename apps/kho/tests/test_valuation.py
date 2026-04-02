"""Tests for valuation strategies (FIFO, Weighted Average, Specific Identification)."""

from datetime import date
from decimal import Decimal

import pytest

from apps.danh_muc.models import HangHoa
from apps.kho.models import Kho, KhoLot, VatTuHangHoa
from apps.kho.valuation.strategies import (
    FIFOStrategy,
    SpecificIdentificationStrategy,
    WeightedAverageStrategy,
)


@pytest.fixture
def hang_hoa_fifo():
    """Create a test goods item with FIFO method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_FIFO",
        ten_hang_hoa="Hàng FIFO",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
    )


@pytest.fixture
def hang_hoa_binh_quan():
    """Create a test goods item with Weighted Average method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_BQ",
        ten_hang_hoa="Hàng Bình quân",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="BINH_QUAN",
    )


@pytest.fixture
def hang_hoa_dich_danh():
    """Create a test goods item with Specific Identification method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_DD",
        ten_hang_hoa="Hàng Đích danh",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="DICH_DANH",
    )


@pytest.fixture
def kho():
    """Create a test warehouse."""
    return Kho.objects.create(ma_kho="KHO_TEST", ten_kho="Kho test")


@pytest.fixture
def fifo_lots(hang_hoa_fifo):
    """Create multiple lots for FIFO testing."""
    lot1 = KhoLot.objects.create(
        ma_lot="LOT_F1",
        hang_hoa=hang_hoa_fifo,
        ngay_nhap=date(2026, 1, 1),
        so_luong_nhap=Decimal("100"),
        so_luong_ton=Decimal("100"),
        don_gia_nhap=Decimal("10000"),
    )
    lot2 = KhoLot.objects.create(
        ma_lot="LOT_F2",
        hang_hoa=hang_hoa_fifo,
        ngay_nhap=date(2026, 1, 5),
        so_luong_nhap=Decimal("200"),
        so_luong_ton=Decimal("200"),
        don_gia_nhap=Decimal("12000"),
    )
    lot3 = KhoLot.objects.create(
        ma_lot="LOT_F3",
        hang_hoa=hang_hoa_fifo,
        ngay_nhap=date(2026, 1, 10),
        so_luong_nhap=Decimal("150"),
        so_luong_ton=Decimal("150"),
        don_gia_nhap=Decimal("11000"),
    )
    return [lot1, lot2, lot3]


@pytest.fixture
def single_lot(hang_hoa_fifo):
    """Create a single lot for edge case testing."""
    return KhoLot.objects.create(
        ma_lot="LOT_SINGLE",
        hang_hoa=hang_hoa_fifo,
        ngay_nhap=date(2026, 1, 1),
        so_luong_nhap=Decimal("50"),
        so_luong_ton=Decimal("50"),
        don_gia_nhap=Decimal("20000"),
    )


@pytest.mark.django_db
class TestFIFOStrategy:
    """Test FIFO valuation strategy."""

    def test_fifo_basic_issue(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO issue consuming oldest lot first."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("50"), fifo_lots
        )

        assert len(result) == 1
        assert result[0]["lot_id"] == fifo_lots[0].pk
        assert result[0]["so_luong"] == Decimal("50")
        assert result[0]["don_gia"] == Decimal("10000")
        assert result[0]["thanh_tien"] == Decimal("500000")

    def test_fifo_split_across_lots(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO issue split across multiple lots."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("150"), fifo_lots
        )

        assert len(result) == 2
        # First lot: 100 units at 10000
        assert result[0]["lot_id"] == fifo_lots[0].pk
        assert result[0]["so_luong"] == Decimal("100")
        assert result[0]["don_gia"] == Decimal("10000")
        assert result[0]["thanh_tien"] == Decimal("1000000")
        # Second lot: 50 units at 12000
        assert result[1]["lot_id"] == fifo_lots[1].pk
        assert result[1]["so_luong"] == Decimal("50")
        assert result[1]["don_gia"] == Decimal("12000")
        assert result[1]["thanh_tien"] == Decimal("600000")

    def test_fifo_consume_all_lots(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO issue consuming all available lots."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("450"), fifo_lots
        )

        assert len(result) == 3
        total = sum(item["thanh_tien"] for item in result)
        expected = (
            Decimal("100") * Decimal("10000")
            + Decimal("200") * Decimal("12000")
            + Decimal("150") * Decimal("11000")
        )
        assert total == expected

    def test_fifo_insufficient_stock(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO raises error when stock is insufficient."""
        strategy = FIFOStrategy()
        with pytest.raises(ValueError, match="Không đủ hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_fifo, Decimal("500"), fifo_lots)

    def test_fifo_zero_quantity(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO with zero quantity returns empty list."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(hang_hoa_fifo, Decimal("0"), fifo_lots)
        assert result == []

    def test_fifo_negative_quantity(self, hang_hoa_fifo, fifo_lots):
        """Test FIFO with negative quantity returns empty list."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("-10"), fifo_lots
        )
        assert result == []

    def test_fifo_single_lot(self, hang_hoa_fifo, single_lot):
        """Test FIFO with single lot."""
        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("30"), [single_lot]
        )

        assert len(result) == 1
        assert result[0]["so_luong"] == Decimal("30")
        assert result[0]["don_gia"] == Decimal("20000")
        assert result[0]["thanh_tien"] == Decimal("600000")

    def test_fifo_skips_empty_lots(self, hang_hoa_fifo):
        """Test FIFO skips lots with zero quantity."""
        lot1 = KhoLot.objects.create(
            ma_lot="LOT_EMPTY",
            hang_hoa=hang_hoa_fifo,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("0"),
            don_gia_nhap=Decimal("10000"),
        )
        lot2 = KhoLot.objects.create(
            ma_lot="LOT_AVAIL",
            hang_hoa=hang_hoa_fifo,
            ngay_nhap=date(2026, 1, 5),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("15000"),
        )

        strategy = FIFOStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_fifo, Decimal("50"), [lot1, lot2]
        )

        assert len(result) == 1
        assert result[0]["lot_id"] == lot2.pk

    def test_fifo_update_ton_kho(self, hang_hoa_fifo, kho):
        """Test FIFO update_ton_kho method."""
        strategy = FIFOStrategy()
        lot = KhoLot.objects.create(
            ma_lot="LOT_UPDATE",
            hang_hoa=hang_hoa_fifo,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )

        current_ton = {"so_luong_ton": Decimal("50"), "gia_tri_ton": Decimal("500000")}
        result = strategy.update_ton_kho(hang_hoa_fifo, lot, Decimal("50"), current_ton)
        assert result["so_luong_ton"] == Decimal("100")
        assert result["gia_tri_ton"] == Decimal("1000000")
        assert "don_gia_binh_quan" in result


@pytest.mark.django_db
class TestWeightedAverageStrategy:
    """Test Weighted Average valuation strategy."""

    def test_binh_quan_basic_issue(self, hang_hoa_binh_quan):
        """Test weighted average with multiple lots."""
        lot1 = KhoLot.objects.create(
            ma_lot="LOT_BQ1",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )
        lot2 = KhoLot.objects.create(
            ma_lot="LOT_BQ2",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 5),
            so_luong_nhap=Decimal("200"),
            so_luong_ton=Decimal("200"),
            don_gia_nhap=Decimal("12000"),
        )

        strategy = WeightedAverageStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_binh_quan, Decimal("150"), [lot1, lot2]
        )

        assert len(result) == 1
        tong_so_luong = Decimal("100") + Decimal("200")
        tong_gia_tri = Decimal("100") * Decimal("10000") + Decimal("200") * Decimal(
            "12000"
        )
        expected_avg = (tong_gia_tri / tong_so_luong).quantize(Decimal("0.0001"))
        assert result[0]["don_gia"] == expected_avg
        assert result[0]["so_luong"] == Decimal("150")

    def test_binh_quan_4_decimal_precision(self, hang_hoa_binh_quan):
        """Test weighted average uses 4 decimal precision."""
        lot1 = KhoLot.objects.create(
            ma_lot="LOT_BQ3",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )
        lot2 = KhoLot.objects.create(
            ma_lot="LOT_BQ4",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 5),
            so_luong_nhap=Decimal("3"),
            so_luong_ton=Decimal("3"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = WeightedAverageStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_binh_quan, Decimal("50"), [lot1, lot2]
        )

        assert len(result) == 1
        don_gia = result[0]["don_gia"]
        assert don_gia == don_gia.quantize(Decimal("0.0001"))

    def test_binh_quan_single_lot(self, hang_hoa_binh_quan):
        """Test weighted average with single lot."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_BQ5",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = WeightedAverageStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_binh_quan, Decimal("50"), [lot]
        )

        assert len(result) == 1
        assert result[0]["don_gia"] == Decimal("10000")

    def test_binh_quan_zero_quantity(self, hang_hoa_binh_quan):
        """Test weighted average with zero quantity."""
        strategy = WeightedAverageStrategy()
        result = strategy.calculate_gia_von_xuat(hang_hoa_binh_quan, Decimal("0"), [])
        assert result == []

    def test_binh_quan_insufficient_stock(self, hang_hoa_binh_quan):
        """Test weighted average raises error on insufficient stock."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_BQ6",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("50"),
            so_luong_ton=Decimal("50"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = WeightedAverageStrategy()
        with pytest.raises(ValueError, match="Không đủ hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_binh_quan, Decimal("100"), [lot])

    def test_binh_quan_no_stock(self, hang_hoa_binh_quan):
        """Test weighted average raises error with no stock."""
        strategy = WeightedAverageStrategy()
        with pytest.raises(ValueError, match="Không có hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_binh_quan, Decimal("10"), [])

    def test_binh_quan_update_ton_kho(self, hang_hoa_binh_quan, kho):
        """Test weighted average update_ton_kho method."""
        strategy = WeightedAverageStrategy()
        lot = KhoLot.objects.create(
            ma_lot="LOT_BQ7",
            hang_hoa=hang_hoa_binh_quan,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )

        current_ton = {"so_luong_ton": Decimal("50"), "gia_tri_ton": Decimal("500000")}
        result = strategy.update_ton_kho(
            hang_hoa_binh_quan, lot, Decimal("50"), current_ton
        )
        assert "don_gia_binh_quan" in result
        assert result["don_gia_binh_quan"] == result["don_gia_binh_quan"].quantize(
            Decimal("0.0001")
        )


@pytest.mark.django_db
class TestSpecificIdentificationStrategy:
    """Test Specific Identification valuation strategy."""

    def test_dich_danh_basic_issue(self, hang_hoa_dich_danh):
        """Test specific identification with designated lot."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_DD1",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("15000"),
        )

        strategy = SpecificIdentificationStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_dich_danh, Decimal("50"), [lot]
        )

        assert len(result) == 1
        assert result[0]["lot_id"] == lot.pk
        assert result[0]["so_luong"] == Decimal("50")
        assert result[0]["don_gia"] == Decimal("15000")
        assert result[0]["thanh_tien"] == Decimal("750000")

    def test_dich_danh_exact_cost(self, hang_hoa_dich_danh):
        """Test specific identification returns exact lot cost."""
        lot1 = KhoLot.objects.create(
            ma_lot="LOT_DD2",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )
        lot2 = KhoLot.objects.create(
            ma_lot="LOT_DD3",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 5),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("20000"),
        )

        strategy = SpecificIdentificationStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_dich_danh, Decimal("50"), [lot2]
        )

        assert result[0]["don_gia"] == Decimal("20000")
        assert result[0]["thanh_tien"] == Decimal("1000000")

    def test_dich_danh_split_across_lots(self, hang_hoa_dich_danh):
        """Test specific identification split across multiple lots."""
        lot1 = KhoLot.objects.create(
            ma_lot="LOT_DD4",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("30"),
            so_luong_ton=Decimal("30"),
            don_gia_nhap=Decimal("10000"),
        )
        lot2 = KhoLot.objects.create(
            ma_lot="LOT_DD5",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 5),
            so_luong_nhap=Decimal("50"),
            so_luong_ton=Decimal("50"),
            don_gia_nhap=Decimal("15000"),
        )

        strategy = SpecificIdentificationStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_dich_danh, Decimal("60"), [lot1, lot2]
        )

        assert len(result) == 2
        assert result[0]["so_luong"] == Decimal("30")
        assert result[1]["so_luong"] == Decimal("30")

    def test_dich_danh_insufficient_lot(self, hang_hoa_dich_danh):
        """Test specific identification raises error on insufficient lot."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_DD6",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("50"),
            so_luong_ton=Decimal("50"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = SpecificIdentificationStrategy()
        with pytest.raises(ValueError, match="Không đủ hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_dich_danh, Decimal("100"), [lot])

    def test_dich_danh_empty_lot(self, hang_hoa_dich_danh):
        """Test specific identification raises error on empty lot."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_DD7",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("0"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = SpecificIdentificationStrategy()
        with pytest.raises(ValueError, match="không còn hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_dich_danh, Decimal("10"), [lot])

    def test_dich_danh_no_lots(self, hang_hoa_dich_danh):
        """Test specific identification raises error with no lots."""
        strategy = SpecificIdentificationStrategy()
        with pytest.raises(ValueError, match="Không có lô hàng"):
            strategy.calculate_gia_von_xuat(hang_hoa_dich_danh, Decimal("10"), [])

    def test_dich_danh_zero_quantity(self, hang_hoa_dich_danh):
        """Test specific identification with zero quantity."""
        lot = KhoLot.objects.create(
            ma_lot="LOT_DD8",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )

        strategy = SpecificIdentificationStrategy()
        result = strategy.calculate_gia_von_xuat(
            hang_hoa_dich_danh, Decimal("0"), [lot]
        )
        assert result == []

    def test_dich_danh_update_ton_kho(self, hang_hoa_dich_danh, kho):
        """Test specific identification update_ton_kho method."""
        strategy = SpecificIdentificationStrategy()
        lot = KhoLot.objects.create(
            ma_lot="LOT_DD9",
            hang_hoa=hang_hoa_dich_danh,
            ngay_nhap=date(2026, 1, 1),
            so_luong_nhap=Decimal("100"),
            so_luong_ton=Decimal("100"),
            don_gia_nhap=Decimal("10000"),
        )

        current_ton = {"so_luong_ton": Decimal("50"), "gia_tri_ton": Decimal("500000")}
        result = strategy.update_ton_kho(
            hang_hoa_dich_danh, lot, Decimal("50"), current_ton
        )
        assert result["so_luong_ton"] == Decimal("100")
        assert result["gia_tri_ton"] == Decimal("1000000")
