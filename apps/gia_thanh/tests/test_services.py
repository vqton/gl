"""Tests for Giá Thành services."""

import pytest
from decimal import Decimal

from django.core.exceptions import ValidationError

from apps.gia_thanh.models import (
    BangPhanBoChiPhi,
    BangTinhGiaThanh,
    ChiTietPhanBoChiPhi,
    DoiTuongTapHopChiPhi,
    KhoanMucChiPhi,
    PhieuTapHopChiPhi,
)
from apps.gia_thanh.services import TinhGiaThanhService, tinh_gia_thanh_don_vi


@pytest.fixture
def tk155(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="155",
        defaults={
            "ten_tai_khoan": "Thành phẩm",
            "cap_do": 1,
            "loai_tai_khoan": "tai_san",
        },
    )
    return tk


@pytest.fixture
def tk631(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="631",
        defaults={
            "ten_tai_khoan": "Giá thành sản xuất",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def tk621(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="621",
        defaults={
            "ten_tai_khoan": "Chi phí NLVL trực tiếp",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def doi_tuong(db):
    return DoiTuongTapHopChiPhi.objects.create(
        ma_doi_tuong="SP001",
        ten_doi_tuong="Sản phẩm A",
        loai="san_pham",
    )


@pytest.fixture
def khoan_muc(db, tk621):
    return KhoanMucChiPhi.objects.create(
        ma_khoan_muc="NVL",
        ten_khoan_muc="Nguyên vật liệu",
        loai="nguyen_vat_lieu",
        tk_chi_phi=tk621,
    )


@pytest.fixture
def service():
    return TinhGiaThanhService(thang=1, nam=2026)


class TestTinhGiaThanhDonVi:
    def test_normal_calculation(self):
        result = tinh_gia_thanh_don_vi(
            cp_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("90000000"),
            cp_cuoi_ky=Decimal("5000000"),
            so_luong=Decimal("100"),
        )
        assert result == Decimal("950000")

    def test_zero_quantity(self):
        result = tinh_gia_thanh_don_vi(
            cp_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("40000000"),
            cp_cuoi_ky=Decimal("0"),
            so_luong=Decimal("0"),
        )
        assert result == Decimal("0")

    def test_negative_result_clamped(self):
        result = tinh_gia_thanh_don_vi(
            cp_dau_ky=Decimal("1000000"),
            cp_phat_sinh=Decimal("2000000"),
            cp_cuoi_ky=Decimal("5000000"),
            so_luong=Decimal("10"),
        )
        assert result == Decimal("0")

    def test_no_wip(self):
        result = tinh_gia_thanh_don_vi(
            cp_dau_ky=Decimal("0"),
            cp_phat_sinh=Decimal("50000000"),
            cp_cuoi_ky=Decimal("0"),
            so_luong=Decimal("500"),
        )
        assert result == Decimal("100000")


class TestGetTongChiPhiTheoDoiTuong:
    def test_no_phieu(self, db, service, doi_tuong):
        total = service.get_tong_chi_phi_theo_doi_tuong(doi_tuong)
        assert total == Decimal("0")

    def test_with_posted_phieu(self, db, service, doi_tuong, khoan_muc):
        from datetime import date
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH001",
            ngay_chung_tu=date(2026, 1, 10),
            doi_tuong=doi_tuong,
            khoan_muc=khoan_muc,
            so_tien=Decimal("30000000"),
            trang_thai="posted",
        )
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH002",
            ngay_chung_tu=date(2026, 1, 20),
            doi_tuong=doi_tuong,
            khoan_muc=khoan_muc,
            so_tien=Decimal("20000000"),
            trang_thai="posted",
        )
        total = service.get_tong_chi_phi_theo_doi_tuong(doi_tuong)
        assert total == Decimal("50000000")

    def test_draft_phieu_not_counted(self, db, service, doi_tuong, khoan_muc):
        from datetime import date
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH003",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong,
            khoan_muc=khoan_muc,
            so_tien=Decimal("10000000"),
            trang_thai="draft",
        )
        total = service.get_tong_chi_phi_theo_doi_tuong(doi_tuong)
        assert total == Decimal("0")

    def test_different_month_not_counted(self, db, doi_tuong, khoan_muc):
        from datetime import date
        service = TinhGiaThanhService(thang=1, nam=2026)
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH004",
            ngay_chung_tu=date(2026, 2, 5),
            doi_tuong=doi_tuong,
            khoan_muc=khoan_muc,
            so_tien=Decimal("15000000"),
            trang_thai="posted",
        )
        total = service.get_tong_chi_phi_theo_doi_tuong(doi_tuong)
        assert total == Decimal("0")


class TestGetCpTheoKhoanMuc:
    def test_breakdown_by_type(self, db, service, doi_tuong, tk621):
        from datetime import date
        from apps.danh_muc.models import TaiKhoanKeToan

        tk622 = TaiKhoanKeToan.objects.create(
            ma_tai_khoan="622",
            ten_tai_khoan="Chi phí nhân công",
            cap_do=1,
            loai_tai_khoan="chi_phi",
        )
        km_nvl = KhoanMucChiPhi.objects.create(
            ma_khoan_muc="NVL",
            ten_khoan_muc="Nguyên vật liệu",
            loai="nguyen_vat_lieu",
            tk_chi_phi=tk621,
        )
        km_nc = KhoanMucChiPhi.objects.create(
            ma_khoan_muc="NC",
            ten_khoan_muc="Nhân công",
            loai="nhan_cong",
            tk_chi_phi=tk622,
        )

        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH100",
            ngay_chung_tu=date(2026, 1, 10),
            doi_tuong=doi_tuong,
            khoan_muc=km_nvl,
            so_tien=Decimal("40000000"),
            trang_thai="posted",
        )
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH101",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong,
            khoan_muc=km_nc,
            so_tien=Decimal("30000000"),
            trang_thai="posted",
        )

        result = service.get_cp_theo_khoan_muc(doi_tuong)
        assert result["nguyen_vat_lieu"] == Decimal("40000000")
        assert result["nhan_cong"] == Decimal("30000000")
        assert result["san_xuat_chung"] == Decimal("0")


