"""Tests for Inventory service layer."""

from datetime import date
from decimal import Decimal

import pytest

from apps.danh_muc.models import HangHoa
from apps.kho.models import Kho, KhoEntry, KhoLot, TonKho, VatTuHangHoa
from apps.kho.services import InventoryValuationService


@pytest.fixture
def service():
    """Create an InventoryValuationService instance."""
    return InventoryValuationService()


@pytest.fixture
def hang_hoa_fifo():
    """Create a test goods item with FIFO method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_SVC_FIFO",
        ten_hang_hoa="Hàng Service FIFO",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
    )


@pytest.fixture
def hang_hoa_binh_quan():
    """Create a test goods item with Weighted Average method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_SVC_BQ",
        ten_hang_hoa="Hàng Service BQ",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="BINH_QUAN",
    )


@pytest.fixture
def hang_hoa_dich_danh():
    """Create a test goods item with Specific Identification method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_SVC_DD",
        ten_hang_hoa="Hàng Service DD",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="DICH_DANH",
    )


@pytest.fixture
def kho_a():
    """Create warehouse A."""
    return Kho.objects.create(ma_kho="KHO_A", ten_kho="Kho A")


@pytest.fixture
def kho_b():
    """Create warehouse B."""
    return Kho.objects.create(ma_kho="KHO_B", ten_kho="Kho B")


@pytest.mark.django_db
class TestInventoryValuationService:
    """Test InventoryValuationService class."""

    def test_get_strategy_fifo(self, service):
        """Test getting FIFO strategy."""
        strategy = service.get_strategy("FIFO")
        assert strategy.__class__.__name__ == "FIFOStrategy"

    def test_get_strategy_binh_quan(self, service):
        """Test getting Weighted Average strategy."""
        strategy = service.get_strategy("BINH_QUAN")
        assert strategy.__class__.__name__ == "WeightedAverageStrategy"

    def test_get_strategy_dich_danh(self, service):
        """Test getting Specific Identification strategy."""
        strategy = service.get_strategy("DICH_DANH")
        assert strategy.__class__.__name__ == "SpecificIdentificationStrategy"

    def test_get_strategy_invalid(self, service):
        """Test getting invalid strategy raises error."""
        with pytest.raises(ValueError, match="không hợp lệ"):
            service.get_strategy("INVALID")


@pytest.mark.django_db
class TestNhapKho:
    """Test goods receipt service."""

    def test_nhap_kho_creates_entries(self, service, hang_hoa_fifo, kho_a):
        """Test that nhap_kho creates KhoEntry records."""
        entries = service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_NK_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_SVC_1",
        )

        assert len(entries) == 1
        assert entries[0].loai == "NHAP"
        assert entries[0].so_chung_tu == "NK_SVC_1"
        assert entries[0].so_luong == Decimal("100")

    def test_nhap_kho_creates_lot(self, service, hang_hoa_fifo, kho_a):
        """Test that nhap_kho creates KhoLot."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_NK_2",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_SVC_2",
        )

        lot = KhoLot.objects.get(ma_lot="LOT_NK_2")
        assert lot.so_luong_nhap == Decimal("100")
        assert lot.so_luong_ton == Decimal("100")
        assert lot.don_gia_nhap == Decimal("10000")

    def test_nhap_kho_updates_ton_kho(self, service, hang_hoa_fifo, kho_a):
        """Test that nhap_kho updates TonKho balance."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_NK_3",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_SVC_3",
        )

        ton = TonKho.objects.get(hang_hoa=hang_hoa_fifo, kho=kho_a)
        assert ton.so_luong_ton == Decimal("100")
        assert ton.gia_tri_ton == Decimal("1000000")

    def test_nhap_kho_multiple_items(self, service, hang_hoa_fifo, kho_a):
        """Test nhap_kho with multiple items."""
        entries = service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "50",
                    "don_gia": "10000",
                    "ma_lot": "LOT_NK_4A",
                },
                {
                    "so_luong": "30",
                    "don_gia": "12000",
                    "ma_lot": "LOT_NK_4B",
                },
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_SVC_4",
        )

        assert len(entries) == 2
        ton = TonKho.objects.get(hang_hoa=hang_hoa_fifo, kho=kho_a)
        assert ton.so_luong_ton == Decimal("80")

    def test_nhap_kho_auto_lot(self, service, hang_hoa_fifo, kho_a):
        """Test nhap_kho auto-generates lot code when not provided."""
        entries = service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_SVC_5",
        )

        assert entries[0].lot is not None
        assert entries[0].lot.ma_lot.startswith("AUTO-")


@pytest.mark.django_db
class TestXuatKho:
    """Test goods issue service."""

    def test_xuat_kho_fifo(self, service, hang_hoa_fifo, kho_a):
        """Test xuat_kho with FIFO method."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_XK_FIFO_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_XK_FIFO_1",
        )

        entry = service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_SVC_FIFO_1",
        )

        assert entry.loai == "XUAT"
        assert entry.so_luong == Decimal("50")
        assert entry.gia_von_chinh_thuc == Decimal("500000")

    def test_xuat_kho_reduces_lot(self, service, hang_hoa_fifo, kho_a):
        """Test that xuat_kho reduces lot quantity."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_XK_FIFO_2",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_XK_FIFO_2",
        )

        service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_SVC_FIFO_2",
        )

        lot = KhoLot.objects.get(ma_lot="LOT_XK_FIFO_2")
        assert lot.so_luong_ton == Decimal("50")

    def test_xuat_kho_reduces_ton_kho(self, service, hang_hoa_fifo, kho_a):
        """Test that xuat_kho reduces TonKho balance."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_XK_FIFO_3",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_XK_FIFO_3",
        )

        service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_SVC_FIFO_3",
        )

        ton = TonKho.objects.get(hang_hoa=hang_hoa_fifo, kho=kho_a)
        assert ton.so_luong_ton == Decimal("50")

    def test_xuat_kho_dich_danh(self, service, hang_hoa_dich_danh, kho_a):
        """Test xuat_kho with Specific Identification method."""
        service.nhap_kho(
            hang_hoa=hang_hoa_dich_danh,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "15000",
                    "ma_lot": "LOT_XK_DD_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_XK_DD_1",
        )

        entry = service.xuat_kho(
            hang_hoa=hang_hoa_dich_danh,
            kho=kho_a,
            so_luong=Decimal("50"),
            lot_id="LOT_XK_DD_1",
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_SVC_DD_1",
        )

        assert entry.gia_von_chinh_thuc == Decimal("750000")


