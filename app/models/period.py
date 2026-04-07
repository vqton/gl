"""Accounting Period model."""
from datetime import datetime

from app.extensions import db


class AccountingPeriod(db.Model):
    __tablename__ = "accounting_periods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    period = db.Column(db.String(7), unique=True, nullable=False)  # YYYY-MM
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="open")  # open, locked, closed
    closed_at = db.Column(db.DateTime, nullable=True)
    closed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    closed_by_user = db.relationship("User", foreign_keys=[closed_by])

    @property
    def display_name(self):
        return f"{self.month:02d}/{self.year}"

    @property
    def is_open(self):
        return self.status == "open"

    @property
    def is_locked(self):
        return self.status == "locked"

    @property
    def is_closed(self):
        return self.status == "closed"

    @classmethod
    def get_current_period(cls):
        """Get the most recent open period, or create one for current month."""
        now = datetime.now()
        period_str = now.strftime("%Y-%m")
        period = cls.query.filter_by(period=period_str).first()
        if not period:
            period = cls(
                period=period_str,
                year=now.year,
                month=now.month,
                status="open",
            )
            db.session.add(period)
            db.session.commit()
        return period

    @classmethod
    def get_open_periods(cls):
        return cls.query.filter_by(status="open").order_by(cls.period.desc()).all()

    @classmethod
    def get_closed_periods(cls):
        return cls.query.filter_by(status="closed").order_by(cls.period.desc()).all()

    def __repr__(self):
        return f"<AccountingPeriod {self.period} ({self.status})>"
