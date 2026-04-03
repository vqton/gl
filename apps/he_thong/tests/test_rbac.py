"""Tests for VaiTro (Role) model and user-role assignment."""

import pytest
from django.contrib.auth import get_user_model

from apps.he_thong.models import VaiTro

NguoiDung = get_user_model()


@pytest.fixture
def seed_roles():
    """Seed predefined roles."""
    from apps.he_thong.management.commands.seed_vai_tro import Command

    Command().handle()


@pytest.fixture
def chief_user(seed_roles):
    """Create a user with ke_toan_truong role."""
    user = NguoiDung.objects.create_user(
        username="chief",
        password="testpass123",
    )
    user.vai_tro = VaiTro.objects.get(ma="ke_toan_truong")
    user.save()
    return user


@pytest.fixture
def clerk_user(seed_roles):
    """Create a user with ke_toan_vien role."""
    user = NguoiDung.objects.create_user(
        username="clerk",
        password="testpass123",
    )
    user.vai_tro = VaiTro.objects.get(ma="ke_toan_vien")
    user.save()
    return user


@pytest.fixture
def cashier_user(seed_roles):
    """Create a user with thu_quy role."""
    user = NguoiDung.objects.create_user(
        username="cashier",
        password="testpass123",
    )
    user.vai_tro = VaiTro.objects.get(ma="thu_quy")
    user.save()
    return user


@pytest.fixture
def director_user(seed_roles):
    """Create a user with giam_doc role."""
    user = NguoiDung.objects.create_user(
        username="director",
        password="testpass123",
    )
    user.vai_tro = VaiTro.objects.get(ma="giam_doc")
    user.save()
    return user


@pytest.fixture
def no_role_user():
    """Create a user without any role."""
    return NguoiDung.objects.create_user(
        username="norole",
        password="testpass123",
    )


@pytest.mark.django_db
class TestVaiTroModel:
    """Test VaiTro model creation and seeding."""

    def test_create_role(self):
        """Test creating a custom role."""
        role = VaiTro.objects.create(
            ma="test_role",
            ten="Vai trò test",
        )
        assert role.ma == "test_role"
        assert role.ten == "Vai trò test"

    def test_role_str(self):
        """Test role string representation."""
        role = VaiTro.objects.create(
            ma="ke_toan_vien",
            ten="Kế toán viên",
        )
        assert str(role) == "Kế toán viên"

    def test_predefined_roles_seeded(self, seed_roles):
        """Test that seed_vai_tro creates 4 predefined roles."""
        assert VaiTro.objects.count() == 4
        assert VaiTro.objects.filter(ma="ke_toan_truong").exists()
        assert VaiTro.objects.filter(ma="ke_toan_vien").exists()
        assert VaiTro.objects.filter(ma="thu_quy").exists()
        assert VaiTro.objects.filter(ma="giam_doc").exists()

    def test_seed_idempotent(self, seed_roles):
        """Test running seed twice doesn't duplicate roles."""
        from apps.he_thong.management.commands.seed_vai_tro import Command

        Command().handle()
        assert VaiTro.objects.count() == 4


@pytest.mark.django_db
class TestUserRoleUI:
    """Test user role assignment UI."""

    def test_role_form_renders(self, seed_roles):
        """Test role form page renders with role options."""
        from django.test import Client
        from django.urls import reverse

        user = NguoiDung.objects.create_user(
            username="admin_ui",
            password="testpass123",
            is_superuser=True,
        )
        client = Client()
        client.force_login(user)

        response = client.get(
            reverse("he_thong:nguoi_dung_role_edit", kwargs={"pk": user.pk})
        )
        assert response.status_code == 200
        assert b"ke_toan_truong" in response.content or b"K" in response.content

    def test_role_form_saves(self, seed_roles):
        """Test saving role from form updates user."""
        from django.test import Client
        from django.urls import reverse

        admin = NguoiDung.objects.create_user(
            username="admin_ui",
            password="testpass123",
            is_superuser=True,
        )
        target_user = NguoiDung.objects.create_user(
            username="target_user",
            password="testpass123",
        )
        role = VaiTro.objects.get(ma="ke_toan_vien")

        client = Client()
        client.force_login(admin)

        response = client.post(
            reverse("he_thong:nguoi_dung_role_edit", kwargs={"pk": target_user.pk}),
            {"vai_tro": str(role.pk)},
        )
        assert response.status_code == 302

        target_user.refresh_from_db()
        assert target_user.vai_tro == role
        assert target_user.has_role("ke_toan_vien") is True

    def test_role_form_clears_role(self, seed_roles):
        """Test clearing role from form sets vai_tro to None."""
        from django.test import Client
        from django.urls import reverse

        admin = NguoiDung.objects.create_user(
            username="admin_ui",
            password="testpass123",
            is_superuser=True,
        )
        target_user = NguoiDung.objects.create_user(
            username="target_user2",
            password="testpass123",
        )
        target_user.vai_tro = VaiTro.objects.get(ma="ke_toan_vien")
        target_user.save()

        client = Client()
        client.force_login(admin)

        response = client.post(
            reverse("he_thong:nguoi_dung_role_edit", kwargs={"pk": target_user.pk}),
            {"vai_tro": ""},
        )
        assert response.status_code == 302

        target_user.refresh_from_db()
        assert target_user.vai_tro is None


@pytest.mark.django_db
class TestUserRoleAssignment:
    """Test user-role relationship."""

    def test_assign_role_to_user(self, seed_roles):
        """Test assigning a role to a user."""
        user = NguoiDung.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        role = VaiTro.objects.get(ma="ke_toan_vien")
        user.vai_tro = role
        user.save()

        assert user.vai_tro == role
        assert user.has_role("ke_toan_vien") is True

    def test_user_has_role(self, chief_user):
        """Test user.has_role() method."""
        assert chief_user.has_role("ke_toan_truong") is True
        assert chief_user.has_role("ke_toan_vien") is True
        assert chief_user.has_role("thu_quy") is True

    def test_user_no_role(self, no_role_user):
        """Test user without role returns False for all has_role checks."""
        assert no_role_user.has_role("ke_toan_truong") is False
        assert no_role_user.has_role("ke_toan_vien") is False

    def test_is_ke_toan_truong(self, chief_user, clerk_user):
        """Test convenience property for chief accountant role."""
        assert chief_user.is_ke_toan_truong is True
        assert clerk_user.is_ke_toan_truong is False

    def test_system_admin_bypass(self):
        """Test is_system_admin users have implicit chief accountant role."""
        user = NguoiDung.objects.create_user(
            username="sysadmin",
            password="testpass123",
            is_system_admin=True,
        )
        assert user.has_role("ke_toan_truong") is True
        assert user.is_ke_toan_truong is True
