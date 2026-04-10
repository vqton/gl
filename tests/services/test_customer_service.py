import pytest
from app.services.customer_service import CustomerService
from app.models.customer import Customer


class TestCustomerService:
    def test_get_all_empty(self, db):
        customers = CustomerService.get_all()
        assert customers == []

    def test_get_all(self, db):
        customer1 = Customer(
            code="KH001",
            name="Customer One",
            tax_code="1111111111"
        )
        customer2 = Customer(
            code="KH002",
            name="Customer Two",
            tax_code="2222222222"
        )
        customer1.save()
        customer2.save()
        db.session.commit()

        customers = CustomerService.get_all()
        assert len(customers) == 2
        # Should be ordered by name
        assert customers[0].name == "Customer One"
        assert customers[1].name == "Customer Two"

    def test_get_by_id(self, db):
        customer = Customer(
            code="KH003",
            name="Test Customer",
            tax_code="3333333333"
        )
        customer.save()
        db.session.commit()

        found = CustomerService.get_by_id(customer.id)
        assert found is not None
        assert found.id == customer.id
        assert found.code == "KH003"

    def test_get_by_id_not_found(self, db):
        found = CustomerService.get_by_id(99999)
        assert found is None

    def test_get_by_code(self, db):
        customer = Customer(
            code="KH004",
            name="Test Customer",
            tax_code="4444444444"
        )
        customer.save()
        db.session.commit()

        found = CustomerService.get_by_code("KH004")
        assert found is not None
        assert found.code == "KH004"
        assert found.name == "Test Customer"

    def test_get_by_code_not_found(self, db):
        found = CustomerService.get_by_code("NONEXISTENT")
        assert found is None

    def test_create_customer(self, db):
        customer = CustomerService.create(
            code="KH005",
            name="New Customer",
            tax_code="5555555555",
            address="123 Test Street",
            phone="0909 123 456",
            email="test@example.com",
            credit_limit=50000000,
            payment_terms=45
        )
        db.session.commit()

        assert customer.id is not None
        assert customer.code == "KH005"
        assert customer.name == "New Customer"
        assert customer.tax_code == "5555555555"
        assert customer.address == "123 Test Street"
        assert customer.phone == "0909 123 456"
        assert customer.email == "test@example.com"
        assert customer.credit_limit == 50000000
        assert customer.payment_terms == 45

    def test_create_duplicate_code_raises_error(self, db):
        CustomerService.create(
            code="KH006",
            name="First Customer",
            tax_code="6666666666"
        )
        db.session.commit()

        with pytest.raises(ValueError, match="Khách hàng với mã"):
            CustomerService.create(
                code="KH006",
                name="Second Customer",
                tax_code="7777777777"
            )
        db.session.rollback()  # Clean up the failed transaction

    def test_create_missing_required_fields(self, db):
        # Missing code
        with pytest.raises(ValueError, match="Mã khách hàng không được để trống"):
            CustomerService.create(
                code="",  # Empty code
                name="Test Customer",
                tax_code="8888888888"
            )
        db.session.rollback()

        # Missing name
        with pytest.raises(ValueError, match="Tên khách hàng không được để trống"):
            CustomerService.create(
                code="KH007",
                name="",  # Empty name
                tax_code="9999999999"
            )
        db.session.rollback()