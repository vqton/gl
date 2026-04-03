"""Tests for SoDuDauKy (Opening Balances) model."""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.danh_muc.models import HangHoa, TaiKhoanKeToan
from apps.he_thong.models import SoDuDauKy
from apps.kho.models import Kho, VatTuHangHoa
from apps.tai_san.models import TaiSanCoDinh


@pytest.fixture
def tk_111(db):
    """Create cash account 111."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={
            "ten_tai_khoan": "Tiền mặt",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk_131(db):
    """Create customer account 131."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={
            "ten_tai_khoan": "Phải thu khách hàng",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk_331(db):
    """Create supplier account 331."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={
            "ten_tai_khoan": "Phải trả người bán",
            "cap_do": 1,
            "loai_tai_khoan": "no_phai_tra",
        },
    )
    return tk


@pytest.fixture
def tk_156(db):
    """Create inventory account 156."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="156",
        defaults={
            "ten_tai_khoan": "Hàng hóa",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk_211(db):
    """Create fixed asset account 211."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="211",
        defaults={
            "ten_tai_khoan": "Tài sản cố định",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk_411(db):
    """Create owner equity account 411."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="411",
        defaults={
            "ten_tai_khoan": "Vốn chủ sở hữu",
            "cap_do": 1,
            "loai_tai_khoan": "von_chu_so_huu",
        },
    )
    return tk


@pytest.fixture
def kho_chn(db):
    """Create default warehouse."""
    return Kho.objects.create(
        ma_kho="KHN",
        ten_kho="Kho chính",
    )


@pytest.fixture
def hang_hoa(db):
    """Create a goods item."""
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH001",
        ten_hang_hoa="Hàng hóa mẫu",
        don_vi_tinh="cái",
    )
    return VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
    )


@pytest.fixture
def tai_san(db):
    """Create a fixed asset."""
    return TaiSanCoDinh.objects.create(
        ma_tai_san="TS001",
        ten_tai_san="Máy tính",
        nguyen_gia=Decimal("20000000"),
        thoi_gian_khau_hao_thang=36,
        ngay_dua_vao_su_dung="2026-01-01",
    )


class TestSoDuDauKyCreation:
    """Test basic SoDuDauKy creation."""

    def test_create_so_du_no_only(self, tk_111):
        """Test creating opening balance with debit only."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        assert sd.so_du_no == Decimal("10000000")
        assert sd.so_du_co == Decimal("0")
        assert sd.da_khoa is False

    def test_create_so_du_co_only(self, tk_411):
        """Test creating opening balance with credit only."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_411,
            so_du_no=Decimal("0"),
            so_du_co=Decimal("50000000"),
            nam=2026,
        )
        assert sd.so_du_no == Decimal("0")
        assert sd.so_du_co == Decimal("50000000")

    def test_create_so_du_with_doi_tuong_ma(self, tk_131):
        """Test creating opening balance with customer code."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_131,
            doi_tuong_ma="KH001",
            so_du_no=Decimal("5000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        assert sd.doi_tuong_ma == "KH001"

    def test_create_so_du_with_kho(self, tk_156, kho_chn, hang_hoa):
        """Test creating inventory opening balance with warehouse and item."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_156,
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        assert sd.kho == kho_chn
        assert sd.hang_hoa == hang_hoa

    def test_create_so_du_with_tai_san(self, tk_211, tai_san):
        """Test creating fixed asset opening balance."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_211,
            tai_san=tai_san,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        assert sd.tai_san == tai_san


class TestSoDuDauKyValidation:
    """Test SoDuDauKy validation rules."""

    def test_both_no_and_co_nonzero_raises_error(self, tk_111):
        """Test that both so_du_no and so_du_co cannot be non-zero."""
        sd = SoDuDauKy(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("5000000"),
            nam=2026,
        )
        with pytest.raises(ValidationError):
            sd.full_clean()

    def test_both_zero_is_allowed(self, tk_111):
        """Test that both zero is allowed (empty opening balance)."""
        sd = SoDuDauKy(
            tai_khoan=tk_111,
            so_du_no=Decimal("0"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd.full_clean()
        sd.save()
        assert sd.pk is not None

    def test_negative_so_du_no_raises_error(self, tk_111):
        """Test that negative debit is not allowed."""
        sd = SoDuDauKy(
            tai_khoan=tk_111,
            so_du_no=Decimal("-1000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        with pytest.raises(ValidationError):
            sd.full_clean()

    def test_negative_so_du_co_raises_error(self, tk_411):
        """Test that negative credit is not allowed."""
        sd = SoDuDauKy(
            tai_khoan=tk_411,
            so_du_no=Decimal("0"),
            so_du_co=Decimal("-5000000"),
            nam=2026,
        )
        with pytest.raises(ValidationError):
            sd.full_clean()


class TestSoDuDauKyUniqueConstraints:
    """Test unique constraint on tai_khoan + doi_tuong_ma + nam."""

    def test_duplicate_tai_khoan_nam_raises_error(self, tk_111):
        """Test that duplicate account + year is not allowed."""
        SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd2 = SoDuDauKy(
            tai_khoan=tk_111,
            so_du_no=Decimal("5000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        with pytest.raises((ValidationError, IntegrityError)):
            sd2.full_clean()
            sd2.save()

    def test_different_doi_tuong_ma_allowed(self, tk_131):
        """Test that different customer codes for same account + year are allowed."""
        SoDuDauKy.objects.create(
            tai_khoan=tk_131,
            doi_tuong_ma="KH001",
            so_du_no=Decimal("5000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd2 = SoDuDauKy(
            tai_khoan=tk_131,
            doi_tuong_ma="KH002",
            so_du_no=Decimal("3000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd2.full_clean()
        sd2.save()
        assert sd2.pk is not None

    def test_different_nam_allowed(self, tk_111):
        """Test that same account with different year is allowed."""
        SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2025,
        )
        sd2 = SoDuDauKy(
            tai_khoan=tk_111,
            so_du_no=Decimal("15000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd2.full_clean()
        sd2.save()
        assert sd2.pk is not None


class TestSoDuDauKyLocking:
    """Test locking mechanism for opening balances."""

    def test_lock_prevents_edit(self, tk_111):
        """Test that locked balance cannot be edited."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
            da_khoa=True,
        )
        sd.so_du_no = Decimal("20000000")
        with pytest.raises(ValidationError):
            sd.full_clean()

    def test_lock_prevents_delete(self, tk_111):
        """Test that locked balance cannot be deleted."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
            da_khoa=True,
        )
        with pytest.raises(ValidationError):
            sd.delete()

    def test_unlocked_can_be_edited(self, tk_111):
        """Test that unlocked balance can be edited."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd.so_du_no = Decimal("20000000")
        sd.full_clean()
        sd.save()
        sd.refresh_from_db()
        assert sd.so_du_no == Decimal("20000000")

    def test_finalize_sets_da_khoa(self, tk_111):
        """Test finalize method sets da_khoa to True."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd.finalize()
        sd.refresh_from_db()
        assert sd.da_khoa is True
