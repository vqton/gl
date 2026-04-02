"""Sổ sách kế toán services - Journal, Cash Book, Bank Book."""

import logging
from datetime import date
from decimal import Decimal

from django.db.models import Sum

from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToanChiTiet

logger = logging.getLogger(__name__)


def get_so_nhat_ky_chung(tu_ngay: date, den_ngay: date) -> dict:
    """
    Generate General Journal (Sổ Nhật Ký Chung).

    Legal basis: Thông tư 99/2025/TT-BTC, Mẫu sổ nhật ký chung
    """
    entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
    ).select_related("but_toan", "tai_khoan").order_by("but_toan__ngay_hach_toan", "pk")

    lines = []
    stt = 0
    for entry in entries:
        stt += 1
        lines.append({
            "stt": stt,
            "ngay_ghi_so": entry.but_toan.ngay_hach_toan,
            "so_chung_tu": entry.but_toan.so_but_toan,
            "dien_giai": entry.dien_giai or entry.but_toan.dien_giai,
            "tk_doi_ung": entry.tai_khoan.ma_tai_khoan,
            "ten_tai_khoan": entry.tai_khoan.ten_tai_khoan,
            "so_tien_no": entry.so_tien if entry.loai_no_co == "no" else Decimal("0"),
            "so_tien_co": entry.so_tien if entry.loai_no_co == "co" else Decimal("0"),
            "so_chung_tu_goc": entry.so_chung_tu_goc,
        })

    tong_no = sum(l["so_tien_no"] for l in lines)
    tong_co = sum(l["so_tien_co"] for l in lines)

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "lines": lines,
        "tong_no": tong_no,
        "tong_co": tong_co,
        "can_doi": abs(tong_no - tong_co) < Decimal("0.01"),
    }


def get_so_quy(tu_ngay: date, den_ngay: date) -> dict:
    """
    Generate Cash Book (Sổ Quỹ) - entries affecting TK 111.

    Shows daily balance, cannot have negative cash balance.
    """
    entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="111",
    ).select_related("but_toan", "tai_khoan").order_by("but_toan__ngay_hach_toan", "pk")

    daily_data = {}
    for entry in entries:
        ngay = entry.but_toan.ngay_hach_toan
        if ngay not in daily_data:
            daily_data[ngay] = {
                "ngay": ngay,
                "phat_sinh_no": Decimal("0"),
                "phat_sinh_co": Decimal("0"),
                "entries": [],
            }
        if entry.loai_no_co == "no":
            daily_data[ngay]["phat_sinh_no"] += entry.so_tien
        else:
            daily_data[ngay]["phat_sinh_co"] += entry.so_tien

        daily_data[ngay]["entries"].append({
            "so_chung_tu": entry.but_toan.so_but_toan,
            "dien_giai": entry.dien_giai or entry.but_toan.dien_giai,
            "loai_no_co": entry.loai_no_co,
            "so_tien": entry.so_tien,
            "tk_doi_ung": entry.tai_khoan.ma_tai_khoan,
        })

    so_du_dau_ky = Decimal("0")
    prior_no = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__lt=tu_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="111",
        loai_no_co="no",
    ).aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    prior_co = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__lt=tu_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="111",
        loai_no_co="co",
    ).aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    so_du_dau_ky = prior_no - prior_co

    days = []
    so_du = so_du_dau_ky
    for ngay in sorted(daily_data.keys()):
        data = daily_data[ngay]
        so_du += data["phat_sinh_no"] - data["phat_sinh_co"]
        data["so_du_cuoi_ngay"] = so_du
        days.append(data)

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "so_du_dau_ky": so_du_dau_ky,
        "days": days,
        "so_du_cuoi_ky": so_du,
    }


def get_so_ngan_hang(tu_ngay: date, den_ngay: date) -> dict:
    """
    Generate Bank Book (Sổ Ngân Hàng) - entries affecting TK 112.

    Shows balance per bank account, reconcile with bank statement.
    """
    entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="112",
    ).select_related("but_toan", "tai_khoan").order_by("but_toan__ngay_hach_toan", "pk")

    daily_data = {}
    for entry in entries:
        ngay = entry.but_toan.ngay_hach_toan
        if ngay not in daily_data:
            daily_data[ngay] = {
                "ngay": ngay,
                "phat_sinh_no": Decimal("0"),
                "phat_sinh_co": Decimal("0"),
                "entries": [],
            }
        if entry.loai_no_co == "no":
            daily_data[ngay]["phat_sinh_no"] += entry.so_tien
        else:
            daily_data[ngay]["phat_sinh_co"] += entry.so_tien

        daily_data[ngay]["entries"].append({
            "so_chung_tu": entry.but_toan.so_but_toan,
            "dien_giai": entry.dien_giai or entry.but_toan.dien_giai,
            "loai_no_co": entry.loai_no_co,
            "so_tien": entry.so_tien,
            "tk_doi_ung": entry.tai_khoan.ma_tai_khoan,
        })

    prior_no = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__lt=tu_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="112",
        loai_no_co="no",
    ).aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    prior_co = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__lt=tu_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan="112",
        loai_no_co="co",
    ).aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    so_du_dau_ky = prior_no - prior_co

    days = []
    so_du = so_du_dau_ky
    for ngay in sorted(daily_data.keys()):
        data = daily_data[ngay]
        so_du += data["phat_sinh_no"] - data["phat_sinh_co"]
        data["so_du_cuoi_ngay"] = so_du
        days.append(data)

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "so_du_dau_ky": so_du_dau_ky,
        "days": days,
        "so_du_cuoi_ky": so_du,
    }
