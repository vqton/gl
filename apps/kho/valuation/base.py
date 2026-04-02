"""Base valuation strategy abstract class."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List


class BaseValuationStrategy(ABC):
    """
    Abstract base for inventory valuation methods.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Inventory valuation
        - Chuẩn mực kế toán Việt Nam VAS 02
    """

    @abstractmethod
    def calculate_gia_von_xuat(
        self,
        hang_hoa,
        so_luong_xuat: Decimal,
        lots: List,
    ) -> List[Dict]:
        """
        Calculate cost of goods issued.

        Args:
            hang_hoa: VatTuHangHoa instance
            so_luong_xuat: Quantity to issue
            lots: List of KhoLot instances with available stock

        Returns:
            List of dicts with keys:
                - lot_id: Primary key of the lot
                - so_luong: Quantity taken from this lot
                - don_gia: Unit price from this lot
                - thanh_tien: Total cost for this portion
        """
        pass

    @abstractmethod
    def update_ton_kho(self, hang_hoa, lot, so_luong: Decimal) -> Dict:
        """
        Update inventory balance after receipt.

        Args:
            hang_hoa: VatTuHangHoa instance
            lot: KhoLot instance being received
            so_luong: Quantity received

        Returns:
            Dict with updated inventory state:
                - so_luong_ton: Total quantity
                - gia_tri_ton: Total value
                - don_gia_binh_quan: Weighted average unit price (if applicable)
        """
        pass
