from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models.journal_entry import JournalEntry, JournalEntryLine
from app.models.user import User


class JournalEntryService:
    @staticmethod
    def get_all(page=1, per_page=20, period=None, status=None):
        query = JournalEntry.query
        if period:
            query = query.filter_by(accounting_period=period)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(JournalEntry.entry_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_id(entry_id):
        return JournalEntry.query.get(entry_id)

    @staticmethod
    def get_by_number(entry_number):
        return JournalEntry.query.filter_by(entry_number=entry_number).first()

    @staticmethod
    def create(
        entry_date,
        description,
        lines,
        entry_type="daily",
        document_date=None,
        document_number=None,
        accounting_period=None,
        currency="VND",
        exchange_rate=1,
        created_by=None,
    ):
        if accounting_period is None:
            accounting_period = entry_date.strftime("%Y-%m")

        entry_number = JournalEntry.generate_entry_number(accounting_period)

        entry = JournalEntry(
            entry_number=entry_number,
            entry_date=entry_date,
            document_date=document_date,
            document_number=document_number,
            description=description,
            entry_type=entry_type,
            accounting_period=accounting_period,
            currency=currency,
            exchange_rate=exchange_rate,
            created_by=created_by,
            status="draft",
        )
        db.session.add(entry)
        db.session.flush()

        for i, line_data in enumerate(lines, 1):
            line = JournalEntryLine(
                journal_entry_id=entry.id,
                line_number=i,
                account_code=line_data["account_code"],
                debit_amount=Decimal(str(line_data.get("debit_amount", 0))),
                credit_amount=Decimal(str(line_data.get("credit_amount", 0))),
                description=line_data.get("description", ""),
                cost_center=line_data.get("cost_center"),
                partner_code=line_data.get("partner_code"),
            )
            db.session.add(line)

        db.session.commit()
        return entry

    @staticmethod
    def approve(entry_id, user_id):
        entry = JournalEntry.query.get(entry_id)
        if not entry:
            raise ValueError(f"Journal entry {entry_id} not found")

        user = db.session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        from app.services.authorization import AuthorizationService

        AuthorizationService.enforce(user, "approve", entry)

        entry.approve(user_id)
        db.session.commit()
        return entry

    @staticmethod
    def reverse(entry_id):
        entry = JournalEntry.query.get(entry_id)
        if not entry:
            raise ValueError(f"Journal entry {entry_id} not found")
        entry.reverse()
        db.session.commit()
        return entry

    @staticmethod
    def get_trial_balance(period):
        from app.models.account import Account

        accounts = Account.query.order_by(Account.code).all()
        result = []
        for acc in accounts:
            debit_q = (
                db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.debit_amount), 0))
                .join(JournalEntry)
                .filter(
                    JournalEntryLine.account_code == acc.code,
                    JournalEntry.accounting_period <= period,
                    JournalEntry.status == "posted",
                )
            )
            credit_q = (
                db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.credit_amount), 0))
                .join(JournalEntry)
                .filter(
                    JournalEntryLine.account_code == acc.code,
                    JournalEntry.accounting_period <= period,
                    JournalEntry.status == "posted",
                )
            )
            total_debit = debit_q.scalar()
            total_credit = credit_q.scalar()
            balance = total_debit - total_credit
            result.append(
                {
                    "code": acc.code,
                    "name": acc.name,
                    "debit": total_debit,
                    "credit": total_credit,
                    "balance": balance,
                }
            )
        return result
