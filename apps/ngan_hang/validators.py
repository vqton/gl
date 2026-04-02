"""Bank-specific validators."""

from django.core.exceptions import ValidationError


def validate_so_tien_duong_choi(so_tien):
    """Validate amount is positive."""
    from decimal import Decimal

    if so_tien <= Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})


def validate_trang_thai_doi_chieu(trang_thai):
    """Validate reconciliation status."""
    valid = ("cho_doi_chieu", "da_doi_chieu", "co_chenh_lech")
    if trang_thai not in valid:
        raise ValidationError(
            {"trang_thai": [f"Trạng thái không hợp lệ. Chỉ chấp nhận: {', '.join(valid)}"]}
        )
