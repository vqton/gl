"""Bank services - auto journal creation, reconciliation."""

import logging
from datetime import date
from decimal import Decimal
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.danh_muc.models import TaiKhoanKeToan
from apps.ngan_hang.models import DoiChieuNganHang, GiayBaoCo, GiayBaoNo
from apps.ngan_hang.validators import validate_so_tien_duong_choi
from apps.nghiep_vu.models import ButToan, ButToanChiTiet

logger = logging.getLogger(__name__)


@transaction.atomic
def post_giay_bao_no(giay_bao_no: GiayBaoNo) -> ButToan:
    """
    Post bank debit notice and create auto journal entry.

    Journal: Nợ 331/642... / Có 112

    Legal basis:
        - Thông tư 99/2025/TT-BTC on bank transaction journaling
    """
    if giay_bao_no.trang_thai != "draft":
        raise ValidationError(
            {"trang_thai": ["Chỉ có thể ghi sổ giấy báo Nợ ở trạng thái nháp"]}
        )

    validate_so_tien_duong_choi(giay_bao_no.so_tien)

    tk_112 = TaiKhoanKeToan.objects.get(ma_tai_khoan="112")
    tk_331 = TaiKhoanKeToan.objects.get(ma_tai_khoan="331")

    count = ButToan.objects.filter(ngay_hach_toan=giay_bao_no.ngay).count() + 1
    so_but_toan = f"BT-GBN{giay_bao_no.ngay.strftime('%Y%m%d')}{count:04d}"

    but_toan = ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=giay_bao_no.ngay,
        dien_giai=giay_bao_no.dien_giai or f"Giấy báo Nợ {giay_bao_no.so_chung_tu}",
    )

    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tk_331,
        loai_no_co="no",
        so_tien=giay_bao_no.so_tien,
        dien_giai=giay_bao_no.dien_giai,
        so_chung_tu_goc=giay_bao_no.so_chung_tu,
    )
    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tk_112,
        loai_no_co="co",
        so_tien=giay_bao_no.so_tien,
        dien_giai=giay_bao_no.dien_giai,
        so_chung_tu_goc=giay_bao_no.so_chung_tu,
    )

    giay_bao_no.trang_thai = "posted"
    giay_bao_no.save()

    logger.info(
        "Posted GiayBaoNo %s: Nợ 331 / Có 112 - %s",
        giay_bao_no.so_chung_tu,
        giay_bao_no.so_tien,
    )
    return but_toan


@transaction.atomic
def post_giay_bao_co(giay_bao_co: GiayBaoCo) -> ButToan:
    """
    Post bank credit notice and create auto journal entry.

    Journal: Nợ 112 / Có 131/511...

    Legal basis:
        - Thông tư 99/2025/TT-BTC on bank transaction journaling
    """
    if giay_bao_co.trang_thai != "draft":
        raise ValidationError(
            {"trang_thai": ["Chỉ có thể ghi sổ giấy báo Có ở trạng thái nháp"]}
        )

    validate_so_tien_duong_choi(giay_bao_co.so_tien)

    tk_112 = TaiKhoanKeToan.objects.get(ma_tai_khoan="112")
    tk_131 = TaiKhoanKeToan.objects.get(ma_tai_khoan="131")

    count = ButToan.objects.filter(ngay_hach_toan=giay_bao_co.ngay).count() + 1
    so_but_toan = f"BT-GBC{giay_bao_co.ngay.strftime('%Y%m%d')}{count:04d}"

    but_toan = ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=giay_bao_co.ngay,
        dien_giai=giay_bao_co.dien_giai or f"Giấy báo Có {giay_bao_co.so_chung_tu}",
    )

    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tk_112,
        loai_no_co="no",
        so_tien=giay_bao_co.so_tien,
        dien_giai=giay_bao_co.dien_giai,
        so_chung_tu_goc=giay_bao_co.so_chung_tu,
    )
    ButToanChiTiet.objects.create(
        but_toan=but_toan,
        tai_khoan=tk_131,
        loai_no_co="co",
        so_tien=giay_bao_co.so_tien,
        dien_giai=giay_bao_co.dien_giai,
        so_chung_tu_goc=giay_bao_co.so_chung_tu,
    )

    giay_bao_co.trang_thai = "posted"
    giay_bao_co.save()

    logger.info(
        "Posted GiayBaoCo %s: Nợ 112 / Có 131 - %s",
        giay_bao_co.so_chung_tu,
        giay_bao_co.so_tien,
    )
    return but_toan


@transaction.atomic
def tao_doi_chieu_ngan_hang(
    tai_khoan_ngan_hang,
    thang: int,
    nam: int,
    so_du_so_sach: Decimal,
    so_du_ngan_hang: Decimal,
) -> DoiChieuNganHang:
    """
    Create bank reconciliation for a given month.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on bank reconciliation
    """
    if not (1 <= thang <= 12):
        raise ValidationError({"thang": ["Tháng phải từ 1 đến 12"]})

    doi_chieu, created = DoiChieuNganHang.objects.update_or_create(
        tai_khoan_ngan_hang=tai_khoan_ngan_hang,
        thang=thang,
        nam=nam,
        defaults={
            "so_du_so_sach": so_du_so_sach,
            "so_du_ngan_hang": so_du_ngan_hang,
        },
    )

    if doi_chieu.chenh_lech == Decimal("0"):
        doi_chieu.trang_thai = "da_doi_chieu"
    else:
        doi_chieu.trang_thai = "co_chenh_lech"
    doi_chieu.save()

    return doi_chieu


def tinh_so_du_so_sach(
    tai_khoan_ngan_hang,
    thang: int,
    nam: int,
) -> Decimal:
    """
    Calculate book balance for a bank account at end of month.

    Sums all posted journal entries affecting TK 112 for the account.
    """
    from datetime import date as date_cls
    from django.db.models import Sum

    from apps.nghiep_vu.models import ButToanChiTiet

    ngay_dau_thang = date_cls(nam, thang, 1)
    if thang == 12:
        ngay_cuoi_thang = date_cls(nam, 12, 31)
    else:
        ngay_cuoi_thang = date_cls(nam, thang + 1, 1)

    entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=ngay_dau_thang,
        but_toan__ngay_hach_toan__lt=ngay_cuoi_thang,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="112",
    )

    tong_no = entries.filter(loai_no_co="no").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")
    tong_co = entries.filter(loai_no_co="co").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    return tong_no - tong_co
