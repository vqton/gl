import pytest
from datetime import datetime
from app.models.account import Account


class TestAccountModel:
    def test_create_account(self, db):
        account = Account(
            code="111",
            name="Tiền mặt",
            account_type="asset",
            level=1,
            is_system=True,
        )
        db.session.add(account)
        db.session.commit()

        assert account.id is not None
        assert account.code == "111"
        assert account.name == "Tiền mặt"
        assert account.account_type == "asset"
        assert account.level == 1
        assert account.is_system is True

    def test_account_unique_code(self, db):
        account1 = Account(code="111", name="Test", account_type="asset", level=1)
        account2 = Account(code="111", name="Test2", account_type="asset", level=1)
        db.session.add(account1)
        db.session.commit()
        db.session.add(account2)
        with pytest.raises(Exception):
            db.session.commit()

    def test_get_by_code(self, db):
        account = Account(code="112", name="Test", account_type="asset", level=1)
        db.session.add(account)
        db.session.commit()

        found = Account.get_by_code("112")
        assert found is not None
        assert found.code == "112"

    def test_get_by_code_not_found(self, db):
        found = Account.get_by_code("999")
        assert found is None

    def test_get_by_type(self, db):
        Asset1 = Account(code="111", name="A1", account_type="asset", level=1)
        Asset2 = Account(code="112", name="A2", account_type="asset", level=1)
        Liability1 = Account(code="331", name="L1", account_type="liability", level=1)
        db.session.add_all([Asset1, Asset2, Liability1])
        db.session.commit()

        assets = Account.get_by_type("asset")
        assert len(assets) == 2

    def test_account_type_properties(self, db):
        acc = Account(code="111", name="Test", account_type="asset", level=1)
        assert acc.is_asset is True
        assert acc.is_liability is False
        assert acc.is_equity is False
        assert acc.is_revenue is False
        assert acc.is_expense is False

    def test_get_level1(self, db):
        Account(code="111", name="L1", account_type="asset", level=1).save()
        Account(code="1331", name="L2", account_type="asset", level=2, parent_code="133").save()
        Account(code="331", name="L1b", account_type="liability", level=1).save()

        level1 = Account.get_all_level1()
        assert len(level1) == 2

    def test_get_circular99_accounts(self):
        accounts = Account.get_circular99_accounts()
        assert len(accounts) > 50
        codes = [a["code"] for a in accounts]
        assert "111" in codes
        assert "33311" in codes
        assert "911" in codes

    def test_parent_child_relationship(self, db):
        parent = Account(code="333", name="Thuế", account_type="liability", level=1)
        child = Account(code="3331", name="VAT", account_type="liability", level=2, parent_code="333")
        db.session.add_all([parent, child])
        db.session.commit()

        assert child.parent == parent
        assert child in parent.children

    def test_repr(self, db):
        account = Account(code="111", name="Test", account_type="asset", level=1)
        assert repr(account) == "<Account 111 - Test>"
