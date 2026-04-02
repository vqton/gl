"""Tests for Thủ Quỹ models."""

import pytest
from decimal import Decimal

from django.core.exceptions import ValidationError


@pytest.fixture
def cashier(db):
    from apps.users.models import NguoiDung
    return NguoiDung.objects.create_user(
        username="thuyquy01",
        password="testpass123",
        user_type="accountant",
    )


@pytest.fixture
def auditor(db):
    from apps.users.models import NguoiDung
    return NguoiDung.objects.create_user(
        username="kiemke01",
        password="testpass123",
        user_type="admin",
    )


class TestKiemKeQuy:
    def test_auto_calc_chen_lech_thieu(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK001",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("98000000"),
            nguoi_kiem_ke="Nguyen Van A",
            thu_quy=cashier,
        )
        assert kk.chen_lech == Decimal("-2000000")

    def test_auto_calc_chen_lech_thua(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK002",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("50000000"),
            so_thuc_te=Decimal("51500000"),
            nguoi_kiem_ke="Tran Thi B",
            thu_quy=cashier,
        )
        assert kk.chen_lech == Decimal("1500000")

    def test_no_chen_lech(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK003",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("75000000"),
            so_thuc_te=Decimal("75000000"),
            nguoi_kiem_ke="Le Van C",
            thu_quy=cashier,
        )
        assert kk.chen_lech == Decimal("0.00")

    def test_so_thuc_te_negative_raises(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy(
            so_kiem_ke="KK004",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("-5000000"),
            nguoi_kiem_ke="Test User",
            thu_quy=cashier,
        )
        with pytest.raises(ValidationError):
            kk.full_clean()

    def test_segregation_of_duties(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy(
            so_kiem_ke="KK005",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("100000000"),
            nguoi_kiem_ke="thuyquy01",
            thu_quy=cashier,
        )
        with pytest.raises(ValidationError):
            kk.full_clean()

    def test_str_representation(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK-TEST",
            ngay_kiem_ke="2026-01-31",
            ky_quy="Q1/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("100000000"),
            nguoi_kiem_ke="Test User",
            thu_quy=cashier,
        )
        assert "KK-TEST" in str(kk)
        assert "Q1/2026" in str(kk)

    def test_unique_so_kiem_ke(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy
        KiemKeQuy.objects.create(
            so_kiem_ke="UNIQUE-KK",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("100000000"),
            nguoi_kiem_ke="User 1",
            thu_quy=cashier,
        )
        with pytest.raises(Exception):
            KiemKeQuy.objects.create(
                so_kiem_ke="UNIQUE-KK",
                ngay_kiem_ke="2026-02-28",
                ky_quy="T02/2026",
                so_du_so_sach=Decimal("200000000"),
                so_thuc_te=Decimal("200000000"),
                nguoi_kiem_ke="User 2",
                thu_quy=cashier,
            )


class TestXuLyChenhLechQuy:
    def test_create_xu_ly_thieu(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy, XuLyChenhLechQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK100",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("95000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        xl = XuLyChenhLechQuy.objects.create(
            kiem_ke=kk,
            loai="thieu",
            so_tien=Decimal("5000000"),
            nguyen_nhan="Thiếu không rõ nguyên nhân",
            xu_ly="bo_thuong",
        )
        assert xl.loai == "thieu"
        assert xl.so_tien == Decimal("5000000")
        assert xl.xu_ly == "bo_thuong"

    def test_so_tien_must_match_chen_lech(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy, XuLyChenhLechQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK101",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("97000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        xl = XuLyChenhLechQuy(
            kiem_ke=kk,
            loai="thieu",
            so_tien=Decimal("1000000"),
            nguyen_nhan="Test",
            xu_ly="bo_thuong",
        )
        with pytest.raises(ValidationError):
            xl.full_clean()

    def test_so_tien_zero_raises(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy, XuLyChenhLechQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK102",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("99000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        xl = XuLyChenhLechQuy(
            kiem_ke=kk,
            loai="thieu",
            so_tien=Decimal("0"),
            nguyen_nhan="Test",
            xu_ly="bo_thuong",
        )
        with pytest.raises(ValidationError):
            xl.full_clean()

    def test_so_tien_matches_abs_chen_lech(self, db, cashier):
        from apps.thu_quy.models import KiemKeQuy, XuLyChenhLechQuy
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK103",
            ngay_kiem_ke="2026-01-31",
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("103000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        xl = XuLyChenhLechQuy(
            kiem_ke=kk,
            loai="thua",
            so_tien=Decimal("3000000"),
            nguyen_nhan="Thừa do khách hàng trả thừa",
            xu_ly="ghi_tang_thu_nhap",
        )
        xl.full_clean()
        assert xl.so_tien == Decimal("3000000")
