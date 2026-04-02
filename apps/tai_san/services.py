"""Fixed Asset service layer (M3)."""

import logging
from datetime import date
from decimal import Decimal
from typing import List, Optional

from django.db import transaction

from apps.nghiep_vu.services import tao_but_toan
from apps.tai_san.models import BangKhauHao, TaiSanCoDinh

logger = logging.getLogger(__name__)


def tinh_khau_hao_thang(
    tai_san: TaiSanCoDinh,
    thang: int,
    nam: int,
) -> Decimal:
    """
    Calculate monthly depreciation for a fixed asset.

    Uses straight-line method: Nguyen gia / Thoi gian khau hao.

    Legal basis:
        - Thông tư 45/2013/TT-BTC on depreciation methods
        - Thông tư 99/2025/TT-BTC on fixed asset accounting

    Args:
        tai_san: TaiSanCoDinh instance
        thang: Month (1-12)
        nam: Year

    Returns:
        Monthly depreciation amount as Decimal
    """
    if tai_san.trang_thai != "dang_su_dung":
        return Decimal("0")

    start_date = tai_san.ngay_dua_vao_su_dung
    asset_month = start_date.month
    asset_year = start_date.year

    if nam < asset_year or (nam == asset_year and thang < asset_month):
        return Decimal("0")

    months_elapsed = (nam - asset_year) * 12 + (thang - asset_month)
    if months_elapsed >= tai_san.thoi_gian_khau_hao_thang:
        return Decimal("0")

    remaining_months = tai_san.thoi_gian_khau_hao_thang - months_elapsed
    remaining_value = tai_san.nguyen_gia - tai_san.khau_hao_luy_ke

    if remaining_months <= 0 or remaining_value <= Decimal("0"):
        return Decimal("0")

    khau_hao = min(
        tai_san.muc_khau_hao_thang,
        remaining_value,
    )
    return khau_hao.quantize(Decimal("0.01"))


@transaction.atomic
def tao_bang_khau_hao_thang(
    thang: int,
    nam: int,
    tai_san_ids: Optional[List[int]] = None,
) -> List[BangKhauHao]:
    """
    Generate monthly depreciation schedule for all active assets.

    Creates BangKhauHao records for each asset that needs depreciation
    in the given month.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on depreciation schedule
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        thang: Month (1-12)
        nam: Year
        tai_san_ids: Optional list of asset IDs (all active if None)

    Returns:
        List of created BangKhauHao instances
    """
    assets = TaiSanCoDinh.objects.filter(trang_thai="dang_su_dung")
    if tai_san_ids:
        assets = assets.filter(pk__in=tai_san_ids)

    records = []
    for ts in assets:
        existing = BangKhauHao.objects.filter(tai_san=ts, thang=thang, nam=nam).first()
        if existing:
            records.append(existing)
            continue

        so_tien = tinh_khau_hao_thang(ts, thang, nam)
        if so_tien <= Decimal("0"):
            continue

        khau_hao_cuoi = ts.khau_hao_luy_ke + so_tien

        record = BangKhauHao.objects.create(
            tai_san=ts,
            thang=thang,
            nam=nam,
            so_tien_khau_hao=so_tien,
            khau_hao_luy_ke_dau_thang=ts.khau_hao_luy_ke,
            khau_hao_luy_ke_cuoi_thang=khau_hao_cuoi,
        )
        records.append(record)

        ts.khau_hao_luy_ke = khau_hao_cuoi
        ts.save(
            update_fields=[
                "khau_hao_luy_ke",
                "gia_tri_con_lai",
                "trang_thai",
                "updated_at",
            ]
        )

    logger.info(
        "Generated depreciation for %d assets - %d/%d",
        len(records),
        thang,
        nam,
    )
    return records


@transaction.atomic
def tach_toan_khau_hao(
    thang: int,
    nam: int,
    tai_san_ids: Optional[List[int]] = None,
) -> int:
    """
    Create journal entries for monthly depreciation.

    Journal entry:
        Nợ 642 (Chi phí QLDN) / Nợ 627 (Chi phí SXC) / ...
        Có 214 (Khấu hao TSCĐ)

    Legal basis:
        - Thông tư 99/2025/TT-BTC on depreciation journal entries
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        thang: Month (1-12)
        nam: Year
        tai_san_ids: Optional list of asset IDs

    Returns:
        Number of assets depreciated
    """
    records = BangKhauHao.objects.filter(
        thang=thang,
        nam=nam,
        da_hach_toan=False,
    )
    if tai_san_ids:
        records = records.filter(tai_san_id__in=tai_san_ids)

    if not records.exists():
        return 0

    tong_khau_hao = sum(r.so_tien_khau_hao for r in records)
    if tong_khau_hao <= Decimal("0"):
        return 0

    count = records.count()

    count = records.count()

    chi_tiet = [
        {
            "tai_khoan": "642",
            "loai_no_co": "no",
            "so_tien": tong_khau_hao,
            "ma_doi_tuong": "",
            "dien_giai": f"Khấu hao TSCĐ tháng {thang}/{nam}",
        },
        {
            "tai_khoan": "214",
            "loai_no_co": "co",
            "so_tien": tong_khau_hao,
            "ma_doi_tuong": "",
            "dien_giai": f"Khấu hao TSCĐ tháng {thang}/{nam}",
        },
    ]

    tao_but_toan(
        ngay=date(nam, thang, 28),
        dien_giai=f"Khấu hao TSCĐ tháng {thang}/{nam}",
        chi_tiet=chi_tiet,
        so_but_toan=f"BT-KH{thang:02d}{nam}",
    )

    BangKhauHao.objects.filter(
        thang=thang,
        nam=nam,
        da_hach_toan=False,
    ).update(da_hach_toan=True)

    logger.info(
        "Created depreciation journal entry for %d/%d: %s VND",
        thang,
        nam,
        tong_khau_hao,
    )
    return count
