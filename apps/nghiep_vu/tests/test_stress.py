"""Data integrity tests: voucher → journal → report chain.

Note: SQLite WAL mode handles sequential writes well.
Concurrent writes from multiple processes are serialized by WAL.
"""

from datetime import date
from decimal import Decimal

import pytest

from apps.danh_muc.models import KhachHang, NhaCungCap, TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet, PhieuChi, PhieuThu
from apps.nghiep_vu.services import tao_phieu_chi, tao_phieu_thu


@pytest.fixture
def khach_hang_stress():
    """Create test customer for stress tests."""
    return KhachHang.objects.create(ma_kh="KH_STRESS", ten_kh="Khách hàng stress test")


@pytest.fixture
def nha_cung_cap_stress():
    """Create test supplier for stress tests."""
    return NhaCungCap.objects.create(
        ma_ncc="NCC_STRESS", ten_ncc="Nhà cung cấp stress test"
    )


@pytest.fixture
def required_accounts():
    """Create all required accounts for stress tests."""
    accounts = {
        "111": "Tiền mặt",
        "112": "Tiền gửi ngân hàng",
        "131": "Phải thu khách hàng",
        "331": "Phải trả người bán",
        "642": "Chi phí QLDN",
        "711": "Thu nhập khác",
    }
    created = {}
    for code, name in accounts.items():
        tk, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan=code,
            defaults={
                "ten_tai_khoan": name,
                "loai_tai_khoan": "1",
                "cap_do": 1,
            },
        )
        created[code] = tk
    return created


@pytest.mark.django_db
class TestDataIntegrityChain:
    """Test voucher → journal → report data chain."""

    def test_phieu_thu_to_journal_chain(self, khach_hang_stress, required_accounts):
        """Test that receipt creates valid journal entry."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang_stress,
            so_tien=Decimal("10000000"),
            tk_co="131",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Test chain",
            so_chung_tu="PT-CHAIN-001",
        )

        # Verify journal entry exists
        bt = ButToan.objects.get(so_but_toan=f"BT-{phieu.so_chung_tu}")
        assert bt is not None

        # Verify journal is balanced
        chi_tiet = list(bt.chi_tiet.all())
        no_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "no")
        co_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "co")
        assert no_total == co_total
        assert no_total == Decimal("10000000")

    def test_phieu_chi_to_journal_chain(self, nha_cung_cap_stress, required_accounts):
        """Test that payment creates valid journal entry."""
        phieu = tao_phieu_chi(
            nha_cung_cap=nha_cung_cap_stress,
            so_tien=Decimal("5000000"),
            tk_no="331",
            ngay_chung_tu=date(2026, 1, 15),
            dien_giai="Test chain",
            so_chung_tu="PC-CHAIN-001",
        )

        bt = ButToan.objects.get(so_but_toan=f"BT-{phieu.so_chung_tu}")
        assert bt is not None

        chi_tiet = list(bt.chi_tiet.all())
        no_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "no")
        co_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "co")
        assert no_total == co_total
        assert no_total == Decimal("5000000")

    def test_multiple_vouchers_journal_balance(
        self, khach_hang_stress, nha_cung_cap_stress, required_accounts
    ):
        """Test that multiple vouchers maintain journal balance."""
        # Create multiple vouchers
        for i in range(5):
            tao_phieu_thu(
                khach_hang=khach_hang_stress,
                so_tien=Decimal("1000000"),
                tk_co="131",
                ngay_chung_tu=date(2026, 1, 15),
                so_chung_tu=f"PT-BAL-{i:04d}",
            )
            tao_phieu_chi(
                nha_cung_cap=nha_cung_cap_stress,
                so_tien=Decimal("500000"),
                tk_no="331",
                ngay_chung_tu=date(2026, 1, 15),
                so_chung_tu=f"PC-BAL-{i:04d}",
            )

        # Verify all journal entries are balanced
        for bt in ButToan.objects.filter(so_but_toan__startswith="BT-PT-BAL-"):
            chi_tiet = list(bt.chi_tiet.all())
            no_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "no")
            co_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "co")
            assert no_total == co_total, f"Unbalanced: {bt.so_but_toan}"

        for bt in ButToan.objects.filter(so_but_toan__startswith="BT-PC-BAL-"):
            chi_tiet = list(bt.chi_tiet.all())
            no_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "no")
            co_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "co")
            assert no_total == co_total, f"Unbalanced: {bt.so_but_toan}"

    def test_foreign_currency_conversion(self, khach_hang_stress, required_accounts):
        """Test foreign currency conversion accuracy."""
        phieu = tao_phieu_thu(
            khach_hang=khach_hang_stress,
            so_tien=Decimal("1000"),
            tk_co="131",
            ty_gia=Decimal("25000"),
            ngay_chung_tu=date(2026, 1, 15),
            so_chung_tu="PT-FOREX-001",
        )

        assert phieu.so_tien == Decimal("1000")
        assert phieu.so_tien_vnd == Decimal("25000000")

        bt = ButToan.objects.get(so_but_toan=f"BT-{phieu.so_chung_tu}")
        chi_tiet = list(bt.chi_tiet.all())
        no_total = sum(c.so_tien for c in chi_tiet if c.loai_no_co == "no")
        assert no_total == Decimal("25000000")