@pytest.mark.django_db
class TestDieuChuyen:
    """Test warehouse transfer service."""

    def test_dieu_chuyen_creates_entries(self, service, hang_hoa_fifo, kho_a, kho_b):
        """Test that dieu_chuyen creates both out and in entries."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_DC_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_DC_1",
        )

        out_entry, in_entry = service.dieu_chuyen(
            hang_hoa=hang_hoa_fifo,
            kho_nguon=kho_a,
            kho_dich=kho_b,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            dien_giai="Điều chuyển test",
        )

        assert out_entry.loai == "XUAT"
        assert out_entry.kho == kho_a
        assert in_entry.loai == "NHAP"
        assert in_entry.kho == kho_b
        assert out_entry.so_chung_tu == in_entry.so_chung_tu

    def test_dieu_chuyen_updates_both_warehouses(
        self, service, hang_hoa_fifo, kho_a, kho_b
    ):
        """Test that dieu_chuyen updates both warehouse balances."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_DC_2",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_DC_2",
        )

        service.dieu_chuyen(
            hang_hoa=hang_hoa_fifo,
            kho_nguon=kho_a,
            kho_dich=kho_b,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
        )

        ton_a = TonKho.objects.get(hang_hoa=hang_hoa_fifo, kho=kho_a)
        ton_b = TonKho.objects.get(hang_hoa=hang_hoa_fifo, kho=kho_b)

        assert ton_a.so_luong_ton == Decimal("50")
        assert ton_b.so_luong_ton == Decimal("50")


@pytest.mark.django_db
class TestGetTonKhoThoiDiem:
    """Test historical inventory balance service."""

    def test_get_ton_kho_thoi_diem(self, service, hang_hoa_fifo, kho_a):
        """Test getting inventory balance at a specific date."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_THOI_DIEM_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_THOI_DIEM_1",
        )

        service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            so_luong=Decimal("30"),
            ngay=date(2026, 1, 10),
            so_chung_tu="XK_THOI_DIEM_1",
        )

        # Balance on 05/01 should be 100 (before issue)
        result = service.get_ton_kho_thoi_diem(hang_hoa_fifo, kho_a, date(2026, 1, 5))
        assert result["so_luong_ton"] == Decimal("100")

        # Balance on 15/01 should be 70 (after issue)
        result = service.get_ton_kho_thoi_diem(hang_hoa_fifo, kho_a, date(2026, 1, 15))
        assert result["so_luong_ton"] == Decimal("70")

    def test_get_ton_kho_thoi_diem_zero(self, service, hang_hoa_fifo, kho_a):
        """Test getting inventory balance with no entries."""
        result = service.get_ton_kho_thoi_diem(hang_hoa_fifo, kho_a, date(2026, 1, 1))
        assert result["so_luong_ton"] == Decimal("0")
        assert result["gia_tri_ton"] == Decimal("0")

    def test_get_ton_kho_thoi_diem_calculates_value(
        self, service, hang_hoa_fifo, kho_a
    ):
        """Test that get_ton_kho_thoi_diem calculates value correctly."""
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho_a,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_THOI_DIEM_2",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_THOI_DIEM_2",
        )

        result = service.get_ton_kho_thoi_diem(hang_hoa_fifo, kho_a, date(2026, 1, 15))
        assert result["so_luong_ton"] == Decimal("100")
        assert result["gia_tri_ton"] == Decimal("1000000")
        assert result["don_gia_binh_quan"] == Decimal("10000")
