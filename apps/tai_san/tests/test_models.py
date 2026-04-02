"""Tests for M3: Tài sản cố định (Fixed Assets)."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.tai_san.models import BangKhauHao, TaiSanCoDinh


@pytest.fixture
def tai_san():
    """Create a test fixed asset."""
    return TaiSanCoDinh.objects.create(
        ma_tai_san="TS001",
        ten_tai_san="Máy tính Dell",
        nhom_tai_san="Thiết bị văn phòng",
        so_luong=Decimal("1"),
        nguyen_gia=Decimal("24000000"),
        thoi_gian_khau_hao_thang=24,
        phuong_phap_khau_hao="duong_thang",
        ngay_dua_vao_su_dung=date(2026, 1, 1),
    )


@pytest.mark.django_db
class TestTaiSanCoDinhModel:
    """Test TaiSanCoDinh model."""

    def test_create_tai_san(self, tai_san):
        """Test basic fixed asset creation."""
        assert tai_san.ma_tai_san == "TS001"
        assert tai_san.nguyen_gia == Decimal("24000000")
        assert tai_san.thoi_gian_khau_hao_thang == 24
        assert tai_san.trang_thai == "dang_su_dung"

    def test_auto_calculate_khau_hao_thang(self, tai_san):
        """Test auto-calculation of monthly depreciation."""
        assert tai_san.muc_khau_hao_thang == Decimal("1000000")

    def test_auto_calculate_gia_tri_con_lai(self, tai_san):
        """Test auto-calculation of remaining value."""
        assert tai_san.gia_tri_con_lai == Decimal("24000000")

    def test_str_representation(self, tai_san):
        """Test string representation."""
        assert "TS001" in str(tai_san)
        assert "Máy tính Dell" in str(tai_san)

    def test_unique_ma_tai_san(self):
        """Test that ma_tai_san must be unique."""
        TaiSanCoDinh.objects.create(
            ma_tai_san="TS002",
            ten_tai_san="TS 2",
            nguyen_gia=Decimal("10000000"),
            thoi_gian_khau_hao_thang=12,
            ngay_dua_vao_su_dung=date(2026, 1, 1),
        )
        with pytest.raises(Exception):
            TaiSanCoDinh.objects.create(
                ma_tai_san="TS002",
                ten_tai_san="TS 2 duplicate",
                nguyen_gia=Decimal("10000000"),
                thoi_gian_khau_hao_thang=12,
                ngay_dua_vao_su_dung=date(2026, 1, 1),
            )


@pytest.mark.django_db
class TestDepreciationLogic:
    """Test depreciation calculation logic."""

    def test_depreciation_updates_remaining_value(self, tai_san):
        """Test that recording depreciation reduces remaining value."""
        tai_san.khau_hao_luy_ke = Decimal("1000000")
        tai_san.save()
        tai_san.refresh_from_db()
        assert tai_san.gia_tri_con_lai == Decimal("23000000")

    def test_depreciation_full_marks_as_done(self, tai_san):
        """Test asset marked as fully depreciated when KH = nguyên giá."""
        tai_san.khau_hao_luy_ke = Decimal("24000000")
        tai_san.save()
        tai_san.refresh_from_db()
        assert tai_san.trang_thai == "dung_khau_hao"
        assert tai_san.gia_tri_con_lai == Decimal("0")

    def test_depreciation_over_limit_caps_at_zero(self, tai_san):
        """Test remaining value caps at 0 even if KH > nguyên giá."""
        tai_san.khau_hao_luy_ke = Decimal("30000000")
        tai_san.save()
        tai_san.refresh_from_db()
        assert tai_san.gia_tri_con_lai == Decimal("0")

    def test_multiple_quantities(self):
        """Test asset with multiple quantities."""
        ts = TaiSanCoDinh.objects.create(
            ma_tai_san="TS003",
            ten_tai_san="Ghế văn phòng",
            so_luong=Decimal("10"),
            nguyen_gia=Decimal("50000000"),
            thoi_gian_khau_hao_thang=60,
            ngay_dua_vao_su_dung=date(2026, 1, 1),
        )
        assert ts.muc_khau_hao_thang == Decimal("833333.33")


@pytest.mark.django_db
class TestBangKhauHao:
    """Test BangKhauHao (Depreciation Schedule) model."""

    def test_create_khau_hao_record(self, tai_san):
        """Test creating a depreciation schedule record."""
        record = BangKhauHao.objects.create(
            tai_san=tai_san,
            thang=1,
            nam=2026,
            so_tien_khau_hao=Decimal("1000000"),
            khau_hao_luy_ke_dau_thang=Decimal("0"),
            khau_hao_luy_ke_cuoi_thang=Decimal("1000000"),
        )
        assert record.so_tien_khau_hao == Decimal("1000000")
        assert not record.da_hach_toan

    def test_str_representation(self, tai_san):
        """Test string representation."""
        record = BangKhauHao.objects.create(
            tai_san=tai_san,
            thang=1,
            nam=2026,
            so_tien_khau_hao=Decimal("1000000"),
            khau_hao_luy_ke_dau_thang=Decimal("0"),
            khau_hao_luy_ke_cuoi_thang=Decimal("1000000"),
        )
        assert "1/2026" in str(record)

    def test_unique_constraint(self, tai_san):
        """Test unique constraint on (tai_san, thang, nam)."""
        BangKhauHao.objects.create(
            tai_san=tai_san,
            thang=1,
            nam=2026,
            so_tien_khau_hao=Decimal("1000000"),
            khau_hao_luy_ke_dau_thang=Decimal("0"),
            khau_hao_luy_ke_cuoi_thang=Decimal("1000000"),
        )
        with pytest.raises(Exception):
            BangKhauHao.objects.create(
                tai_san=tai_san,
                thang=1,
                nam=2026,
                so_tien_khau_hao=Decimal("1000000"),
                khau_hao_luy_ke_dau_thang=Decimal("0"),
                khau_hao_luy_ke_cuoi_thang=Decimal("1000000"),
            )
