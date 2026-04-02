"""Tests for Thủ Quỹ services."""

import pytest
from datetime import date
from decimal import Decimal

from apps.thu_quy.models import KiemKeQuy, XuLyChenhLechQuy
from apps.thu_quy.services import ThuQuyService


@pytest.fixture
def cashier(db):
    from apps.users.models import NguoiDung
    return NguoiDung.objects.create_user(
        username="thuyquy01",
        password="testpass123",
        user_type="accountant",
    )


@pytest.fixture
def tk111(db):
    from apps.danh_muc.models import TaiKhoanKeToan
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
def tk1388(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="1388",
        defaults={
            "ten_tai_khoan": "Phải thu khác",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk642(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="642",
        defaults={
            "ten_tai_khoan": "Chi phí quản lý doanh nghiệp",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def tk711(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="711",
        defaults={
            "ten_tai_khoan": "Thu nhập khác",
            "cap_do": 1,
            "loai_tai_khoan": "thu_nhap_khac",
        },
    )
    return tk


class TestGetSoDuTienMat:
    def test_zero_balance_no_entries(self, db):
        service = ThuQuyService()
        balance = service.get_so_du_tien_mat(date(2026, 1, 31))
        assert balance == Decimal("0")

    def test_balance_with_receipts(self, db, tk111):
        from apps.nghiep_vu.models import PhieuThu
        PhieuThu.objects.create(
            so_chung_tu="PT001",
            ngay_chung_tu=date(2026, 1, 10),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("50000000"),
            so_tien_vnd=Decimal("50000000"),
            hinh_thuc_thanh_toan="tien_mat",
            tk_no=tk111,
            tk_co=tk111,
            trang_thai="posted",
        )
        service = ThuQuyService()
        balance = service.get_so_du_tien_mat(date(2026, 1, 31))
        assert balance == Decimal("50000000")

    def test_balance_with_receipts_and_payments(self, db, tk111):
        from apps.nghiep_vu.models import PhieuChi, PhieuThu
        PhieuThu.objects.create(
            so_chung_tu="PT002",
            ngay_chung_tu=date(2026, 1, 10),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("100000000"),
            so_tien_vnd=Decimal("100000000"),
            hinh_thuc_thanh_toan="tien_mat",
            tk_no=tk111,
            tk_co=tk111,
            trang_thai="posted",
        )
        PhieuChi.objects.create(
            so_chung_tu="PC001",
            ngay_chung_tu=date(2026, 1, 15),
            loai_chung_tu="phieu_chi",
            so_tien=Decimal("30000000"),
            so_tien_vnd=Decimal("30000000"),
            hinh_thuc_thanh_toan="tien_mat",
            tk_no=tk111,
            tk_co=tk111,
            trang_thai="posted",
        )
        service = ThuQuyService()
        balance = service.get_so_du_tien_mat(date(2026, 1, 31))
        assert balance == Decimal("70000000")

    def test_draft_entries_not_counted(self, db, tk111):
        from apps.nghiep_vu.models import PhieuThu
        PhieuThu.objects.create(
            so_chung_tu="PT003",
            ngay_chung_tu=date(2026, 1, 10),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("25000000"),
            so_tien_vnd=Decimal("25000000"),
            hinh_thuc_thanh_toan="tien_mat",
            tk_no=tk111,
            tk_co=tk111,
            trang_thai="draft",
        )
        service = ThuQuyService()
        balance = service.get_so_du_tien_mat(date(2026, 1, 31))
        assert balance == Decimal("0")


class TestTaoKiemKeQuy:
    def test_create_with_no_entries(self, db, cashier):
        service = ThuQuyService()
        kk = service.tao_kiem_ke_quy(
            so_kiem_ke="KK200",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_thuc_te=Decimal("0"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        assert kk.so_du_so_sach == Decimal("0")
        assert kk.chen_lech == Decimal("0")

    def test_create_with_chen_lech(self, db, cashier, tk111):
        from apps.nghiep_vu.models import PhieuThu
        PhieuThu.objects.create(
            so_chung_tu="PT010",
            ngay_chung_tu=date(2026, 1, 10),
            loai_chung_tu="phieu_thu",
            so_tien=Decimal("100000000"),
            so_tien_vnd=Decimal("100000000"),
            hinh_thuc_thanh_toan="tien_mat",
            tk_no=tk111,
            tk_co=tk111,
            trang_thai="posted",
        )
        service = ThuQuyService()
        kk = service.tao_kiem_ke_quy(
            so_kiem_ke="KK201",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_thuc_te=Decimal("97000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        assert kk.so_du_so_sach == Decimal("100000000")
        assert kk.chen_lech == Decimal("-3000000")


class TestXuLyChenhLech:
    def test_create_xu_ly(self, db, cashier):
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK300",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("96000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        service = ThuQuyService()
        xl = service.xu_ly_chenh_lech(
            kiem_ke=kk,
            loai="thieu",
            nguyen_nhan="Thiếu không rõ nguyên nhân",
            xu_ly="bo_thuong",
        )
        assert xl.so_tien == Decimal("4000000")
        assert xl.loai == "thieu"


class TestDangKiemKeQuy:
    def test_post_no_difference(self, db, cashier):
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK400",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("50000000"),
            so_thuc_te=Decimal("50000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        service = ThuQuyService()
        result = service.dang_kiem_ke_quy(kk)
        assert result is None
        kk.refresh_from_db()
        assert kk.trang_thai == "da_xu_ly"

    def test_post_thieu_quy_bo_thuong(self, db, cashier, tk111, tk1388):
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK401",
            ngay_kiem_ke=date(2026, 1, 31),
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
        service = ThuQuyService()
        but_toan = service.dang_kiem_ke_quy(kk, xl)

        assert but_toan is not None
        chi_tiet = list(but_toan.chi_tiet.all())
        assert len(chi_tiet) == 2
        no_entry = [ct for ct in chi_tiet if ct.loai_no_co == "no"][0]
        assert no_entry.tai_khoan.ma_tai_khoan == "1388"
        assert no_entry.so_tien == Decimal("5000000")

    def test_post_thua_quy(self, db, cashier, tk111, tk711):
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK402",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("80000000"),
            so_thuc_te=Decimal("82000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        xl = XuLyChenhLechQuy.objects.create(
            kiem_ke=kk,
            loai="thua",
            so_tien=Decimal("2000000"),
            nguyen_nhan="Khách hàng trả thừa",
            xu_ly="ghi_tang_thu_nhap",
        )
        service = ThuQuyService()
        but_toan = service.dang_kiem_ke_quy(kk, xl)

        assert but_toan is not None
        chi_tiet = list(but_toan.chi_tiet.all())
        no_entry = [ct for ct in chi_tiet if ct.loai_no_co == "no"][0]
        co_entry = [ct for ct in chi_tiet if ct.loai_no_co == "co"][0]
        assert no_entry.tai_khoan.ma_tai_khoan == "111"
        assert co_entry.tai_khoan.ma_tai_khoan == "711"
        assert no_entry.so_tien == Decimal("2000000")

    def test_post_without_xu_ly_raises(self, db, cashier):
        kk = KiemKeQuy.objects.create(
            so_kiem_ke="KK403",
            ngay_kiem_ke=date(2026, 1, 31),
            ky_quy="T01/2026",
            so_du_so_sach=Decimal("100000000"),
            so_thuc_te=Decimal("90000000"),
            nguoi_kiem_ke="Auditor",
            thu_quy=cashier,
        )
        service = ThuQuyService()
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError):
            service.dang_kiem_ke_quy(kk)
