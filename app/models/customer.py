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

    invoices = db.relationship("Invoice", back_populates="customer")

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def __repr__(self):
        return f"<Customer {self.code} - {self.name}>"


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

    invoice = db.relationship("Invoice", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.payment_number}>"
