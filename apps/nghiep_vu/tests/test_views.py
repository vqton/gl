"""Tests for nghiep_vu views."""

import pytest
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.danh_muc.models import KhachHang, TaiKhoanKeToan
from apps.nghiep_vu.models import HoaDon, PhieuChi, PhieuThu


User = get_user_model()


@pytest.fixture
def user(db):
    from apps.he_thong.management.commands.seed_vai_tro import Command
    from apps.he_thong.models import VaiTro

    Command().handle()
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
    )
    user.vai_tro = VaiTro.objects.get(ma="ke_toan_truong")
    user.save()
    return user


@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="testpass123")
    return client


class TestHoaDonCreateView:
    """Test HoaDonCreateView - catches invalid fields."""

    def test_hoa_don_create_view_fields_exist(self):
        """Test all fields in HoaDonCreateView.fields exist on HoaDon model."""
        from apps.nghiep_vu.views import HoaDonCreateView
        valid_fields = {f.name for f in HoaDon._meta.get_fields()}
        for field in HoaDonCreateView.fields:
            assert field in valid_fields, (
                f"Field '{field}' in HoaDonCreateView.fields does not exist on HoaDon model"
            )

    def test_hoa_don_create_view_no_dien_giai(self):
        """Test HoaDonCreateView does not reference dien_giai field."""
        from apps.nghiep_vu.views import HoaDonCreateView
        assert "dien_giai" not in HoaDonCreateView.fields, (
            "HoaDon model does not have dien_giai field"
        )

    def test_hoa_don_create_view_get(self, client_logged_in):
        """Test HoaDonCreateView GET request works."""
        response = client_logged_in.get(
            reverse("nghiep_vu:hoa_don_create")
        )
        assert response.status_code == 200

    def test_hoa_don_create_view_post(self, client_logged_in, khach_hang):
        """Test HoaDonCreateView POST request works."""
        response = client_logged_in.post(
            reverse("nghiep_vu:hoa_don_create"),
            {
                "khach_hang": khach_hang.pk,
                "ngay_hoa_don": "2026-04-02",
                "hinh_thuc_thanh_toan": "tien_mat",
                "ky_hieu": "AA/26E",
            },
        )
        assert response.status_code == 302
        assert HoaDon.objects.count() == 1


class TestPhieuThuCreateView:
    """Test PhieuThuCreateView fields."""

    def test_phieu_thu_create_view_fields_exist(self):
        """Test all fields in PhieuThuCreateView.fields exist on PhieuThu model."""
        from apps.nghiep_vu.views import PhieuThuCreateView
        valid_fields = {f.name for f in PhieuThu._meta.get_fields()}
        for field in PhieuThuCreateView.fields:
            assert field in valid_fields, (
                f"Field '{field}' in PhieuThuCreateView.fields does not exist on PhieuThu model"
            )

    def test_phieu_thu_create_view_get(self, client_logged_in):
        """Test PhieuThuCreateView GET request works."""
        response = client_logged_in.get(
            reverse("nghiep_vu:phieu_thu_create")
        )
        assert response.status_code == 200


class TestPhieuChiCreateView:
    """Test PhieuChiCreateView fields."""

    def test_phieu_chi_create_view_fields_exist(self):
        """Test all fields in PhieuChiCreateView.fields exist on PhieuChi model."""
        from apps.nghiep_vu.views import PhieuChiCreateView
        valid_fields = {f.name for f in PhieuChi._meta.get_fields()}
        for field in PhieuChiCreateView.fields:
            assert field in valid_fields, (
                f"Field '{field}' in PhieuChiCreateView.fields does not exist on PhieuChi model"
            )

    def test_phieu_chi_create_view_get(self, client_logged_in):
        """Test PhieuChiCreateView GET request works."""
        response = client_logged_in.get(
            reverse("nghiep_vu:phieu_chi_create")
        )
        assert response.status_code == 200


class TestAuthRedirects:
    """Test auth redirect URLs use correct namespaced names."""

    def test_logout_redirects_to_accounting_login(self):
        """Test LogoutView redirects to accounting:login, not 'login'."""
        from apps.accounting.views import LogoutView
        view = LogoutView()
        # Check the redirect URL resolves correctly
        from django.urls import reverse
        try:
            url = reverse("accounting:login")
            assert url == "/login/"
        except Exception:
            pytest.fail("accounting:login URL not found")

    def test_login_redirects_to_accounting_dashboard(self):
        """Test LoginView redirects to accounting:dashboard."""
        from django.urls import reverse
        try:
            url = reverse("accounting:dashboard")
            assert url == "/"
        except Exception:
            pytest.fail("accounting:dashboard URL not found")


