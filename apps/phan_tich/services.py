"""Phân Tích Tài Chính (Financial Analysis) services."""

import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional

from apps.bao_cao.services import (
    lap_bang_can_doi_ke_toan,
    lap_bao_cao_kq_kinh_doanh,
    lap_bao_cao_luu_chuyen_tien_te,
)

logger = logging.getLogger(__name__)


def _safe_div(numerator: Decimal, denominator: Decimal, default: Decimal = Decimal("0")) -> Decimal:
    """
    Safe division returning default when denominator is zero.

    Args:
        numerator: Numerator
        denominator: Denominator
        default: Value to return if denominator is zero

    Returns:
        Result of division or default
    """
    if denominator == Decimal("0"):
        return default
    return (numerator / denominator).quantize(Decimal("0.0001"))


class PhanTichTaiChinhService:
    """
    Financial analysis service calculating key ratios.

    Legal basis:
        - Thông tư 99/2025/TT-BTC
        - Chuẩn mực kế toán Việt Nam

    Ratio categories:
        1. Liquidity (Khả năng thanh toán)
        2. Solvency (Khả năng cân đối vốn)
        3. Activity (Hiệu quả hoạt động)
        4. Profitability (Khả năng sinh lời)
        5. Cash Flow (Dòng tiền)
    """

    def __init__(self, tu_ngay: date, den_ngay: date):
        """
        Initialize with analysis period.

        Args:
            tu_ngay: Start date of analysis period
            den_ngay: End date of analysis period
        """
        self.tu_ngay = tu_ngay
        self.den_ngay = den_ngay

    def _get_bang_can_doi(self) -> Dict:
        """Get balance sheet data."""
        return lap_bang_can_doi_ke_toan(self.den_ngay)

    def _get_kq_kd(self) -> Dict:
        """Get P&L data."""
        return lap_bao_cao_kq_kinh_doanh(self.tu_ngay, self.den_ngay)

    def _get_luu_chuyen_tien_te(self) -> Dict:
        """Get cash flow data."""
        return lap_bao_cao_luu_chuyen_tien_te(self.tu_ngay, self.den_ngay)

    def get_he_so_thanh_toan(self) -> Dict:
        """
        Calculate liquidity ratios.

        Returns:
            Dict with:
                - hien_hanh: Current ratio = Tài sản ngắn hạn / Nợ ngắn hạn
                - nhanh: Quick ratio = (Tài sản ngắn hạn - Hàng tồn kho) / Nợ ngắn hạn
                - tuc_thoi: Cash ratio = Tiền / Nợ ngắn hạn
        """
        bcd = self._get_bang_can_doi()

        tai_san_nh = bcd["tai_san"]["A"]["tong_cong"]
        no_ngan_han = bcd["nguon_von"]["C"]["tong_cong"]
        hang_ton_kho = bcd["tai_san"]["A"]["chi_tiet"]["140"]["so_tien"]
        tien = bcd["tai_san"]["A"]["chi_tiet"]["110"]["so_tien"]

        return {
            "hien_hanh": _safe_div(tai_san_nh, no_ngan_han),
            "nhanh": _safe_div(tai_san_nh - hang_ton_kho, no_ngan_han),
            "tuc_thoi": _safe_div(tien, no_ngan_han),
        }

    def get_he_so_no(self) -> Dict:
        """
        Calculate solvency ratios.

        Returns:
            Dict with:
                - he_so_no: Debt ratio = Nợ phải trả / Tổng tài sản
                - tu_tai_tro: Equity ratio = Vốn chủ sở hữu / Tổng tài sản
                - cau_truc_von: Debt-to-equity = Nợ dài hạn / Vốn chủ sở hữu
        """
        bcd = self._get_bang_can_doi()

        tong_tai_san = bcd["tong_tai_san"]
        tong_no = bcd["nguon_von"]["C"]["tong_cong"] + bcd["nguon_von"]["D"]["tong_cong"]
        von_chu_so_huu = bcd["nguon_von"]["E"]["tong_cong"]
        no_dai_han = bcd["nguon_von"]["D"]["tong_cong"]

        return {
            "he_so_no": _safe_div(tong_no, tong_tai_san),
            "tu_tai_tro": _safe_div(von_chu_so_huu, tong_tai_san),
            "cau_truc_von": _safe_div(no_dai_han, von_chu_so_huu),
        }

    def get_hieu_qua_hoat_dong(self) -> Dict:
        """
        Calculate activity ratios.

        Returns:
            Dict with:
                - vong_quay_ton_kho: Inventory turnover = Giá vốn / Tồn kho bình quân
                - ky_thu_tien: DSO = Phải thu bình quân × 365 / Doanh thu thuần
                - vong_quay_tai_san: Asset turnover = Doanh thu / Tổng tài sản bình quân
        """
        kqkd = self._get_kq_kd()
        bcd = self._get_bang_can_doi()

        gia_von = kqkd["chi_tiet"]["11"]["so_tien"]
        doanh_thu_thuan = kqkd["chi_tiet"]["10"]["so_tien"]
        hang_ton_kho = bcd["tai_san"]["A"]["chi_tiet"]["140"]["so_tien"]
        phai_thu = bcd["tai_san"]["A"]["chi_tiet"]["130"]["so_tien"]
        tong_tai_san = bcd["tong_tai_san"]

        return {
            "vong_quay_ton_kho": _safe_div(gia_von, hang_ton_kho),
            "ky_thu_tien": _safe_div(phai_thu * Decimal("365"), doanh_thu_thuan),
            "vong_quay_tai_san": _safe_div(doanh_thu_thuan, tong_tai_san),
        }

    def get_kha_nang_sinh_loi(self) -> Dict:
        """
        Calculate profitability ratios.

        Returns:
            Dict with:
                - bien_loi_nhuan_gop: Gross margin = Lợi nhuận gộp / Doanh thu thuần
                - bien_loi_nhuan_rong: Net margin = Lợi nhuận sau thuế / Doanh thu thuần
                - roa: Return on Assets = Lợi nhuận sau thuế / Tổng tài sản
                - roe: Return on Equity = Lợi nhuận sau thuế / Vốn chủ sở hữu
        """
        kqkd = self._get_kq_kd()
        bcd = self._get_bang_can_doi()

        loi_nhuan_gop = kqkd["chi_tiet"]["20"]["so_tien"]
        loi_nhuan_rong = kqkd["chi_tiet"]["80"]["so_tien"]
        doanh_thu_thuan = kqkd["chi_tiet"]["10"]["so_tien"]
        tong_tai_san = bcd["tong_tai_san"]
        von_chu_so_huu = bcd["nguon_von"]["E"]["tong_cong"]

        return {
            "bien_loi_nhuan_gop": _safe_div(loi_nhuan_gop, doanh_thu_thuan),
            "bien_loi_nhuan_rong": _safe_div(loi_nhuan_rong, doanh_thu_thuan),
            "roa": _safe_div(loi_nhuan_rong, tong_tai_san),
            "roe": _safe_div(loi_nhuan_rong, von_chu_so_huu),
        }

    def get_dong_tien(self) -> Dict:
        """
        Calculate cash flow indicators.

        Returns:
            Dict with:
                - cfo: Cash flow from operations
                - free_cash_flow: FCF = CFO - CapEx
                - ty_le_dong_tien: Cash flow / Profit ratio
        """
        lctt = self._get_luu_chuyen_tien_te()
        kqkd = self._get_kq_kd()

        cfo = lctt["I"]["luu_chuyen_thuan"]
        capex = lctt["II"]["tong_chi"]
        loi_nhuan = kqkd["chi_tiet"]["80"]["so_tien"]

        return {
            "cfo": cfo,
            "free_cash_flow": cfo - capex,
            "ty_le_dong_tien": _safe_div(cfo, loi_nhuan) if loi_nhuan > Decimal("0") else Decimal("0"),
        }

    def get_bang_tong_hop(self) -> Dict:
        """
        Return all ratios in one dict for dashboard.

        Returns:
            Dict with period, all ratio categories, health assessment
        """
        return {
            "period": {
                "tu_ngay": self.tu_ngay.isoformat(),
                "den_ngay": self.den_ngay.isoformat(),
            },
            "ratios": {
                "thanh_toan": self.get_he_so_thanh_toan(),
                "no": self.get_he_so_no(),
                "hoat_dong": self.get_hieu_qua_hoat_dong(),
                "sinh_loi": self.get_kha_nang_sinh_loi(),
                "dong_tien": self.get_dong_tien(),
            },
            "health": self.get_suc_khoe_doanh_nghiep(),
        }

    def get_trend_data(self, so_ky: int = 4) -> Dict:
        """
        Return multi-period trend data for charts.

        Args:
            so_ky: Number of periods to look back

        Returns:
            Dict with period labels and ratio values for each period
        """
        from datetime import date as date_cls

        periods = []
        current_year = self.den_ngay.year
        current_month = self.den_ngay.month

        for i in range(so_ky):
            month = current_month - i
            year = current_year
            while month <= 0:
                month += 12
                year -= 1

            tu = date_cls(year, month, 1)
            if month == 12:
                den = date_cls(year + 1, 1, 1) - timedelta(days=1)
            else:
                den = date_cls(year, month + 1, 1) - timedelta(days=1)

            service = PhanTichTaiChinhService(tu_ngay=tu, den_ngay=den)
            try:
                ratios = service.get_bang_tong_hop()
                periods.append({
                    "label": f"T{month}/{year}",
                    "roa": float(ratios["ratios"]["sinh_loi"]["roa"]),
                    "roe": float(ratios["ratios"]["sinh_loi"]["roe"]),
                    "current_ratio": float(ratios["ratios"]["thanh_toan"]["hien_hanh"]),
                    "debt_ratio": float(ratios["ratios"]["no"]["he_so_no"]),
                })
            except Exception:
                periods.append({
                    "label": f"T{month}/{year}",
                    "roa": 0,
                    "roe": 0,
                    "current_ratio": 0,
                    "debt_ratio": 0,
                })

        periods.reverse()
        return {"periods": periods}

    def get_suc_khoe_doanh_nghiep(self) -> Dict:
        """
        Return overall health score and rating.

        Scoring:
            - Current ratio > 1.5: +15 points
            - Quick ratio > 1.0: +10 points
            - Debt ratio < 0.5: +15 points
            - ROA > 0.05: +15 points
            - ROE > 0.10: +15 points
            - Gross margin > 0.20: +15 points
            - DSO < 60 days: +15 points

        Returns:
            Dict with score (0-100), rating, and warnings
        """
        score = 0
        warnings = []

        thanh_toan = self.get_he_so_thanh_toan()
        no = self.get_he_so_no()
        hoat_dong = self.get_hieu_qua_hoat_dong()
        sinh_loi = self.get_kha_nang_sinh_loi()

        if thanh_toan["hien_hanh"] > Decimal("1.5"):
            score += 15
        else:
            warnings.append("Hệ số thanh toán hiện hành < 1.5")

        if thanh_toan["nhanh"] > Decimal("1.0"):
            score += 10
        else:
            warnings.append("Hệ số thanh toán nhanh < 1.0")

        if no["he_so_no"] < Decimal("0.5"):
            score += 15
        else:
            warnings.append("Hệ số nợ > 50%")

        if sinh_loi["roa"] > Decimal("0.05"):
            score += 15
        else:
            warnings.append("ROA < 5%")

        if sinh_loi["roe"] > Decimal("0.10"):
            score += 15
        else:
            warnings.append("ROE < 10%")

        if sinh_loi["bien_loi_nhuan_gop"] > Decimal("0.20"):
            score += 15
        else:
            warnings.append("Biên lợi nhuận gộp < 20%")

        if hoat_dong["ky_thu_tien"] < Decimal("60"):
            score += 15
        else:
            warnings.append("Kỳ thu tiền > 60 ngày")

        if score >= 80:
            rating = "Tốt"
        elif score >= 60:
            rating = "Khá"
        elif score >= 40:
            rating = "Trung bình"
        else:
            rating = "Yếu"

        return {
            "score": score,
            "rating": rating,
            "warnings": warnings,
        }
