"""Inventory valuation strategies: FIFO, Weighted Average, Specific Identification."""

from decimal import Decimal
from typing import Dict, List

from .base import BaseValuationStrategy


class FIFOStrategy(BaseValuationStrategy):
    """
    First-In-First-Out valuation strategy.

    Consumes oldest lots first by ngay_nhap date.
    Splits quantities across multiple lots if needed.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    def calculate_gia_von_xuat(
        self,
        hang_hoa,
        so_luong_xuat: Decimal,
        lots: List,
    ) -> List[Dict]:
        """
        Calculate cost using FIFO method.

        Args:
            hang_hoa: VatTuHangHoa instance
            so_luong_xuat: Quantity to issue
            lots: List of KhoLot instances sorted by ngay_nhap

        Returns:
            List of dicts with lot_id, so_luong, don_gia, thanh_tien
        """
        if so_luong_xuat <= 0:
            return []

        sorted_lots = sorted(lots, key=lambda lot: (lot.ngay_nhap, lot.pk))
        result = []
        remaining = so_luong_xuat

        for lot in sorted_lots:
            if remaining <= 0:
                break

            if lot.so_luong_ton <= 0:
                continue

            qty = min(remaining, lot.so_luong_ton)
            cost = qty * lot.don_gia_nhap

            result.append(
                {
                    "lot_id": lot.pk,
                    "so_luong": qty,
                    "don_gia": lot.don_gia_nhap,
                    "thanh_tien": cost,
                }
            )
            remaining -= qty

        if remaining > 0:
            raise ValueError(
                f"Không đủ hàng tồn kho: cần {so_luong_xuat}, "
                f"chỉ có {so_luong_xuat - remaining}"
            )

        return result

    def update_ton_kho(
        self,
        hang_hoa,
        lot,
        so_luong: Decimal,
        current_ton: Dict = None,
    ) -> Dict:
        """
        Update inventory balance after receipt (FIFO).

        For FIFO, we simply add the new lot to the queue.

        Args:
            hang_hoa: VatTuHangHoa instance
            lot: KhoLot instance being received
            so_luong: Quantity received
            current_ton: Optional dict with current balance
                (so_luong_ton, gia_tri_ton)
        """
        if current_ton is None:
            current_ton = {"so_luong_ton": Decimal("0"), "gia_tri_ton": Decimal("0")}

        tong_so_luong = current_ton["so_luong_ton"] + so_luong
        tong_gia_tri = current_ton["gia_tri_ton"] + (so_luong * lot.don_gia_nhap)

        return {
            "so_luong_ton": tong_so_luong,
            "gia_tri_ton": tong_gia_tri,
            "don_gia_binh_quan": (
                tong_gia_tri / tong_so_luong if tong_so_luong > 0 else Decimal("0")
            ),
        }


class WeightedAverageStrategy(BaseValuationStrategy):
    """
    Perpetual weighted average valuation strategy.

    Formula: (ton_dau_gia_tri + nhap_moi_gia_tri) / (ton_dau_so_luong + nhap_moi_so_luong)
    Uses 4 decimal precision for unit price.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    def calculate_gia_von_xuat(
        self,
        hang_hoa,
        so_luong_xuat: Decimal,
        lots: List,
    ) -> List[Dict]:
        """
        Calculate cost using perpetual weighted average method.

        Args:
            hang_hoa: VatTuHangHoa instance
            so_luong_xuat: Quantity to issue
            lots: List of KhoLot instances

        Returns:
            List of dicts with lot_id, so_luong, don_gia, thanh_tien
        """
        if so_luong_xuat <= 0:
            return []

        tong_so_luong = sum(lot.so_luong_ton for lot in lots)
        tong_gia_tri = sum(lot.so_luong_ton * lot.don_gia_nhap for lot in lots)

        if tong_so_luong <= 0:
            raise ValueError("Không có hàng tồn kho để xuất")

        if so_luong_xuat > tong_so_luong:
            raise ValueError(
                f"Không đủ hàng tồn kho: cần {so_luong_xuat}, "
                f"chỉ có {tong_so_luong}"
            )

        don_gia_bq = (tong_gia_tri / tong_so_luong).quantize(Decimal("0.0001"))
        thanh_tien = (so_luong_xuat * don_gia_bq).quantize(Decimal("0.01"))

        # Return as single entry from aggregate lots
        first_lot = lots[0] if lots else None
        return [
            {
                "lot_id": first_lot.pk if first_lot else None,
                "so_luong": so_luong_xuat,
                "don_gia": don_gia_bq,
                "thanh_tien": thanh_tien,
            }
        ]

    def update_ton_kho(
        self,
        hang_hoa,
        lot,
        so_luong: Decimal,
        current_ton: Dict = None,
    ) -> Dict:
        """
        Update inventory balance after receipt (Weighted Average).

        Recalculates weighted average unit price.

        Args:
            hang_hoa: VatTuHangHoa instance
            lot: KhoLot instance being received
            so_luong: Quantity received
            current_ton: Optional dict with current balance
                (so_luong_ton, gia_tri_ton)
        """
        if current_ton is None:
            current_ton = {"so_luong_ton": Decimal("0"), "gia_tri_ton": Decimal("0")}

        tong_so_luong = current_ton["so_luong_ton"] + so_luong
        tong_gia_tri = current_ton["gia_tri_ton"] + (so_luong * lot.don_gia_nhap)

        don_gia_bq = (
            (tong_gia_tri / tong_so_luong).quantize(Decimal("0.0001"))
            if tong_so_luong > 0
            else Decimal("0")
        )

        return {
            "so_luong_ton": tong_so_luong,
            "gia_tri_ton": tong_gia_tri,
            "don_gia_binh_quan": don_gia_bq,
        }


