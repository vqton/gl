"""Year-end closing service (Kết chuyển TK 911).

Legal basis:
    - Thông tư 99/2025/TT-BTC on year-end closing
    - Chế độ kế toán doanh nghiệp nhỏ và vừa
    - TK 911 (Xác định kết quả kinh doanh)
    - TK 421 (Lợi nhuận chưa phân phối)

Closing flow:
    1. Close revenue accounts (TK 5, 7) → Có 911
    2. Close expense accounts (TK 6, 8) → Nợ 911
    3. Close TK 911 → TK 421 (profit or loss)
"""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from django.db import transaction
from django.db.models import Sum

from apps.nghiep_vu.models import ButToan, ButToanChiTiet
from apps.nghiep_vu.services import tao_but_toan

logger = logging.getLogger(__name__)

# Account groups for closing
DOANH_THU_ACCOUNTS = ["511", "515", "711"]  # Revenue, financial income, other income
CHI_PHI_ACCOUNTS = [
    "632",
    "641",
    "642",
    "635",
    "811",
]  # COGS, selling, admin, financial, other expense


def get_tong_phatsinh(
    ma_tai_khoan: str,
    tu_ngay: date,
    den_ngay: date,
) -> Tuple[Decimal, Decimal]:
    """
    Get total debit/credit turnover for an account in a period.

    Args:
        ma_tai_khoan: Account code
        tu_ngay: Start date
        den_ngay: End date

    Returns:
        Tuple of (no_tong, co_tong)
    """
    but_toan_ids = ButToan.objects.filter(
        ngay_hach_toan__gte=tu_ngay,
        ngay_hach_toan__lte=den_ngay,
    ).values_list("pk", flat=True)

    chi_tiet = ButToanChiTiet.objects.filter(
        but_toan_id__in=but_toan_ids,
        tai_khoan__ma_tai_khoan=ma_tai_khoan,
    )

    no_tong = chi_tiet.filter(loai_no_co="no").aggregate(total=Sum("so_tien"))[
        "total"
    ] or Decimal("0")
    co_tong = chi_tiet.filter(loai_no_co="co").aggregate(total=Sum("so_tien"))[
        "total"
    ] or Decimal("0")

    return no_tong, co_tong


