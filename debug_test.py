from app.services.customer_service import CustomerService
from app.extensions import db

try:
    customer = CustomerService.create(
        code="KH007",
        name="",  # Empty name
        tax_code="9999999999"
    )
    db.session.commit()
    print("No exception raised!")
    print(f"Created customer: {customer}")
except Exception as e:
    print(f"Exception type: {type(e)}")
    print(f"Exception message: {e}")
    db.session.rollback()