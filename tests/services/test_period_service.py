import pytest
from datetime import date, datetime
from app.services.period_service import PeriodService
from app.models.period import AccountingPeriod


class TestPeriodService:
    def test_get_all_empty(self, db):
        periods = PeriodService.get_all()
        assert periods == []

    def test_get_all_with_periods(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="open")
        db.session.add(period)
        db.session.commit()

        periods = PeriodService.get_all()
        assert len(periods) == 1

    def test_get_by_period(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="open")
        db.session.add(period)
        db.session.commit()

        found = PeriodService.get_by_period("2026-01")
        assert found is not None
        assert found.period == "2026-01"

    def test_get_by_period_not_found(self, db):
        found = PeriodService.get_by_period("2026-99")
        assert found is None

    def test_open_period_create_new(self, db):
        period = PeriodService.open_period("2026-01", user_id=1)
        assert period.status == "open"
        assert period.period == "2026-01"

    def test_open_period_existing(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="locked")
        db.session.add(period)
        db.session.commit()

        result = PeriodService.open_period("2026-01", user_id=1)
        assert result.status == "open"

    def test_open_period_closed_raises_error(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="closed")
        db.session.add(period)
        db.session.commit()

        with pytest.raises(ValueError, match="đã khóa"):
            PeriodService.open_period("2026-01", user_id=1)
        db.session.rollback()

    def test_open_invalid_format_raises_error(self, db):
        with pytest.raises(ValueError, match="không hợp lệ"):
            PeriodService.open_period("invalid", user_id=1)
        db.session.rollback()

    def test_lock_period(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="open")
        db.session.add(period)
        db.session.commit()

        result = PeriodService.lock_period("2026-01", user_id=1)
        assert result.status == "locked"

    def test_lock_closed_period_raises_error(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="closed")
        db.session.add(period)
        db.session.commit()

        with pytest.raises(ValueError, match="đã khóa cứng"):
            PeriodService.lock_period("2026-01", user_id=1)
        db.session.rollback()

    def test_lock_nonexistent_period_raises_error(self, db):
        with pytest.raises(ValueError, match="không tồn tại"):
            PeriodService.lock_period("2099-99", user_id=1)
        db.session.rollback()

    def test_close_period(self, db):
        period = AccountingPeriod(period="2026-01", year=2026, month=1, status="locked")
        db.session.add(period)
        db.session.commit()

        result = PeriodService.close_period("2026-01", user_id=1)
        assert result.status == "closed"
        assert result.closed_by == 1

    def test_auto_create_periods(self, db):
        created = PeriodService.auto_create_periods(months=3)
        assert created >= 3
        periods = PeriodService.get_all()
        assert len(periods) >= 3