import pytest
from datetime import date
from decimal import Decimal
from app.services.journal_entry_service import JournalEntryService
from app.services.authorization import AuthorizationService
from app.services.rule_engine import RuleEngine
from app.models.account import Account
from app.models.journal_entry import JournalEntry, JournalEntryLine
from app.models.user import User


class TestJournalEntryService:
    def _setup(self, db):
        Account(code="111", name="Cash", account_type="asset", level=1).save()
        Account(code="511", name="Revenue", account_type="revenue", level=1).save()
        user = User(username="je_svc", email="je@svc.com", full_name="JE", role="accountant")
        user.password = "pass"
        db.session.add(user)
        db.session.commit()
        return user

    def test_create_entry(self, db):
        user = self._setup(db)
        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Test JE",
            lines=[
                {"account_code": "111", "debit_amount": 1000000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 1000000},
            ],
            created_by=user.id,
        )
        assert entry.entry_number is not None
        assert entry.description == "Test JE"
        assert entry.status == "draft"
        assert entry.total_debit == Decimal("1000000")
        assert entry.total_credit == Decimal("1000000")
        assert entry.is_balanced is True

    def test_get_by_id(self, db):
        user = self._setup(db)
        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Find me",
            lines=[
                {"account_code": "111", "debit_amount": 500000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 500000},
            ],
            created_by=user.id,
        )
        found = JournalEntryService.get_by_id(entry.id)
        assert found is not None
        assert found.id == entry.id

    def test_get_by_number(self, db):
        user = self._setup(db)
        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="By number",
            lines=[
                {"account_code": "111", "debit_amount": 200000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 200000},
            ],
            created_by=user.id,
        )
        found = JournalEntryService.get_by_number(entry.entry_number)
        assert found is not None
        assert found.entry_number == entry.entry_number

    def test_approve_entry(self, db):
        creator = self._setup(db)
        approver = User(
            username="je_approver", email="approver@svc.com",
            full_name="Approver", role="chief_accountant",
        )
        approver.password = "pass"
        db.session.add(approver)
        db.session.commit()

        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Approve me",
            lines=[
                {"account_code": "111", "debit_amount": 300000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 300000},
            ],
            created_by=creator.id,
        )
        approved = JournalEntryService.approve(entry.id, approver.id)
        assert approved.status == "posted"

    def test_approve_not_found_raises_error(self, db):
        with pytest.raises(ValueError, match="not found"):
            JournalEntryService.approve(99999, 1)

    def test_reverse_entry(self, db):
        creator = self._setup(db)
        approver = User(
            username="je_approver2", email="approver2@svc.com",
            full_name="Approver2", role="chief_accountant",
        )
        approver.password = "pass"
        db.session.add(approver)
        db.session.commit()

        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Reverse me",
            lines=[
                {"account_code": "111", "debit_amount": 400000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 400000},
            ],
            created_by=creator.id,
        )
        JournalEntryService.approve(entry.id, approver.id)
        reversed_entry = JournalEntryService.reverse(entry.id)
        assert reversed_entry.status == "reversed"

    def test_get_all_paginated(self, db):
        user = self._setup(db)
        for i in range(5):
            JournalEntryService.create(
                entry_date=date(2026, 1, 15),
                description=f"Entry {i}",
                lines=[
                    {"account_code": "111", "debit_amount": 100000, "credit_amount": 0},
                    {"account_code": "511", "debit_amount": 0, "credit_amount": 100000},
                ],
                created_by=user.id,
            )
        pagination = JournalEntryService.get_all(page=1, per_page=3)
        assert pagination.total == 5
        assert len(pagination.items) == 3

    def test_get_all_filter_by_period(self, db):
        user = self._setup(db)
        JournalEntryService.create(
            entry_date=date(2026, 1, 15), description="Jan",
            lines=[
                {"account_code": "111", "debit_amount": 100000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 100000},
            ],
            accounting_period="2026-01", created_by=user.id,
        )
        JournalEntryService.create(
            entry_date=date(2026, 2, 15), description="Feb",
            lines=[
                {"account_code": "111", "debit_amount": 200000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 200000},
            ],
            accounting_period="2026-02", created_by=user.id,
        )
        jan_entries = JournalEntryService.get_all(period="2026-01")
        assert jan_entries.total == 1


