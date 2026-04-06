import pytest
from datetime import date
from decimal import Decimal
from app.models.user import User
from app.models.account import Account
from app.models.journal_entry import JournalEntry, JournalEntryLine


class TestUserModel:
    def test_create_user(self, db):
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            role="accountant",
        )
        user.password = "password123"
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.role == "accountant"
        assert user.password_hash != "password123"

    def test_password_hashing(self, db):
        user = User(username="u1", email="u1@test.com", full_name="U1", role="accountant")
        user.password = "secret"
        assert user.password_hash != "secret"
        assert user.verify_password("secret") is True
        assert user.verify_password("wrong") is False

    def test_password_not_readable(self, db):
        user = User(username="u2", email="u2@test.com", full_name="U2", role="accountant")
        user.password = "secret"
        with pytest.raises(AttributeError):
            _ = user.password

    def test_get_by_username(self, db):
        user = User(username="findme", email="fm@test.com", full_name="FM", role="accountant")
        user.password = "pass"
        db.session.add(user)
        db.session.commit()

        found = User.get_by_username("findme")
        assert found is not None
        assert found.username == "findme"

    def test_get_by_email(self, db):
        user = User(username="em", email="find@email.com", full_name="EM", role="accountant")
        user.password = "pass"
        db.session.add(user)
        db.session.commit()

        found = User.get_by_email("find@email.com")
        assert found is not None

    def test_has_role_admin(self):
        admin = User(username="adm", email="adm@test.com", full_name="ADM", role="admin")
        admin.password = "pass"
        assert admin.has_role("accountant") is True
        assert admin.has_role("cfo") is True

    def test_has_role_specific(self):
        user = User(username="acc", email="acc@test.com", full_name="ACC", role="accountant")
        user.password = "pass"
        assert user.has_role("accountant") is True
        assert user.has_role("cfo") is False

    def test_user_mixin(self):
        user = User(username="mix", email="mix@test.com", full_name="MIX", role="accountant")
        user.password = "pass"
        assert user.is_authenticated is True
        assert user.is_active is True
        assert user.is_anonymous is False
        assert user.get_id() is not None


class TestJournalEntryModel:
    def _setup(self, db):
        a1 = Account(code="111", name="Cash", account_type="asset", level=1)
        a2 = Account(code="511", name="Revenue", account_type="revenue", level=1)
        db.session.add_all([a1, a2])
        user = User(username="je_user", email="je@test.com", full_name="JE", role="accountant")
        user.password = "pass"
        db.session.add(user)
        db.session.commit()
        return user

    def test_create_journal_entry(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000001",
            entry_date=date(2026, 1, 15),
            description="Test entry",
            entry_type="daily",
            accounting_period="2026-01",
            created_by=user.id,
        )
        db.session.add(entry)
        db.session.commit()

        line1 = JournalEntryLine(
            journal_entry_id=entry.id,
            line_number=1,
            account_code="111",
            debit_amount=Decimal("1000000"),
            credit_amount=Decimal("0"),
        )
        line2 = JournalEntryLine(
            journal_entry_id=entry.id,
            line_number=2,
            account_code="511",
            debit_amount=Decimal("0"),
            credit_amount=Decimal("1000000"),
        )
        db.session.add_all([line1, line2])
        db.session.commit()

        assert entry.total_debit == Decimal("1000000")
        assert entry.total_credit == Decimal("1000000")
        assert entry.is_balanced is True
        assert entry.status == "draft"
        assert entry.can_edit is True

    def test_entry_not_balanced(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000002",
            entry_date=date(2026, 1, 15),
            description="Unbalanced",
            accounting_period="2026-01",
            created_by=user.id,
        )
        db.session.add(entry)
        db.session.commit()

        line = JournalEntryLine(
            journal_entry_id=entry.id, line_number=1, account_code="111",
            debit_amount=Decimal("1000000"), credit_amount=Decimal("0"),
        )
        db.session.add(line)
        db.session.commit()

        assert entry.is_balanced is False

    def test_approve_entry(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000003",
            entry_date=date(2026, 1, 15),
            description="To approve",
            accounting_period="2026-01",
            created_by=user.id,
        )
        db.session.add(entry)
        db.session.commit()
        l1 = JournalEntryLine(
            journal_entry_id=entry.id, line_number=1, account_code="111",
            debit_amount=Decimal("500000"), credit_amount=Decimal("0"),
        )
        l2 = JournalEntryLine(
            journal_entry_id=entry.id, line_number=2, account_code="511",
            debit_amount=Decimal("0"), credit_amount=Decimal("500000"),
        )
        db.session.add_all([l1, l2])
        db.session.commit()

        entry.approve(user.id)
        assert entry.status == "posted"
        assert entry.approved_by == user.id
        assert entry.approved_at is not None

    def test_approve_unbalanced_raises_error(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000004",
            entry_date=date(2026, 1, 15),
            description="Unbalanced",
            accounting_period="2026-01",
            created_by=user.id,
        )
        db.session.add(entry)
        db.session.commit()
        line = JournalEntryLine(
            journal_entry_id=entry.id, line_number=1, account_code="111",
            debit_amount=Decimal("1000000"), credit_amount=Decimal("0"),
        )
        db.session.add(line)
        db.session.commit()

        with pytest.raises(ValueError, match="must be balanced"):
            entry.approve(user.id)

    def test_reverse_entry(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000005",
            entry_date=date(2026, 1, 15),
            description="To reverse",
            accounting_period="2026-01",
            created_by=user.id,
            status="posted",
        )
        db.session.add(entry)
        db.session.commit()

        entry.reverse()
        assert entry.status == "reversed"

    def test_reverse_draft_raises_error(self, db):
        user = self._setup(db)

        entry = JournalEntry(
            entry_number="JE202601000006",
            entry_date=date(2026, 1, 15),
            description="Draft",
            accounting_period="2026-01",
            created_by=user.id,
            status="draft",
        )
        db.session.add(entry)
        db.session.commit()

        with pytest.raises(ValueError, match="Only posted"):
            entry.reverse()

    def test_generate_entry_number(self, db):
        user = self._setup(db)

        num1 = JournalEntry.generate_entry_number("2026-01")
        assert num1 == "JE202601000001"

        entry = JournalEntry(
            entry_number=num1, entry_date=date(2026, 1, 1),
            description="x", accounting_period="2026-01", created_by=user.id,
        )
        db.session.add(entry)
        db.session.commit()

        num2 = JournalEntry.generate_entry_number("2026-01")
        assert num2 == "JE202601000002"

    def test_journal_entry_repr(self, db):
        user = self._setup(db)
        entry = JournalEntry(
            entry_number="JE202601000010", entry_date=date(2026, 1, 1),
            description="repr test", accounting_period="2026-01", created_by=user.id,
        )
        assert repr(entry) == "<JournalEntry JE202601000010>"
