"""Thủ Quỹ (Cashier Reconciliation) services."""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from apps.nghiep_vu.models import ButToan, PhieuThu, PhieuChi

from .models import KiemKeQuy, XuLyChenhLechQuy

logger = logging.getLogger(__name__)


class ThuQuyService:
    """
    Service for cashier reconciliation operations.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Quy định về quản lý tiền mặt
        - Chế độ kế toán doanh nghiệp nhỏ và vừa
    """

    def get_so_du_tien_mat(self, ngay: date) -> Decimal:
        """
        Get cash book balance at a specific date.

        Sums all posted PhieuThu (tien_mat) minus all posted PhieuChi (tien_mat)
        up to the given date.

        Args:
            ngay: Date to check balance

        Returns:
            Cash balance as Decimal
        """
        tong_thu = PhieuThu.objects.filter(
            ngay_chung_tu__lte=ngay,
            hinh_thuc_thanh_toan="tien_mat",
            trang_thai="posted",
        ).aggregate(total=Sum("so_tien_vnd"))["total"] or Decimal("0")

        tong_chi = PhieuChi.objects.filter(
            ngay_chung_tu__lte=ngay,
            hinh_thuc_thanh_toan="tien_mat",
            trang_thai="posted",
        ).aggregate(total=Sum("so_tien_vnd"))["total"] or Decimal("0")

        return tong_thu - tong_chi

    def get_so_quy_tien_mat(
        self, tu_ngay: date, den_ngay: date
    ) -> Dict:
        """
        Get cash book entries for a period.

        Args:
            tu_ngay: Start date
            den_ngay: End date

        Returns:
            Dict with entries list and summary totals
        """
        thu_entries = PhieuThu.objects.filter(
            ngay_chung_tu__gte=tu_ngay,
            ngay_chung_tu__lte=den_ngay,
            hinh_thuc_thanh_toan="tien_mat",
            trang_thai="posted",
        ).order_by("ngay_chung_tu")

        chi_entries = PhieuChi.objects.filter(
            ngay_chung_tu__gte=tu_ngay,
            ngay_chung_tu__lte=den_ngay,
            hinh_thuc_thanh_toan="tien_mat",
            trang_thai="posted",
        ).order_by("ngay_chung_tu")

        tong_thu = sum(e.so_tien_vnd for e in thu_entries)
        tong_chi = sum(e.so_tien_vnd for e in chi_entries)

        return {
            "tu_ngay": tu_ngay,
            "den_ngay": den_ngay,
            "thu_entries": list(thu_entries),
            "chi_entries": list(chi_entries),
            "tong_thu": tong_thu,
            "tong_chi": tong_chi,
            "chenh_lech": tong_thu - tong_chi,
        }

    @transaction.atomic
    def tao_kiem_ke_quy(
        self,
        so_kiem_ke: str,
        ngay_kiem_ke: date,
        ky_quy: str,
        so_thuc_te: Decimal,
        nguoi_kiem_ke: str,
        thu_quy,
        ly_do: str = "",
    ) -> KiemKeQuy:
        """
        Create cash count record.

        Auto-calculates book balance and difference.

        Args:
            so_kiem_ke: Count record number
            ngay_kiem_ke: Count date
            ky_quy: Period label (e.g., "T01/2026")
            so_thuc_te: Physical cash count
            nguoi_kiem_ke: Name of person conducting count
            thu_quy: Cashier user (NguoiDung)
            ly_do: Reason for any difference

        Returns:
            Created KiemKeQuy instance

        Raises:
            ValidationError: If validation fails
        """
        so_du_so_sach = self.get_so_du_tien_mat(ngay_kiem_ke)

        kk = KiemKeQuy(
            so_kiem_ke=so_kiem_ke,
            ngay_kiem_ke=ngay_kiem_ke,
            ky_quy=ky_quy,
            so_du_so_sach=so_du_so_sach,
            so_thuc_te=so_thuc_te,
            nguoi_kiem_ke=nguoi_kiem_ke,
            thu_quy=thu_quy,
            ly_do=ly_do,
        )
        kk.full_clean()
        kk.save()

        logger.info(
            "Created cash count %s: Book=%s, Actual=%s, Diff=%s",
            so_kiem_ke,
            so_du_so_sach,
            so_thuc_te,
            kk.chen_lech,
        )
        return kk

    @transaction.atomic
    def xu_ly_chenh_lech(
        self,
        kiem_ke: KiemKeQuy,
        loai: str,
        nguyen_nhan: str,
        xu_ly: str,
    ) -> XuLyChenhLechQuy:
        """
        Create cash difference resolution.

        Args:
            kiem_ke: Cash count record
            loai: 'thieu' or 'thua'
            nguyen_nhan: Reason for difference
            xu_ly: Resolution method

        Returns:
            Created XuLyChenhLechQuy instance
        """
        so_tien = abs(kiem_ke.chen_lech)

        xl = XuLyChenhLechQuy(
            kiem_ke=kiem_ke,
            loai=loai,
            so_tien=so_tien,
            nguyen_nhan=nguyen_nhan,
            xu_ly=xu_ly,
        )
        xl.full_clean()
        xl.save()

        logger.info(
            "Created difference resolution: %s %s = %s",
            loai,
            so_tien,
            xu_ly,
        )
        return xl

    @transaction.atomic
    def dang_kiem_ke_quy(
        self,
        kiem_ke: KiemKeQuy,
        xu_ly: Optional[XuLyChenhLechQuy] = None,
    ) -> Optional[ButToan]:
        """
        Post cash count and create journal entries for differences.

        Journal entries:
            Thiếu quỹ:
                Step 1: Nợ 1388 / Có 111
                Step 2: Nợ 331/642 / Có 1388
            Thừa quỹ:
                Step 1: Nợ 111 / Có 3388
                Step 2: Nợ 3388 / Có 711

        Args:
            kiem_ke: Cash count record
            xu_ly: Resolution record (required if there's a difference)

        Returns:
            ButToan if difference was resolved, None otherwise
        """
        from apps.danh_muc.models import TaiKhoanKeToan
        from apps.nghiep_vu.services import tao_but_toan

        if kiem_ke.chen_lech == Decimal("0"):
            kiem_ke.trang_thai = "da_xu_ly"
            kiem_ke.save(update_fields=["trang_thai", "updated_at"])
            return None

        if not xu_ly:
            raise ValidationError(
                {"xu_ly": ["Phải có xử lý chênh lệch trước khi ghi sổ"]}
            )

        abs_chenh_lech = abs(kiem_ke.chen_lech)
        if abs(xu_ly.so_tien - abs_chenh_lech) > Decimal("0.01"):
            raise ValidationError(
                {"xu_ly": ["Số tiền xử lý không khớp với chênh lệch"]}
            )

        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        if not tk111:
            raise ValidationError(
                {"tai_khoan": ["Cần có TK 111 để xử lý chênh lệch"]}
            )

        if kiem_ke.chen_lech < Decimal("0"):
            but_toan = self._but_toan_thieu_quy(
                kiem_ke, xu_ly, tk111, tao_but_toan
            )
        else:
            but_toan = self._but_toan_thua_quy(
                kiem_ke, xu_ly, tk111, tao_but_toan
            )

        kiem_ke.trang_thai = "da_xu_ly"
        kiem_ke.save(update_fields=["trang_thai", "updated_at"])

        logger.info(
            "Posted cash count %s with resolution %s",
            kiem_ke.so_kiem_ke,
            xu_ly.xu_ly,
        )
        return but_toan

    def _but_toan_thieu_quy(self, kiem_ke, xu_ly, tk111, tao_but_toan):
        """Create journal entry for cash shortage."""
        from apps.danh_muc.models import TaiKhoanKeToan

        so_tien = abs(kiem_ke.chen_lech)

        if xu_ly.xu_ly == "bo_thuong":
            tk1388 = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan="1388"
            ).first()
            if not tk1388:
                raise ValidationError(
                    {"tai_khoan": ["Cần có TK 1388 để xử lý thiếu quỹ"]}
                )
            chi_tiet = [
                {
                    "tai_khoan": tk1388,
                    "loai_no_co": "no",
                    "so_tien": so_tien,
                    "dien_giai": f"Thiếu quỹ {kiem_ke.so_kiem_ke} - bồi thường",
                },
                {
                    "tai_khoan": tk111,
                    "loai_no_co": "co",
                    "so_tien": so_tien,
                    "dien_giai": f"Thiếu quỹ {kiem_ke.so_kiem_ke} - bồi thường",
                },
            ]
        elif xu_ly.xu_ly == "ghi_giam_chi_phi":
            tk642 = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan="642"
            ).first()
            if not tk642:
                raise ValidationError(
                    {"tai_khoan": ["Cần có TK 642 để ghi giảm chi phí"]}
                )
            chi_tiet = [
                {
                    "tai_khoan": tk642,
                    "loai_no_co": "no",
                    "so_tien": so_tien,
                    "dien_giai": f"Thiếu quỹ {kiem_ke.so_kiem_ke} - ghi giảm CP",
                },
                {
                    "tai_khoan": tk111,
                    "loai_no_co": "co",
                    "so_tien": so_tien,
                    "dien_giai": f"Thiếu quỹ {kiem_ke.so_kiem_ke} - ghi giảm CP",
                },
            ]
        else:
            raise ValidationError(
                {"xu_ly": ["Hình thức xử lý không hợp lệ cho thiếu quỹ"]}
            )

        return tao_but_toan(
            ngay=kiem_ke.ngay_kiem_ke,
            dien_giai=f"Xử lý thiếu quỹ {kiem_ke.so_kiem_ke}",
            chi_tiet=chi_tiet,
            so_but_toan=f"XLTT-{kiem_ke.so_kiem_ke}",
        )

    def _but_toan_thua_quy(self, kiem_ke, xu_ly, tk111, tao_but_toan):
        """Create journal entry for cash overage."""
        from apps.danh_muc.models import TaiKhoanKeToan

        so_tien = abs(kiem_ke.chen_lech)

        if xu_ly.xu_ly == "ghi_tang_thu_nhap":
            tk711 = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan="711"
            ).first()
            if not tk711:
                raise ValidationError(
                    {"tai_khoan": ["Cần có TK 711 để ghi tăng thu nhập"]}
                )
            chi_tiet = [
                {
                    "tai_khoan": tk111,
                    "loai_no_co": "no",
                    "so_tien": so_tien,
                    "dien_giai": f"Thừa quỹ {kiem_ke.so_kiem_ke} - thu nhập khác",
                },
                {
                    "tai_khoan": tk711,
                    "loai_no_co": "co",
                    "so_tien": so_tien,
                    "dien_giai": f"Thừa quỹ {kiem_ke.so_kiem_ke} - thu nhập khác",
                },
            ]
        else:
            raise ValidationError(
                {"xu_ly": ["Hình thức xử lý không hợp lệ cho thừa quỹ"]}
            )

        return tao_but_toan(
            ngay=kiem_ke.ngay_kiem_ke,
            dien_giai=f"Xử lý thừa quỹ {kiem_ke.so_kiem_ke}",
            chi_tiet=chi_tiet,
            so_but_toan=f"XLTT-{kiem_ke.so_kiem_ke}",
        )
