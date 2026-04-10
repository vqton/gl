import pytest
from app.services.account_service import AccountService
from app.models.account import Account


class TestAccountService:
    def test_get_all_empty(self, db):
        accounts = AccountService.get_all()
        assert accounts == []

    def test_get_all(self, db):
        Account(code="111", name="Cash", account_type="asset", level=1).save()
        Account(code="331", name="Payable", account_type="liability", level=1).save()

        accounts = AccountService.get_all()
        assert len(accounts) == 2

    def test_get_by_code(self, db):
        Account(code="111", name="Cash", account_type="asset", level=1).save()
        account = AccountService.get_by_code("111")
        assert account is not None
        assert account.code == "111"

    def test_get_by_type(self, db):
        Account(code="111", name="A1", account_type="asset", level=1).save()
        Account(code="112", name="A2", account_type="asset", level=1).save()
        Account(code="331", name="L1", account_type="liability", level=1).save()

        assets = AccountService.get_by_type("asset")
        assert len(assets) == 2

    def test_create_account(self, db):
        account = AccountService.create(
            code="111", name="Cash", account_type="asset", level=1
        )
        assert account.code == "111"
        assert account.name == "Cash"
        assert account.is_system is False

    def test_create_duplicate_raises_error(self, db):
        AccountService.create(code="111", name="Cash", account_type="asset")
        with pytest.raises(ValueError, match="đã tồn tại"):
            AccountService.create(code="111", name="Cash2", account_type="asset")

    def test_create_missing_required_fields(self, db):
        with pytest.raises(ValueError, match="Mã tài khoản không được để trống"):
            AccountService.create(code="", name="Cash", account_type="asset")
        
        with pytest.raises(ValueError, match="Tên tài khoản không được để trống"):
            AccountService.create(code="111", name="", account_type="asset")

    def test_update_account(self, db):
        AccountService.create(code="111", name="Cash", account_type="asset")
        account = AccountService.update("111", name="Cash Updated")
        assert account.name == "Cash Updated"

    def test_update_not_found_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            AccountService.update("999", name="Nope")

    def test_delete_account(self, db):
        AccountService.create(code="111", name="Cash", account_type="asset", is_system=False)
        AccountService.delete("111")
        assert AccountService.get_by_code("111") is None

    def test_delete_system_account_raises_error(self, db):
        AccountService.create(code="111", name="Cash", account_type="asset", is_system=True)
        with pytest.raises(ValueError, match="hệ thống"):
            AccountService.delete("111")

    def test_delete_not_found_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            AccountService.delete("999")

    def test_seed_circular99(self, db):
        AccountService.seed_circular99()
        accounts = AccountService.get_all()
        assert len(accounts) > 50
        assert AccountService.get_by_code("111") is not None
        assert AccountService.get_by_code("911") is not None

    def test_seed_circular99_idempotent(self, db):
        AccountService.seed_circular99()
        AccountService.seed_circular99()
        accounts = AccountService.get_all()
        assert len(accounts) > 50