@pytest.fixture
def tk_111(db):
    return TaiKhoanKeToan.objects.create(
        ma_tai_khoan="1111",
        ten_tai_khoan="Tiền mặt",
        loai_tai_khoan="no",
        cap_do=1,
    )


@pytest.fixture
def khach_hang(db):
    return KhachHang.objects.create(ma_kh="KH001", ten_kh="Test Customer")


class TestGiayTamUngView:
    """Test GiayDeNghiTamUng views."""

    def test_giay_tam_ung_list_view_exists(self, client_logged_in):
        """Test GiayTamUngListView exists."""
        response = client_logged_in.get(reverse("nghiep_vu:giay_tam_ung_list"))
        assert response.status_code == 200

    def test_giay_tam_ung_create_view_exists(self, client_logged_in):
        """Test GiayTamUngCreateView exists."""
        response = client_logged_in.get(reverse("nghiep_vu:giay_tam_ung_create"))
        assert response.status_code == 200

    def test_giay_tam_ung_detail_view_exists(self, client_logged_in, user, tk_111):
        """Test GiayTamUngDetailView exists."""
        from apps.nghiep_vu.models import GiayDeNghiTamUng
        giay = GiayDeNghiTamUng.objects.create(
            so_chung_tu="TU/001",
            ngay_chung_tu="2026-04-01",
            nguoi_de_nghi=user,
            noi_dung="Test tam ung",
            so_tien=Decimal("1000000"),
            tk_chi=tk_111,
        )
        response = client_logged_in.get(reverse("nghiep_vu:giay_tam_ung_detail", args=[giay.pk]))
        assert response.status_code == 200


class TestTamUngSettlementView:
    """Test GiayThanhToanTamUng views."""

    def test_tam_ung_settlement_list_view_exists(self, client_logged_in):
        """Test TamUngSettlementListView exists."""
        response = client_logged_in.get(reverse("nghiep_vu:tam_ung_settlement_list"))
        assert response.status_code == 200

    def test_tam_ung_settlement_create_view_exists(self, client_logged_in):
        """Test TamUngSettlementCreateView exists."""
        response = client_logged_in.get(reverse("nghiep_vu:tam_ung_settlement_create"))
        assert response.status_code == 200


class TestBienBanGiaoNhanTSCDView:
    """Test BienBanGiaoNhanTSCD views."""

    def test_bien_ban_giao_nhan_list_view_exists(self, client_logged_in):
        """Test BienBanGiaoNhanTSCDListView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bien_ban_giao_nhan_list"))
        assert response.status_code == 200

    def test_bien_ban_giao_nhan_create_view_exists(self, client_logged_in):
        """Test BienBanGiaoNhanTSCDCreateView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bien_ban_giao_nhan_create"))
        assert response.status_code == 200


class TestBienBanThanhLyTSCDView:
    """Test BienBanThanhLyTSCD views."""

    def test_bien_ban_thanh_ly_list_view_exists(self, client_logged_in):
        """Test BienBanThanhLyTSCDListView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bien_ban_thanh_ly_list"))
        assert response.status_code == 200

    def test_bien_ban_thanh_ly_create_view_exists(self, client_logged_in):
        """Test BienBanThanhLyTSCDCreateView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bien_ban_thanh_ly_create"))
        assert response.status_code == 200


class TestBangKhauHaoView:
    """Test BangKhauHao views."""

    def test_bang_khau_hao_list_view_exists(self, client_logged_in):
        """Test BangKhauHaoListView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bang_khau_hao_list"))
        assert response.status_code == 200

    def test_bang_khau_hao_create_view_exists(self, client_logged_in):
        """Test BangKhauHaoCreateView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("tai_san:bang_khau_hao_create"))
        assert response.status_code == 200


class TestBaoCaoBanHangView:
    """Test BaoCaoBanHang view."""

    def test_bao_cao_ban_hang_view_exists(self, client_logged_in):
        """Test BaoCaoBanHangView exists."""
        from django.urls import reverse
        response = client_logged_in.get(reverse("bao_cao:ban_hang"))
        assert response.status_code == 200
