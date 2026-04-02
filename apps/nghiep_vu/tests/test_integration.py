"""Tests for M1/M8: Mua hàng/Bán hàng integration."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.danh_muc.models import HangHoa, KhachHang, NhaCungCap, TaiKhoanKeToan
from apps.kho.models import Kho as KhoInventory, VatTuHangHoa
from apps.nghiep_vu.integration_services import (
    HoaDonDienTuMock,
    hoan_thanh_nhap_kho,
    phat_hanh_hoa_don,
)
from apps.nghiep_vu.models import (
    ButToan,
    ButToanChiTiet,
    HoaDon,
    HoaDonChiTiet,
    Kho as KhoNghiepVu,
    NhapKho,
    NhapKhoChiTiet,
    XuatKho,
    XuatKhoChiTiet,
)
from apps.nghiep_vu.services import tao_hoa_don, tao_nhap_kho


@pytest.fixture
def kho():
    """Create test warehouse (nghiep_vu Kho)."""
    return KhoNghiepVu.objects.create(ma_kho="KHO_M1", ten_kho="Kho M1")


@pytest.fixture
def khach_hang():
    """Create test customer."""
    return KhachHang.objects.create(ma_kh="KH_M1", ten_kh="Khách hàng M1")


@pytest.fixture
def nha_cung_cap():
    """Create test supplier."""
    return NhaCungCap.objects.create(ma_ncc="NCC_M1", ten_ncc="Nhà cung cấp M1")


@pytest.fixture
def hang_hoa():
    """Create test goods item."""
    hh = HangHoa.objects.create(ma_hang_hoa="HH_M1", ten_hang_hoa="Hàng M1")
    VatTuHangHoa.objects.create(
        hang_hoa=hh,
        phuong_phap_tinh_gia="FIFO",
    )
    return hh


@pytest.fixture
def tai_khoan_131():
    """Create or get account 131 (Phải thu khách hàng)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="131",
        defaults={
            "ten_tai_khoan": "Phải thu khách hàng",
            "loai_tai_khoan": "1",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_511():
    """Create or get account 511 (Doanh thu)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="511",
        defaults={
            "ten_tai_khoan": "Doanh thu bán hàng",
            "loai_tai_khoan": "4",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_3331():
    """Create or get account 3331 (Thuế GTGT)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="3331",
        defaults={
            "ten_tai_khoan": "Thuế GTGT phải nộp",
            "loai_tai_khoan": "3",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_156():
    """Create or get account 156 (Hàng hóa)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="156",
        defaults={
            "ten_tai_khoan": "Hàng hóa",
            "loai_tai_khoan": "1",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_331():
    """Create or get account 331 (Phải trả người bán)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="331",
        defaults={
            "ten_tai_khoan": "Phải trả người bán",
            "loai_tai_khoan": "3",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def tai_khoan_632():
    """Create or get account 632 (Giá vốn)."""
    tk, _ = TaiKhoanKeToan.objects.get_or_create(
        ma_tai_khoan="632",
        defaults={
            "ten_tai_khoan": "Giá vốn hàng bán",
            "loai_tai_khoan": "6",
            "cap_do": 1,
        },
    )
    return tk


@pytest.fixture
def hoa_don_with_items(khach_hang, hang_hoa):
    """Create invoice with line items."""
    hoa_don = HoaDon.objects.create(
        so_hoa_don="HD_M1_001",
        ngay_hoa_don=date(2026, 1, 15),
        khach_hang=khach_hang,
        hinh_thuc_thanh_toan="tien_mat",
        trang_thai="draft",
    )
    HoaDonChiTiet.objects.create(
        hoa_don=hoa_don,
        hang_hoa=hang_hoa,
        so_luong=Decimal("10"),
        don_gia=Decimal("100000"),
        thue_suat="10",
        tien_thue=Decimal("100000"),
        tong_tien=Decimal("1100000"),
    )
    hoa_don.tong_tien_truoc_thue = Decimal("1000000")
    hoa_don.tien_thue_gtgt = Decimal("100000")
    hoa_don.tong_cong_thanh_toan = Decimal("1100000")
    hoa_don.save()
    return hoa_don


@pytest.fixture
def nhap_kho_with_items(nha_cung_cap, kho, hang_hoa):
    """Create goods receipt with line items."""
    nhap_kho = NhapKho.objects.create(
        so_chung_tu="NK_M1_001",
        ngay=date(2026, 1, 10),
        kho=kho,
        nha_cung_cap=nha_cung_cap,
        trang_thai="draft",
        tong_tien=Decimal("500000"),
    )
    NhapKhoChiTiet.objects.create(
        nhap_kho=nhap_kho,
        hang_hoa=hang_hoa,
        so_luong=Decimal("10"),
        don_gia=Decimal("50000"),
        thanh_tien=Decimal("500000"),
    )
    return nhap_kho


@pytest.mark.django_db
class TestPhatHanhHoaDon:
    """Test phat_hanh_hoa_don service."""

    def test_issue_invoice_creates_revenue_journal(
        self,
        hoa_don_with_items,
        kho,
        tai_khoan_131,
        tai_khoan_511,
        tai_khoan_3331,
        tai_khoan_632,
        tai_khoan_156,
    ):
        """Test that issuing invoice creates revenue journal entry."""
        result = phat_hanh_hoa_don(hoa_don_with_items, kho_xuat=kho)

        assert result["but_toan_doanh_thu"] is not None
        bt = result["but_toan_doanh_thu"]
        assert bt.so_but_toan == f"BT-HD-{hoa_don_with_items.so_hoa_don}"

        chi_tiet = list(bt.chi_tiet.all())
        assert len(chi_tiet) == 3

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "131"
        assert no_line.so_tien == Decimal("1100000")

        co_lines = [c for c in chi_tiet if c.loai_no_co == "co"]
        assert any(c.tai_khoan.ma_tai_khoan == "511" for c in co_lines)
        assert any(c.tai_khoan.ma_tai_khoan == "3331" for c in co_lines)

    def test_issue_invoice_auto_xuat_kho(
        self,
        hoa_don_with_items,
        kho,
        tai_khoan_131,
        tai_khoan_511,
        tai_khoan_3331,
        tai_khoan_632,
        tai_khoan_156,
    ):
        """Test that issuing invoice auto-creates XuatKho."""
        result = phat_hanh_hoa_don(
            hoa_don_with_items, kho_xuat=kho, tu_dong_xuat_kho=True
        )

        assert len(result["xuat_kho"]) == 1
        xk = result["xuat_kho"][0]
        assert xk.so_chung_tu == f"XK-HD-{hoa_don_with_items.so_hoa_don}"
        assert xk.trang_thai == "completed"

        hoa_don_with_items.refresh_from_db()
        assert hoa_don_with_items.da_xuat_kho is True

    def test_issue_invoice_auto_thanh_toan(
        self,
        hoa_don_with_items,
        kho,
        tai_khoan_131,
        tai_khoan_511,
        tai_khoan_3331,
    ):
        """Test that issuing invoice auto-creates PhieuThu."""
        result = phat_hanh_hoa_don(
            hoa_don_with_items,
            kho_xuat=kho,
            tu_dong_xuat_kho=False,
            tu_dong_thanh_toan=True,
        )

        assert result["phieu_thu"] is not None
        pt = result["phieu_thu"]
        assert pt.so_chung_tu == f"PT-HD-{hoa_don_with_items.so_hoa_don}"
        assert pt.so_tien == Decimal("1100000")

        hoa_don_with_items.refresh_from_db()
        assert hoa_don_with_items.da_thanh_toan is True

    def test_issue_invoice_updates_status(
        self,
        hoa_don_with_items,
        kho,
        tai_khoan_131,
        tai_khoan_511,
        tai_khoan_3331,
        tai_khoan_632,
        tai_khoan_156,
    ):
        """Test that issuing invoice updates status to 'issued'."""
        phat_hanh_hoa_don(hoa_don_with_items, kho_xuat=kho)

        hoa_don_with_items.refresh_from_db()
        assert hoa_don_with_items.trang_thai == "issued"

    def test_issue_invoice_already_issued_raises_error(self, hoa_don_with_items, kho):
        """Test issuing already-issued invoice raises error."""
        hoa_don_with_items.trang_thai = "issued"
        hoa_don_with_items.save()

        with pytest.raises(ValidationError, match="không ở trạng thái nháp"):
            phat_hanh_hoa_don(hoa_don_with_items, kho_xuat=kho)

    def test_issue_invoice_no_items_raises_error(self, khach_hang, kho):
        """Test issuing invoice with no items raises error."""
        hoa_don = HoaDon.objects.create(
            so_hoa_don="HD_EMPTY",
            ngay_hoa_don=date(2026, 1, 15),
            khach_hang=khach_hang,
            trang_thai="draft",
        )

        with pytest.raises(ValidationError, match="ít nhất một mặt hàng"):
            phat_hanh_hoa_don(hoa_don, kho_xuat=kho)


@pytest.mark.django_db
class TestHoanThanhNhapKho:
    """Test hoan_thanh_nhap_kho service."""

    def test_complete_nhap_kho_creates_journal(
        self, nhap_kho_with_items, tai_khoan_156, tai_khoan_331
    ):
        """Test completing receipt creates journal entry."""
        result = hoan_thanh_nhap_kho(nhap_kho_with_items)

        assert result["but_toan"] is not None
        bt = result["but_toan"]
        assert bt.so_but_toan == f"BT-NK-{nhap_kho_with_items.so_chung_tu}"

        chi_tiet = list(bt.chi_tiet.all())
        assert len(chi_tiet) == 2

        no_line = next(c for c in chi_tiet if c.loai_no_co == "no")
        assert no_line.tai_khoan.ma_tai_khoan == "156"
        assert no_line.so_tien == Decimal("500000")

        co_line = next(c for c in chi_tiet if c.loai_no_co == "co")
        assert co_line.tai_khoan.ma_tai_khoan == "331"
        assert co_line.so_tien == Decimal("500000")

    def test_complete_nhap_kho_updates_status(
        self, nhap_kho_with_items, tai_khoan_156, tai_khoan_331
    ):
        """Test completing receipt updates status to 'completed'."""
        hoan_thanh_nhap_kho(nhap_kho_with_items)

        nhap_kho_with_items.refresh_from_db()
        assert nhap_kho_with_items.trang_thai == "completed"

    def test_complete_nhap_kho_already_completed_raises_error(
        self, nhap_kho_with_items
    ):
        """Test completing already-completed receipt raises error."""
        nhap_kho_with_items.trang_thai = "completed"
        nhap_kho_with_items.save()

        with pytest.raises(ValidationError, match="không ở trạng thái nháp"):
            hoan_thanh_nhap_kho(nhap_kho_with_items)

    def test_complete_nhap_kho_no_items_raises_error(self, nha_cung_cap, kho):
        """Test completing receipt with no items raises error."""
        nhap_kho = NhapKho.objects.create(
            so_chung_tu="NK_EMPTY",
            ngay=date(2026, 1, 10),
            kho=kho,
            nha_cung_cap=nha_cung_cap,
            trang_thai="draft",
        )

        with pytest.raises(ValidationError, match="ít nhất một mặt hàng"):
            hoan_thanh_nhap_kho(nhap_kho)


@pytest.mark.django_db
class TestHoaDonDienTuMock:
    """Test HoaDonDienTuMock e-invoice API."""

    def test_dang_ky_hoa_don(self, hoa_don_with_items):
        """Test registering invoice with mock API."""
        result = HoaDonDienTuMock.dang_ky_hoa_don(hoa_don_with_items)

        assert result["trang_thai"] == "accepted"
        assert result["ma_hoa_don_gdt"] == f"GDT{hoa_don_with_items.so_hoa_don}"

    def test_huy_hoa_don(self, hoa_don_with_items):
        """Test cancelling invoice via mock API."""
        result = HoaDonDienTuMock.huy_hoa_don(hoa_don_with_items, ly_do="Sai thông tin")

        assert result["trang_thai"] == "cancelled"
        assert result["ly_do"] == "Sai thông tin"

    def test_tra_cuu_hoa_don(self):
        """Test looking up invoice status."""
        result = HoaDonDienTuMock.tra_cuu_hoa_don("GDT001")

        assert result["trang_thai"] == "valid"
        assert result["da_ghi_nhan"] is True
