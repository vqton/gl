from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models.base import BaseModel


class JournalEntry(BaseModel):
    __tablename__ = "journal_entries"

    entry_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    entry_date = db.Column(db.Date, nullable=False, index=True)
    document_date = db.Column(db.Date, nullable=True)
    document_number = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    entry_type = db.Column(
        db.String(32), nullable=False, default="daily"
    )
    accounting_period = db.Column(db.String(7), nullable=False, index=True)
    currency = db.Column(db.String(3), default="VND", nullable=False)
    exchange_rate = db.Column(db.Numeric(12, 4), default=1, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(
        db.String(20), nullable=False, default="draft", index=True
    )

    lines = db.relationship(
        "JournalEntryLine",
        backref="journal_entry",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="JournalEntryLine.line_number",
    )
    creator = db.relationship("User", foreign_keys=[created_by])
    approver = db.relationship("User", foreign_keys=[approved_by])

    @property
    def total_debit(self):
        return sum(line.debit_amount for line in self.lines if line.debit_amount) or Decimal("0")

    @property
    def total_credit(self):
        return sum(line.credit_amount for line in self.lines if line.credit_amount) or Decimal("0")

    @property
    def is_balanced(self):
        return self.total_debit == self.total_credit

    @property
    def can_edit(self):
        return self.status in ("draft", "pending")

    def approve(self, user_id):
        if not self.is_balanced:
            raise ValueError("Entry must be balanced before approval")
        self.status = "posted"
        self.approved_by = user_id
        self.approved_at = datetime.utcnow()

    def reverse(self):
        if self.status != "posted":
            raise ValueError("Only posted entries can be reversed")
        self.status = "reversed"

    @classmethod
    def generate_entry_number(cls, period):
        prefix = period.replace("-", "")
        last = cls.query.filter(
            cls.entry_number.like(f"JE{prefix}%")
        ).order_by(cls.entry_number.desc()).first()
        if last:
            seq = int(last.entry_number[-6:]) + 1
        else:
            seq = 1
        return f"JE{prefix}{seq:06d}"

    def __repr__(self):
        return f"<JournalEntry {self.entry_number}>"


class JournalEntryLine(BaseModel):
    __tablename__ = "journal_entry_lines"

    journal_entry_id = db.Column(
        db.Integer, db.ForeignKey("journal_entries.id"), nullable=False
    )
    line_number = db.Column(db.Integer, nullable=False)
    account_code = db.Column(
        db.String(10), db.ForeignKey("accounts.code"), nullable=False
    )
    debit_amount = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    credit_amount = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    description = db.Column(db.String(500), default="")
    cost_center = db.Column(db.String(20), nullable=True)
    partner_code = db.Column(db.String(20), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("journal_entry_id", "line_number", name="uq_entry_line"),
    )

    @property
    def amount(self):
        return self.debit_amount or self.credit_amount

    def __repr__(self):
        return f"<JournalEntryLine {self.account_code}: {self.amount}>"
