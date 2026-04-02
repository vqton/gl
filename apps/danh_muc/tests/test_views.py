"""Tests for danh_muc views - catches missing templates and invalid fields."""

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template import loader

from apps.danh_muc.models import DonVi, HangHoa, KhachHang, NganHang, NhaCungCap, TaiKhoanKeToan
from apps.danh_muc.views import (
    DanhMucDashboardView,
    DonViListView,
    HangHoaCreateView,
    HangHoaDeleteView,
    HangHoaListView,
    HangHoaUpdateView,
    KhachHangCreateView,
    KhachHangDeleteView,
    KhachHangListView,
    KhachHangUpdateView,
    NganHangCreateView,
    NganHangDeleteView,
    NganHangListView,
    NganHangUpdateView,
    NhaCungCapCreateView,
    NhaCungCapDeleteView,
    NhaCungCapListView,
    NhaCungCapUpdateView,
    TaiKhoanCreateView,
    TaiKhoanDeleteView,
    TaiKhoanListView,
    TaiKhoanUpdateView,
)


User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="testpass123")
    return client


class TestTemplateExists:
    """Test all templates referenced by views actually exist."""

    def test_taikhoan_list_template(self):
        assert loader.get_template("danh_muc/taikhoan_list.html")

    def test_taikhoan_form_template(self):
        assert loader.get_template("danh_muc/taikhoan_form.html")

    def test_taikhoan_delete_template(self):
        assert loader.get_template("danh_muc/confirm_delete.html")

    def test_khachhang_list_template(self):
        assert loader.get_template("danh_muc/khachhang_list.html")

    def test_khachhang_form_template(self):
        assert loader.get_template("danh_muc/khachhang_form.html")

    def test_khachhang_delete_template(self):
        assert loader.get_template("danh_muc/confirm_delete.html")

    def test_nhacungcap_list_template(self):
        assert loader.get_template("danh_muc/nhacungcap_list.html")

    def test_nhacungcap_form_template(self):
        assert loader.get_template("danh_muc/nhacungcap_form.html")

    def test_nhacungcap_delete_template(self):
        assert loader.get_template("danh_muc/confirm_delete.html")

    def test_hanghoa_list_template(self):
        assert loader.get_template("danh_muc/hanghoa_list.html")

    def test_hanghoa_form_template(self):
        assert loader.get_template("danh_muc/hanghoa_form.html")

    def test_hanghoa_delete_template(self):
        assert loader.get_template("danh_muc/confirm_delete.html")

    def test_nganhang_list_template(self):
        assert loader.get_template("danh_muc/nganhang_list.html")

    def test_nganhang_form_template(self):
        assert loader.get_template("danh_muc/nganhang_form.html")

    def test_nganhang_delete_template(self):
        assert loader.get_template("danh_muc/confirm_delete.html")

    def test_donvi_list_template(self):
        assert loader.get_template("danh_muc/donvi_list.html")

    def test_dashboard_template(self):
        assert loader.get_template("danh_muc/dashboard.html")


class TestViewFieldsValid:
    """Test all fields referenced in CreateView/UpdateView exist on models."""

    def test_taikhoan_create_fields(self):
        valid = {f.name for f in TaiKhoanKeToan._meta.get_fields()}
        for field in TaiKhoanCreateView.fields:
            assert field in valid, f"TaiKhoanCreateView: '{field}' not on model"

    def test_taikhoan_update_fields(self):
        valid = {f.name for f in TaiKhoanKeToan._meta.get_fields()}
        for field in TaiKhoanUpdateView.fields:
            assert field in valid, f"TaiKhoanUpdateView: '{field}' not on model"

    def test_khachhang_create_fields(self):
        valid = {f.name for f in KhachHang._meta.get_fields()}
        for field in KhachHangCreateView.fields:
            assert field in valid, f"KhachHangCreateView: '{field}' not on model"

    def test_khachhang_update_fields(self):
        valid = {f.name for f in KhachHang._meta.get_fields()}
        for field in KhachHangUpdateView.fields:
            assert field in valid, f"KhachHangUpdateView: '{field}' not on model"

    def test_nhacungcap_create_fields(self):
        valid = {f.name for f in NhaCungCap._meta.get_fields()}
        for field in NhaCungCapCreateView.fields:
            assert field in valid, f"NhaCungCapCreateView: '{field}' not on model"

    def test_nhacungcap_update_fields(self):
        valid = {f.name for f in NhaCungCap._meta.get_fields()}
        for field in NhaCungCapUpdateView.fields:
            assert field in valid, f"NhaCungCapUpdateView: '{field}' not on model"

    def test_hanghoa_create_fields(self):
        valid = {f.name for f in HangHoa._meta.get_fields()}
        for field in HangHoaCreateView.fields:
            assert field in valid, f"HangHoaCreateView: '{field}' not on model"

    def test_hanghoa_update_fields(self):
        valid = {f.name for f in HangHoa._meta.get_fields()}
        for field in HangHoaUpdateView.fields:
            assert field in valid, f"HangHoaUpdateView: '{field}' not on model"

    def test_nganhang_create_fields(self):
        valid = {f.name for f in NganHang._meta.get_fields()}
        for field in NganHangCreateView.fields:
            assert field in valid, f"NganHangCreateView: '{field}' not on model"

    def test_nganhang_update_fields(self):
        valid = {f.name for f in NganHang._meta.get_fields()}
        for field in NganHangUpdateView.fields:
            assert field in valid, f"NganHangUpdateView: '{field}' not on model"


class TestDanhMucViews:
    """Test all danh_muc views respond correctly."""

    def test_taikhoan_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:taikhoan_list"))
        assert response.status_code == 200

    def test_khachhang_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:khachhang_list"))
        assert response.status_code == 200

    def test_nhacungcap_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:nhacungcap_list"))
        assert response.status_code == 200

    def test_hanghoa_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:hanghoa_list"))
        assert response.status_code == 200

    def test_nganhang_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:nganhang_list"))
        assert response.status_code == 200

    def test_donvi_list(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:donvi_list"))
        assert response.status_code == 200

    def test_dashboard(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:dashboard"))
        assert response.status_code == 200

    def test_taikhoan_create(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:taikhoan_create"))
        assert response.status_code == 200

    def test_khachhang_create(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:khachhang_create"))
        assert response.status_code == 200

    def test_nhacungcap_create(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:nhacungcap_create"))
        assert response.status_code == 200

    def test_hanghoa_create(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:hanghoa_create"))
        assert response.status_code == 200

    def test_nganhang_create(self, client_logged_in):
        response = client_logged_in.get(reverse("danh_muc:nganhang_create"))
        assert response.status_code == 200
