"""Payroll service layer (M7: Lương & BHXH)."""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from django.db import transaction

from apps.luong.constants import (
    BHXT_DN_BHXH,
    BHXT_DN_BHTN,
    BHXT_DN_BHTNLĐ_BNN,
    BHXT_DN_BHYT,
    BHXT_NLD_BHXH,
    BHXT_NLD_BHTN,
    BHXT_NLD_BHYT,
    BHXT_TONG_DN,
    BHXT_TONG_NLD,
    GIAM_TRU_BAN_THAN,
    GIAM_TRU_PHU_THUOC,
    MAX_LUONG_BHXH,
    THUE_TNCN_BRACKETS,
)
from apps.luong.models import BangLuong, NhanVien
from apps.nghiep_vu.services import tao_but_toan

logger = logging.getLogger(__name__)


def tinh_bhxh_nld(luong_dong_bhxh: Decimal) -> Dict[str, Decimal]:
    """
    Calculate employee social insurance contributions.

    Legal basis:
        - Nghị định 58/2020/NĐ-CP on social insurance rates
        - BHXH 8%, BHYT 1.5%, BHTN 1%

    Args:
        luong_dong_bhxh: Salary base for insurance (capped at 20x base)

    Returns:
        Dict with bhxh, bhyt, bhtn, tong
    """
    base = min(luong_dong_bhxh, MAX_LUONG_BHXH)
    bhxh = (base * BHXT_NLD_BHXH).quantize(Decimal("0.01"))
    bhyt = (base * BHXT_NLD_BHYT).quantize(Decimal("0.01"))
    bhtn = (base * BHXT_NLD_BHTN).quantize(Decimal("0.01"))
    return {
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "tong": bhxh + bhyt + bhtn,
    }


def tinh_bhxh_dn(luong_dong_bhxh: Decimal) -> Dict[str, Decimal]:
    """
    Calculate employer social insurance contributions.

    Legal basis:
        - Nghị định 58/2020/NĐ-CP on employer rates
        - BHXH 17.5%, BHYT 3%, BHTN 1%, BHTNLĐ-BNN 0.5%

    Args:
        luong_dong_bhxh: Salary base for insurance (capped at 20x base)

    Returns:
        Dict with bhxh, bhyt, bhtn, bhtnld_bnn, tong
    """
    base = min(luong_dong_bhxh, MAX_LUONG_BHXH)
    bhxh = (base * BHXT_DN_BHXH).quantize(Decimal("0.01"))
    bhyt = (base * BHXT_DN_BHYT).quantize(Decimal("0.01"))
    bhtn = (base * BHXT_DN_BHTN).quantize(Decimal("0.01"))
    bhtnld = (base * BHXT_DN_BHTNLĐ_BNN).quantize(Decimal("0.01"))
    return {
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "bhtnld_bnn": bhtnld,
        "tong": bhxh + bhyt + bhtn + bhtnld,
    }


def tinh_thue_tncn(thu_nhap_tinh_thue: Decimal) -> Decimal:
    """
    Calculate personal income tax (Thuế TNCN) using progressive brackets.

    Legal basis:
        - Luật 67/2025/QH15 on Personal Income Tax
        - Biểu thuế lũy tiến từng phần (7 brackets)

    Args:
        thu_nhap_tinh_thue: Taxable income after deductions

    Returns:
        Tax amount as Decimal
    """
    if thu_nhap_tinh_thue <= Decimal("0"):
        return Decimal("0")

    for i, (min_val, max_val, rate, deduct) in enumerate(THUE_TNCN_BRACKETS):
        if max_val is None or thu_nhap_tinh_thue < max_val:
            return (thu_nhap_tinh_thue * rate - deduct).quantize(Decimal("0.01"))

    # Should not reach here, but fallback to last bracket
    last = THUE_TNCN_BRACKETS[-1]
    return (thu_nhap_tinh_thue * last[2] - last[3]).quantize(Decimal("0.01"))


