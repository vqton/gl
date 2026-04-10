import pytest
from datetime import date
from decimal import Decimal
from app.services.bill_service import BillService, SupplierService
from app.models.bill import Bill, BillLine, BillPayment
from app.models.supplier import Supplier


class TestBillService:
    def test_get_all_empty(self, db):
        bills = BillService.get_all()
        assert bills.items == []

    def test_get_all_with_bills(self, db):
        supplier = Supplier(code="NCC001", name="Supplier 1", tax_code="1234567890")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000001",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=100000,
            vat_rate=10,
            vat_amount=10000,
            total_amount=110000,
        )
        bill.save()
        db.session.commit()

        bills = BillService.get_all()
        assert len(bills.items) == 1

    def test_get_by_id(self, db):
        supplier = Supplier(code="NCC002", name="Supplier 2", tax_code="1234567891")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000002",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=200000,
            vat_rate=10,
            vat_amount=20000,
            total_amount=220000,
        )
        bill.save()
        db.session.commit()

        found = BillService.get_by_id(bill.id)
        assert found is not None
        assert found.bill_number == "BL202601000002"

    def test_get_by_id_not_found(self, db):
        found = BillService.get_by_id(99999)
        assert found is None

    def test_create_bill(self, db):
        supplier = Supplier(code="NCC003", name="Supplier 3", tax_code="1234567892")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test purchase",
            lines=[
                {"description": "Item 1", "quantity": 2, "unit_price": 50000},
                {"description": "Item 2", "quantity": 1, "unit_price": 100000},
            ],
            vat_rate=10,
        )
        db.session.commit()

        assert bill.id is not None
        assert bill.bill_number is not None
        assert bill.status == "draft"
        assert float(bill.subtotal) == 200000
        assert float(bill.vat_amount) == 20000
        assert float(bill.total_amount) == 220000

    def test_create_bill_missing_supplier(self, db):
        with pytest.raises(ValueError, match="Supplier is required"):
            BillService.create(
                invoice_date=date.today(),
                supplier_id=None,
                description="Test",
                lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
            )

    def test_create_bill_no_lines(self, db):
        supplier = Supplier(code="NCC004", name="Supplier 4", tax_code="1234567893")
        supplier.save()
        db.session.commit()

        with pytest.raises(ValueError, match="At least one line item is required"):
            BillService.create(
                invoice_date=date.today(),
                supplier_id=supplier.id,
                description="Test",
                lines=[],
            )

    def test_submit_bill(self, db):
        supplier = Supplier(code="NCC005", name="Supplier 5", tax_code="1234567894")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
        )
        db.session.commit()

        result = BillService.submit(bill.id)
        assert result.status == "submitted"

    def test_submit_non_draft_bill(self, db):
        supplier = Supplier(code="NCC006", name="Supplier 6", tax_code="1234567895")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
        )
        db.session.commit()

        BillService.submit(bill.id)

        with pytest.raises(ValueError, match="Only draft bills can be submitted"):
            BillService.submit(bill.id)

    def test_approve_bill(self, db):
        supplier = Supplier(code="NCC007", name="Supplier 7", tax_code="1234567896")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
        )
        db.session.commit()

        BillService.submit(bill.id)

        from app.models.user import User
        user = User(username="testuser", email="test@example.com", full_name="Test User", role="accountant")
        user.password = "testpass"
        db.session.add(user)
        db.session.commit()

        result = BillService.approve(bill.id, user.id)
        assert result.status == "approved"

    def test_approve_non_submitted_bill(self, db):
        supplier = Supplier(code="NCC008", name="Supplier 8", tax_code="1234567897")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
        )
        db.session.commit()

        with pytest.raises(ValueError, match="Only submitted bills can be approved"):
            BillService.approve(bill.id, 1)

    def test_record_payment(self, db):
        supplier = Supplier(code="NCC009", name="Supplier 9", tax_code="1234567898")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 100000}],
            vat_rate=10,
        )
        db.session.commit()

        BillService.submit(bill.id)

        from app.models.user import User
        user = User(username="testuser2", email="test2@example.com", full_name="Test User 2", role="accountant")
        user.password = "testpass"
        db.session.add(user)
        db.session.commit()

        BillService.approve(bill.id, user.id)

        payment = BillService.record_payment(bill.id, 55000)
        assert payment is not None
        assert float(payment.amount) == 55000

        db.session.refresh(bill)
        assert float(bill.paid_amount) == 55000
        assert bill.status == "partial"

    def test_record_payment_exceeds_remaining(self, db):
        supplier = Supplier(code="NCC010", name="Supplier 10", tax_code="1234567899")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 100000}],
            vat_rate=10,
        )
        db.session.commit()

        BillService.submit(bill.id)

        from app.models.user import User
        user = User(username="testuser3", email="test3@example.com", full_name="Test User 3", role="accountant")
        user.password = "testpass"
        db.session.add(user)
        db.session.commit()

        BillService.approve(bill.id, user.id)

        with pytest.raises(ValueError, match="Payment exceeds remaining amount"):
            BillService.record_payment(bill.id, 200000)

    def test_record_payment_before_approval(self, db):
        supplier = Supplier(code="NCC011", name="Supplier 11", tax_code="1234567900")
        supplier.save()
        db.session.commit()

        bill = BillService.create(
            invoice_date=date.today(),
            supplier_id=supplier.id,
            description="Test",
            lines=[{"description": "Item 1", "quantity": 1, "unit_price": 10000}],
        )
        db.session.commit()

        with pytest.raises(ValueError, match="Bill must be approved before payment"):
            BillService.record_payment(bill.id, 10000)

    def test_get_aging(self, db):
        supplier = Supplier(code="NCC012", name="Supplier 12", tax_code="1234567901")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000012",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            due_date=date.today(),
            accounting_period="2026-01",
            status="approved",
            subtotal=100000,
            vat_rate=10,
            vat_amount=10000,
            total_amount=110000,
            paid_amount=0,
        )
        bill.save()
        db.session.commit()

        aging = BillService.get_aging()
        assert "0-30" in aging
        assert aging["0-30"] > 0


