"""Tests for Ngân hàng app."""

import pytest
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

from apps.danh_muc.models import NganHang, TaiKhoanNganHang
from apps.ngan_hang.models import DoiChieuNganHang, GiayBaoCo, GiayBaoNo, UyNhiemChi
from apps.ngan_hang.services import (
    post_giay_bao_co,
    post_giay_bao_no,
    tao_doi_chieu_ngan_hang,
    tinh_so_du_so_sach,
)
from apps.ngan_hang.validators import validate_so_tien_duong_choi


@pytest.fixture
def ngan_hang(db):
    return NganHang.objects.create(
        ma_ngan_hang="VCB",
        ten_ngan_hang="Ngân hàng Vietcombank",
    )


@pytest.fixture
def tai_khoan_ngan_hang(db, ngan_hang):
    return TaiKhoanNganHang.objects.create(
        ngan_hang=ngan_hang,
        so_tai_khoan="0123456789",
        ten_chu_tai_khoan="Công ty TNHH SME",
    )


@pytest.fixture
def tk_112(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="112",
        defaults={"ten_tai_khoan": "Tiền gửi ngân hàng", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_131(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={"ten_tai_khoan": "Phải thu khách hàng", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_331(db):
    from apps.danh_muc.models import TaiKhoanKeToan
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={"ten_tai_khoan": "Phải trả người bán", "cap_do": 1, "loai_tai_khoan": "no_phai_tra"},
    )
    return tk


class TestGiayBaoNoModel:
    def test_create_giay_bao_no(self, tai_khoan_ngan_hang):
        gbn = GiayBaoNo.objects.create(
            so_chung_tu="GBN-001",
            ngay=date(2026, 1, 15),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("10000000"),
            dien_giai="Phí ngân hàng tháng 1",
        )
        assert gbn.trang_thai == "draft"
        assert gbn.da_doi_chieu is False
        assert str(gbn) == "GBN-001 - 2026-01-15 - 10000000"

    def test_giay_bao_no_str(self, tai_khoan_ngan_hang):
        gbn = GiayBaoNo(
            so_chung_tu="GBN-002",
            ngay=date(2026, 2, 1),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("5000000"),
        )
        assert "GBN-002" in str(gbn)


class TestGiayBaoCoModel:
    def test_create_giay_bao_co(self, tai_khoan_ngan_hang):
        gbc = GiayBaoCo.objects.create(
            so_chung_tu="GBC-001",
            ngay=date(2026, 1, 20),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("50000000"),
            dien_giai="Khách hàng chuyển khoản thanh toán",
        )
        assert gbc.trang_thai == "draft"
        assert str(gbc) == "GBC-001 - 2026-01-20 - 50000000"


class TestUyNhiemChiModel:
    def test_create_uy_nhiem_chi(self, tai_khoan_ngan_hang):
        from apps.danh_muc.models import NhaCungCap
        ncc = NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Nhà cung cấp A",
        )
        unc = UyNhiemChi.objects.create(
            so_chung_tu="UNC-001",
            ngay=date(2026, 1, 25),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            nha_cung_cap=ncc,
            so_tien=Decimal("25000000"),
            noi_dung="Thanh toán hóa đơn tháng 1",
        )
        assert unc.trang_thai == "draft"
        assert "UNC-001" in str(unc)


class TestDoiChieuNganHangModel:
    def test_create_doi_chieu(self, tai_khoan_ngan_hang):
        dc = DoiChieuNganHang.objects.create(
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            thang=1,
            nam=2026,
            so_du_so_sach=Decimal("100000000"),
            so_du_ngan_hang=Decimal("100000000"),
        )
        assert dc.chenh_lech == Decimal("0")
        assert dc.trang_thai == "da_doi_chieu"

    def test_doi_chieu_co_chenh_lech(self, tai_khoan_ngan_hang):
        dc = DoiChieuNganHang.objects.create(
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            thang=2,
            nam=2026,
            so_du_so_sach=Decimal("100000000"),
            so_du_ngan_hang=Decimal("98000000"),
        )
        assert dc.chenh_lech == Decimal("2000000")
        assert dc.trang_thai == "co_chenh_lech"

    def test_unique_constraint(self, tai_khoan_ngan_hang):
        DoiChieuNganHang.objects.create(
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            thang=1,
            nam=2026,
            so_du_so_sach=Decimal("100000000"),
            so_du_ngan_hang=Decimal("100000000"),
        )
        with pytest.raises(Exception):
            DoiChieuNganHang.objects.create(
                tai_khoan_ngan_hang=tai_khoan_ngan_hang,
                thang=1,
                nam=2026,
                so_du_so_sach=Decimal("50000000"),
                so_du_ngan_hang=Decimal("50000000"),
            )


class TestValidators:
    def test_validate_so_tien_duong_choi_valid(self):
        validate_so_tien_duong_choi(Decimal("1000000"))

    def test_validate_so_tien_duong_choi_zero(self):
        with pytest.raises(ValidationError):
            validate_so_tien_duong_choi(Decimal("0"))

    def test_validate_so_tien_duong_choi_negative(self):
        with pytest.raises(ValidationError):
            validate_so_tien_duong_choi(Decimal("-1000"))


class TestBankServices:
    @pytest.mark.django_db
    def test_post_giay_bao_no_creates_journal(self, tai_khoan_ngan_hang, tk_112, tk_331):
        gbn = GiayBaoNo.objects.create(
            so_chung_tu="GBN-TEST-001",
            ngay=date(2026, 1, 15),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("10000000"),
            dien_giai="Phí dịch vụ",
        )
        but_toan = post_giay_bao_no(gbn)
        assert but_toan is not None
        assert gbn.trang_thai == "posted"
        assert but_toan.chi_tiet.count() == 2

    @pytest.mark.django_db
    def test_post_giay_bao_co_creates_journal(self, tai_khoan_ngan_hang, tk_112, tk_131):
        gbc = GiayBaoCo.objects.create(
            so_chung_tu="GBC-TEST-001",
            ngay=date(2026, 1, 20),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("50000000"),
            dien_giai="Khách hàng thanh toán",
        )
        but_toan = post_giay_bao_co(gbc)
        assert but_toan is not None
        assert gbc.trang_thai == "posted"
        assert but_toan.chi_tiet.count() == 2

    @pytest.mark.django_db
    def test_post_giay_bao_no_already_posted(self, tai_khoan_ngan_hang, tk_112, tk_331):
        gbn = GiayBaoNo.objects.create(
            so_chung_tu="GBN-TEST-002",
            ngay=date(2026, 1, 15),
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            so_tien=Decimal("10000000"),
            trang_thai="posted",
        )
        with pytest.raises(ValidationError):
            post_giay_bao_no(gbn)

    @pytest.mark.django_db
    def test_tao_doi_chieu_ngan_hang_matched(self, tai_khoan_ngan_hang):
        dc = tao_doi_chieu_ngan_hang(
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            thang=3,
            nam=2026,
            so_du_so_sach=Decimal("100000000"),
            so_du_ngan_hang=Decimal("100000000"),
        )
        assert dc.trang_thai == "da_doi_chieu"
        assert dc.chenh_lech == Decimal("0")

    @pytest.mark.django_db
    def test_tao_doi_chieu_ngan_hang_mismatch(self, tai_khoan_ngan_hang):
        dc = tao_doi_chieu_ngan_hang(
            tai_khoan_ngan_hang=tai_khoan_ngan_hang,
            thang=4,
            nam=2026,
            so_du_so_sach=Decimal("100000000"),
            so_du_ngan_hang=Decimal("95000000"),
        )
        assert dc.trang_thai == "co_chenh_lech"
        assert dc.chenh_lech == Decimal("5000000")

    @pytest.mark.django_db
    def test_tao_doi_chieu_invalid_month(self, tai_khoan_ngan_hang):
        with pytest.raises(ValidationError):
            tao_doi_chieu_ngan_hang(
                tai_khoan_ngan_hang=tai_khoan_ngan_hang,
                thang=13,
                nam=2026,
                so_du_so_sach=Decimal("0"),
                so_du_ngan_hang=Decimal("0"),
            )

    @pytest.mark.django_db
    def test_tinh_so_du_so_sach_empty(self, tai_khoan_ngan_hang, tk_112):
        result = tinh_so_du_so_sach(tai_khoan_ngan_hang, 1, 2026)
        assert result == Decimal("0")
