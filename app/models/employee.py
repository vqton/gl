"""Employee model for Payroll."""
from app.extensions import db
from app.models.base import BaseModel


class Employee(BaseModel):
    __tablename__ = "employees"

    employee_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    id_number = db.Column(db.String(20), nullable=True)
    id_issue_date = db.Column(db.Date, nullable=True)
    id_issue_place = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    tax_code = db.Column(db.String(20), nullable=True)
    bank_account = db.Column(db.String(30), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(50), nullable=True)
    contract_type = db.Column(db.String(20), default="indefinite")
    hire_date = db.Column(db.Date, nullable=False)
    gross_salary = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    salary_allowance = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    dependents = db.Column(db.Integer, default=0, nullable=False)
    is_insured = db.Column(db.Boolean, default=True, nullable=False)
    insurance_salary = db.Column(db.Numeric(18, 2), nullable=True)
    status = db.Column(db.String(20), default="active", nullable=False)

    payslips = db.relationship("Payslip", back_populates="employee", cascade="all, delete-orphan")

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(employee_code=code).first()

    def __repr__(self):
        return f"<Employee {self.employee_code} - {self.full_name}>"


class Payslip(BaseModel):
    """Monthly payslip for an employee."""
    __tablename__ = "payslips"

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    period = db.Column(db.String(7), nullable=False, index=True)
    working_days = db.Column(db.Integer, default=26, nullable=False)
    actual_days = db.Column(db.Integer, default=26, nullable=False)
    gross_salary = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    overtime_hours = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    overtime_pay = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    allowance = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bonus = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    total_income = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhxh_employee = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhyt_employee = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhtn_employee = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    pit = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    total_deductions = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    net_salary = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhxh_employer = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhyt_employer = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    bhtn_employer = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    kpcd = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    total_employer_cost = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    status = db.Column(db.String(20), default="draft", nullable=False)
    notes = db.Column(db.Text, default="")

    employee = db.relationship("Employee", back_populates="payslips")

    __table_args__ = (
        db.UniqueConstraint("employee_id", "period", name="uq_payslip_employee_period"),
    )

    def __repr__(self):
        return f"<Payslip {self.employee_id} {self.period}>"
