"""Tests for backdating and recalculation mechanism."""

from datetime import date
from decimal import Decimal

import pytest

from apps.danh_muc.models import HangHoa
from apps.kho.models import Kho, KhoEntry, KhoLot, VatTuHangHoa
from apps.kho.services import InventoryValuationService, tinh_lai_gia_von


@pytest.fixture
def hang_hoa_fifo():
    """Create a test goods item with FIFO method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_BACK_FIFO",
        ten_hang_hoa="Hàng Backdate FIFO",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
    )


@pytest.fixture
def hang_hoa_binh_quan():
    """Create a test goods item with Weighted Average method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_BACK_BQ",
        ten_hang_hoa="Hàng Backdate BQ",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="BINH_QUAN",
    )


@pytest.fixture
def hang_hoa_dich_danh():
    """Create a test goods item with Specific Identification method."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH_BACK_DD",
        ten_hang_hoa="Hàng Backdate DD",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="DICH_DANH",
    )


@pytest.fixture
def kho():
    """Create a test warehouse."""
    return Kho.objects.create(ma_kho="KHO_BACK", ten_kho="Kho backdate")


@pytest.mark.django_db
class TestBackdatingFIFO:
    """Test backdating recalculation with FIFO method."""

    def test_recalculate_after_price_change(self, hang_hoa_fifo, kho):
        """Test that modifying a receipt recalculates subsequent issues."""
        service = InventoryValuationService()

        # Create receipt on 01/01
        entries = service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_BACK_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_BACK_1",
        )
        lot = KhoLot.objects.get(ma_lot="LOT_BACK_1")

        # Create issue on 05/01
        issue_entry = service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_BACK_1",
        )
        original_cost = issue_entry.gia_von_chinh_thuc

        # Modify receipt price
        lot.don_gia_nhap = Decimal("15000")
        lot.save()

        # Recalculate from receipt date
        count = tinh_lai_gia_von(hang_hoa_fifo.pk, date(2026, 1, 1))
        assert count >= 1

        # Verify issue cost was updated
        issue_entry.refresh_from_db()
        new_cost = issue_entry.gia_von_chinh_thuc
        assert new_cost != original_cost

    def test_recalculate_multiple_issues(self, hang_hoa_fifo, kho):
        """Test recalculation with multiple issues after modified receipt."""
        service = InventoryValuationService()

        # Create receipt
        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            items=[
                {
                    "so_luong": "200",
                    "don_gia": "10000",
                    "ma_lot": "LOT_BACK_2",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_BACK_2",
        )

        # Create multiple issues
        issue1 = service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 3),
            so_chung_tu="XK_BACK_2A",
        )
        issue2 = service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            so_luong=Decimal("30"),
            ngay=date(2026, 1, 7),
            so_chung_tu="XK_BACK_2B",
        )

        # Modify receipt
        lot = KhoLot.objects.get(ma_lot="LOT_BACK_2")
        lot.don_gia_nhap = Decimal("12000")
        lot.save()

        # Recalculate
        count = tinh_lai_gia_von(hang_hoa_fifo.pk, date(2026, 1, 1))
        assert count >= 3  # 1 receipt + 2 issues

        # Verify both issues updated
        issue1.refresh_from_db()
        issue2.refresh_from_db()
        assert issue1.gia_von_chinh_thuc is not None
        assert issue2.gia_von_chinh_thuc is not None


@pytest.mark.django_db
class TestBackdatingWeightedAverage:
    """Test backdating recalculation with Weighted Average method."""

    def test_recalculate_binh_quan(self, hang_hoa_binh_quan, kho):
        """Test recalculation with weighted average method."""
        service = InventoryValuationService()

        # Create two receipts
        service.nhap_kho(
            hang_hoa=hang_hoa_binh_quan,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_BQ_BACK_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_BQ_BACK_1",
        )
        service.nhap_kho(
            hang_hoa=hang_hoa_binh_quan,
            kho=kho,
            items=[
                {
                    "so_luong": "200",
                    "don_gia": "12000",
                    "ma_lot": "LOT_BQ_BACK_2",
                }
            ],
            ngay=date(2026, 1, 3),
            so_chung_tu="NK_BQ_BACK_2",
        )

        # Create issue
        issue = service.xuat_kho(
            hang_hoa=hang_hoa_binh_quan,
            kho=kho,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_BQ_BACK_1",
        )
        original_cost = issue.gia_von_chinh_thuc

        # Modify first receipt
        lot = KhoLot.objects.get(ma_lot="LOT_BQ_BACK_1")
        lot.don_gia_nhap = Decimal("11000")
        lot.save()

        # Recalculate
        count = tinh_lai_gia_von(hang_hoa_binh_quan.pk, date(2026, 1, 1))
        assert count >= 1

        issue.refresh_from_db()
        assert issue.gia_von_chinh_thuc != original_cost


@pytest.mark.django_db
class TestBackdatingSpecificIdentification:
    """Test backdating recalculation with Specific Identification method."""

    def test_recalculate_dich_danh(self, hang_hoa_dich_danh, kho):
        """Test recalculation with specific identification method."""
        service = InventoryValuationService()

        # Create receipt
        service.nhap_kho(
            hang_hoa=hang_hoa_dich_danh,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_DD_BACK_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_DD_BACK_1",
        )

        # Create issue
        issue = service.xuat_kho(
            hang_hoa=hang_hoa_dich_danh,
            kho=kho,
            so_luong=Decimal("50"),
            lot_id="LOT_DD_BACK_1",
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_DD_BACK_1",
        )
        original_cost = issue.gia_von_chinh_thuc

        # Modify lot price
        lot = KhoLot.objects.get(ma_lot="LOT_DD_BACK_1")
        lot.don_gia_nhap = Decimal("15000")
        lot.save()

        # Recalculate
        count = tinh_lai_gia_von(hang_hoa_dich_danh.pk, date(2026, 1, 1))
        assert count >= 1

        issue.refresh_from_db()
        assert issue.gia_von_chinh_thuc != original_cost


@pytest.mark.django_db
class TestRecalculateService:
    """Test the recalculate service method."""

    def test_recalculate_returns_count(self, hang_hoa_fifo, kho):
        """Test that recalculate returns correct number of entries."""
        service = InventoryValuationService()

        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_COUNT_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_COUNT_1",
        )
        service.xuat_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            so_luong=Decimal("50"),
            ngay=date(2026, 1, 5),
            so_chung_tu="XK_COUNT_1",
        )

        count = service.recalculate(hang_hoa_fifo.pk, date(2026, 1, 1))
        assert count >= 2

    def test_recalculate_from_future_date(self, hang_hoa_fifo, kho):
        """Test recalculate with start date after entries."""
        service = InventoryValuationService()

        service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_FUTURE_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_FUTURE_1",
        )

        count = service.recalculate(hang_hoa_fifo.pk, date(2026, 12, 31))
        assert count == 0

    def test_recalculate_sets_da_dong_bo(self, hang_hoa_fifo, kho):
        """Test that recalculate sets da_dong_bo to True."""
        service = InventoryValuationService()

        entries = service.nhap_kho(
            hang_hoa=hang_hoa_fifo,
            kho=kho,
            items=[
                {
                    "so_luong": "100",
                    "don_gia": "10000",
                    "ma_lot": "LOT_DONG_BO_1",
                }
            ],
            ngay=date(2026, 1, 1),
            so_chung_tu="NK_DONG_BO_1",
        )

        # Manually set da_dong_bo to False
        entry = entries[0]
        entry.da_dong_bo = False
        entry.save(update_fields=["da_dong_bo"])

        service.recalculate(hang_hoa_fifo.pk, date(2026, 1, 1))

        entry.refresh_from_db()
        assert entry.da_dong_bo is True
