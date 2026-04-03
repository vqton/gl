"""Tests for he_thong views."""

from datetime import date

import pytest
from django.test import Client
from django.urls import reverse

from apps.he_thong.models import AuditLog, KyKeToan, ThongTinCongTy


@pytest.mark.django_db
class TestCompanyInfoView:
    """Test company info CRUD views."""

    def test_company_info_view_renders(self):
        """Test company info page renders."""
        client = Client()
        response = client.get(reverse("he_thong:cong_ty"))
        assert response.status_code == 200
        assert (
            b"ThongTinCongTy" in response.content
            or b"cong-ty" in response.content
            or b"Th\xc3\xb4ng tin c\xc3\xb4ng ty" in response.content
        )

    def test_company_info_save(self):
        """Test saving company info creates singleton."""
        client = Client()
        response = client.post(
            reverse("he_thong:cong_ty"),
            {
                "ten_cong_ty": "Công ty Test",
                "ma_so_thue": "0123456789",
                "dia_chi": "Hà Nội",
                "dien_thoai": "02412345678",
                "email": "test@test.vn",
                "nguoi_dai_dien": "Nguyễn Văn A",
                "chuc_vu_ndd": "Giám đốc",
                "ke_toan_truong": "Trần Thị B",
                "hinh_thuc_ke_toan": "nhat_ky_chung",
                "phuong_phap_gtgt": "khau_tru",
                "phuong_phap_ton_kho": "binh_quan_lien_hoan",
            },
        )
        assert response.status_code == 302
        company = ThongTinCongTy.get_instance()
        assert company.ten_cong_ty == "Công ty Test"
        assert company.ma_so_thue == "0123456789"

    def test_company_info_update(self):
        """Test updating existing company info."""
        ThongTinCongTy.objects.create(
            ten_cong_ty="Old Name",
            ma_so_thue="0123456789",
        )
        client = Client()
        response = client.post(
            reverse("he_thong:cong_ty"),
            {
                "ten_cong_ty": "New Name",
                "ma_so_thue": "0123456789",
                "dia_chi": "",
                "dien_thoai": "",
                "email": "",
                "nguoi_dai_dien": "",
                "chuc_vu_ndd": "",
                "ke_toan_truong": "",
                "hinh_thuc_ke_toan": "nhat_ky_chung",
                "phuong_phap_gtgt": "khau_tru",
                "phuong_phap_ton_kho": "binh_quan_lien_hoan",
            },
        )
        assert response.status_code == 302
        company = ThongTinCongTy.get_instance()
        assert company.ten_cong_ty == "New Name"


@pytest.mark.django_db
class TestKyKeToanView:
    """Test accounting period views."""

    def test_period_list_view(self):
        """Test period list page renders."""
        client = Client()
        response = client.get(reverse("he_thong:ky_ke_toan_list"))
        assert response.status_code == 200

    def test_period_create(self):
        """Test creating a new accounting period."""
        client = Client()
        response = client.post(
            reverse("he_thong:ky_ke_toan_create"),
            {
                "nam": 2026,
                "ngay_bat_dau": "2026-01-01",
                "ngay_ket_thuc": "2026-12-31",
                "trang_thai": "open",
            },
        )
        assert response.status_code == 302
        assert KyKeToan.objects.filter(nam=2026).exists()

    def test_period_lock(self):
        """Test locking a period via view."""
        period = KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="open",
        )
        client = Client()
        response = client.post(
            reverse("he_thong:ky_ke_toan_lock", kwargs={"pk": period.pk})
        )
        assert response.status_code == 302
        period.refresh_from_db()
        assert period.trang_thai == "locked"

    def test_period_unlock(self):
        """Test unlocking a period via view."""
        period = KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="locked",
        )
        client = Client()
        response = client.post(
            reverse("he_thong:ky_ke_toan_unlock", kwargs={"pk": period.pk})
        )
        assert response.status_code == 302
        period.refresh_from_db()
        assert period.trang_thai == "open"


@pytest.mark.django_db
class TestAuditLogView:
    """Test audit log viewer."""

    def test_audit_log_list(self):
        """Test audit log list page renders."""
        AuditLog.objects.create(
            user="admin",
            action="CREATE",
            model_name="Test",
        )
        client = Client()
        response = client.get(reverse("he_thong:audit_log_list"))
        assert response.status_code == 200

    def test_audit_log_filter_by_user(self):
        """Test filtering audit logs by user."""
        AuditLog.objects.create(user="admin", action="CREATE", model_name="Test")
        AuditLog.objects.create(user="user1", action="UPDATE", model_name="Test")
        client = Client()
        response = client.get(
            reverse("he_thong:audit_log_list"),
            {"user": "admin"},
        )
        assert response.status_code == 200
        assert b"admin" in response.content
        assert b"user1" not in response.content

    def test_audit_log_export_csv(self):
        """Test exporting audit logs to CSV."""
        AuditLog.objects.create(
            user="admin",
            action="CREATE",
            model_name="Test",
            object_id="1",
        )
        client = Client()
        response = client.get(reverse("he_thong:audit_log_export"))
        assert response.status_code == 200
        assert "text/csv" in response["Content-Type"]
