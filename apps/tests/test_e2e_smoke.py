"""E2E Smoke Tests - Quick verification that all modules work end-to-end.

Run with: pytest apps/tests/test_e2e_smoke.py -v

These tests verify the complete flow from data creation to reporting.
"""

from datetime import date
from decimal import Decimal

import pytest
from django.urls import reverse

from apps.danh_muc.models import HangHoa, KhachHang, NhaCungCap, TaiKhoanKeToan
from apps.kho.models import Kho as KhoInventory, VatTuHangHoa
from apps.nghiep_vu.ket_chuyen import ket_chuyen_cuoi_ky
from apps.nghiep_vu.models import ButToan, ButToanChiTiet, PhieuChi, PhieuThu
from apps.nghiep_vu.services import tao_phieu_chi, tao_phieu_thu


@pytest.fixture
def setup_e2e_data():
    """Create minimal data for E2E testing."""
    # Create accounts
    for code, name in [
        ("111", "Tiền mặt"),
        ("112", "Tiền gửi NH"),
        ("131", "Phải thu KH"),
        ("331", "Phải trả NCC"),
        ("511", "Doanh thu"),
        ("642", "Chi phí QLDN"),
        ("911", "Xác định KQKD"),
        ("421", "Lợi nhuận chưa phân phối"),
    ]:
        TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan=code,
            defaults={"ten_tai_khoan": name, "loai_tai_khoan": "1", "cap_do": 1},
        )

    # Create customer and supplier
    kh = KhachHang.objects.create(ma_kh="E2E_KH", ten_kh="KH E2E")
    ncc = NhaCungCap.objects.create(ma_ncc="E2E_NCC", ten_ncc="NCC E2E")

    # Create goods
    hh = HangHoa.objects.create(ma_hang_hoa="E2E_HH", ten_hang_hoa="Hàng E2E")
    VatTuHangHoa.objects.create(hang_hoa=hh, phuong_phap_tinh_gia="FIFO")

    # Create warehouse
    kho = KhoInventory.objects.create(ma_kho="E2E_KHO", ten_kho="Kho E2E")

    return {"kh": kh, "ncc": ncc, "hh": hh, "kho": kho}


@pytest.mark.django_db
class TestE2EFlow:
    """Test complete business flow end-to-end."""

    def test_full_accounting_cycle(self, setup_e2e_data):
        """Test: Receipt → Payment → Closing → Verify balances."""
        data = setup_e2e_data

        # Step 1: Create receipt
        pt = tao_phieu_thu(
            khach_hang=data["kh"],
            so_tien=Decimal("50000000"),
            tk_co="511",
            ngay_chung_tu=date(2025, 6, 15),
            so_chung_tu="E2E-PT-001",
        )
        assert PhieuThu.objects.filter(so_chung_tu="E2E-PT-001").exists()

        # Step 2: Create payment
        pc = tao_phieu_chi(
            nha_cung_cap=data["ncc"],
            so_tien=Decimal("20000000"),
            tk_no="642",
            ngay_chung_tu=date(2025, 6, 20),
            so_chung_tu="E2E-PC-001",
        )
        assert PhieuChi.objects.filter(so_chung_tu="E2E-PC-001").exists()

        # Step 3: Verify journal entries created
        assert ButToan.objects.filter(so_but_toan="BT-E2E-PT-001").exists()
        assert ButToan.objects.filter(so_but_toan="BT-E2E-PC-001").exists()

        # Step 4: Year-end closing
        result = ket_chuyen_cuoi_ky(date(2025, 1, 1), date(2025, 12, 31), nam=2025)
        assert result["doanh_thu"] == Decimal("50000000")
        assert result["chi_phi"] == Decimal("20000000")
        assert result["loi_nhuan"] == Decimal("30000000")

    def test_url_accessibility(self, setup_e2e_data, client):
        """Test that all main pages are accessible."""
        from django.contrib.auth.models import User

        user = User.objects.create_user("e2e_user", password="test123")
        client.login(username="e2e_user", password="test123")

        # Test all main pages return 200
        urls = [
            reverse("nghiep_vu:index"),
            reverse("nghiep_vu:phieu_thu_list"),
            reverse("nghiep_vu:phieu_chi_list"),
            reverse("nghiep_vu:hoa_don_list"),
            reverse("kho:kho_list"),
            reverse("kho:kho_entry_list"),
            reverse("kho:ton_kho_list"),
            reverse("tai_san:taisan_list"),
            reverse("luong:nhanvien_list"),
            reverse("luong:bangluong_list"),
            reverse("bao_cao:bang_cdk"),
            reverse("bao_cao:kqkd"),
        ]

        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, f"Failed: {url}"

    def test_form_submission_flow(self, setup_e2e_data, client):
        """Test form submission creates records."""
        from django.contrib.auth.models import User

        user = User.objects.create_user("e2e_user2", password="test123")
        client.login(username="e2e_user2", password="test123")

        # Test Phieu Thu form submission
        response = client.post(
            reverse("nghiep_vu:phieu_thu_create"),
            {
                "so_tien": "1000000",
                "ty_gia": "1",
                "hinh_thuc_thanh_toan": "tien_mat",
                "tk_co": "511",
                "ngay_chung_tu": "2025-06-15",
                "dien_giai": "E2E Test Receipt",
            },
            follow=True,
        )
        assert response.status_code == 200

        # Verify receipt was created
        assert PhieuThu.objects.filter(dien_giai="E2E Test Receipt").exists()
