"""Tests for Thuế app."""

import pytest
from datetime import date
from decimal import Decimal

from apps.thue.models import BangKeHoaDonBanRa, BangKeHoaDonMuaVao, ToKhaiGTGT, ToKhaiTNCN, ToKhaiTNDNTamTinh
from apps.thue.services import tinh_thue_tncn


class TestBangKeHoaDon:
    @pytest.mark.django_db
    def test_create_bang_ke_mua_vao(self):
        bk = BangKeHoaDonMuaVao.objects.create(
            thang=1,
            nam=2026,
            ma_so_thue_ncc="0123456789",
            tien_chua_thue=Decimal("100000000"),
            thue_gtgt=Decimal("10000000"),
        )
        assert bk.tong_tien == Decimal("110000000")

    @pytest.mark.django_db
    def test_create_bang_ke_ban_ra(self):
        from apps.danh_muc.models import KhachHang
        from apps.nghiep_vu.models import HoaDon
        kh = KhachHang.objects.create(ma_kh="KH010", ten_kh="KH Ban Ra")
        hd = HoaDon.objects.create(
            so_hoa_don="HD-TEST-001",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=kh,
        )
        bk = BangKeHoaDonBanRa.objects.create(
            thang=1,
            nam=2026,
            hoa_don=hd,
            ma_so_thue_kh="0123456789",
            tien_chua_thue=Decimal("200000000"),
            thue_gtgt=Decimal("20000000"),
        )
        assert bk.tong_tien == Decimal("220000000")


class TestToKhaiGTGT:
    @pytest.mark.django_db
    def test_create_to_khai_gtgt(self):
        tk = ToKhaiGTGT.objects.create(
            thang=1,
            nam=2026,
            tong_doanh_so_ban=Decimal("500000000"),
            thue_gtgt_dau_ra=Decimal("50000000"),
            tong_gia_tri_mua_vao=Decimal("300000000"),
            thue_gtgt_dau_vao=Decimal("30000000"),
        )
        assert tk.thue_gtgt_phai_nop == Decimal("20000000")

    @pytest.mark.django_db
    def test_to_khai_gtgt_no_tax_due(self):
        tk = ToKhaiGTGT.objects.create(
            thang=2,
            nam=2026,
            tong_doanh_so_ban=Decimal("100000000"),
            thue_gtgt_dau_ra=Decimal("10000000"),
            tong_gia_tri_mua_vao=Decimal("200000000"),
            thue_gtgt_dau_vao=Decimal("20000000"),
        )
        assert tk.thue_gtgt_phai_nop == Decimal("0")

    @pytest.mark.django_db
    def test_to_khai_unique_constraint(self):
        ToKhaiGTGT.objects.create(
            thang=3,
            nam=2026,
            tong_doanh_so_ban=Decimal("100000000"),
            thue_gtgt_dau_ra=Decimal("10000000"),
            tong_gia_tri_mua_vao=Decimal("50000000"),
            thue_gtgt_dau_vao=Decimal("5000000"),
        )
        with pytest.raises(Exception):
            ToKhaiGTGT.objects.create(
                thang=3,
                nam=2026,
                tong_doanh_so_ban=Decimal("200000000"),
                thue_gtgt_dau_ra=Decimal("20000000"),
                tong_gia_tri_mua_vao=Decimal("100000000"),
                thue_gtgt_dau_vao=Decimal("10000000"),
            )


class TestToKhaiTNDNTamTinh:
    @pytest.mark.django_db
    def test_create_to_khai_tndn(self):
        tk = ToKhaiTNDNTamTinh.objects.create(
            quy=1,
            nam=2026,
            doanh_thu=Decimal("1000000000"),
            chi_phi_duoc_tru=Decimal("700000000"),
            loi_nhuan=Decimal("300000000"),
            thue_phai_nop=Decimal("45000000"),
        )
        assert tk.thue_phai_nop == Decimal("45000000")
        assert str(tk) == "TNDN Q1/2026"


class TestToKhaiTNCN:
    @pytest.mark.django_db
    def test_create_to_khai_tncn(self):
        tk = ToKhaiTNCN.objects.create(
            thang=1,
            nam=2026,
            tong_thu_nhap=Decimal("500000000"),
            tong_thue_tncn=Decimal("50000000"),
            so_nhan_vien=10,
        )
        assert tk.tong_thue_tncn == Decimal("50000000")
        assert str(tk) == "TNCN - 1/2026"


class TestTNCNCalculation:
    def test_tinh_thue_tncn_zero(self):
        assert tinh_thue_tncn(Decimal("0")) == Decimal("0")

    def test_tinh_thue_tncn_low_income(self):
        thue = tinh_thue_tncn(Decimal("5000000"))
        assert thue >= 0

    def test_tinh_thue_tncn_high_income(self):
        thue = tinh_thue_tncn(Decimal("100000000"))
        assert thue > 0
