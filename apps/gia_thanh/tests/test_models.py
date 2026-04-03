"""Tests for Giá Thành models."""

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


@pytest.fixture
def tk621(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="621",
        defaults={
            "ten_tai_khoan": "Chi phí nguyên liệu, vật liệu trực tiếp",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def tk622(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="622",
        defaults={
            "ten_tai_khoan": "Chi phí nhân công trực tiếp",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def tk627(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="627",
        defaults={
            "ten_tai_khoan": "Chi phí sản xuất chung",
            "cap_do": 1,
            "loai_tai_khoan": "chi_phi",
        },
    )
    return tk


@pytest.fixture
def doi_tuong_san_pham(db):
    return DoiTuongTapHopChiPhi.objects.create(
        ma_doi_tuong="SP001",
        ten_doi_tuong="Sản phẩm A",
        loai="san_pham",
    )


@pytest.fixture
def doi_tuong_don_hang(db):
    return DoiTuongTapHopChiPhi.objects.create(
        ma_doi_tuong="DH001",
        ten_doi_tuong="Đơn hàng #100",
        loai="don_hang",
    )


@pytest.fixture
def khoan_muc_nvl(db, tk621):
    return KhoanMucChiPhi.objects.create(
        ma_khoan_muc="NVL",
        ten_khoan_muc="Nguyên vật liệu trực tiếp",
        loai="nguyen_vat_lieu",
        tk_chi_phi=tk621,
    )


@pytest.fixture
def khoan_muc_nc(db, tk622):
    return KhoanMucChiPhi.objects.create(
        ma_khoan_muc="NC",
        ten_khoan_muc="Nhân công trực tiếp",
        loai="nhan_cong",
        tk_chi_phi=tk622,
    )


@pytest.fixture
def khoan_muc_sxc(db, tk627):
    return KhoanMucChiPhi.objects.create(
        ma_khoan_muc="SXC",
        ten_khoan_muc="Chi phí sản xuất chung",
        loai="san_xuat_chung",
        tk_chi_phi=tk627,
    )


class TestDoiTuongTapHopChiPhi:
    def test_create_san_pham(self, doi_tuong_san_pham):
        assert doi_tuong_san_pham.ma_doi_tuong == "SP001"
        assert doi_tuong_san_pham.loai == "san_pham"
        assert str(doi_tuong_san_pham) == "SP001 - Sản phẩm A"

    def test_create_don_hang(self, doi_tuong_don_hang):
        assert doi_tuong_don_hang.loai == "don_hang"

    def test_unique_ma_doi_tuong(self, db):
        DoiTuongTapHopChiPhi.objects.create(
            ma_doi_tuong="X1", ten_doi_tuong="X", loai="san_pham"
        )
        with pytest.raises(Exception):
            DoiTuongTapHopChiPhi.objects.create(
                ma_doi_tuong="X1", ten_doi_tuong="Y", loai="san_pham"
            )


class TestKhoanMucChiPhi:
    def test_create_khoan_muc(self, khoan_muc_nvl):
        assert khoan_muc_nvl.ma_khoan_muc == "NVL"
        assert khoan_muc_nvl.loai == "nguyen_vat_lieu"
        assert str(khoan_muc_nvl) == "NVL - Nguyên vật liệu trực tiếp"

    def test_khoan_muc_has_account(self, khoan_muc_nvl, tk621):
        assert khoan_muc_nvl.tk_chi_phi == tk621


class TestPhieuTapHopChiPhi:
    def test_create_phieu(self, db, doi_tuong_san_pham, khoan_muc_nvl):
        from datetime import date
        phieu = PhieuTapHopChiPhi.objects.create(
            so_chung_tu="TH001",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong_san_pham,
            khoan_muc=khoan_muc_nvl,
            so_tien=Decimal("50000000"),
            dien_giai="Mua nguyên liệu sản xuất A",
        )
        assert phieu.trang_thai == "draft"
        assert phieu.so_tien == Decimal("50000000")
        assert str(phieu) == "TH001 - SP001 - Sản phẩm A"

    def test_so_tien_must_be_positive(self, db, doi_tuong_san_pham, khoan_muc_nvl):
        from datetime import date
        phieu = PhieuTapHopChiPhi(
            so_chung_tu="TH002",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong_san_pham,
            khoan_muc=khoan_muc_nvl,
            so_tien=Decimal("-1000"),
        )
        with pytest.raises(ValidationError):
            phieu.full_clean()

    def test_so_tien_zero_invalid(self, db, doi_tuong_san_pham, khoan_muc_nvl):
        from datetime import date
        phieu = PhieuTapHopChiPhi(
            so_chung_tu="TH003",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong_san_pham,
            khoan_muc=khoan_muc_nvl,
            so_tien=Decimal("0"),
        )
        with pytest.raises(ValidationError):
            phieu.full_clean()

    def test_unique_so_chung_tu(self, db, doi_tuong_san_pham, khoan_muc_nvl):
        from datetime import date
        PhieuTapHopChiPhi.objects.create(
            so_chung_tu="UNIQUE1",
            ngay_chung_tu=date(2026, 1, 15),
            doi_tuong=doi_tuong_san_pham,
            khoan_muc=khoan_muc_nvl,
            so_tien=Decimal("100000"),
        )
        with pytest.raises(Exception):
            PhieuTapHopChiPhi.objects.create(
                so_chung_tu="UNIQUE1",
                ngay_chung_tu=date(2026, 1, 16),
                doi_tuong=doi_tuong_san_pham,
                khoan_muc=khoan_muc_nvl,
                so_tien=Decimal("200000"),
            )


class TestBangPhanBoChiPhi:
    def test_create_bang_phan_bo(self, db):
        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="he_so",
            tieu_thuc_phan_bo="gio_cong",
            tong_chi_phi=Decimal("100000000"),
        )
        assert bang.trang_thai == "draft"
        assert str(bang) == "Phân bổ T1/2026 - Hệ số"

    def test_tong_chi_phi_must_be_positive(self, db):
        bang = BangPhanBoChiPhi(
            thang=1,
            nam=2026,
            phuong_phap="he_so",
            tieu_thuc_phan_bo="gio_cong",
            tong_chi_phi=Decimal("-5000"),
        )
        with pytest.raises(ValidationError):
            bang.full_clean()

    def test_tong_da_phan_bo(self, db, doi_tuong_san_pham, doi_tuong_don_hang):
        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="ty_le",
            tieu_thuc_phan_bo="chi_phi_truc_tiep",
            tong_chi_phi=Decimal("100000000"),
        )
        ChiTietPhanBoChiPhi.objects.create(
            bang_phan_bo=bang,
            doi_tuong=doi_tuong_san_pham,
            he_so=Decimal("1.5000"),
            muc_phan_bo=Decimal("60000000"),
        )
        ChiTietPhanBoChiPhi.objects.create(
            bang_phan_bo=bang,
            doi_tuong=doi_tuong_don_hang,
            he_so=Decimal("1.0000"),
            muc_phan_bo=Decimal("40000000"),
        )
        assert bang.tong_da_phan_bo() == Decimal("100000000")


class TestChiTietPhanBoChiPhi:
    def test_create_chi_tiet(self, db, doi_tuong_san_pham):
        bang = BangPhanBoChiPhi.objects.create(
            thang=1,
            nam=2026,
            phuong_phap="he_so",
            tieu_thuc_phan_bo="gio_cong",
            tong_chi_phi=Decimal("100000000"),
        )
        ct = ChiTietPhanBoChiPhi.objects.create(
            bang_phan_bo=bang,
            doi_tuong=doi_tuong_san_pham,
            he_so=Decimal("1.5000"),
            muc_phan_bo=Decimal("60000000"),
        )
        assert ct.he_so == Decimal("1.5000")
        assert ct.muc_phan_bo == Decimal("60000000")


class TestBangTinhGiaThanh:
    def test_auto_calc_gia_thanh(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("90000000"),
            cp_dở_dang_cuoi_ky=Decimal("5000000"),
            so_luong_sp=Decimal("100"),
        )
        bang.save()
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("95000000")
        assert bang.gia_thanh_don_vi == Decimal("950000")

    def test_gia_thanh_formula(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("0"),
            cp_phat_sinh=Decimal("50000000"),
            cp_dở_dang_cuoi_ky=Decimal("0"),
            so_luong_sp=Decimal("50"),
        )
        bang.save()
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("50000000")
        assert bang.gia_thanh_don_vi == Decimal("1000000")

    def test_cp_dở_dang_cuoi_ky_exceeds_total(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("20000000"),
            cp_dở_dang_cuoi_ky=Decimal("50000000"),
            so_luong_sp=Decimal("10"),
        )
        with pytest.raises(ValidationError):
            bang.full_clean()

    def test_cp_phat_sinh_negative(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("-5000000"),
            cp_dở_dang_cuoi_ky=Decimal("0"),
            so_luong_sp=Decimal("10"),
        )
        with pytest.raises(ValidationError):
            bang.full_clean()

    def test_gia_thanh_zero_when_negative(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("5000000"),
            cp_phat_sinh=Decimal("10000000"),
            cp_dở_dang_cuoi_ky=Decimal("20000000"),
            so_luong_sp=Decimal("10"),
        )
        bang.save()
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("0.00")
        assert bang.gia_thanh_don_vi == Decimal("0.0000")

    def test_gia_thanh_don_vi_zero_when_no_quantity(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("10000000"),
            cp_phat_sinh=Decimal("40000000"),
            cp_dở_dang_cuoi_ky=Decimal("0"),
            so_luong_sp=Decimal("0"),
        )
        bang.save()
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("50000000")
        assert bang.gia_thanh_don_vi == Decimal("0.0000")

    def test_str_representation(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh.objects.create(
            thang=3,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_phat_sinh=Decimal("100000000"),
        )
        assert "GT T3/2026" in str(bang)

    def test_decimal_precision(self, db, doi_tuong_san_pham):
        bang = BangTinhGiaThanh(
            thang=1,
            nam=2026,
            doi_tuong=doi_tuong_san_pham,
            cp_dở_dang_dau_ky=Decimal("10000000.50"),
            cp_phat_sinh=Decimal("89999999.50"),
            cp_dở_dang_cuoi_ky=Decimal("0.00"),
            so_luong_sp=Decimal("3"),
        )
        bang.save()
        assert bang.gia_thanh_sp_hoan_thanh == Decimal("100000000.00")
        assert bang.gia_thanh_don_vi == Decimal("33333333.3333")
