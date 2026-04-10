import pytest
from datetime import date
from decimal import Decimal
from app.models.bill import Bill, BillLine, BillPayment
from app.models.supplier import Supplier


class TestBillModel:
    def test_create_bill(self, db):
        supplier = Supplier(code="TEST001", name="Test Supplier", tax_code="1234567890")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000001",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        bill.save()
        db.session.commit()

        assert bill.id is not None
        assert bill.bill_number == "BL202601000001"
        assert bill.status == "draft"

    def test_bill_unique_number(self, db):
        supplier = Supplier(code="TEST002", name="Test Supplier 2", tax_code="1234567891")
        supplier.save()
        db.session.commit()

        bill1 = Bill(
            bill_number="BL202601000002",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        bill1.save()
        db.session.commit()

        with pytest.raises(Exception):
            bill2 = Bill(
                bill_number="BL202601000002",
                supplier_id=supplier.id,
                invoice_date=date.today(),
                accounting_period="2026-01",
                status="draft",
                subtotal=Decimal("200000.00"),
                vat_rate=Decimal("10.00"),
                vat_amount=Decimal("20000.00"),
                total_amount=Decimal("220000.00"),
            )
            bill2.save()
            db.session.commit()

    def test_get_by_id(self, db):
        supplier = Supplier(code="TEST003", name="Test Supplier 3", tax_code="1234567892")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000003",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        bill.save()
        db.session.commit()

        found = Bill.query.get(bill.id)
        assert found is not None
        assert found.bill_number == "BL202601000003"

    def test_remaining_amount_property(self, db):
        supplier = Supplier(code="TEST004", name="Test Supplier 4", tax_code="1234567893")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000004",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="approved",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
            paid_amount=Decimal("55000.00"),
        )
        bill.save()
        db.session.commit()

        assert bill.remaining_amount == 55000

    def test_is_fully_paid_property(self, db):
        supplier = Supplier(code="TEST005", name="Test Supplier 5", tax_code="1234567894")
        supplier.save()
        db.session.commit()

        bill1 = Bill(
            bill_number="BL202601000005",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="paid",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
            paid_amount=Decimal("110000.00"),
        )
        bill1.save()
        db.session.commit()

        assert bill1.is_fully_paid is True

        bill2 = Bill(
            bill_number="BL202601000006",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="partial",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
            paid_amount=Decimal("50000.00"),
        )
        bill2.save()
        db.session.commit()

        assert bill2.is_fully_paid is False

    def test_generate_bill_number(self, db):
        number1 = Bill.generate_bill_number("2026-01")
        assert number1 == "BL202601000001"

    def test_repr(self, db):
        supplier = Supplier(code="TEST006", name="Test Supplier 6", tax_code="1234567895")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000007",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        assert repr(bill) == "<Bill BL202601000007>"


class TestBillLineModel:
    def test_create_bill_line(self, db):
        supplier = Supplier(code="TEST007", name="Test Supplier 7", tax_code="1234567896")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000008",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        bill.save()
        db.session.commit()

        line = BillLine(
            bill_id=bill.id,
            line_number=1,
            description="Test Item",
            quantity=Decimal("2.0000"),
            unit_price=Decimal("50000.00"),
            account_code="1561",
        )
        line.save()
        db.session.commit()

        assert line.id is not None
        assert line.line_total == 100000

    def test_line_total_property(self, db):
        supplier = Supplier(code="TEST008", name="Test Supplier 8", tax_code="1234567897")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000009",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="draft",
            subtotal=Decimal("150000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("15000.00"),
            total_amount=Decimal("165000.00"),
        )
        bill.save()
        db.session.commit()

        line = BillLine(
            bill_id=bill.id,
            line_number=1,
            description="Test Item",
            quantity=Decimal("3.0000"),
            unit_price=Decimal("50000.00"),
        )
        assert float(line.line_total) == 150000


class TestBillPaymentModel:
    def test_create_bill_payment(self, db):
        supplier = Supplier(code="TEST009", name="Test Supplier 9", tax_code="1234567898")
        supplier.save()
        db.session.commit()

        bill = Bill(
            bill_number="BL202601000010",
            supplier_id=supplier.id,
            invoice_date=date.today(),
            accounting_period="2026-01",
            status="approved",
            subtotal=Decimal("100000.00"),
            vat_rate=Decimal("10.00"),
            vat_amount=Decimal("10000.00"),
            total_amount=Decimal("110000.00"),
        )
        bill.save()
        db.session.commit()

        payment = BillPayment(
            payment_number="BP202601000001",
            bill_id=bill.id,
            payment_date=date.today(),
            amount=Decimal("55000.00"),
            payment_method="bank_transfer",
            reference="PAY001",
        )
        payment.save()
        db.session.commit()

        assert payment.id is not None
        assert payment.payment_number == "BP202601000001"

    def test_generate_payment_number(self, db):
        number = BillPayment.generate_payment_number("2026-01")
        assert number == "BP202601000001"