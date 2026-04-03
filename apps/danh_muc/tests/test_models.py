"""Tests for danh_muc models."""

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import DonVi, TaiKhoanKeToan


@pytest.mark.django_db
class TestTaiKhoanKeToan:
    """Tests for TaiKhoanKeToan model."""

    def test_create_tai_khoan_cap_1(self):
        """Test creating a Tier-1 accounting account."""
        tk = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="999",
            ten_tai_khoan="Test account",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        assert tk.ma_tai_khoan == "999"
        assert tk.ten_tai_khoan == "Test account"
        assert tk.cap_do == 1
        assert tk.is_immutable is False

    def test_create_tai_khoan_cap_2_with_parent(self):
        """Test creating a Tier-2 account with parent."""
        parent = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="998",
            ten_tai_khoan="Parent account",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        child = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="9981",
            ten_tai_khoan="Child account",
            cap_do=2,
            tai_khoan_me=parent,
            loai_tai_khoan="tai_san",
        )
        assert child.tai_khoan_me == parent
        assert parent.tai_khoan_con.count() == 1

    def test_cap_2_requires_parent(self):
        """Test that Tier-2 account requires a parent."""
        tk = TaiKhoanKeToan(
            ma_tai_khoan="9971",
            ten_tai_khoan="Orphan account",
            cap_do=2,
            loai_tai_khoan="tai_san",
        )
        with pytest.raises(ValidationError):
            tk.full_clean()

    def test_cap_1_cannot_have_parent(self):
        """Test that Tier-1 account cannot have a parent."""
        parent = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="996",
            ten_tai_khoan="Parent account",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        tk = TaiKhoanKeToan(
            ma_tai_khoan="995",
            ten_tai_khoan="Child account",
            cap_do=1,
            tai_khoan_me=parent,
            loai_tai_khoan="tai_san",
        )
        with pytest.raises(ValidationError):
            tk.full_clean()

    def test_auto_detect_account_type(self):
        """Test automatic account type detection from code prefix."""
        tk = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="681",
            ten_tai_khoan="Test expense account",
            cap_do=1,
        )
        assert tk.loai_tai_khoan == "chi_phi"

    def test_string_representation(self):
        """Test string representation of account."""
        tk = TaiKhoanKeToan(
            ma_tai_khoan="999",
            ten_tai_khoan="Test account",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        assert str(tk) == "999 - Test account"

    def test_unique_account_code(self):
        """Test that account codes must be unique."""
        TaiKhoanKeToan.objects.create(
            ma_tai_khoan="994",
            ten_tai_khoan="First account",
            cap_do=1,
            loai_tai_khoan="tai_san",
        )
        with pytest.raises(Exception):
            TaiKhoanKeToan.objects.create(
                ma_tai_khoan="994",
                ten_tai_khoan="Duplicate account",
                cap_do=1,
                loai_tai_khoan="tai_san",
            )


@pytest.mark.django_db
class TestDonVi:
    """Tests for DonVi model."""

    def test_create_don_vi(self):
        """Test creating a company entity."""
        dv = DonVi.objects.create(
            ma_so_thue="0123456789",
            ten_don_vi="Công ty TNHH ABC",
            loai_don_vi="tnhh",
            dia_chi="Hà Nội",
        )
        assert dv.ma_so_thue == "0123456789"
        assert dv.ten_don_vi == "Công ty TNHH ABC"

    def test_string_representation(self):
        """Test string representation of entity."""
        dv = DonVi(
            ma_so_thue="0123456789",
            ten_don_vi="Công ty TNHH ABC",
            loai_don_vi="tnhh",
        )
        assert str(dv) == "Công ty TNHH ABC (0123456789)"

    def test_unique_tax_code(self):
        """Test that tax codes must be unique."""
        DonVi.objects.create(
            ma_so_thue="0123456789",
            ten_don_vi="Công ty A",
            loai_don_vi="tnhh",
        )
        with pytest.raises(Exception):
            DonVi.objects.create(
                ma_so_thue="0123456789",
                ten_don_vi="Công ty B",
                loai_don_vi="tnhh",
            )
