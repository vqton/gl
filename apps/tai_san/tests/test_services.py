"""Tests for M3: Tài sản cố định - Services."""

from datetime import date
from decimal import Decimal

import pytest

from apps.nghiep_vu.models import ButToan, ButToanChiTiet
from apps.tai_san.models import BangKhauHao, TaiSanCoDinh
from apps.tai_san.services import (
    tach_toan_khau_hao,
    tao_bang_khau_hao_thang,
    tinh_khau_hao_thang,
)


@pytest.fixture
def tai_san():
    """Create a test fixed asset."""
    return TaiSanCoDinh.objects.create(
        ma_tai_san="TS_SVC_001",
        ten_tai_san="Máy tính Dell",
        nguyen_gia=Decimal("24000000"),
        thoi_gian_khau_hao_thang=24,
        phuong_phap_khau_hao="duong_thang",
        ngay_dua_vao_su_dung=date(2026, 1, 1),
    )


@pytest.fixture
def tai_san_2():
    """Create a second test fixed asset."""
    return TaiSanCoDinh.objects.create(
        ma_tai_san="TS_SVC_002",
        ten_tai_san="Bàn làm việc",
        nguyen_gia=Decimal("12000000"),
        thoi_gian_khau_hao_thang=12,
        phuong_phap_khau_hao="duong_thang",
        ngay_dua_vao_su_dung=date(2026, 1, 1),
    )