@transaction.atomic
def tao_bang_luong_thang(
    thang: int,
    nam: int,
    nhan_vien_ids: Optional[List[int]] = None,
) -> List[BangLuong]:
    """
    Generate monthly payroll for all active employees.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on payroll accounting
        - Nghị định 58/2020/NĐ-CP on social insurance

    Args:
        thang: Month (1-12)
        nam: Year
        nhan_vien_ids: Optional list of employee IDs (all active if None)

    Returns:
        List of created BangLuong instances
    """
    employees = NhanVien.objects.filter(trang_thai="dang_lam_viec")
    if nhan_vien_ids:
        employees = employees.filter(pk__in=nhan_vien_ids)

    records = []
    for nv in employees:
        existing = BangLuong.objects.filter(nhan_vien=nv, thang=thang, nam=nam).first()
        if existing:
            records.append(existing)
            continue

        luong_cb = nv.luong_co_ban
        phu_cap = luong_cb * nv.he_so_phu_cap
        tong_thu_nhap = luong_cb + phu_cap

        # BHXH calculations
        bhxh_nld = tinh_bhxh_nld(luong_cb)
        bhxh_dn = tinh_bhxh_dn(luong_cb)

        # Tax calculation
        giam_tru_gc = GIAM_TRU_BAN_THAN + GIAM_TRU_PHU_THUOC * nv.so_nguoi_phu_thuoc
        thu_nhap_tinh_thue = max(
            tong_thu_nhap - bhxh_nld["tong"] - giam_tru_gc, Decimal("0")
        )
        thue_tncn = tinh_thue_tncn(thu_nhap_tinh_thue)

        # Net salary
        thuc_linh = tong_thu_nhap - bhxh_nld["tong"] - thue_tncn

        record = BangLuong.objects.create(
            nhan_vien=nv,
            thang=thang,
            nam=nam,
            luong_co_ban=luong_cb,
            phu_cap=phu_cap,
            tong_thu_nhap=tong_thu_nhap,
            bhxh_nld=bhxh_nld["bhxh"],
            bhyt_nld=bhxh_nld["bhyt"],
            bhtn_nld=bhxh_nld["bhtn"],
            tong_bhxh_nld=bhxh_nld["tong"],
            thu_nhap_tinh_thue=thu_nhap_tinh_thue,
            thue_tncn=thue_tncn,
            thuc_linh=thuc_linh,
            bhxh_dn=bhxh_dn["bhxh"],
            bhyt_dn=bhxh_dn["bhyt"],
            bhtn_dn=bhxh_dn["bhtn"],
            bhtnld_bnn_dn=bhxh_dn["bhtnld_bnn"],
            tong_bhxh_dn=bhxh_dn["tong"],
        )
        records.append(record)

    logger.info(
        "Generated payroll for %d employees - %d/%d",
        len(records),
        thang,
        nam,
    )
    return records


@transaction.atomic
def tach_toan_luong(
    thang: int,
    nam: int,
) -> int:
    """
    Create journal entries for monthly payroll.

    Journal entries:
        1. Salary expense:
           Nợ 334 (Phải trả NLĐ)
           Có 111/112 (Tiền mặt/Tiền gửi)

        2. BHXH contributions:
           Nợ 642 (Chi phí QLDN)
           Có 3383 (BHXH phải nộp)
           Có 3384 (BHYT phải nộp)
           Có 3386 (BHTN phải nộp)

        3. TNCN withholding:
           Nợ 334 (Phải trả NLĐ)
           Có 3335 (Thuế TNCN phải nộp)

    Legal basis:
        - Thông tư 99/2025/TT-BTC on payroll journal entries
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        thang: Month (1-12)
        nam: Year

    Returns:
        Number of payroll records processed
    """
    records = BangLuong.objects.filter(
        thang=thang,
        nam=nam,
        da_hach_toan=False,
    )

    if not records.exists():
        return 0

    tong_thuc_linh = sum(r.thuc_linh for r in records)
    tong_bhxh_nld = sum(r.tong_bhxh_nld for r in records)
    tong_thue_tncn = sum(r.thue_tncn for r in records)
    tong_bhxh_dn = sum(r.tong_bhxh_dn for r in records)

    # Entry 1: Salary payment
    tao_but_toan(
        ngay=date(nam, thang, 28),
        dien_giai=f"Lương tháng {thang}/{nam}",
        chi_tiet=[
            {
                "tai_khoan": "334",
                "loai_no_co": "no",
                "so_tien": tong_thuc_linh,
                "dien_giai": f"Phải trả lương tháng {thang}/{nam}",
            },
            {
                "tai_khoan": "111",
                "loai_no_co": "co",
                "so_tien": tong_thuc_linh,
                "dien_giai": f"Chi lương tháng {thang}/{nam}",
            },
        ],
        so_but_toan=f"BT-LUONG{thang:02d}{nam}",
    )

    # Entry 2: Employer BHXH
    tao_but_toan(
        ngay=date(nam, thang, 28),
        dien_giai=f"BHXH DN tháng {thang}/{nam}",
        chi_tiet=[
            {
                "tai_khoan": "642",
                "loai_no_co": "no",
                "so_tien": tong_bhxh_dn,
                "dien_giai": f"Chi phí BHXH DN tháng {thang}/{nam}",
            },
            {
                "tai_khoan": "3383",
                "loai_no_co": "co",
                "so_tien": tong_bhxh_dn,
                "dien_giai": f"BHXH phải nộp tháng {thang}/{nam}",
            },
        ],
        so_but_toan=f"BT-BHXH{thang:02d}{nam}",
    )

    # Entry 3: TNCN withholding
    if tong_thue_tncn > Decimal("0"):
        tao_but_toan(
            ngay=date(nam, thang, 28),
            dien_giai=f"Thuế TNCN tháng {thang}/{nam}",
            chi_tiet=[
                {
                    "tai_khoan": "334",
                    "loai_no_co": "no",
                    "so_tien": tong_thue_tncn,
                    "dien_giai": f"Khấu trừ thuế TNCN tháng {thang}/{nam}",
                },
                {
                    "tai_khoan": "3335",
                    "loai_no_co": "co",
                    "so_tien": tong_thue_tncn,
                    "dien_giai": f"Thuế TNCN phải nộp tháng {thang}/{nam}",
                },
            ],
            so_but_toan=f"BT-TNCN{thang:02d}{nam}",
        )

    count = records.count()
    BangLuong.objects.filter(thang=thang, nam=nam, da_hach_toan=False).update(
        da_hach_toan=True
    )

    logger.info(
        "Created payroll journal entries for %d/%d: %s VND",
        thang,
        nam,
        tong_thuc_linh,
    )
    return count
