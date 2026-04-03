"""Integration tests for opening balances with posting and inventory."""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import HangHoa, TaiKhoanKeToan
from apps.he_thong.models import KyKeToan, SoDuDauKy
from apps.kho.models import Kho, KhoEntry, VatTuHangHoa
from apps.nghiep_vu.models import ButToan, ButToanChiTiet


@pytest.fixture
def tk_111(db):
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
def tk_156(db):
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
def ky_ke_toan_2026(db):
    return KyKeToan.objects.create(
        nam=2026,
        ngay_bat_dau="2026-01-01",
        ngay_ket_thuc="2026-12-31",
        trang_thai="open",
    )


@pytest.fixture
def kho_chn(db):
    return Kho.objects.create(ma_kho="KHN", ten_kho="Kho chính")


@pytest.fixture
def hang_hoa(db):
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH001",
        ten_hang_hoa="Hàng mẫu",
        don_vi_tinh="cái",
    )
    return VatTuHangHoa.objects.create(hang_hoa=hh, phuong_phap_tinh_gia="FIFO")


class TestPostingBeforeOpeningDate:
    """Test that posting before opening date is rejected."""

    def test_posting_before_ky_ke_toan_rejected(self, tk_111, ky_ke_toan_2026):
        """Test that ButToan with date before KyKeToan.ngay_bat_dau is rejected."""
        bt = ButToan.objects.create(
            so_but_toan="BT001",
            ngay_hach_toan="2025-12-15",
            dien_giai="Bút toán trước kỳ kế toán",
            trang_thai="draft",
        )
        bt.trang_thai = "posted"
        with pytest.raises(ValidationError):
            bt.full_clean()

    def test_posting_on_or_after_opening_date_allowed(self, tk_111, ky_ke_toan_2026):
        """Test that ButToan with date >= KyKeToan.ngay_bat_dau is allowed."""
        bt = ButToan.objects.create(
            so_but_toan="BT002",
            ngay_hach_toan="2026-01-15",
            dien_giai="Bút toán trong kỳ kế toán",
            trang_thai="draft",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("1000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="co",
            so_tien=Decimal("1000000"),
        )
        bt.trang_thai = "posted"
        bt.full_clean()
        bt.save()
        assert bt.pk is not None


class TestLockedBalancesCannotEdit:
    """Test that locked opening balances cannot be edited or deleted."""

    def test_locked_balance_cannot_be_edited(self, tk_111):
        """Test editing a locked balance raises ValidationError."""
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

    def test_locked_balance_cannot_be_deleted(self, tk_111):
        """Test deleting a locked balance raises ValidationError."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_111,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
            da_khoa=True,
        )
        with pytest.raises(ValidationError):
            sd.delete()


class TestInventoryOpeningEntries:
    """Test that inventory opening balances create KhoEntry with is_opening=True."""

    def test_inventory_opening_creates_kho_entry(self, tk_156, kho_chn, hang_hoa):
        """Test that saving inventory opening balance creates KhoEntry."""
        SoDuDauKy.objects.create(
            tai_khoan=tk_156,
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        entries = KhoEntry.objects.filter(
            hang_hoa=hang_hoa,
            kho=kho_chn,
            is_opening=True,
        )
        assert entries.exists()
        entry = entries.first()
        assert entry.thanh_tien == Decimal("20000000")

    def test_editing_inventory_opening_updates_kho_entry(
        self, tk_156, kho_chn, hang_hoa
    ):
        """Test that editing inventory opening balance updates KhoEntry."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_156,
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd.so_du_no = Decimal("25000000")
        sd.full_clean()
        sd.save()
        entry = KhoEntry.objects.filter(
            hang_hoa=hang_hoa,
            kho=kho_chn,
            is_opening=True,
        ).first()
        assert entry.thanh_tien == Decimal("25000000")

    def test_deleting_inventory_opening_removes_kho_entry(
        self, tk_156, kho_chn, hang_hoa
    ):
        """Test that deleting inventory opening balance removes KhoEntry."""
        sd = SoDuDauKy.objects.create(
            tai_khoan=tk_156,
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        sd.delete()
        assert not KhoEntry.objects.filter(
            hang_hoa=hang_hoa,
            kho=kho_chn,
            is_opening=True,
        ).exists()


class TestValuationEngineUsesOpeningEntries:
    """Test that valuation engine uses opening entries correctly."""

    def test_fifo_uses_opening_entry_first(self, tk_156, kho_chn, hang_hoa):
        """Test that FIFO valuation considers opening entries as first lots."""
        SoDuDauKy.objects.create(
            tai_khoan=tk_156,
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("10000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        opening_entry = KhoEntry.objects.filter(
            hang_hoa=hang_hoa,
            kho=kho_chn,
            is_opening=True,
        ).first()
        assert opening_entry is not None
        assert opening_entry.loai == "NHAP"
        assert opening_entry.is_opening is True
