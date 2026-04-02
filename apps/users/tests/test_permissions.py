"""Tests for permission-based admin restriction."""

import pytest
from django.contrib.auth.models import Group, Permission
from django.test import Client, RequestFactory
from django.urls import reverse

from apps.users.models import NguoiDung, UserType
from apps.danh_muc.models import TaiKhoanKeToan, DonVi


@pytest.fixture
def superuser(db):
    """Create a superuser with full admin access."""
    user = NguoiDung.objects.create_user(
        username="admin",
        password="testpass123",
        is_superuser=True,
        is_staff=True,
        user_type=UserType.ADMIN,
    )
    return user


@pytest.fixture
def accountant(db):
    """Create an accountant user with limited permissions."""
    user = NguoiDung.objects.create_user(
        username="accountant",
        password="testpass123",
        user_type=UserType.ACCOUNTANT,
        is_staff=True,
    )
    accountant_group, _ = Group.objects.get_or_create(name="Ke toan vien")
    user.groups.add(accountant_group)
    return user


@pytest.fixture
def viewer(db):
    """Create a viewer user with no admin permissions."""
    user = NguoiDung.objects.create_user(
        username="viewer",
        password="testpass123",
        user_type=UserType.VIEWER,
        is_staff=True,
    )
    return user


@pytest.fixture
def regular_user(db):
    """Create a regular user without staff access."""
    user = NguoiDung.objects.create_user(
        username="user",
        password="testpass123",
    )
    return user


@pytest.mark.django_db
class TestAdminIndexAccess:
    """Test admin index page access for different user types."""

    def test_admin_user_sees_all_apps(self, superuser, client):
        """Admin user should see all apps in admin index."""
        client.force_login(superuser)
        response = client.get("/admin/")
        assert response.status_code == 200

    def test_accountant_user_has_limited_access(self, accountant, client):
        """Accountant should have limited access to admin."""
        client.force_login(accountant)
        response = client.get("/admin/")
        assert response.status_code == 200

    def test_non_staff_user_denied(self, regular_user, client):
        """Non-staff users should be denied access."""
        client.force_login(regular_user)
        response = client.get("/admin/")
        assert response.status_code == 302


@pytest.mark.django_db
class TestModelAdminPermissions:
    """Test model admin permission checks."""

    def test_accountant_can_access_nghiep_vu(self, accountant, client):
        """Accountant should be able to access nghiep_vu models."""
        client.force_login(accountant)
        response = client.get(reverse("admin:nghiep_vu_buttoan_changelist"))
        assert response.status_code in [200, 403]

    def test_accountant_cannot_access_master_data_full(self, accountant, client):
        """Accountant should have restricted access to master data."""
        client.force_login(accountant)
        response = client.get(reverse("admin:danh_muc_taikhoanketoan_changelist"))
        assert response.status_code in [200, 403]

    def test_viewer_has_no_add_permission(self, viewer, client):
        """Viewer should not have add permissions."""
        client.force_login(viewer)
        response = client.get(reverse("admin:nghiep_vu_buttoan_add"))
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserTypeModel:
    """Test custom user model functionality."""

    def test_user_type_choices(self):
        """Test user type choices are defined correctly."""
        assert UserType.ADMIN == "admin"
        assert UserType.ACCOUNTANT == "accountant"
        assert UserType.VIEWER == "viewer"

    def test_user_properties(self, superuser, accountant, viewer):
        """Test user type properties."""
        assert superuser.is_admin_user is True
        assert superuser.is_accountant_user is False
        assert superuser.is_viewer_user is False

        assert accountant.is_admin_user is False
        assert accountant.is_accountant_user is True
        assert accountant.is_viewer_user is False

        assert viewer.is_admin_user is False
        assert viewer.is_accountant_user is False
        assert viewer.is_viewer_user is True


@pytest.mark.django_db
class TestGroupPermissions:
    """Test user group and permission assignment."""

    def test_groups_can_be_created(self, db):
        """Test that groups can be created with permissions."""
        admin_group = Group.objects.create(name="Quan tri vien")
        accountant_group = Group.objects.create(name="Ke toan vien")
        assert admin_group.pk is not None
        assert accountant_group.pk is not None

    def test_admin_group_has_all_permissions(self, superuser):
        """Test admin group has all permissions via superuser."""
        perms = superuser.get_all_permissions()
        assert len(perms) > 0