@transaction.atomic
def ket_chuyen_cuoi_ky(
    tu_ngay: date,
    den_ngay: date,
    nam: Optional[int] = None,
) -> Dict:
    """
    Execute year-end closing entries.

    Step 1: Close revenue accounts (TK 5, 7) to TK 911
        Nợ 511/515/711 / Có 911

    Step 2: Close expense accounts (TK 6, 8) to TK 911
        Nợ 911 / Có 632/641/642/635/811

    Step 3: Close TK 911 to TK 421
        If profit: Nợ 911 / Có 421
        If loss: Nợ 421 / Có 911

    Legal basis:
        - Thông tư 99/2025/TT-BTC on year-end closing
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        tu_ngay: Start date of closing period
        den_ngay: End date of closing period
        nam: Year (for voucher numbering, defaults to den_ngay.year)

    Returns:
        Dict with:
            - doanh_thu: Total revenue closed
            - chi_phi: Total expense closed
            - loi_nhuan: Net profit/loss (positive = profit)
            - but_toan_list: List of created ButToan instances
    """
    if nam is None:
        nam = den_ngay.year

    result = {
        "doanh_thu": Decimal("0"),
        "chi_phi": Decimal("0"),
        "loi_nhuan": Decimal("0"),
        "but_toan_list": [],
    }

    # Step 1: Close revenue accounts to 911
    chi_tiet_revenue = []
    tong_doanh_thu = Decimal("0")

    for tk in DOANH_THU_ACCOUNTS:
        no_tong, co_tong = get_tong_phatsinh(tk, tu_ngay, den_ngay)
        # Revenue accounts have credit balance, so we debit to close
        if co_tong > Decimal("0"):
            chi_tiet_revenue.append(
                {
                    "tai_khoan": tk,
                    "loai_no_co": "no",
                    "so_tien": co_tong,
                    "dien_giai": f"Kết chuyển {tk}",
                }
            )
            tong_doanh_thu += co_tong

    if chi_tiet_revenue:
        chi_tiet_revenue.append(
            {
                "tai_khoan": "911",
                "loai_no_co": "co",
                "so_tien": tong_doanh_thu,
                "dien_giai": "Kết chuyển doanh thu",
            }
        )
        bt_revenue = tao_but_toan(
            ngay=den_ngay,
            dien_giai=f"Kết chuyển doanh thu kỳ {tu_ngay} - {den_ngay}",
            chi_tiet=chi_tiet_revenue,
            so_but_toan=f"BT-KC-DT{nam:04d}",
        )
        result["but_toan_list"].append(bt_revenue)

    # Step 2: Close expense accounts to 911
    chi_tiet_expense = []
    tong_chi_phi = Decimal("0")

    for tk in CHI_PHI_ACCOUNTS:
        no_tong, co_tong = get_tong_phatsinh(tk, tu_ngay, den_ngay)
        # Expense accounts have debit balance, so we credit to close
        if no_tong > Decimal("0"):
            chi_tiet_expense.append(
                {
                    "tai_khoan": tk,
                    "loai_no_co": "co",
                    "so_tien": no_tong,
                    "dien_giai": f"Kết chuyển {tk}",
                }
            )
            tong_chi_phi += no_tong

    if chi_tiet_expense:
        chi_tiet_expense.append(
            {
                "tai_khoan": "911",
                "loai_no_co": "no",
                "so_tien": tong_chi_phi,
                "dien_giai": "Kết chuyển chi phí",
            }
        )
        bt_expense = tao_but_toan(
            ngay=den_ngay,
            dien_giai=f"Kết chuyển chi phí kỳ {tu_ngay} - {den_ngay}",
            chi_tiet=chi_tiet_expense,
            so_but_toan=f"BT-KC-CP{nam:04d}",
        )
        result["but_toan_list"].append(bt_expense)

    # Step 3: Close TK 911 to TK 421
    # Get TK 911 balance after steps 1 and 2
    no_911, co_911 = get_tong_phatsinh("911", tu_ngay, den_ngay)
    loi_nhuan = co_911 - no_911

    if loi_nhuan != Decimal("0"):
        if loi_nhuan > Decimal("0"):
            # Profit: Nợ 911 / Có 421
            chi_tiet_profit = [
                {
                    "tai_khoan": "911",
                    "loai_no_co": "no",
                    "so_tien": loi_nhuan,
                    "dien_giai": "Lợi nhuận ròng",
                },
                {
                    "tai_khoan": "421",
                    "loai_no_co": "co",
                    "so_tien": loi_nhuan,
                    "dien_giai": "Lợi nhuận chưa phân phối",
                },
            ]
        else:
            # Loss: Nợ 421 / Có 911
            lo_rong = abs(loi_nhuan)
            chi_tiet_profit = [
                {
                    "tai_khoan": "421",
                    "loai_no_co": "no",
                    "so_tien": lo_rong,
                    "dien_giai": "Lỗ ròng",
                },
                {
                    "tai_khoan": "911",
                    "loai_no_co": "co",
                    "so_tien": lo_rong,
                    "dien_giai": "Kết chuyển lỗ",
                },
            ]

        bt_profit = tao_but_toan(
            ngay=den_ngay,
            dien_giai=f"Kết chuyển lãi/lỗ kỳ {tu_ngay} - {den_ngay}",
            chi_tiet=chi_tiet_profit,
            so_but_toan=f"BT-KC-LN{nam:04d}",
        )
        result["but_toan_list"].append(bt_profit)

    result["doanh_thu"] = tong_doanh_thu
    result["chi_phi"] = tong_chi_phi
    result["loi_nhuan"] = loi_nhuan

    logger.info(
        "Year-end closing %s - %s: DT=%s, CP=%s, LN=%s, entries=%d",
        tu_ngay,
        den_ngay,
        tong_doanh_thu,
        tong_chi_phi,
        loi_nhuan,
        len(result["but_toan_list"]),
    )
    return result
