"""Tests for Sổ sách kế toán app."""

import pytest
from datetime import date
from decimal import Decimal

from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet
from apps.so_sach.services import (
    get_so_ngan_hang,
    get_so_nhat_ky_chung,
    get_so_quy,
)


@pytest.fixture
def tk_111(db):
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="111",
        defaults={"ten_tai_khoan": "Tiền mặt", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_112(db):
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="112",
        defaults={"ten_tai_khoan": "Tiền gửi ngân hàng", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def tk_131(db):
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={"ten_tai_khoan": "Phải thu khách hàng", "cap_do": 1, "loai_tai_khoan": "tai_san"},
    )
    return tk


@pytest.fixture
def posted_journal(db, tk_111, tk_131):
    bt = ButToan.objects.create(
        so_but_toan="BT-TEST-001",
        ngay_hach_toan=date(2026, 1, 15),
        dien_giai="Thu tiền khách hàng",
        trang_thai="posted",
    )
    ButToanChiTiet.objects.create(
        but_toan=bt,
        tai_khoan=tk_111,
        loai_no_co="no",
        so_tien=Decimal("10000000"),
    )
    ButToanChiTiet.objects.create(
        but_toan=bt,
        tai_khoan=tk_131,
        loai_no_co="co",
        so_tien=Decimal("10000000"),
    )
    return bt


class TestSoNhatKyChung:
    @pytest.mark.django_db
    def test_empty_period(self):
        result = get_so_nhat_ky_chung(date(2026, 1, 1), date(2026, 1, 31))
        assert result["lines"] == []
        assert result["tong_no"] == Decimal("0")
        assert result["tong_co"] == Decimal("0")

    @pytest.mark.django_db
    def test_with_posted_entries(self, posted_journal):
        result = get_so_nhat_ky_chung(date(2026, 1, 1), date(2026, 1, 31))
        assert len(result["lines"]) == 2
        assert result["tong_no"] == Decimal("10000000")
        assert result["tong_co"] == Decimal("10000000")
        assert result["can_doi"] is True

    @pytest.mark.django_db
    def test_excludes_draft_entries(self, tk_111, tk_131):
        bt = ButToan.objects.create(
            so_but_toan="BT-DRAFT-001",
            ngay_hach_toan=date(2026, 1, 20),
            dien_giai="Draft entry",
            trang_thai="draft",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_111,
            loai_no_co="no",
            so_tien=Decimal("5000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("5000000"),
        )
        result = get_so_nhat_ky_chung(date(2026, 1, 1), date(2026, 1, 31))
        assert result["lines"] == []


class TestSoQuy:
    @pytest.mark.django_db
    def test_empty_so_quy(self):
        result = get_so_quy(date(2026, 1, 1), date(2026, 1, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert result["days"] == []
        assert result["so_du_cuoi_ky"] == Decimal("0")

    @pytest.mark.django_db
    def test_so_quy_with_entries(self, posted_journal):
        result = get_so_quy(date(2026, 1, 1), date(2026, 1, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert len(result["days"]) == 1
        assert result["so_du_cuoi_ky"] == Decimal("10000000")


class TestSoNganHang:
    @pytest.mark.django_db
    def test_empty_so_ngan_hang(self):
        result = get_so_ngan_hang(date(2026, 1, 1), date(2026, 1, 31))
        assert result["so_du_dau_ky"] == Decimal("0")
        assert result["days"] == []

    @pytest.mark.django_db
    def test_so_ngan_hang_with_entries(self, tk_112, tk_131):
        bt = ButToan.objects.create(
            so_but_toan="BT-BANK-001",
            ngay_hach_toan=date(2026, 2, 1),
            dien_giai="Nhận tiền từ KH",
            trang_thai="posted",
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_112,
            loai_no_co="no",
            so_tien=Decimal("50000000"),
        )
        ButToanChiTiet.objects.create(
            but_toan=bt,
            tai_khoan=tk_131,
            loai_no_co="co",
            so_tien=Decimal("50000000"),
        )
        result = get_so_ngan_hang(date(2026, 2, 1), date(2026, 2, 28))
        assert result["so_du_cuoi_ky"] == Decimal("50000000")
