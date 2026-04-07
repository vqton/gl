"""Bill model for Accounts Payable."""
from datetime import datetime

from app.extensions import db
from app.models.base import BaseModel


class Bill(BaseModel):
    """Supplier bill/purchase invoice."""
    __tablename__ = "bills"

    bill_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, default="")
    subtotal = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    vat_rate = db.Column(db.Numeric(5, 2), default=10, nullable=False)
    vat_amount = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    total_amount = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    paid_amount = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    accounting_period = db.Column(db.String(7), nullable=False, index=True)
    status = db.Column(db.String(20), default="draft", nullable=False, index=True)
    document_number = db.Column(db.String(50), nullable=True)
    supplier_invoice_number = db.Column(db.String(50), nullable=True)

    supplier = db.relationship("Supplier", back_populates="bills")
    payments = db.relationship("BillPayment", back_populates="bill", cascade="all, delete-orphan")

    @property
    def remaining_amount(self):
        return float(self.total_amount) - float(self.paid_amount)

    @property
    def is_fully_paid(self):
        return float(self.paid_amount) >= float(self.total_amount)

    @classmethod
    def generate_bill_number(cls, period):
        prefix = period.replace("-", "")
        last = cls.query.filter(cls.bill_number.like(f"BL{prefix}%")).order_by(
            cls.bill_number.desc()
        ).first()
        if last:
            seq = int(last.bill_number[-6:]) + 1
        else:
            seq = 1
        return f"BL{prefix}{seq:06d}"

    def __repr__(self):
        return f"<Bill {self.bill_number}>"


class BillLine(BaseModel):
    """Line item for a supplier bill."""
    __tablename__ = "bill_lines"

    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"), nullable=False)
    line_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), default="")
    quantity = db.Column(db.Numeric(18, 4), default=1, nullable=False)
    unit_price = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    account_code = db.Column(db.String(10), db.ForeignKey("accounts.code"), nullable=True)
    cost_center = db.Column(db.String(20), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("bill_id", "line_number", name="uq_bill_line"),
    )

    @property
    def line_total(self):
        return float(self.quantity) * float(self.unit_price)

    def __repr__(self):
        return f"<BillLine {self.description}: {self.line_total}>"


class BillPayment(BaseModel):
    """Payment record for a supplier bill."""
    __tablename__ = "bill_payments"

    payment_number = db.Column(db.String(30), unique=True, nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    payment_method = db.Column(db.String(20), default="bank_transfer")
    reference = db.Column(db.String(100), default="")
    notes = db.Column(db.Text, default="")

    bill = db.relationship("Bill", back_populates="payments")

    @classmethod
    def generate_payment_number(cls, period):
        prefix = period.replace("-", "")
        last = cls.query.filter(cls.payment_number.like(f"BP{prefix}%")).order_by(
            cls.payment_number.desc()
        ).first()
        if last:
            seq = int(last.payment_number[-6:]) + 1
        else:
            seq = 1
        return f"BP{prefix}{seq:06d}"

    def __repr__(self):
        return f"<BillPayment {self.payment_number}>"
