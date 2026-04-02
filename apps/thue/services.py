"""Thuế services - Tax declaration generation."""

import logging
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from django.db import models

from apps.nghiep_vu.constants import THUE_SUAT_TNDN_DEFAULT, THUE_SUAT_TNDN_SME, THUE_TNCN_BRACKETS
from apps.thue.models import BangKeHoaDonBanRa, BangKeHoaDonMuaVao, ToKhaiGTGT, ToKhaiTNCN, ToKhaiTNDNTamTinh

logger = logging.getLogger(__name__)


@transaction.atomic
def tao_to_khai_gtgt(thang: int, nam: int) -> ToKhaiGTGT:
    """
    Generate VAT declaration for a month.

    Thue GTGT phải nộp = Thuế đầu ra - Thuế đầu vào
    """
    ban_ra = BangKeHoaDonBanRa.objects.filter(thang=thang, nam=nam)
    mua_vao = BangKeHoaDonMuaVao.objects.filter(thang=thang, nam=nam)

    tong_doanh_so = ban_ra.aggregate(total=models.Sum("tong_tien"))["total"] or Decimal("0")
    thue_dau_ra = ban_ra.aggregate(total=models.Sum("thue_gtgt"))["total"] or Decimal("0")
    tong_mua_vao = mua_vao.aggregate(total=models.Sum("tong_tien"))["total"] or Decimal("0")
    thue_dau_vao = mua_vao.aggregate(total=models.Sum("thue_gtgt"))["total"] or Decimal("0")

    to_khai, _ = ToKhaiGTGT.objects.update_or_create(
        thang=thang,
        nam=nam,
        defaults={
            "tong_doanh_so_ban": tong_doanh_so,
            "thue_gtgt_dau_ra": thue_dau_ra,
            "tong_gia_tri_mua_vao": tong_mua_vao,
            "thue_gtgt_dau_vao": thue_dau_vao,
        },
    )
    return to_khai


@transaction.atomic
def tao_to_khai_tndn_tam_tinh(quy: int, nam: int) -> ToKhaiTNDNTamTinh:
    """
    Generate quarterly corporate income tax declaration.
    """
    if not (1 <= quy <= 4):
        raise ValidationError({"quy": ["Quý phải từ 1 đến 4"]})

    from apps.bao_cao.services import lap_bao_cao_kq_kinh_doanh

    if quy == 1:
        tu_ngay = date(nam, 1, 1)
        den_ngay = date(nam, 3, 31)
    elif quy == 2:
        tu_ngay = date(nam, 1, 1)
        den_ngay = date(nam, 6, 30)
    elif quy == 3:
        tu_ngay = date(nam, 1, 1)
        den_ngay = date(nam, 9, 30)
    else:
        tu_ngay = date(nam, 1, 1)
        den_ngay = date(nam, 12, 31)

    kqkd = lap_bao_cao_kq_kinh_doanh(tu_ngay, den_ngay)
    loi_nhuan = kqkd["chi_tiet"]["80"]["so_tien"]
    doanh_thu = kqkd["chi_tiet"]["10"]["so_tien"]
    chi_phi = doanh_thu - loi_nhuan

    if doanh_thu < Decimal("3000000000"):
        rate = THUE_SUAT_TNDN_SME
    else:
        rate = THUE_SUAT_TNDN_DEFAULT

    thue_phai_nop = Decimal("0")
    if loi_nhuan > 0:
        thue_phai_nop = (loi_nhuan * rate).quantize(Decimal("0.01"))

    to_khai, _ = ToKhaiTNDNTamTinh.objects.update_or_create(
        quy=quy,
        nam=nam,
        defaults={
            "doanh_thu": doanh_thu,
            "chi_phi_duoc_tru": chi_phi,
            "loi_nhuan": loi_nhuan,
            "thue_phai_nop": thue_phai_nop,
        },
    )
    return to_khai


def tinh_thue_tncn(thu_nhap_tinh_thue: Decimal) -> Decimal:
    """
    Calculate personal income tax using progressive brackets.
    """
    if thu_nhap_tinh_thue <= 0:
        return Decimal("0")

    thue = Decimal("0")
    remaining = thu_nhap_tinh_thue

    for i, (min_val, max_val, rate) in enumerate(THUE_TNCN_BRACKETS):
        if max_val is None:
            thue += remaining * rate
            break
        bracket_size = max_val - min_val
        taxable_in_bracket = min(remaining, bracket_size)
        if taxable_in_bracket <= 0:
            break
        thue += taxable_in_bracket * rate
        remaining -= taxable_in_bracket

    return thue.quantize(Decimal("0.01"))


@transaction.atomic
def tao_to_khai_tncn(thang: int, nam: int) -> ToKhaiTNCN:
    """
    Generate monthly personal income tax declaration.
    """
    from apps.luong.models import BangLuong

    luongs = BangLuong.objects.filter(thang=thang, nam=nam)
    tong_thu_nhap = luongs.aggregate(total=models.Sum("tong_thu_nhap"))["total"] or Decimal("0")
    tong_thue = luongs.aggregate(total=models.Sum("thue_tncn"))["total"] or Decimal("0")
    so_nv = luongs.count()

    to_khai, _ = ToKhaiTNCN.objects.update_or_create(
        thang=thang,
        nam=nam,
        defaults={
            "tong_thu_nhap": tong_thu_nhap,
            "tong_thue_tncn": tong_thue,
            "so_nhan_vien": so_nv,
        },
    )
    return to_khai


def kiem_tra_hoa_don_da_khai(hoa_don) -> bool:
    """
    Check if an invoice is already included in a submitted tax declaration.
    """
    from apps.nghiep_vu.models import HoaDon

    if not isinstance(hoa_don, HoaDon):
        return False

    thang = hoa_don.ngay_hoa_don.month
    nam = hoa_don.ngay_hoa_don.year

    return ToKhaiGTGT.objects.filter(
        thang=thang,
        nam=nam,
        trang_thai="da_nop",
    ).exists()
