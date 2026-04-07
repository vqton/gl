"""add ap payroll fa inventory models

Revision ID: 5a3b7c8d9e0f
Revises: 4629b4853422
Create Date: 2026-04-07
"""
from alembic import op
import sqlalchemy as sa

revision = '5a3b7c8d9e0f'
down_revision = '4629b4853422'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('bills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('bill_number', sa.String(length=30), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('invoice_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subtotal', sa.Numeric(18, 2), nullable=False),
        sa.Column('vat_rate', sa.Numeric(5, 2), nullable=False),
        sa.Column('vat_amount', sa.Numeric(18, 2), nullable=False),
        sa.Column('total_amount', sa.Numeric(18, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(18, 2), nullable=False),
        sa.Column('accounting_period', sa.String(length=7), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('document_number', sa.String(length=50), nullable=True),
        sa.Column('supplier_invoice_number', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bill_number')
    )
    op.create_index(op.f('ix_bills_bill_number'), 'bills', ['bill_number'], unique=False)
    op.create_index(op.f('ix_bills_accounting_period'), 'bills', ['accounting_period'], unique=False)
    op.create_index(op.f('ix_bills_status'), 'bills', ['status'], unique=False)

    op.create_table('bill_lines',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('line_number', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('quantity', sa.Numeric(18, 4), nullable=False),
        sa.Column('unit_price', sa.Numeric(18, 2), nullable=False),
        sa.Column('account_code', sa.String(length=10), nullable=True),
        sa.Column('cost_center', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ),
        sa.ForeignKeyConstraint(['account_code'], ['accounts.code'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bill_id', 'line_number', name='uq_bill_line')
    )

    op.create_table('bill_payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('payment_number', sa.String(length=30), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(18, 2), nullable=False),
        sa.Column('payment_method', sa.String(length=20), nullable=True),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('payment_number')
    )

    op.create_table('employees',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('employee_code', sa.String(length=20), nullable=False),
        sa.Column('full_name', sa.String(length=128), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('id_number', sa.String(length=20), nullable=True),
        sa.Column('id_issue_date', sa.Date(), nullable=True),
        sa.Column('id_issue_place', sa.String(length=100), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=128), nullable=True),
        sa.Column('tax_code', sa.String(length=20), nullable=True),
        sa.Column('bank_account', sa.String(length=30), nullable=True),
        sa.Column('bank_name', sa.String(length=100), nullable=True),
        sa.Column('department', sa.String(length=50), nullable=True),
        sa.Column('position', sa.String(length=50), nullable=True),
        sa.Column('contract_type', sa.String(length=20), nullable=True),
        sa.Column('hire_date', sa.Date(), nullable=False),
        sa.Column('gross_salary', sa.Numeric(18, 2), nullable=False),
        sa.Column('salary_allowance', sa.Numeric(18, 2), nullable=False),
        sa.Column('dependents', sa.Integer(), nullable=False),
        sa.Column('is_insured', sa.Boolean(), nullable=False),
        sa.Column('insurance_salary', sa.Numeric(18, 2), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code')
    )
    op.create_index(op.f('ix_employees_employee_code'), 'employees', ['employee_code'], unique=False)

    op.create_table('payslips',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('period', sa.String(length=7), nullable=False),
        sa.Column('working_days', sa.Integer(), nullable=False),
        sa.Column('actual_days', sa.Integer(), nullable=False),
        sa.Column('gross_salary', sa.Numeric(18, 2), nullable=False),
        sa.Column('overtime_hours', sa.Numeric(10, 2), nullable=False),
        sa.Column('overtime_pay', sa.Numeric(18, 2), nullable=False),
        sa.Column('allowance', sa.Numeric(18, 2), nullable=False),
        sa.Column('bonus', sa.Numeric(18, 2), nullable=False),
        sa.Column('total_income', sa.Numeric(18, 2), nullable=False),
        sa.Column('bxhs_employee', sa.Numeric(18, 2), nullable=False),
        sa.Column('bhyt_employee', sa.Numeric(18, 2), nullable=False),
        sa.Column('bhtn_employee', sa.Numeric(18, 2), nullable=False),
        sa.Column('pit', sa.Numeric(18, 2), nullable=False),
        sa.Column('total_deductions', sa.Numeric(18, 2), nullable=False),
        sa.Column('net_salary', sa.Numeric(18, 2), nullable=False),
        sa.Column('bxhs_employer', sa.Numeric(18, 2), nullable=False),
        sa.Column('bhyt_employer', sa.Numeric(18, 2), nullable=False),
        sa.Column('bhtn_employer', sa.Numeric(18, 2), nullable=False),
        sa.Column('kpcd', sa.Numeric(18, 2), nullable=False),
        sa.Column('total_employer_cost', sa.Numeric(18, 2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_id', 'period', name='uq_payslip_employee_period')
    )
    op.create_index(op.f('ix_payslips_period'), 'payslips', ['period'], unique=False)

    op.create_table('payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('payment_number', sa.String(length=30), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('invoice_id', sa.Integer(), nullable=True),
        sa.Column('payment_date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(18, 2), nullable=False),
        sa.Column('payment_method', sa.String(length=20), nullable=True),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('payment_number')
    )

    op.add_column('fixed_assets', sa.Column('disposal_date', sa.Date(), nullable=True))
    op.add_column('fixed_assets', sa.Column('disposal_value', sa.Numeric(18, 2), nullable=True))
    op.add_column('fixed_assets', sa.Column('disposal_reason', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('fixed_assets', 'disposal_reason')
    op.drop_column('fixed_assets', 'disposal_value')
    op.drop_column('fixed_assets', 'disposal_date')
    op.drop_table('payments')
    op.drop_table('payslips')
    op.drop_table('employees')
    op.drop_table('bill_payments')
    op.drop_table('bill_lines')
    op.drop_table('bills')
