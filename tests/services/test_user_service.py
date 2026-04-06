import pytest
from datetime import date
from decimal import Decimal
from app.services.user_service import UserService
from app.models.user import User


class TestUserService:
    def test_create_user(self, db):
        user = UserService.create(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.verify_password("password123") is True

    def test_create_duplicate_username_raises_error(self, db):
        UserService.create("dup", "dup@test.com", "pass", "Dup")
        with pytest.raises(ValueError, match="already exists"):
            UserService.create("dup", "dup2@test.com", "pass", "Dup2")

    def test_create_duplicate_email_raises_error(self, db):
        UserService.create("u1", "same@test.com", "pass", "U1")
        with pytest.raises(ValueError, match="already exists"):
            UserService.create("u2", "same@test.com", "pass", "U2")

    def test_get_by_username(self, db):
        UserService.create("find", "find@test.com", "pass", "Find")
        user = UserService.get_by_username("find")
        assert user is not None
        assert user.username == "find"

    def test_authenticate_success(self, db):
        UserService.create("auth", "auth@test.com", "secret", "Auth")
        user = UserService.authenticate("auth", "secret")
        assert user is not None
        assert user.username == "auth"

    def test_authenticate_wrong_password(self, db):
        UserService.create("bad", "bad@test.com", "secret", "Bad")
        user = UserService.authenticate("bad", "wrong")
        assert user is None

    def test_authenticate_wrong_username(self, db):
        user = UserService.authenticate("nonexistent", "pass")
        assert user is None

    def test_update_user(self, db):
        user = UserService.create("upd", "upd@test.com", "pass", "Upd")
        updated = UserService.update(user.id, full_name="Updated Name")
        assert updated.full_name == "Updated Name"

    def test_update_password(self, db):
        user = UserService.create("pwd", "pwd@test.com", "oldpass", "Pwd")
        UserService.update(user.id, password="newpass")
        assert user.verify_password("newpass") is True
        assert user.verify_password("oldpass") is False

    def test_delete_user(self, db):
        user = UserService.create("del", "del@test.com", "pass", "Del")
        UserService.delete(user.id)
        assert UserService.get_by_id(user.id) is None

    def test_get_all(self, db):
        UserService.create("a1", "a1@test.com", "pass", "A1")
        UserService.create("a2", "a2@test.com", "pass", "A2")
        users = UserService.get_all()
        assert len(users) >= 2
