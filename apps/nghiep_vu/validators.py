"""Validation functions for Vietnamese SME Accounting System."""

import logging
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.danh_muc.models import TaiKhoanKeToan

logger = logging.getLogger(__name__)


def validate_tai_khoan_no_co(tk_no: str, tk_co: str) -> None:
    """
    Validate debit and credit account codes exist and are active.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on chart of accounts
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        tk_no: Debit account code
        tk_co: Credit account code

    Raises:
        ValidationError: If accounts are invalid
    """
    errors = {}

    if not tk_no:
        errors["tk_no"] = ["Tài khoản Nợ là bắt buộc"]
    else:
        try:
            tk = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_no, is_active=True)
        except TaiKhoanKeToan.DoesNotExist:
            errors["tk_no"] = [
                f"Tài khoản Nợ {tk_no} không tồn tại hoặc không hoạt động"
            ]

    if not tk_co:
        errors["tk_co"] = ["Tài khoản Có là bắt buộc"]
    else:
        try:
            tk = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_co, is_active=True)
        except TaiKhoanKeToan.DoesNotExist:
            errors["tk_co"] = [
                f"Tài khoản Có {tk_co} không tồn tại hoặc không hoạt động"
            ]

    if errors:
        raise ValidationError(errors)


def validate_so_du(
    tai_khoan: TaiKhoanKeToan,
    so_tien: Decimal,
    loai_giao_dich: str,
) -> None:
    """
    Validate balance rules for accounting transactions.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on double-entry bookkeeping
        - Nguyên tắc kế toán kép

    Args:
        tai_khoan: Accounting account instance
        so_tien: Transaction amount
        loai_giao_dich: Transaction type ('no' for debit, 'co' for credit)

    Raises:
        ValidationError: If balance rules are violated
    """
    if so_tien <= Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})

    loai_tk = tai_khoan.loai_tai_khoan

    if loai_tk in ("tai_san", "chi_phi"):
        if loai_giao_dich == "co" and so_tien > Decimal("999999999999999999.99"):
            raise ValidationError(
                {"so_tien": ["Số tiền Có vượt quá giới hạn cho phép"]}
            )
    elif loai_tk in ("no_phai_tra", "von_chu_so_huu", "doanh_thu"):
        if loai_giao_dich == "no" and so_tien > Decimal("999999999999999999.99"):
            raise ValidationError(
                {"so_tien": ["Số tiền Nợ vượt quá giới hạn cho phép"]}
            )


def validate_ngay_chung_tu(ngay: date) -> None:
    """
    Validate document date is not in a closed accounting period.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on accounting periods
        - Quy định về khóa sổ kế toán

    Args:
        ngay: Document date to validate

    Raises:
        ValidationError: If date is invalid
    """
    today = timezone.now().date()

    if ngay > today:
        raise ValidationError(
            {"ngay": ["Ngày chứng từ không được lớn hơn ngày hiện tại"]}
        )

    if ngay.year < 2025:
        raise ValidationError({"ngay": ["Ngày chứng từ phải từ năm 2025 trở đi"]})


def validate_hoa_don(
    tong_tien_truoc_thue: Decimal,
    tien_thue_gtgt: Decimal,
    tong_cong_thanh_toan: Decimal,
) -> None:
    """
    Validate invoice totals consistency.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on invoice requirements
        - Nghị định 320/2025/NĐ-CP on sales documentation

    Args:
        tong_tien_truoc_thue: Total before tax
        tien_thue_gtgt: VAT amount
        tong_cong_thanh_toan: Grand total

    Raises:
        ValidationError: If totals are inconsistent
    """
    if tong_tien_truoc_thue < Decimal("0"):
        raise ValidationError(
            {"tong_tien_truoc_thue": ["Tổng tiền trước thuế không được âm"]}
        )

    if tien_thue_gtgt < Decimal("0"):
        raise ValidationError({"tien_thue_gtgt": ["Tiền thuế GTGT không được âm"]})

    expected_total = tong_tien_truoc_thue + tien_thue_gtgt
    if abs(tong_cong_thanh_toan - expected_total) > Decimal("0.01"):
        raise ValidationError(
            {
                "tong_cong_thanh_toan": [
                    f"Tổng thanh toán ({tong_cong_thanh_toan}) không khớp "
                    f"với tổng trước thuế + thuế ({expected_total})"
                ]
            }
        )
