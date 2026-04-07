"""Tax calculation service — Circular 99/2025 compliance.

VAT rates: 0%, 5%, 8%, 10% (per current regulations)
CIT rate: 20% standard
PIT: progressive brackets with deductions
"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.extensions import db
from app.models.journal_entry import JournalEntry, JournalEntryLine
from app.models.invoice import Invoice
from app.models.bill import Bill


VAT_RATES = {0: "0%", 5: "5%", 8: "8%", 10: "10%"}
CIT_RATE = Decimal("0.20")
PIT_PERSONAL_DEDUCTION = Decimal("11000000")
PIT_DEPENDENT_DEDUCTION = Decimal("4400000")
PIT_BRACKETS = [
    (Decimal("5000000"), Decimal("0.05")),
    (Decimal("10000000"), Decimal("0.10")),
    (Decimal("18000000"), Decimal("0.15")),
    (Decimal("32000000"), Decimal("0.20")),
    (Decimal("52000000"), Decimal("0.25")),
    (Decimal("80000000"), Decimal("0.30")),
    (None, Decimal("0.35")),
]


class TaxService:
    """Tax calculation and reporting."""

    @staticmethod
    def get_vat_summary(period):
        """VAT summary for a given period (YYYY-MM).

        Returns output VAT (from invoices) and input VAT (from bills).
        """
        output_invoices = Invoice.query.filter(
            Invoice.accounting_period == period,
            Invoice.status.in_(["approved", "paid", "partial"]),
        ).all()

        input_bills = Bill.query.filter(
            Bill.accounting_period == period,
            Bill.status.in_(["approved", "paid", "partial"]),
        ).all()

        output_vat = sum(float(inv.vat_amount) for inv in output_invoices)
        input_vat = sum(float(bill.vat_amount) for bill in input_bills)

        by_rate = {}
        for inv in output_invoices:
            rate = float(inv.vat_rate)
            if rate not in by_rate:
                by_rate[rate] = {"subtotal": 0, "vat": 0, "total": 0}
            by_rate[rate]["subtotal"] += float(inv.subtotal)
            by_rate[rate]["vat"] += float(inv.vat_amount)
            by_rate[rate]["total"] += float(inv.total_amount)

        return {
            "period": period,
            "output_vat": output_vat,
            "input_vat": input_vat,
            "vat_payable": output_vat - input_vat,
            "by_rate": by_rate,
            "output_count": len(output_invoices),
            "input_count": len(input_bills),
        }

    @staticmethod
    def get_cit_estimate(year):
        """Estimate Corporate Income Tax for a fiscal year.

        CIT = (Revenue - Deductible Expenses) * 20%
        """
        revenue_accounts = ("511", "515", "711")
        expense_accounts = ("621", "622", "627", "632", "635", "641", "642", "811", "821")

        total_revenue = Decimal("0")
        total_expense = Decimal("0")

        for month in range(1, 13):
            period = f"{year}-{month:02d}"
            entries = JournalEntry.query.filter_by(
                accounting_period=period, status="posted"
            ).all()
            for entry in entries:
                for line in entry.lines:
                    acc = line.account_code[:3]
                    if acc in revenue_accounts:
                        total_revenue += line.credit_amount
                    if acc in expense_accounts:
                        total_revenue += line.debit_amount

        profit = total_revenue - total_expense
        cit = max(profit * CIT_RATE, Decimal("0"))

        return {
            "year": year,
            "total_revenue": total_revenue,
            "total_expense": total_expense,
            "profit_before_tax": profit,
            "cit_estimate": cit,
        }

    @staticmethod
    def calc_pit(gross_salary, dependents=0, insurance_deductions=0):
        """Calculate Personal Income Tax for an employee.

        Taxable = gross - insurance - personal deduction - dependent deductions
        """
        income = Decimal(str(gross_salary))
        ins = Decimal(str(insurance_deductions))
        deductions = PIT_PERSONAL_DEDUCTION + (PIT_DEPENDENT_DEDUCTION * dependents)
        taxable = max(income - ins - deductions, Decimal("0"))

        if taxable == 0:
            return Decimal("0")

        prev = Decimal("0")
        tax = Decimal("0")
        for threshold, rate in PIT_BRACKETS:
            if threshold is None:
                tax += (taxable - prev) * rate
                break
            if taxable <= threshold:
                tax += (taxable - prev) * rate
                break
            tax += (threshold - prev) * rate
            prev = threshold

        return tax.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    @staticmethod
    def get_tax_dashboard(period):
        """Dashboard summary for current period."""
        vat = TaxService.get_vat_summary(period)

        year = int(period.split("-")[0])
        cit = TaxService.get_cit_estimate(year)

        from app.models.employee import Payslip
        payslips = Payslip.query.filter_by(period=period, status="approved").all()
        total_pit = sum(float(p.pit) for p in payslips)
        total_bhxh = sum(float(p.bhxh_employee) + float(p.bhxh_employer) for p in payslips)
        total_bhyt = sum(float(p.bhyt_employee) + float(p.bhyt_employer) for p in payslips)
        total_bhtn = sum(float(p.bhtn_employee) + float(p.bhtn_employer) for p in payslips)
        total_kpcd = sum(float(p.kpcd) for p in payslips)

        return {
            "vat": vat,
            "cit": cit,
            "payroll_taxes": {
                "pit": total_pit,
                "bxhs": total_bhxh,
                "bhyt": total_bhyt,
                "bhtn": total_bhtn,
                "kpcd": total_kpcd,
                "total": total_pit + total_bhxh + total_bhyt + total_bhtn + total_kpcd,
            },
            "period": period,
        }
