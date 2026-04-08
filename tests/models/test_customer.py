import pytest
from app.models.customer import Customer


class TestCustomerModel:
    def test_create_customer(self, db):
        customer = Customer(
            code="KH001",
            name="Công ty TNHH ABC",
            tax_code="0123456789",
            address="123 Đường ABC, Quận 1, TP.HCM",
            phone="0909 123 456",
            email="abc@example.com",
            credit_limit=100000000,
            payment_terms=30
        )
        db.session.add(customer)
        db.session.commit()

        assert customer.id is not None
        assert customer.code == "KH001"
        assert customer.name == "Công ty TNHH ABC"
        assert customer.tax_code == "0123456789"
        assert customer.address == "123 Đường ABC, Quận 1, TP.HCM"
        assert customer.phone == "0909 123 456"
        assert customer.email == "abc@example.com"
        assert customer.credit_limit == 100000000
        assert customer.payment_terms == 30

    def test_customer_unique_code(self, db):
        customer1 = Customer(
            code="KH001",
            name="Customer 1",
            tax_code="0123456789"
        )
        customer2 = Customer(
            code="KH001",
            name="Customer 2",
            tax_code="9876543210"
        )
        db.session.add(customer1)
        db.session.commit()
        db.session.add(customer2)
        with pytest.raises(Exception):
            db.session.commit()

    def test_get_by_code(self, db):
        customer = Customer(
            code="KH002",
            name="Test Customer",
            tax_code="1111111111"
        )
        db.session.add(customer)
        db.session.commit()

        found = Customer.get_by_code("KH002")
        assert found is not None
        assert found.code == "KH002"
        assert found.name == "Test Customer"

    def test_get_by_code_not_found(self, db):
        found = Customer.get_by_code("NONEXISTENT")
        assert found is None

    def test_repr(self, db):
        customer = Customer(
            code="KH003",
            name="Test Customer",
            tax_code="2222222222"
        )
        db.session.add(customer)
        db.session.commit()
        assert repr(customer) == "<Customer KH003 - Test Customer>"

    def test_customer_relationships(self, db):
        # Test that relationships are properly set up
        customer = Customer(
            code="KH004",
            name="Test Customer",
            tax_code="3333333333"
        )
        db.session.add(customer)
        db.session.commit()

        # Check that relationships exist (will be empty lists initially)
        assert hasattr(customer, 'invoices')
        assert hasattr(customer, 'payments')
        assert isinstance(customer.invoices, list)
        assert isinstance(customer.payments, list)