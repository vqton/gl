"""CCDC services - Allocation calculation, auto journal."""

import logging
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.ccdc.models import BangPhanBoCCDC, CongCuDungCu
from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet

logger = logging.getLogger(__name__)


def tinh_muc_phan_bo_thang(ccdc: CongCuDungCu) -> Decimal:
    """
    Calculate monthly allocation amount for CCDC.

    Monthly allocation = tong_gia_tri / so_ky_phan_bo
    """
    if ccdc.so_ky_phan_bo <= 0:
        raise ValidationError({"so_ky_phan_bo": ["Số kỳ phân bổ phải lớn hơn 0"]})

    tong_gia_tri = ccdc.tong_gia_tri or (ccdc.gia_mua * ccdc.so_luong)
    return (tong_gia_tri / ccdc.so_ky_phan_bo).quantize(Decimal("0.01"))


@transaction.atomic
def tao_bang_phan_bo(ccdc: CongCuDungCu) -> list:
    """
    Generate all monthly allocation entries for a CCDC.

    For 1-lan: single entry in the month of purchase.
    For nhieu-lan: spread over so_ky_phan_bo months.
    """
    muc_phan_bo = tinh_muc_phan_bo_thang(ccdc)

    from datetime import timedelta

    existing = BangPhanBoCCDC.objects.filter(ccdc=ccdc)
    if existing.exists():
        raise ValidationError({"ccdc": ["CCDC này đã có bảng phân bổ"]})

    allocations = []
    current_date = ccdc.ky_phan_bo_bat_dau

    for i in range(ccdc.so_ky_phan_bo):
        thang = current_date.month
        nam = current_date.year

        so_tien = muc_phan_bo
        if i == ccdc.so_ky_phan_bo - 1:
            so_tien = ccdc.tong_gia_tri - (muc_phan_bo * (ccdc.so_ky_phan_bo - 1))

        allocation = BangPhanBoCCDC.objects.create(
            ccdc=ccdc,
            thang=thang,
            nam=nam,
            so_tien_phan_bo=so_tien,
        )
        allocations.append(allocation)

        if thang == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    if ccdc.phuong_phap_phan_bo == "1_lan":
        ccdc.trang_thai = "da_phan_bo_het"
    ccdc.save()

    return allocations


@transaction.atomic
def hach_toan_phan_bo_ccdc(allocation: BangPhanBoCCDC) -> ButToan:
    """
    Post CCDC allocation journal entry.

    Journal: Nợ 642/154/241... / Có 242 (or 153 for 1-lan)
    """
    if allocation.trang_thai == "da_hach_toan":
        raise ValidationError(
            {"trang_thai": ["Phân bổ này đã được hạch toán"]}
        )

    ccdc = allocation.ccdc
    tk_242 = TaiKhoanKeToan.objects.get(ma_tai_khoan="242")

    count = ButToan.objects.filter(ngay_hach_toan=date(allocation.nam, allocation.thang, 1)).count() + 1
    so_but_toan = f"BT-CCDC{allocation.nam}{allocation.thang:02d}{count:04d}"

    but_toan = ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=date(allocation.nam, allocation.thang, 1),
        dien_giai=f"Phân bổ CCDC {ccdc.ma_ccdc} - {allocation.thang}/{allocation.nam}",
    )

    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=ccdc.tk_chi_phi,
        loai_no_co="no",
        so_tien=allocation.so_tien_phan_bo,
        dien_giai=f"Phân bổ {ccdc.ten_ccdc}",
    )

    if ccdc.phuong_phap_phan_bo == "1_lan":
        tk_co = TaiKhoanKeToan.objects.get(ma_tai_khoan="153")
    else:
        tk_co = tk_242

    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tk_co,
        loai_no_co="co",
        so_tien=allocation.so_tien_phan_bo,
        dien_giai=f"Phân bổ {ccdc.ten_ccdc}",
    )

    allocation.trang_thai = "da_hach_toan"
    allocation.save()

    all_allocated = allocation.ccdc.bang_phan_bo.filter(trang_thai="da_hach_toan").count()
    if all_allocated >= ccdc.so_ky_phan_bo:
        ccdc.trang_thai = "da_phan_bo_het"
        ccdc.save()

    return but_toan
