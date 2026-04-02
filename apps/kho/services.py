"""Inventory service layer for goods receipt, issue, transfer, and recalculation."""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, List, Tuple

from django.db import transaction

from apps.kho.constants import LOAI_CHUNG_TU_KHO, LOAI_KHO_ENTRY
from apps.kho.models import Kho, KhoEntry, KhoLot, TonKho, VatTuHangHoa
from apps.kho.valuation.strategies import (
    FIFOStrategy,
    SpecificIdentificationStrategy,
    WeightedAverageStrategy,
)

logger = logging.getLogger(__name__)


class InventoryValuationService:
    """
    Main service for inventory operations.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Inventory valuation
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    def __init__(self):
        self.strategies = {
            "FIFO": FIFOStrategy(),
            "BINH_QUAN": WeightedAverageStrategy(),
            "DICH_DANH": SpecificIdentificationStrategy(),
        }

    def get_strategy(self, phuong_phap: str):
        """
        Get valuation strategy by method name.

        Args:
            phuong_phap: One of 'FIFO', 'BINH_QUAN', 'DICH_DANH'

        Returns:
            BaseValuationStrategy instance
        """
        strategy = self.strategies.get(phuong_phap)
        if not strategy:
            raise ValueError(f"Phương pháp tính giá không hợp lệ: {phuong_phap}")
        return strategy

    @transaction.atomic
    def nhap_kho(
        self,
        hang_hoa: VatTuHangHoa,
        kho: Kho,
        items: List[Dict],
        ngay: date,
        so_chung_tu: str,
    ) -> List[KhoEntry]:
        """
        Process goods receipt, update lots and balances.

        Args:
            hang_hoa: VatTuHangHoa instance
            kho: Kho instance
            items: List of dicts with keys:
                - so_luong: Quantity received
                - don_gia: Unit price
                - ma_lot: Optional lot code
                - han_dung: Optional expiry date
            ngay: Receipt date
            so_chung_tu: Receipt document number

        Returns:
            List of created KhoEntry instances
        """
        entries = []
        strategy = self.get_strategy(hang_hoa.phuong_phap_tinh_gia)

        for item in items:
            so_luong = Decimal(str(item["so_luong"]))
            don_gia = Decimal(str(item["don_gia"]))
            ma_lot = item.get("ma_lot")
            han_dung = item.get("han_dung")

            # Create or update lot
            lot = None
            if ma_lot:
                lot, _ = KhoLot.objects.update_or_create(
                    ma_lot=ma_lot,
                    defaults={
                        "hang_hoa": hang_hoa,
                        "ngay_nhap": ngay,
                        "so_luong_nhap": so_luong,
                        "so_luong_ton": so_luong,
                        "don_gia_nhap": don_gia,
                        "han_dung": han_dung,
                    },
                )
            else:
                lot = KhoLot.objects.create(
                    ma_lot=f"AUTO-{hang_hoa.pk}-{ngay}-{len(entries)}",
                    hang_hoa=hang_hoa,
                    ngay_nhap=ngay,
                    so_luong_nhap=so_luong,
                    so_luong_ton=so_luong,
                    don_gia_nhap=don_gia,
                    han_dung=han_dung,
                )

            # Create inventory entry
            entry = KhoEntry.objects.create(
                hang_hoa=hang_hoa,
                kho=kho,
                loai=LOAI_KHO_ENTRY[0][0],  # 'NHAP'
                ngay_chung_tu=ngay,
                so_chung_tu=so_chung_tu,
                loai_chung_tu="NK",
                so_luong=so_luong,
                don_gia=don_gia,
                thanh_tien=so_luong * don_gia,
                gia_von_tam_tinh=so_luong * don_gia,
                gia_von_chinh_thuc=so_luong * don_gia,
                lot=lot,
                da_dong_bo=True,
            )
            entries.append(entry)

            # Update ton kho
            self._update_ton_kho_balance(hang_hoa, kho, so_luong, don_gia)

            # Update strategy-specific state
            strategy.update_ton_kho(hang_hoa, lot, so_luong)

        logger.info(
            "Nhập kho: %s - %s - %d items",
            so_chung_tu,
            hang_hoa,
            len(entries),
        )
        return entries

    @transaction.atomic
    def xuat_kho(
        self,
        hang_hoa: VatTuHangHoa,
        kho: Kho,
        so_luong: Decimal,
        lot_id: str = None,
        ngay: date = None,
        so_chung_tu: str = "",
    ) -> KhoEntry:
        """
        Process goods issue using configured valuation method.

        Args:
            hang_hoa: VatTuHangHoa instance
            kho: Kho instance
            so_luong: Quantity to issue
            lot_id: Specific lot code (for DICH_DANH method)
            ngay: Issue date
            so_chung_tu: Issue document number

        Returns:
            Created KhoEntry instance
        """
        so_luong = Decimal(str(so_luong))
        strategy = self.get_strategy(hang_hoa.phuong_phap_tinh_gia)

        # Get available lots for this item in this warehouse
        lots = KhoLot.objects.filter(
            hang_hoa=hang_hoa,
            so_luong_ton__gt=0,
        ).order_by("ngay_nhap", "pk")

        # For specific identification, filter by lot_id
        if hang_hoa.phuong_phap_tinh_gia == "DICH_DANH" and lot_id:
            lots = lots.filter(ma_lot=lot_id)

        # Calculate cost
        cost_breakdown = strategy.calculate_gia_von_xuat(hang_hoa, so_luong, list(lots))

        # Update lot quantities
        total_cost = Decimal("0")
        for cost_item in cost_breakdown:
            lot = KhoLot.objects.get(pk=cost_item["lot_id"])
            lot.so_luong_ton -= cost_item["so_luong"]
            lot.save(update_fields=["so_luong_ton", "updated_at"])
            total_cost += cost_item["thanh_tien"]

        # Calculate average unit price for the issue
        avg_don_gia = total_cost / so_luong if so_luong > 0 else Decimal("0")

        # Create inventory entry
        entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho,
            loai=LOAI_KHO_ENTRY[1][0],  # 'XUAT'
            ngay_chung_tu=ngay,
            so_chung_tu=so_chung_tu,
            loai_chung_tu="XK",
            so_luong=so_luong,
            don_gia=avg_don_gia,
            thanh_tien=total_cost,
            gia_von_tam_tinh=total_cost,
            gia_von_chinh_thuc=total_cost,
            lot=KhoLot.objects.filter(ma_lot=lot_id).first() if lot_id else None,
            da_dong_bo=True,
        )

        # Update ton kho
        self._update_ton_kho_balance(hang_hoa, kho, -so_luong, avg_don_gia)

        logger.info(
            "Xuất kho: %s - %s - SL: %s",
            so_chung_tu,
            hang_hoa,
            so_luong,
        )
        return entry

    @transaction.atomic
    def dieu_chuyen(
        self,
        hang_hoa: VatTuHangHoa,
        kho_nguon: Kho,
        kho_dich: Kho,
        so_luong: Decimal,
        ngay: date,
        dien_giai: str = "",
    ) -> Tuple[KhoEntry, KhoEntry]:
        """
        Transfer goods between warehouses.

        Args:
            hang_hoa: VatTuHangHoa instance
            kho_nguon: Source warehouse
            kho_dich: Destination warehouse
            so_luong: Quantity to transfer
            ngay: Transfer date
            dien_giai: Description

        Returns:
            Tuple of (out_entry, in_entry)
        """
        so_luong = Decimal(str(so_luong))
        so_chung_tu = f"DC-{ngay}-{hang_hoa.pk}"

        # Issue from source
        out_entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho_nguon,
            loai=LOAI_KHO_ENTRY[1][0],  # 'XUAT'
            ngay_chung_tu=ngay,
            so_chung_tu=so_chung_tu,
            loai_chung_tu="DC",
            so_luong=so_luong,
            don_gia=Decimal("0"),
            thanh_tien=Decimal("0"),
            dien_giai=dien_giai,
            da_dong_bo=True,
        )

        # Receive at destination
        in_entry = KhoEntry.objects.create(
            hang_hoa=hang_hoa,
            kho=kho_dich,
            loai=LOAI_KHO_ENTRY[0][0],  # 'NHAP'
            ngay_chung_tu=ngay,
            so_chung_tu=so_chung_tu,
            loai_chung_tu="DC",
            so_luong=so_luong,
            don_gia=Decimal("0"),
            thanh_tien=Decimal("0"),
            dien_giai=dien_giai,
            da_dong_bo=True,
        )

        # Update ton kho
        self._update_ton_kho_balance(hang_hoa, kho_nguon, -so_luong, Decimal("0"))
        self._update_ton_kho_balance(hang_hoa, kho_dich, so_luong, Decimal("0"))

        logger.info(
            "Điều chuyển: %s -> %s - %s",
            kho_nguon,
            kho_dich,
            hang_hoa,
        )
        return out_entry, in_entry

    def recalculate(
        self,
        hang_hoa_id: int,
        start_date: date,
    ) -> int:
        """
        Recalculate cost from a given date point.

        Finds all entries for the item from start_date onwards
        and recalculates gia_von_chinh_thuc.

        Args:
            hang_hoa_id: VatTuHangHoa primary key
            start_date: Date from which to recalculate

        Returns:
            Number of entries recalculated
        """
        hang_hoa = VatTuHangHoa.objects.get(pk=hang_hoa_id)
        strategy = self.get_strategy(hang_hoa.phuong_phap_tinh_gia)

        # Get all entries from start_date onwards, ordered by date
        entries = KhoEntry.objects.filter(
            hang_hoa_id=hang_hoa_id,
            ngay_chung_tu__gte=start_date,
        ).order_by("ngay_chung_tu", "created_at")

        recalculated_count = 0

        for entry in entries:
            if entry.loai == LOAI_KHO_ENTRY[0][0]:  # 'NHAP'
                # Receipt: cost is known
                entry.gia_von_chinh_thuc = entry.thanh_tien
                entry.da_dong_bo = True
                entry.save(
                    update_fields=["gia_von_chinh_thuc", "da_dong_bo", "updated_at"]
                )
                recalculated_count += 1
            else:
                # Issue: recalculate cost based on current lots
                lots = KhoLot.objects.filter(
                    hang_hoa=hang_hoa,
                    so_luong_ton__gt=0,
                ).order_by("ngay_nhap", "pk")

                try:
                    cost_breakdown = strategy.calculate_gia_von_xuat(
                        hang_hoa, entry.so_luong, list(lots)
                    )
                    total_cost = sum(item["thanh_tien"] for item in cost_breakdown)
                    entry.gia_von_chinh_thuc = total_cost
                    entry.da_dong_bo = True
                    entry.save(
                        update_fields=["gia_von_chinh_thuc", "da_dong_bo", "updated_at"]
                    )
                    recalculated_count += 1
                except ValueError:
                    logger.warning(
                        "Không thể tính lại giá vốn cho entry %s",
                        entry.pk,
                    )

        logger.info(
            "Recalculate: hang_hoa_id=%s, start_date=%s, recalculated=%d",
            hang_hoa_id,
            start_date,
            recalculated_count,
        )
        return recalculated_count

    def get_ton_kho_thoi_diem(
        self,
        hang_hoa: VatTuHangHoa,
        kho: Kho,
        ngay: date,
    ) -> Dict:
        """
        Get inventory balance at a specific date.

        Args:
            hang_hoa: VatTuHangHoa instance
            kho: Kho instance
            ngay: Date to check balance

        Returns:
            Dict with keys:
                - so_luong_ton: Quantity on hand
                - gia_tri_ton: Value on hand
                - don_gia_binh_quan: Average unit price
        """
        entries = KhoEntry.objects.filter(
            hang_hoa=hang_hoa,
            kho=kho,
            ngay_chung_tu__lte=ngay,
        ).order_by("ngay_chung_tu", "created_at")

        so_luong_ton = Decimal("0")
        gia_tri_ton = Decimal("0")

        for entry in entries:
            if entry.loai == LOAI_KHO_ENTRY[0][0]:  # 'NHAP'
                so_luong_ton += entry.so_luong
                gia_tri_ton += entry.thanh_tien
            else:  # 'XUAT'
                so_luong_ton -= entry.so_luong
                cost = entry.gia_von_chinh_thuc or entry.gia_von_tam_tinh
                if cost:
                    gia_tri_ton -= cost

        don_gia_bq = gia_tri_ton / so_luong_ton if so_luong_ton > 0 else Decimal("0")

        return {
            "so_luong_ton": so_luong_ton,
            "gia_tri_ton": gia_tri_ton,
            "don_gia_binh_quan": don_gia_bq.quantize(Decimal("0.0001")),
        }

    def _update_ton_kho_balance(
        self,
        hang_hoa: VatTuHangHoa,
        kho: Kho,
        so_luong: Decimal,
        don_gia: Decimal,
    ) -> None:
        """
        Update TonKho balance for a specific item and warehouse.

        Args:
            hang_hoa: VatTuHangHoa instance
            kho: Kho instance
            so_luong: Quantity change (positive for in, negative for out)
            don_gia: Unit price
        """
        ton, created = TonKho.objects.get_or_create(
            hang_hoa=hang_hoa,
            kho=kho,
        )

        ton.so_luong_ton += so_luong
        if so_luong > 0:
            ton.gia_tri_ton += so_luong * don_gia
        else:
            # For issues, reduce value proportionally
            if ton.so_luong_ton + abs(so_luong) > 0:
                ratio = abs(so_luong) / (ton.so_luong_ton + abs(so_luong))
                ton.gia_tri_ton -= ton.gia_tri_ton * ratio
            else:
                ton.gia_tri_ton = Decimal("0")

        ton.save(update_fields=["so_luong_ton", "gia_tri_ton", "ngay_cap_nhat_cuoi"])


def tinh_lai_gia_von(hang_hoa_id: int, start_date: date) -> int:
    """
    Module-level function to trigger recalculation.

    Called by signals when past entries are modified.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Inventory valuation
        - Chuẩn mực kế toán Việt Nam VAS 02

    Args:
        hang_hoa_id: Goods/item ID
        start_date: Date from which to recalculate

    Returns:
        Number of entries recalculated
    """
    service = InventoryValuationService()
    return service.recalculate(hang_hoa_id, start_date)
