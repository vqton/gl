"""Customer service for Accounts Receivable."""
from app.extensions import db
from app.models.customer import Customer


class CustomerService:
    """Business logic for AR customers."""

    @staticmethod
    def get_all():
        return Customer.query.order_by(Customer.name).all()

    @staticmethod
    def get_by_id(customer_id):
        return db.session.get(Customer, customer_id)

    @staticmethod
    def get_by_code(code):
        return Customer.query.filter_by(code=code).first()

    @staticmethod
    def create(code, name, tax_code="", address="", phone="", email="", credit_limit=0, payment_terms=30):
        if not code or not code.strip():
            raise ValueError("Mã khách hàng không được để trống")
        if not name or not name.strip():
            raise ValueError("Tên khách hàng không được để trống")
        if Customer.get_by_code(code):
            raise ValueError(f"Khách hàng với mã '{code}' đã tồn tại")
        customer = Customer(
            code=code,
            name=name,
            tax_code=tax_code,
            address=address,
            phone=phone,
            email=email,
            credit_limit=credit_limit,
            payment_terms=payment_terms,
        )
        db.session.add(customer)
        db.session.commit()
        return customer
