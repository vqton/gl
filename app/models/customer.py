from app.extensions import db
from app.models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    tax_code = db.Column(db.String(20), nullable=True, index=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    payment_terms = db.Column(db.Integer, default=30)
    credit_limit = db.Column(db.Numeric(18, 2), default=0)

    invoices = db.relationship("Invoice", backref="customer", lazy="dynamic")

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def __repr__(self):
        return f"<Customer {self.code} - {self.name}>"


class Invoice(BaseModel):
    __tablename__ = "invoices"

    invoice_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    subtotal = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    vat_rate = db.Column(db.Numeric(5, 2), default=10)
    vat_amount = db.Column(db.Numeric(18, 2), default=0)
    total_amount = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    paid_amount = db.Column(db.Numeric(18, 2), default=0)
    status = db.Column(db.String(20), default="draft", nullable=False)
    notes = db.Column(db.Text, default="")

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount

    @property
    def is_fully_paid(self):
        return self.paid_amount >= self.total_amount

    @property
    def is_overdue(self):
        from datetime import date
        return not self.is_fully_paid and self.due_date < date.today()

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"


class Payment(BaseModel):
    __tablename__ = "payments"

    payment_number = db.Column(db.String(30), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    payment_method = db.Column(db.String(20), default="bank_transfer")
    reference = db.Column(db.String(100), default="")
    notes = db.Column(db.Text, default="")

    invoice = db.relationship("Invoice", backref="payments")

    def __repr__(self):
        return f"<Payment {self.payment_number}>"