class SpecificIdentificationStrategy(BaseValuationStrategy):
    """
    Specific Identification valuation strategy.

    Matches lot_id from issue to receipt exactly.
    Validates lot has sufficient quantity.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    def calculate_gia_von_xuat(
        self,
        hang_hoa,
        so_luong_xuat: Decimal,
        lots: List,
    ) -> List[Dict]:
        """
        Calculate cost using specific identification method.

        Args:
            hang_hoa: VatTuHangHoa instance
            so_luong_xuat: Quantity to issue
            lots: List of KhoLot instances (should contain exactly the target lot)

        Returns:
            List of dicts with lot_id, so_luong, don_gia, thanh_tien
        """
        if so_luong_xuat <= 0:
            return []

        if not lots:
            raise ValueError("Không có lô hàng được chỉ định")

        result = []
        remaining = so_luong_xuat

        for lot in lots:
            if remaining <= 0:
                break

            if lot.so_luong_ton <= 0:
                raise ValueError(f"Lô {lot.ma_lot} không còn hàng tồn")

            qty = min(remaining, lot.so_luong_ton)
            cost = qty * lot.don_gia_nhap

            result.append(
                {
                    "lot_id": lot.pk,
                    "so_luong": qty,
                    "don_gia": lot.don_gia_nhap,
                    "thanh_tien": cost,
                }
            )
            remaining -= qty

        if remaining > 0:
            raise ValueError(
                f"Không đủ hàng trong lô được chỉ định: "
                f"cần {so_luong_xuat}, chỉ có {so_luong_xuat - remaining}"
            )

        return result

    def update_ton_kho(
        self,
        hang_hoa,
        lot,
        so_luong: Decimal,
        current_ton: Dict = None,
    ) -> Dict:
        """
        Update inventory balance after receipt (Specific Identification).

        Each lot is tracked independently.

        Args:
            hang_hoa: VatTuHangHoa instance
            lot: KhoLot instance being received
            so_luong: Quantity received
            current_ton: Optional dict with current balance
                (so_luong_ton, gia_tri_ton)
        """
        if current_ton is None:
            current_ton = {"so_luong_ton": Decimal("0"), "gia_tri_ton": Decimal("0")}

        tong_so_luong = current_ton["so_luong_ton"] + so_luong
        tong_gia_tri = current_ton["gia_tri_ton"] + (so_luong * lot.don_gia_nhap)

        return {
            "so_luong_ton": tong_so_luong,
            "gia_tri_ton": tong_gia_tri,
            "don_gia_binh_quan": (
                tong_gia_tri / tong_so_luong if tong_so_luong > 0 else Decimal("0")
            ),
        }