class TestSupplierService:
    def test_get_all_empty(self, db):
        suppliers = SupplierService.get_all()
        assert suppliers == []

    def test_get_all(self, db):
        s1 = Supplier(code="NCC101", name="Supplier A", tax_code="1111111111")
        s2 = Supplier(code="NCC102", name="Supplier B", tax_code="2222222222")
        s1.save()
        s2.save()
        db.session.commit()

        suppliers = SupplierService.get_all()
        assert len(suppliers) == 2

    def test_get_by_id(self, db):
        supplier = Supplier(code="NCC103", name="Supplier C", tax_code="3333333333")
        supplier.save()
        db.session.commit()

        found = SupplierService.get_by_id(supplier.id)
        assert found is not None
        assert found.id == supplier.id

    def test_get_by_id_not_found(self, db):
        found = SupplierService.get_by_id(99999)
        assert found is None

    def test_get_by_code(self, db):
        supplier = Supplier(code="NCC104", name="Supplier D", tax_code="4444444444")
        supplier.save()
        db.session.commit()

        found = SupplierService.get_by_code("NCC104")
        assert found is not None
        assert found.code == "NCC104"

    def test_get_by_code_not_found(self, db):
        found = SupplierService.get_by_code("NONEXISTENT")
        assert found is None

    def test_create_supplier(self, db):
        supplier = SupplierService.create(
            code="NCC105",
            name="New Supplier",
            tax_code="5555555555",
            address="123 Test Street",
            phone="0909 123 456",
            email="test@supplier.com",
            payment_terms=45,
        )
        db.session.commit()

        assert supplier.id is not None
        assert supplier.code == "NCC105"
        assert supplier.name == "New Supplier"
        assert supplier.tax_code == "5555555555"
        assert supplier.payment_terms == 45

    def test_create_duplicate_code_raises_error(self, db):
        SupplierService.create(
            code="NCC106",
            name="First Supplier",
            tax_code="6666666666",
        )
        db.session.commit()

        with pytest.raises(ValueError, match="Nhà cung cấp với mã"):
            SupplierService.create(
                code="NCC106",
                name="Second Supplier",
                tax_code="7777777777",
            )
        db.session.rollback()

    def test_create_missing_required_fields(self, db):
        with pytest.raises(ValueError, match="Mã nhà cung cấp không được để trống"):
            SupplierService.create(
                code="",
                name="Test Supplier",
                tax_code="8888888888",
            )
        db.session.rollback()

        with pytest.raises(ValueError, match="Tên nhà cung cấp không được để trống"):
            SupplierService.create(
                code="NCC107",
                name="",
                tax_code="9999999999",
            )
        db.session.rollback()
