"""Accounting Period Management Service."""
from datetime import datetime

from app.extensions import db
from app.models.period import AccountingPeriod


class PeriodService:
    """Manage accounting periods (open, lock, close)."""

    @staticmethod
    def get_all():
        return AccountingPeriod.query.order_by(AccountingPeriod.period.desc()).all()

    @staticmethod
    def get_current():
        return AccountingPeriod.get_current_period()

    @staticmethod
    def get_by_period(period_str):
        return AccountingPeriod.query.filter_by(period=period_str).first()

    @staticmethod
    def open_period(period_str, user_id):
        """Open or create an accounting period."""
        try:
            dt = datetime.strptime(period_str, "%Y-%m")
        except ValueError:
            raise ValueError("Định dạng kỳ không hợp lệ. Sử dụng YYYY-MM")

        period = AccountingPeriod.query.filter_by(period=period_str).first()
        if period:
            if period.status == "closed":
                raise ValueError(f"Kỳ {period.display_name} đã khóa, không thể mở lại")
            period.status = "open"
        else:
            period = AccountingPeriod(
                period=period_str,
                year=dt.year,
                month=dt.month,
                status="open",
            )
            db.session.add(period)
        db.session.commit()
        return period

    @staticmethod
    def lock_period(period_str, user_id):
        """Lock an accounting period (no new entries, adjustments require override)."""
        period = AccountingPeriod.query.filter_by(period=period_str).first()
        if not period:
            raise ValueError(f"Kỳ {period_str} không tồn tại")
        if period.status == "closed":
            raise ValueError(f"Kỳ {period.display_name} đã khóa cứng")
        period.status = "locked"
        db.session.commit()
        return period

    @staticmethod
    def close_period(period_str, user_id):
        """Close an accounting period permanently."""
        period = AccountingPeriod.query.filter_by(period=period_str).first()
        if not period:
            raise ValueError(f"Kỳ {period_str} không tồn tại")
        period.status = "closed"
        period.closed_at = datetime.utcnow()
        period.closed_by = user_id
        db.session.commit()
        return period

    @staticmethod
    def auto_create_periods(months=12):
        """Auto-create periods for the next N months from current date."""
        now = datetime.now()
        created = 0
        for i in range(months):
            year = now.year + (now.month + i - 1) // 12
            month = (now.month + i - 1) % 12 + 1
            period_str = f"{year}-{month:02d}"
            existing = AccountingPeriod.query.filter_by(period=period_str).first()
            if not existing:
                p = AccountingPeriod(period=period_str, year=year, month=month, status="open")
                db.session.add(p)
                created += 1
        db.session.commit()
        return created
