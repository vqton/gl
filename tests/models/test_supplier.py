import pytest
from decimal import Decimal
from app.models.supplier import Supplier


class TestSupplierModel:
    def test_create_supplier(self, db):
        supplier = Supplier(
            code="NCC001",
            name="Test Supplier",
            tax_code="1234567890",
            address="123 Test Street",
            phone="0909 123 456",
            email="test@supplier.com",
            payment_terms=30,
        )
        db.session.add(supplier)
        db.session.commit()

        assert supplier.id is not None
        assert supplier.code == "NCC001"
        assert supplier.name == "Test Supplier"
        assert supplier.tax_code == "1234567890"

    def test_supplier_unique_code(self, db):
        supplier = Supplier(
            code="NCC002",
            name="First Supplier",
            tax_code="1234567891",
        )
        db.session.add(supplier)
        db.session.commit()

        with pytest.raises(Exception):
            duplicate = Supplier(
                code="NCC002",
                name="Duplicate Supplier",
                tax_code="1234567892",
            )
            db.session.add(duplicate)
            db.session.commit()

    def test_get_by_code(self, db):
        supplier = Supplier(
            code="NCC003",
            name="Test Supplier",
            tax_code="1234567892",
        )
        db.session.add(supplier)
        db.session.commit()

        found = Supplier.get_by_code("NCC003")
        assert found is not None
        assert found.code == "NCC003"

    def test_get_by_code_not_found(self, db):
        found = Supplier.get_by_code("NONEXISTENT")
        assert found is None

    def test_repr(self, db):
        supplier = Supplier(
            code="NCC004",
            name="Test Supplier",
            tax_code="1234567893",
        )
        assert repr(supplier) == "<Supplier NCC004 - Test Supplier>"

    def test_supplier_relationships(self, db):
        supplier = Supplier(
            code="NCC005",
            name="Test Supplier",
            tax_code="1234567894",
        )
        db.session.add(supplier)
        db.session.commit()

        assert hasattr(supplier, "bills")