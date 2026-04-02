"""Công nợ services - Aging calculation, debt confirmation."""

import logging
from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from django.contrib.contenttypes.models import ContentType
from django.db import models as django_models

from apps.cong_no.models import BienBanDoiChieuCongNo, CongNoPhaiThu, CongNoPhaiTra

logger = logging.getLogger(__name__)

AGING_BUCKETS = [
    (0, 30, "0-30 ngày"),
    (31, 60, "31-60 ngày"),
    (61, 90, "61-90 ngày"),
    (91, 120, "91-120 ngày"),
    (121, None, ">120 ngày"),
]


def tinh_cong_no_phai_thu(khach_hang) -> CongNoPhaiThu:
    """
    Calculate receivable for a customer from invoices and receipts.

    Công nợ phải thu = Tổng hóa đơn bán - Tổng phiếu thu từ KH
    """
    from apps.nghiep_vu.models import HoaDon, PhieuThu

    tong_hoa_don = HoaDon.objects.filter(
        khach_hang=khach_hang,
        trang_thai__in=["issued", "draft"],
    ).aggregate(total=django_models.Sum("tong_cong_thanh_toan"))["total"] or Decimal("0")

    tong_phieu_thu = PhieuThu.objects.filter(
        khach_hang=khach_hang,
        trang_thai="posted",
    ).aggregate(total=django_models.Sum("so_tien_vnd"))["total"] or Decimal("0")

    con_no = tong_hoa_don - tong_phieu_thu
    if con_no < 0:
        con_no = Decimal("0")

    cong_no, _ = CongNoPhaiThu.objects.update_or_create(
        khach_hang=khach_hang,
        defaults={
            "tong_no": tong_hoa_don,
            "da_thu": tong_phieu_thu,
            "con_no": con_no,
        },
    )
    return cong_no


def tinh_cong_no_phai_tra(nha_cung_cap) -> CongNoPhaiTra:
    """
    Calculate payable for a supplier from receipts and payments.

    Công nợ phải trả = Tổng phiếu nhập kho - Tổng phiếu chi cho NCC
    """
    from apps.nghiep_vu.models import NhapKho, PhieuChi

    tong_nhap = NhapKho.objects.filter(
        nha_cung_cap=nha_cung_cap,
        trang_thai="completed",
    ).aggregate(total=django_models.Sum("tong_tien"))["total"] or Decimal("0")

    tong_chi = PhieuChi.objects.filter(
        nha_cung_cap=nha_cung_cap,
        trang_thai="posted",
    ).aggregate(total=django_models.Sum("so_tien_vnd"))["total"] or Decimal("0")

    con_no = tong_nhap - tong_chi
    if con_no < 0:
        con_no = Decimal("0")

    cong_no, _ = CongNoPhaiTra.objects.update_or_create(
        nha_cung_cap=nha_cung_cap,
        defaults={
            "tong_no": tong_nhap,
            "da_tra": tong_chi,
            "con_no": con_no,
        },
    )
    return cong_no


def phan_loai_cong_no(cong_no_list, hom_nay=None):
    """
    Classify debts into aging buckets.

    Args:
        cong_no_list: List of CongNoPhaiThu or CongNoPhaiTra
        hom_nay: Reference date (default today)

    Returns:
        Dict with bucket names as keys and list of debts as values
    """
    if hom_nay is None:
        hom_nay = date.today()

    buckets = {label: [] for _, _, label in AGING_BUCKETS}

    for cong_no in cong_no_list:
        if cong_no.con_no <= 0:
            continue

        if cong_no.ngay_den_han:
            so_ngay_qua_han = (hom_nay - cong_no.ngay_den_han).days
        else:
            so_ngay_qua_han = 0

        for min_days, max_days, label in AGING_BUCKETS:
            if max_days is None:
                if so_ngay_qua_han >= min_days:
                    buckets[label].append(cong_no)
                    break
            elif min_days <= so_ngay_qua_han <= max_days:
                buckets[label].append(cong_no)
                break

    return buckets


@transaction.atomic
def tao_bien_ban_doi_chieu(
    doi_tuong,
    loai: str,
    thang: int,
    nam: int,
    so_dau_ky: Decimal,
    phat_sinh_no: Decimal,
    phat_sinh_co: Decimal,
) -> BienBanDoiChieuCongNo:
    """
    Create debt confirmation document.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on debt confirmation
    """
    if not (1 <= thang <= 12):
        raise ValidationError({"thang": ["Tháng phải từ 1 đến 12"]})

    bien_ban, _ = BienBanDoiChieuCongNo.objects.update_or_create(
        doi_tuong_content_type=ContentType.objects.get_for_model(doi_tuong),
        doi_tuong_object_id=doi_tuong.pk,
        loai=loai,
        thang=thang,
        nam=nam,
        defaults={
            "so_dau_ky": so_dau_ky,
            "phat_sinh_no": phat_sinh_no,
            "phat_sinh_co": phat_sinh_co,
        },
    )

    return bien_ban


def kiem_tra_cong_no_chua_doi_chieu(thang: int, nam: int) -> bool:
    """
    Check if there are unreconciled debts for a period.

    Returns True if there are unreconciled debts.
    """
    return BienBanDoiChieuCongNo.objects.filter(
        thang=thang,
        nam=nam,
        da_xac_nhan=False,
    ).exists()