class TestTaoBangTinhGiaThanh:
    def test_create_with_auto_calc(self, db, service, doi_tuong, khoan_muc):
        from datetime import date
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH200",
            ngay_chung_tu=date(2026, 1, 10),
            doi_tuong=doi_tuong,
            khoan_muc=khoan_muc,
            so_tien=Decimal("80000000"),
            trang_thai="posted",
        )

        bang = service.tao_bang_tinh_gia_thanh(
            doi_tuong=doi_tuong,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_dở_dang_cuoi_ky=Decimal("5000000"),
            so_luong_sp=Decimal("100"),
        )

        assert bang.cp_phat_sinh == Decimal("80000000")
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("85000000")
        assert bang.gia_thanh_don_vi == Decimal("850000")
        assert bang.trang_thai == "draft"


class TestPhanBoChiPhi:
    def test_allocate_by_he_so(self, db, service):
        d1 = DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="DT1", ten_doi_tuong="DT1", loai="san_pham"
        )
        d2 = DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="DT2", ten_doi_tuong="DT2", loai="san_pham"
        )

        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="he_so",
            tieu_thuc_phan_bo="gio_cong",
            tong_chi_phi=Decimal("100000000"),
        )

        service.phan_bo_chi_phi(
            bang_phan_bo=bang,
            chi_tiet_data=[
                {"doi_tuong": d1, "he_so": Decimal("1.5000")},
                {"doi_tuong": d2, "he_so": Decimal("1.0000")},
            ],
        )

        ct_list = list(
            ChiTietPhanBoChiPhi.objects.filter(bang_phan_bo=bang).order_by("pk")
        )
        assert len(ct_list) == 2
        assert ct_list[0].muc_phan_bo == Decimal("60000000")
        assert ct_list[1].muc_phan_bo == Decimal("40000000")

    def test_allocation_rounding_adjustment(self, db):
        d1 = DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="R1", ten_doi_tuong="R1", loai="san_pham"
        )
        d2 = DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="R2", ten_doi_tuong="R2", loai="san_pham"
        )
        d3 = DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="R3", ten_doi_tuong="R3", loai="san_pham"
        )

        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="ty_le",
            tieu_thuc_phan_bo="chi_phi_truc_tiep",
            tong_chi_phi=Decimal("100000000"),
        )
        svc = TinhGiaThanhService(thang=1, nam=2026)
        svc.phan_bo_chi_phi(
            bang_phan_bo=bang,
            chi_tiet_data=[
                {"doi_tuong": d1, "he_so": Decimal("1")},
                {"doi_tuong": d2, "he_so": Decimal("1")},
                {"doi_tuong": d3, "he_so": Decimal("1")},
            ],
        )

        ct_list = list(
            ChiTietPhanBoChiPhi.objects.filter(bang_phan_bo=bang).order_by("pk")
        )
        tong = sum(ct.muc_phan_bo for ct in ct_list)
        assert tong == Decimal("100000000")

    def test_zero_he_so_raises(self, db, doi_tuong):
        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="he_so",
            tieu_thuc_phan_bo="gio_cong",
            tong_chi_phi=Decimal("50000000"),
        )
        service = TinhGiaThanhService(thang=1, nam=2026)
        with pytest.raises(Exception):
            service.phan_bo_chi_phi(
                bang_phan_bo=bang,
                chi_tiet_data=[
                    {"doi_tuong": doi_tuong, "he_so": Decimal("0")},
                ],
            )


class TestDangBangTinhGiaThanh:
    def test_post_creates_journal(self, db, doi_tuong, tk155, tk631):
        bang = BangTinhGiaThanh.objects.create(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("90000000"),
            cp_dở_dang_cuoi_ky=Decimal("0"),
            so_luong_sp=Decimal("100"),
        )
        service = TinhGiaThanhService(thang=1, nam=2026)
        but_toan = service.dang_bang_tinh_gia_thanh(bang)

        assert but_toan is not None
        bang.refresh_from_db()
        assert bang.trang_thai == "posted"

        chi_tiet = list(but_toan.chi_tiet.all())
        assert len(chi_tiet) == 2
        no_entry = [ct for ct in chi_tiet if ct.loai_no_co == "no"][0]
        co_entry = [ct for ct in chi_tiet if ct.loai_no_co == "co"][0]
        assert no_entry.tai_khoan.ma_tai_khoan == "155"
        assert co_entry.tai_khoan.ma_tai_khoan == "631"
        assert no_entry.so_tien == Decimal("100000000")
        assert co_entry.so_tien == Decimal("100000000")

    def test_post_zero_gia_thanh_raises(self, db, doi_tuong):
        bang = BangTinhGiaThanh.objects.create(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong,
            cp_dở_dang_dau_ky=Decimal("0"),
            cp_phat_sinh=Decimal("0"),
            cp_dở_dang_cuoi_ky=Decimal("0"),
            so_luong_sp=Decimal("10"),
        )
        service = TinhGiaThanhService(thang=1, nam=2026)
        with pytest.raises(ValidationError):
            service.dang_bang_tinh_gia_thanh(bang)
