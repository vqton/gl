"""Tests for Công nợ app."""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from apps.cong_no.models import BienBanDoiChieuCongNo, CongNoPhaiThu, CongNoPhaiTra
from apps.cong_no.services import (
    AGING_BUCKETS,
    kiem_tra_cong_no_chua_doi_chieu,
    phan_loai_cong_no,
    tao_bien_ban_doi_chieu,
)


class TestCongNoPhaiThuModel:
    @pytest.mark.django_db
    def test_create_cong_no_phai_thu(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH001", ten_kh="Khách hàng A")
        cn = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("100000000"),
            da_thu=Decimal("30000000"),
        )
        assert cn.con_no == Decimal("70000000")
        assert cn.qua_han is False

    @pytest.mark.django_db
    def test_cong_no_overdue(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH002", ten_kh="Khách hàng B")
        cn = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("50000000"),
            da_thu=Decimal("0"),
            ngay_den_han=date.today() - timedelta(days=30),
        )
        assert cn.qua_han is True
        assert cn.con_no == Decimal("50000000")

    @pytest.mark.django_db
    def test_cong_no_fully_paid(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH003", ten_kh="Khách hàng C")
        cn = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("50000000"),
            da_thu=Decimal("50000000"),
        )
        assert cn.con_no == Decimal("0")


class TestCongNoPhaiTraModel:
    @pytest.mark.django_db
    def test_create_cong_no_phai_tra(self):
        from apps.danh_muc.models import NhaCungCap
        ncc = NhaCungCap.objects.create(ma_ncc="NCC001", ten_ncc="NCC A")
        cn = CongNoPhaiTra.objects.create(
            nha_cung_cap=ncc,
            tong_no=Decimal("200000000"),
            da_tra=Decimal("50000000"),
        )
        assert cn.con_no == Decimal("150000000")


class TestBienBanDoiChieuCongNo:
    @pytest.mark.django_db
    def test_create_bien_ban(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH004", ten_kh="Khách hàng D")
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(kh)
        bb = BienBanDoiChieuCongNo.objects.create(
            doi_tuong_content_type=ct,
            doi_tuong_object_id=kh.pk,
            loai="phai_thu",
            thang=1,
            nam=2026,
            so_dau_ky=Decimal("100000000"),
            phat_sinh_no=Decimal("50000000"),
            phat_sinh_co=Decimal("30000000"),
        )
        assert bb.so_cuoi_ky == Decimal("120000000")
        assert bb.da_xac_nhan is False


class TestAgingClassification:
    @pytest.mark.django_db
    def test_phan_loai_cong_no(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH005", ten_kh="KH Test")
        cn1 = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("10000000"),
            da_thu=Decimal("0"),
            ngay_den_han=date.today() - timedelta(days=10),
        )
        cn2 = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("20000000"),
            da_thu=Decimal("0"),
            ngay_den_han=date.today() - timedelta(days=45),
        )
        buckets = phan_loai_cong_no([cn1, cn2])
        assert len(buckets["0-30 ngày"]) == 1
        assert len(buckets["31-60 ngày"]) == 1

    @pytest.mark.django_db
    def test_phan_loai_cong_no_no_debt(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH006", ten_kh="KH No Debt")
        cn = CongNoPhaiThu.objects.create(
            khach_hang=kh,
            tong_no=Decimal("10000000"),
            da_thu=Decimal("10000000"),
        )
        buckets = phan_loai_cong_no([cn])
        for label in ["0-30 ngày", "31-60 ngày", "61-90 ngày", "91-120 ngày", ">120 ngày"]:
            assert len(buckets[label]) == 0


class TestDebtConfirmation:
    @pytest.mark.django_db
    def test_tao_bien_ban_doi_chieu(self):
        from apps.danh_muc.models import KhachHang
        kh = KhachHang.objects.create(ma_kh="KH007", ten_kh="KH Confirm")
        bb = tao_bien_ban_doi_chieu(
            doi_tuong=kh,
            loai="phai_thu",
            thang=6,
            nam=2026,
            so_dau_ky=Decimal("50000000"),
            phat_sinh_no=Decimal("20000000"),
            phat_sinh_co=Decimal("10000000"),
        )
        assert bb.so_cuoi_ky == Decimal("60000000")

    @pytest.mark.django_db
    def test_kiem_tra_cong_no_chua_doi_chieu(self):
        assert kiem_tra_cong_no_chua_doi_chieu(12, 2025) is False

    @pytest.mark.django_db
    def test_invalid_month(self):
        from apps.danh_muc.models import KhachHang
        from django.core.exceptions import ValidationError
        kh = KhachHang.objects.create(ma_kh="KH008", ten_kh="KH Invalid")
        with pytest.raises(ValidationError):
            tao_bien_ban_doi_chieu(kh, "phai_thu", 13, 2026, Decimal("0"), Decimal("0"), Decimal("0"))
