"""Tests for nghiep_vu validators."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.validators import (
    validate_hoa_don,
    validate_ngay_chung_tu,
    validate_so_du,
    validate_tai_khoan_no_co,
)


@pytest.mark.django_db
class TestValidateTaiKhoanNoCo:
    """Tests for account validation."""

    def test_valid_accounts(self):
        """Test valid debit and credit accounts."""
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="111",
            defaults={"ten_tai_khoan": "Tiền mặt", "cap_do": 1},
        )
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="131",
            defaults={"ten_tai_khoan": "Phải thu", "cap_do": 1},
        )

        validate_tai_khoan_no_co("111", "131")

    def test_nonexistent_debit_account(self):
        """Test nonexistent debit account raises error."""
        with pytest.raises(ValidationError):
            validate_tai_khoan_no_co("999", "131")

    def test_nonexistent_credit_account(self):
        """Test nonexistent credit account raises error."""
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="111",
            defaults={"ten_tai_khoan": "Tiền mặt", "cap_do": 1},
        )
        with pytest.raises(ValidationError):
            validate_tai_khoan_no_co("111", "999")

    def test_inactive_account(self):
        """Test inactive account raises error."""
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="119",
            defaults={
                "ten_tai_khoan": "Test inactive",
                "cap_do": 1,
                "is_active": False,
            },
        )
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan="139",
            defaults={"ten_tai_khoan": "Test active", "cap_do": 1},
        )
        with pytest.raises(ValidationError):
            validate_tai_khoan_no_co("119", "139")

    def test_empty_accounts(self):
        """Test empty account codes raise errors."""
        with pytest.raises(ValidationError):
            validate_tai_khoan_no_co("", "")


@pytest.mark.django_db
class TestValidateSoDu:
    """Tests for balance validation."""

    def test_positive_amount(self):
        """Test positive amount passes validation."""
        tk = TaiKhoanKeToan(
            ma_tai_khoan="111",
            ten_tai_khoan="Tiền mặt",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        validate_so_du(tk, Decimal("1000000"), "no")

    def test_negative_amount_raises_error(self):
        """Test negative amount raises error."""
        tk = TaiKhoanKeToan(
            ma_tai_khoan="111",
            ten_tai_khoan="Tiền mặt",
            cap_do=1,
        )
        with pytest.raises(ValidationError):
            validate_so_du(tk, Decimal("-1000000"), "no")

    def test_zero_amount_raises_error(self):
        """Test zero amount raises error."""
        tk = TaiKhoanKeToan(
            ma_tai_khoan="111",
            ten_tai_khoan="Tiền mặt",
            cap_do=1,
        )
        with pytest.raises(ValidationError):
            validate_so_du(tk, Decimal("0"), "no")


class TestValidateNgayChungTu:
    """Tests for document date validation."""

    def test_valid_date(self):
        """Test valid date passes validation."""
        validate_ngay_chung_tu(date(2026, 1, 15))

    def test_future_date_raises_error(self):
        """Test future date raises error."""
        with pytest.raises(ValidationError):
            validate_ngay_chung_tu(date(2099, 1, 1))

    def test_old_date_raises_error(self):
        """Test date before 2025 raises error."""
        with pytest.raises(ValidationError):
            validate_ngay_chung_tu(date(2024, 12, 31))

    def test_today_date(self):
        """Test today's date passes validation."""
        from datetime import date as date_cls

        validate_ngay_chung_tu(date_cls.today())


class TestValidateHoaDon:
    """Tests for invoice validation."""

    def test_valid_invoice(self):
        """Test valid invoice passes validation."""
        validate_hoa_don(
            Decimal("1000000"),
            Decimal("100000"),
            Decimal("1100000"),
        )

    def test_negative_total_raises_error(self):
        """Test negative total raises error."""
        with pytest.raises(ValidationError):
            validate_hoa_don(
                Decimal("-1000000"),
                Decimal("100000"),
                Decimal("-900000"),
            )

    def test_negative_tax_raises_error(self):
        """Test negative tax raises error."""
        with pytest.raises(ValidationError):
            validate_hoa_don(
                Decimal("1000000"),
                Decimal("-100000"),
                Decimal("900000"),
            )

    def test_mismatched_totals_raises_error(self):
        """Test mismatched totals raise error."""
        with pytest.raises(ValidationError):
            validate_hoa_don(
                Decimal("1000000"),
                Decimal("100000"),
                Decimal("1200000"),
            )

    def test_zero_invoice(self):
        """Test zero invoice passes validation."""
        validate_hoa_don(
            Decimal("0"),
            Decimal("0"),
            Decimal("0"),
        )