class TestRuleEngine:
    def test_sod_creator_cannot_approve(self, db):
        creator = User(
            username="creator", email="creator@test.com",
            full_name="Creator", role="accountant",
        )
        creator.password = "pass"
        db.session.add(creator)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000001",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=creator.id,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_sod_creator_approver(creator, entry)
        assert result["allowed"] is False
        assert "Segregation of Duties" in result["reason"]

    def test_sod_different_user_can_approve(self, db):
        creator = User(
            username="creator2", email="creator2@test.com",
            full_name="Creator2", role="accountant",
        )
        creator.password = "pass"
        db.session.add(creator)

        approver = User(
            username="approver2", email="approver2@test.com",
            full_name="Approver2", role="chief_accountant",
        )
        approver.password = "pass"
        db.session.add(approver)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000002",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=creator.id,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_sod_creator_approver(approver, entry)
        assert result["allowed"] is True

    def test_sod_approver_cannot_execute(self, db):
        approver = User(
            username="approver3", email="approver3@test.com",
            full_name="Approver3", role="chief_accountant",
        )
        approver.password = "pass"
        db.session.add(approver)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000003",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=1,
            approved_by=approver.id,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_sod_approver_executor(approver, entry)
        assert result["allowed"] is False

    def test_amount_below_threshold(self):
        user = User(username="u1", email="u1@test.com", full_name="U1", role="accountant")
        result = RuleEngine.check_amount_threshold(Decimal("500000000"), user)
        assert result["allowed"] is True
        assert result["requires_escalation"] is False

    def test_amount_above_threshold_regular_user(self):
        user = User(username="u2", email="u2@test.com", full_name="U2", role="accountant")
        result = RuleEngine.check_amount_threshold(Decimal("2000000000"), user)
        assert result["allowed"] is True
        assert result["requires_escalation"] is True

    def test_amount_above_threshold_cfo(self):
        user = User(username="u3", email="u3@test.com", full_name="U3", role="cfo")
        result = RuleEngine.check_amount_threshold(Decimal("2000000000"), user)
        assert result["allowed"] is True
        assert result["requires_escalation"] is False

    def test_amount_above_threshold_admin(self):
        user = User(username="u4", email="u4@test.com", full_name="U4", role="admin")
        result = RuleEngine.check_amount_threshold(Decimal("5000000000"), user)
        assert result["allowed"] is True
        assert result["requires_escalation"] is False

    def test_period_lock_denies(self, db):
        from app.models.period import AccountingPeriod

        period = AccountingPeriod(
            period="2025-12", year=2025, month=12, status="locked",
        )
        db.session.add(period)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202512000001",
            entry_date=date(2025, 12, 15),
            description="Test",
            accounting_period="2025-12",
            created_by=1,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_period_lock(entry)
        assert result["allowed"] is False
        assert "locked" in result["reason"].lower()

    def test_period_closed_denies(self, db):
        from app.models.period import AccountingPeriod

        period = AccountingPeriod(
            period="2025-11", year=2025, month=11, status="closed",
        )
        db.session.add(period)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202511000001",
            entry_date=date(2025, 11, 15),
            description="Test",
            accounting_period="2025-11",
            created_by=1,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_period_lock(entry)
        assert result["allowed"] is False
        assert "closed" in result["reason"].lower()

    def test_period_open_allows(self, db):
        from app.models.period import AccountingPeriod

        period = AccountingPeriod(
            period="2026-01", year=2026, month=1, status="open",
        )
        db.session.add(period)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000004",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=1,
        )
        db.session.add(entry)
        db.session.commit()

        result = RuleEngine.check_period_lock(entry)
        assert result["allowed"] is True


class TestAuthorizationService:
    def test_enforce_raises_on_sod_violation(self, db):
        creator = User(
            username="auth_creator", email="auth_creator@test.com",
            full_name="AuthCreator", role="accountant",
        )
        creator.password = "pass"
        db.session.add(creator)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000005",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=creator.id,
        )
        db.session.add(entry)
        db.session.commit()

        with pytest.raises(PermissionError):
            AuthorizationService.enforce(creator, "approve", entry)

    def test_enforce_passes_for_different_approver(self, db):
        creator = User(
            username="auth_creator2", email="auth_creator2@test.com",
            full_name="AuthCreator2", role="accountant",
        )
        creator.password = "pass"
        db.session.add(creator)

        approver = User(
            username="auth_approver", email="auth_approver@test.com",
            full_name="AuthApprover", role="chief_accountant",
        )
        approver.password = "pass"
        db.session.add(approver)
        db.session.commit()

        entry = JournalEntry(
            entry_number="JE202601000006",
            entry_date=date(2026, 1, 15),
            description="Test",
            accounting_period="2026-01",
            created_by=creator.id,
        )
        db.session.add(entry)
        db.session.commit()

        AuthorizationService.enforce(approver, "approve", entry)
