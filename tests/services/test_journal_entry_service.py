import pytest
from datetime import date
from decimal import Decimal
from app.services.journal_entry_service import JournalEntryService
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
        user = self._setup(db)
        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Approve me",
            lines=[
                {"account_code": "111", "debit_amount": 300000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 300000},
            ],
            created_by=user.id,
        )
        approved = JournalEntryService.approve(entry.id, user.id)
        assert approved.status == "posted"

    def test_approve_not_found_raises_error(self, db):
        with pytest.raises(ValueError, match="not found"):
            JournalEntryService.approve(99999, 1)

    def test_reverse_entry(self, db):
        user = self._setup(db)
        entry = JournalEntryService.create(
            entry_date=date(2026, 1, 15),
            description="Reverse me",
            lines=[
                {"account_code": "111", "debit_amount": 400000, "credit_amount": 0},
                {"account_code": "511", "debit_amount": 0, "credit_amount": 400000},
            ],
            created_by=user.id,
        )
        JournalEntryService.approve(entry.id, user.id)
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
