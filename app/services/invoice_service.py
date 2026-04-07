"""Invoice service for Accounts Receivable."""
from datetime import date

from app.extensions import db
from app.models.invoice import Invoice


class InvoiceService:
    """Business logic for AR invoices."""

    @staticmethod
    def get_all(page=1, per_page=20, status=None, customer_id=None):
        """Get paginated invoices with optional filters."""
        query = Invoice.query
        if status:
            query = query.filter_by(status=status)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        return query.order_by(Invoice.invoice_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_id(invoice_id):
        return db.session.get(Invoice, invoice_id)

    @staticmethod
    def create(invoice_date, customer_id, description, lines, vat_rate=10, due_date=None):
        """Create a new invoice.

        Args:
            invoice_date: Date of the invoice.
            customer_id: FK to Customer.
            description: Invoice description.
            lines: List of dicts with 'description', 'quantity', 'unit_price'.
            vat_rate: VAT percentage (0, 5, 8, 10).
            due_date: Payment due date.

        Returns:
            Invoice object.

        Raises:
            ValueError: If validation fails.
        """
        if not customer_id:
            raise ValueError("Customer is required")
        if not lines:
            raise ValueError("At least one line item is required")

        period = invoice_date.strftime("%Y-%m")
        invoice_number = Invoice.generate_invoice_number(period)

        subtotal = sum(
            float(line.get("quantity", 0)) * float(line.get("unit_price", 0))
            for line in lines
        )
        vat_amount = subtotal * float(vat_rate) / 100
        total_amount = subtotal + vat_amount

        invoice = Invoice(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            customer_id=customer_id,
            description=description,
            subtotal=subtotal,
            vat_rate=vat_rate,
            vat_amount=vat_amount,
            total_amount=total_amount,
            due_date=due_date or invoice_date,
            accounting_period=period,
            status="draft",
        )
        db.session.add(invoice)
        db.session.commit()
        return invoice

    @staticmethod
    def submit(invoice_id):
        """Submit invoice for approval."""
        invoice = db.session.get(Invoice, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
        if invoice.status != "draft":
            raise ValueError("Only draft invoices can be submitted")
        invoice.status = "submitted"
        db.session.commit()
        return invoice

    @staticmethod
    def approve(invoice_id, user_id):
        """Approve an invoice."""
        from app.services.authorization import AuthorizationService
        from app.models.user import User

        invoice = db.session.get(Invoice, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
        if invoice.status != "submitted":
            raise ValueError("Only submitted invoices can be approved")

        user = db.session.get(User, user_id)
        if user:
            AuthorizationService.enforce(user, "approve", invoice)

        invoice.status = "approved"
        db.session.commit()
        return invoice

    @staticmethod
    def record_payment(invoice_id, amount):
        """Record a payment against an invoice."""
        invoice = db.session.get(Invoice, invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
        if invoice.status not in ("approved", "partial"):
            raise ValueError("Invoice must be approved before payment")

        amount = float(amount)
        invoice.paid_amount = float(invoice.paid_amount) + amount
        if invoice.paid_amount >= float(invoice.total_amount):
            invoice.status = "paid"
        else:
            invoice.status = "partial"

        db.session.commit()
        return invoice

    @staticmethod
    def get_aging(customer_id=None):
        """Get AR aging summary."""
        from app.models.customer import Customer

        query = Invoice.query.filter(Invoice.status.in_(["approved", "partial"]))
        if customer_id:
            query = query.filter_by(customer_id=customer_id)

        invoices = query.all()
        aging = {"0-30": 0, "31-60": 0, "61-90": 0, "91-180": 0, "180+": 0}
        today = date.today()

        for inv in invoices:
            balance = float(inv.total_amount) - float(inv.paid_amount)
            if balance <= 0:
                continue
            days = (today - inv.due_date).days if inv.due_date else 0
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
