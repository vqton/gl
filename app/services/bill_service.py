"""Bill service for Accounts Payable."""
from datetime import date

from app.extensions import db
from app.models.bill import Bill, BillLine, BillPayment
from app.models.supplier import Supplier


class BillService:
    """Business logic for AP bills."""

    @staticmethod
    def get_all(page=1, per_page=20, status=None, supplier_id=None):
        query = Bill.query
        if status:
            query = query.filter_by(status=status)
        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)
        return query.order_by(Bill.invoice_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_id(bill_id):
        return db.session.get(Bill, bill_id)

    @staticmethod
    def create(invoice_date, supplier_id, description, lines, vat_rate=10, due_date=None,
               document_number=None, supplier_invoice_number=None):
        if not supplier_id:
            raise ValueError("Supplier is required")
        if not lines:
            raise ValueError("At least one line item is required")

        period = invoice_date.strftime("%Y-%m")
        bill_number = Bill.generate_bill_number(period)

        subtotal = sum(
            float(line.get("quantity", 0)) * float(line.get("unit_price", 0))
            for line in lines
        )
        vat_amount = subtotal * float(vat_rate) / 100
        total_amount = subtotal + vat_amount

        bill = Bill(
            bill_number=bill_number,
            supplier_id=supplier_id,
            invoice_date=invoice_date,
            description=description,
            subtotal=subtotal,
            vat_rate=vat_rate,
            vat_amount=vat_amount,
            total_amount=total_amount,
            due_date=due_date or invoice_date,
            accounting_period=period,
            status="draft",
            document_number=document_number,
            supplier_invoice_number=supplier_invoice_number,
        )
        db.session.add(bill)
        db.session.flush()

        for i, line_data in enumerate(lines, 1):
            line = BillLine(
                bill_id=bill.id,
                line_number=i,
                description=line_data.get("description", ""),
                quantity=line_data.get("quantity", 1),
                unit_price=line_data.get("unit_price", 0),
                account_code=line_data.get("account_code"),
                cost_center=line_data.get("cost_center"),
            )
            db.session.add(line)

        db.session.commit()
        return bill

    @staticmethod
    def submit(bill_id):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            raise ValueError("Bill not found")
        if bill.status != "draft":
            raise ValueError("Only draft bills can be submitted")
        bill.status = "submitted"
        db.session.commit()
        return bill

    @staticmethod
    def approve(bill_id, user_id):
        from app.services.authorization import AuthorizationService
        from app.models.user import User

        bill = db.session.get(Bill, bill_id)
        if not bill:
            raise ValueError("Bill not found")
        if bill.status != "submitted":
            raise ValueError("Only submitted bills can be approved")

        user = db.session.get(User, user_id)
        if user:
            AuthorizationService.enforce(user, "approve", bill)

        bill.status = "approved"
        db.session.commit()
        return bill

    @staticmethod
    def record_payment(bill_id, amount, payment_date=None, payment_method="bank_transfer",
                       reference="", notes=""):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            raise ValueError("Bill not found")
        if bill.status not in ("approved", "partial"):
            raise ValueError("Bill must be approved before payment")

        amount = float(amount)
        remaining = float(bill.total_amount) - float(bill.paid_amount)
        if amount > remaining:
            raise ValueError(f"Payment exceeds remaining amount of {remaining:,.0f}")

        period = (payment_date or date.today()).strftime("%Y-%m")
        payment_number = BillPayment.generate_payment_number(period)

        payment = BillPayment(
            payment_number=payment_number,
            bill_id=bill_id,
            payment_date=payment_date or date.today(),
            amount=amount,
            payment_method=payment_method,
            reference=reference,
            notes=notes,
        )
        db.session.add(payment)

        bill.paid_amount = float(bill.paid_amount) + amount
        if bill.paid_amount >= float(bill.total_amount):
            bill.status = "paid"
        else:
            bill.status = "partial"

        db.session.commit()
        return payment

    @staticmethod
    def get_aging(supplier_id=None):
        query = Bill.query.filter(Bill.status.in_(["approved", "partial"]))
        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)

        bills = query.all()
        aging = {"0-30": 0, "31-60": 0, "61-90": 0, "91-180": 0, "180+": 0}
        today = date.today()

        for bill in bills:
            balance = float(bill.total_amount) - float(bill.paid_amount)
            if balance <= 0:
                continue
            days = (today - bill.due_date).days if bill.due_date else 0
            if days <= 30:
                aging["0-30"] += balance
            elif days <= 60:
                aging["31-60"] += balance
            elif days <= 90:
                aging["61-90"] += balance
            elif days <= 180:
                aging["91-180"] += balance
            else:
                aging["180+"] += balance

        return aging


class SupplierService:
    """Business logic for AP suppliers."""

    @staticmethod
    def get_all():
        return Supplier.query.order_by(Supplier.name).all()

    @staticmethod
    def get_by_id(supplier_id):
        return db.session.get(Supplier, supplier_id)

    @staticmethod
    def get_by_code(code):
        return Supplier.get_by_code(code)

    @staticmethod
    def create(code, name, tax_code="", address="", phone="", email="", payment_terms=30):
        if not code or not code.strip():
            raise ValueError("Mã nhà cung cấp không được để trống")
        if not name or not name.strip():
            raise ValueError("Tên nhà cung cấp không được để trống")
        if Supplier.get_by_code(code):
            raise ValueError(f"Nhà cung cấp với mã '{code}' đã tồn tại")
        supplier = Supplier(
            code=code,
            name=name,
            tax_code=tax_code,
            address=address,
            phone=phone,
            email=email,
            payment_terms=payment_terms,
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @staticmethod
    def update(supplier_id, **kwargs):
        supplier = db.session.get(Supplier, supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")
        supplier.update(**kwargs)
        db.session.commit()
        return supplier

    @staticmethod
    def delete(supplier_id):
        supplier = db.session.get(Supplier, supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")
        if supplier.bills:
            raise ValueError("Cannot delete supplier with existing bills")
        db.session.delete(supplier)
        db.session.commit()