@pytest.fixture
def tai_khoan_642():
    """Create account 642."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={
            "ten_tai_khoan": "Chi phí QLDN",
            "loai_tai_khoan": "6",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_214():
    """Create account 214."""
    from apps.danh_muc.models import TaiKhoanKeToan

    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="214",
        defaults={
            "ten_tai_khoan": "Khấu hao TSCĐ",
            "loai_tai_khoan": "2",
            "cap_do": 1,
        },
    )
    return tk


@pytest.mark.django_db
class TestTinhKhauHaoThang:
    """Test tinh_khau_hao_thang function."""

    def test_first_month_depreciation(self, tai_san):
        """Test depreciation for first month."""
        amount = tinh_khau_hao_thang(tai_san, 1, 2026)
        assert amount == Decimal("1000000")

    def test_mid_life_depreciation(self, tai_san):
        """Test depreciation in middle of asset life."""
        # Simulate 12 months of depreciation
        tai_san.khau_hao_luy_ke = Decimal("12000000")
        tai_san.save()

        amount = tinh_khau_hao_thang(tai_san, 1, 2027)
        assert amount == Decimal("1000000")

    def test_past_depreciation_period(self, tai_san):
        """Test depreciation after asset is fully depreciated."""
        tai_san.khau_hao_luy_ke = Decimal("24000000")
        tai_san.trang_thai = "dung_khau_hao"
        tai_san.save()

        amount = tinh_khau_hao_thang(tai_san, 1, 2028)
        assert amount == Decimal("0")

    def test_before_start_date(self, tai_san):
        """Test depreciation before asset start date."""
        amount = tinh_khau_hao_thang(tai_san, 12, 2025)
        assert amount == Decimal("0")

    def test_last_month_partial(self):
        """Test last month depreciation when remaining < monthly."""
        ts = TaiSanCoDinh.objects.create(
            ma_tai_san="TS_PARTIAL",
            ten_tai_san="Test Partial",
            nguyen_gia=Decimal("24000000"),
            thoi_gian_khau_hao_thang=24,
            ngay_dua_vao_su_dung=date(2026, 1, 1),
        )
        # Simulate 23 months of depreciation (month 24 is last)
        ts.khau_hao_luy_ke = Decimal("23000000")
        ts.save()

        # Month 24 = 12/2027 (23 months after start)
        amount = tinh_khau_hao_thang(ts, 12, 2027)
        assert amount == Decimal("1000000")


@pytest.mark.django_db
class TestTaoBangKhauHaoThang:
    """Test tao_bang_khau_hao_thang function."""

    def test_generate_for_single_asset(self, tai_san):
        """Test generating depreciation for one asset."""
        records = tao_bang_khau_hao_thang(1, 2026)

        assert len(records) == 1
        assert records[0].so_tien_khau_hao == Decimal("1000000")
        assert records[0].khau_hao_luy_ke_dau_thang == Decimal("0")
        assert records[0].khau_hao_luy_ke_cuoi_thang == Decimal("1000000")

        tai_san.refresh_from_db()
        assert tai_san.khau_hao_luy_ke == Decimal("1000000")

    def test_generate_for_multiple_assets(self, tai_san, tai_san_2):
        """Test generating depreciation for multiple assets."""
        records = tao_bang_khau_hao_thang(1, 2026)

        assert len(records) == 2
        total = sum(r.so_tien_khau_hao for r in records)
        assert total == Decimal("2000000")

    def test_no_duplicate_for_same_month(self, tai_san):
        """Test that duplicate records are not created."""
        tao_bang_khau_hao_thang(1, 2026)
        records = tao_bang_khau_hao_thang(1, 2026)

        assert len(records) == 1
        tai_san.refresh_from_db()
        assert tai_san.khau_hao_luy_ke == Decimal("1000000")

    def test_filter_by_asset_ids(self, tai_san, tai_san_2):
        """Test generating depreciation for specific assets."""
        records = tao_bang_khau_hao_thang(1, 2026, [tai_san.pk])

        assert len(records) == 1
        assert records[0].tai_san.pk == tai_san.pk

    def test_skips_fully_depreciated(self):
        """Test that fully depreciated assets are skipped."""
        ts = TaiSanCoDinh.objects.create(
            ma_tai_san="TS_DONE",
            ten_tai_san="Done",
            nguyen_gia=Decimal("10000000"),
            thoi_gian_khau_hao_thang=1,
            ngay_dua_vao_su_dung=date(2025, 1, 1),
        )
        ts.khau_hao_luy_ke = Decimal("10000000")
        ts.trang_thai = "dung_khau_hao"
        ts.save()

        records = tao_bang_khau_hao_thang(1, 2026)
        assert len(records) == 0


@pytest.mark.django_db
class TestTachToanKhauHao:
    """Test tach_toan_khau_hao function."""

    def test_create_journal_entry(self, tai_san, tai_khoan_642, tai_khoan_214):
        """Test creating journal entry for depreciation."""
        tao_bang_khau_hao_thang(1, 2026)

        count = tach_toan_khau_hao(1, 2026)
        assert count == 1

        bt = ButToan.objects.get(so_but_toan="BT-KH012026")
        assert bt is not None

        chi_tiet = list(bt.chi_tiet.all())
        assert len(chi_tiet) == 2

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "642"
        assert no_line.so_tien == Decimal("1000000")

        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")
        assert co_line.tai_khoan.ma_tai_khoan == "214"

    def test_marks_records_as_hach_toan(self, tai_san, tai_khoan_642, tai_khoan_214):
        """Test that records are marked as da_hach_toan."""
        tao_bang_khau_hao_thang(1, 2026)
        tach_toan_khau_hao(1, 2026)

        record = BangKhauHao.objects.get(tai_san=tai_san, thang=1, nam=2026)
        assert record.da_hach_toan is True

    def test_no_double_entry(self, tai_san, tai_khoan_642, tai_khoan_214):
        """Test that running twice doesn't create duplicate entries."""
        tao_bang_khau_hao_thang(1, 2026)
        tach_toan_khau_hao(1, 2026)

        count = tach_toan_khau_hao(1, 2026)
        assert count == 0

    def test_no_records_no_entry(self, tai_khoan_642, tai_khoan_214):
        """Test that no records means no journal entry."""
        count = tach_toan_khau_hao(1, 2026)
        assert count == 0
