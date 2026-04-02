"""Tests for CCDC app."""

import pytest
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

from apps.ccdc.models import BangPhanBoCCDC, CongCuDungCu
from apps.ccdc.services import (
    hach_toan_phan_bo_ccdc,
    tao_bang_phan_bo,
    tinh_muc_phan_bo_thang,
)


@pytest.fixture
def tk_642(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={"ten_tai_khoan": "Chi phí quản lý doanh nghiệp", "cap_do": 1, "loai_tai_khoan": "chi_phi"},
    )
    return tk


@pytest.fixture
def tk_242(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="242",
        defaults={"ten_tai_khoan": "Chi phí trả trước dài hạn", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_153(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="153",
        defaults={"ten_tai_khoan": "Công cụ dụng cụ", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


class TestCongCuDungCuModel:
    @pytest.mark.django_db
    def test_create_ccdc_nhieu_lan(self, tk_642):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC001",
            ten_ccdc="Máy tính xách tay",
            ngay_mua=date(2026, 1, 15),
            so_luong=Decimal("1"),
            gia_mua=Decimal("15000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=12,
            ky_phan_bo_bat_dau=date(2026, 2, 1),
            ky_phan_bo_ket_thuc=date(2027, 1, 31),
            tk_chi_phi=tk_642,
        )
        assert ccdc.tong_gia_tri == Decimal("15000000")
        assert ccdc.trang_thai == "dang_theo_doi"

    @pytest.mark.django_db
    def test_create_ccdc_1_lan(self, tk_642):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC002",
            ten_ccdc="Văn phòng phẩm",
            ngay_mua=date(2026, 1, 10),
            so_luong=Decimal("10"),
            gia_mua=Decimal("500000"),
            phuong_phap_phan_bo="1_lan",
            so_ky_phan_bo=1,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 1, 31),
            tk_chi_phi=tk_642,
        )
        assert ccdc.tong_gia_tri == Decimal("5000000")
        assert ccdc.so_ky_phan_bo == 1

    @pytest.mark.django_db
    def test_ccdc_str(self, tk_642):
        ccdc = CongCuDungCu(
            ma_ccdc="CCDC003",
            ten_ccdc="Bàn làm việc",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("3000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=24,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2027, 12, 31),
            tk_chi_phi=tk_642,
        )
        assert "CCDC003" in str(ccdc)


class TestCCDCServices:
    @pytest.mark.django_db
    def test_tinh_muc_phan_bo_thang(self, tk_642):
        ccdc = CongCuDungCu(
            ma_ccdc="CCDC004",
            ten_ccdc="Test CCDC",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("12000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=12,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 12, 31),
            tk_chi_phi=tk_642,
        )
        muc = tinh_muc_phan_bo_thang(ccdc)
        assert muc == Decimal("1000000")

    @pytest.mark.django_db
    def test_tinh_muc_phan_bo_invalid(self, tk_642):
        ccdc = CongCuDungCu(
            ma_ccdc="CCDC005",
            ten_ccdc="Invalid CCDC",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("1000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=0,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 12, 31),
            tk_chi_phi=tk_642,
        )
        with pytest.raises(ValidationError):
            tinh_muc_phan_bo_thang(ccdc)

    @pytest.mark.django_db
    def test_tao_bang_phan_bo(self, tk_642):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC006",
            ten_ccdc="Allocated CCDC",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("12000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=3,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 3, 31),
            tk_chi_phi=tk_642,
        )
        allocations = tao_bang_phan_bo(ccdc)
        assert len(allocations) == 3
        assert allocations[0].so_tien_phan_bo == Decimal("4000000")

    @pytest.mark.django_db
    def test_tao_bang_phan_bo_already_exists(self, tk_642):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC007",
            ten_ccdc="Already Allocated",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("6000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=2,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 2, 28),
            tk_chi_phi=tk_642,
        )
        tao_bang_phan_bo(ccdc)
        with pytest.raises(ValidationError):
            tao_bang_phan_bo(ccdc)

    @pytest.mark.django_db
    def test_hach_toan_phan_bo_ccdc(self, tk_642, tk_242):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC008",
            ten_ccdc="Journal CCDC",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("6000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=2,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 2, 28),
            tk_chi_phi=tk_642,
        )
        allocations = tao_bang_phan_bo(ccdc)
        but_toan = hach_toan_phan_bo_ccdc(allocations[0])
        assert but_toan is not None
        assert allocations[0].trang_thai == "da_hach_toan"
        assert but_toan.chi_tiet.count() == 2

    @pytest.mark.django_db
    def test_hach_toan_already_done(self, tk_642, tk_242):
        ccdc = CongCuDungCu.objects.create(
            ma_ccdc="CCDC009",
            ten_ccdc="Double Journal",
            ngay_mua=date(2026, 1, 1),
            so_luong=Decimal("1"),
            gia_mua=Decimal("6000000"),
            phuong_phap_phan_bo="nhieu_lan",
            so_ky_phan_bo=2,
            ky_phan_bo_bat_dau=date(2026, 1, 1),
            ky_phan_bo_ket_thuc=date(2026, 2, 28),
            tk_chi_phi=tk_642,
        )
        allocations = tao_bang_phan_bo(ccdc)
        hach_toan_phan_bo_ccdc(allocations[0])
        with pytest.raises(ValidationError):
            hach_toan_phan_bo_ccdc(allocations[0])
