"""Tests for permission decorators."""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory

from apps.tien_ich.permissions import (can_delete_posted_voucher, require_role,
                                       salary_access)

NguoiDung = get_user_model()


@pytest.fixture
def seed_roles():
    """Seed predefined roles."""
    from apps.he_thong.management.commands.seed_vai_tro import Command

    Command().handle()


@pytest.fixture
def factory():
    """Create a RequestFactory instance."""
    return RequestFactory()


@pytest.fixture
def chief_user(seed_roles):
    """Create a user with ke_toan_truong role."""
    user = NguoiDung.objects.create_user(username="chief", password="testpass123")
    from apps.he_thong.models import VaiTro

    user.vai_tro = VaiTro.objects.get(ma="ke_toan_truong")
    user.save()
    return user


@pytest.fixture
def clerk_user(seed_roles):
    """Create a user with ke_toan_vien role."""
    user = NguoiDung.objects.create_user(username="clerk", password="testpass123")
    from apps.he_thong.models import VaiTro

    user.vai_tro = VaiTro.objects.get(ma="ke_toan_vien")
    user.save()
    return user


@pytest.fixture
def cashier_user(seed_roles):
    """Create a user with thu_quy role."""
    user = NguoiDung.objects.create_user(username="cashier", password="testpass123")
    from apps.he_thong.models import VaiTro

    user.vai_tro = VaiTro.objects.get(ma="thu_quy")
    user.save()
    return user


@pytest.mark.django_db
class TestRequireRoleDecorator:
    """Test @require_role decorator."""

    def test_require_role_allows_authorized_user(self, chief_user, factory):
        """Test that user with correct role gets 200."""

        @require_role("ke_toan_truong")
        def protected_view(request):
            return HttpResponse("OK")

        request = factory.get("/protected/")
        request.user = chief_user
        response = protected_view(request)
        assert response.status_code == 200

    def test_require_role_blocks_unauthorized_user(self, clerk_user, factory):
        """Test that user without role gets 403."""

        @require_role("ke_toan_truong")
        def protected_view(request):
            return HttpResponse("OK")

        request = factory.get("/protected/")
        request.user = clerk_user
        response = protected_view(request)
        assert response.status_code == 403
        assert b"quy" in response.content

    def test_require_role_blocks_user_no_role(self, factory):
        """Test that user without any role gets 403."""
        user = NguoiDung.objects.create_user(username="norole", password="testpass123")

        @require_role("ke_toan_truong")
        def protected_view(request):
            return HttpResponse("OK")

        request = factory.get("/protected/")
        request.user = user
        response = protected_view(request)
        assert response.status_code == 403

    def test_require_role_blocks_anonymous_user(self, factory):
        """Test that anonymous user gets 403."""

        @require_role("ke_toan_truong")
        def protected_view(request):
            return HttpResponse("OK")

        request = factory.get("/protected/")
        request.user = AnonymousUser()
        response = protected_view(request)
        assert response.status_code == 403

    def test_require_role_system_admin_bypass(self, factory):
        """Test that system admin bypasses role check."""
        sysadmin = NguoiDung.objects.create_user(
            username="sysadmin",
            password="testpass123",
            is_system_admin=True,
        )

        @require_role("ke_toan_truong")
        def protected_view(request):
            return HttpResponse("OK")

        request = factory.get("/protected/")
        request.user = sysadmin
        response = protected_view(request)
        assert response.status_code == 200


@pytest.mark.django_db
class TestCanDeletePostedVoucherDecorator:
    """Test @can_delete_posted_voucher decorator."""

    def test_chief_can_delete_posted(self, chief_user, factory):
        """Test chief accountant can delete posted vouchers."""

        @can_delete_posted_voucher
        def delete_view(request, pk):
            return HttpResponse("Deleted")

        request = factory.delete("/phieu-thu/1/delete/")
        request.user = chief_user
        response = delete_view(request, pk=1)
        assert response.status_code == 200

    def test_clerk_cannot_delete_posted(self, clerk_user, factory):
        """Test clerk cannot delete posted vouchers."""

        @can_delete_posted_voucher
        def delete_view(request, pk):
            return HttpResponse("Deleted")

        request = factory.delete("/phieu-thu/1/delete/")
        request.user = clerk_user
        response = delete_view(request, pk=1)
        assert response.status_code == 403
        assert b"x\xc3\xb3a" in response.content


@pytest.mark.django_db
class TestSalaryAccessDecorator:
    """Test @salary_access decorator."""

    def test_chief_can_access_payroll(self, chief_user, factory):
        """Test chief accountant can access payroll."""

        @salary_access
        def payroll_view(request):
            return HttpResponse("Payroll data")

        request = factory.get("/luong/bang-luong/")
        request.user = chief_user
        response = payroll_view(request)
        assert response.status_code == 200

    def test_clerk_cannot_access_payroll(self, clerk_user, factory):
        """Test clerk cannot access payroll."""

        @salary_access
        def payroll_view(request):
            return HttpResponse("Payroll data")

        request = factory.get("/luong/bang-luong/")
        request.user = clerk_user
        response = payroll_view(request)
        assert response.status_code == 403
        content = response.content.decode("utf-8")
        assert "lương" in content

    def test_cashier_cannot_access_payroll(self, cashier_user, factory):
        """Test cashier cannot access payroll."""

        @salary_access
        def payroll_view(request):
            return HttpResponse("Payroll data")

        request = factory.get("/luong/bang-luong/")
        request.user = cashier_user
        response = payroll_view(request)
        assert response.status_code == 403


@pytest.mark.django_db
class TestRoleIntegration:
    """Integration tests for role-based access across modules."""

    def test_cashier_access_thu_chi(self, cashier_user, factory):
        """Test cashier can access cash/bank modules."""

        @require_role("thu_quy")
        def cash_view(request):
            return HttpResponse("Cash module")

        request = factory.get("/nghiep-vu/phieu-thu/")
        request.user = cashier_user
        response = cash_view(request)
        assert response.status_code == 200

    def test_cashier_blocked_from_kho(self, cashier_user, factory):
        """Test cashier cannot access inventory module."""

        @require_role("ke_toan_truong")
        def kho_view(request):
            return HttpResponse("Inventory module")

        request = factory.get("/kho/")
        request.user = cashier_user
        response = kho_view(request)
        assert response.status_code == 403

    def test_cashier_blocked_from_luong(self, cashier_user, factory):
        """Test cashier cannot access payroll module."""

        @salary_access
        def luong_view(request):
            return HttpResponse("Payroll module")

        request = factory.get("/luong/bang-luong/")
        request.user = cashier_user
        response = luong_view(request)
        assert response.status_code == 403
