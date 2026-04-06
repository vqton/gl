from app.extensions import db
from app.models.account import Account


class AccountService:
    @staticmethod
    def get_all():
        return Account.query.order_by(Account.code).all()

    @staticmethod
    def get_by_code(code):
        return Account.get_by_code(code)

    @staticmethod
    def get_by_type(account_type):
        return Account.get_by_type(account_type)

    @staticmethod
    def get_level1():
        return Account.get_all_level1()

    @staticmethod
    def create(code, name, account_type, level=1, parent_code=None, description="", is_system=False):
        if Account.get_by_code(code):
            raise ValueError(f"Account with code {code} already exists")
        account = Account(
            code=code,
            name=name,
            account_type=account_type,
            level=level,
            parent_code=parent_code,
            description=description,
            is_system=is_system,
        )
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def update(code, **kwargs):
        account = Account.get_by_code(code)
        if not account:
            raise ValueError(f"Account {code} not found")
        if "code" in kwargs and kwargs["code"] != code:
            if Account.get_by_code(kwargs["code"]):
                raise ValueError(f"Account code {kwargs['code']} already exists")
        account.update(**kwargs)
        db.session.commit()
        return account

    @staticmethod
    def delete(code):
        account = Account.get_by_code(code)
        if not account:
            raise ValueError(f"Account {code} not found")
        if account.is_system:
            raise ValueError("Cannot delete system accounts")
        if account.journal_lines.first():
            raise ValueError("Cannot delete account with journal entries")
        account.delete()
        db.session.commit()

    @staticmethod
    def seed_circular99():
        accounts = Account.get_circular99_accounts()
        type_map = {
            "asset": "asset",
            "liability": "liability",
            "equity": "equity",
            "revenue": "revenue",
            "expense": "expense",
        }
        for acc in accounts:
            if not Account.get_by_code(acc["code"]):
                db.session.add(Account(
                    code=acc["code"],
                    name=acc["name"],
                    account_type=type_map[acc["type"]],
                    level=acc["level"],
                    is_system=True,
                ))
        db.session.commit()
