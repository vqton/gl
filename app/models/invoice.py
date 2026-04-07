"""Invoice model for Accounts Receivable."""
from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class Invoice(BaseModel):
    __tablename__ = "invoices"

    invoice_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    invoice_date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    description = db.Column(db.Text, default="")
    subtotal = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    vat_rate = db.Column(db.Numeric(5, 2), nullable=False, default=10)
    vat_amount = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    paid_amount = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="draft")
    due_date = db.Column(db.Date, nullable=True)
    accounting_period = db.Column(db.String(7), nullable=False)

    customer = db.relationship("Customer", back_populates="invoices")
    payments = db.relationship("Payment", back_populates="invoice", lazy="dynamic")

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    @property
    def is_paid(self):
        return self.paid_amount >= self.total_amount

    @property
    def is_overdue(self):
        if self.due_date and not self.is_paid:
            return datetime.now().date() > self.due_date
        return False

    @classmethod
    def generate_invoice_number(cls, period):
        """Generate sequential invoice number like INV-2026-04-0001."""
        prefix = f"INV-{period}-"
        last = cls.query.filter(cls.invoice_number.like(f"{prefix}%")).order_by(
            cls.invoice_number.desc()
        ).first()
        if last:
            seq = int(last.invoice_number.split("-")[-1]) + 1
        else:
            seq = 1
        return f"{prefix}{seq:04d}"

    def __repr__(self):
        return f"<Invoice {self.invoice_number} - {self.total_amount}>"
