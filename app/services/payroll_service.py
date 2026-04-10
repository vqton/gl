"""Payroll service with Circular 99/2025 compliance.

Insurance rates 2026 (per Law 41/2024/QH15, Decree 158/2025/ND-CP):
- BHXH: 25.5% total (Employer 17.5%, Employee 8%)
  - O&D fund: 3% (Employer only)
  - Retirement/Death: 22% (Employer 14%, Employee 8%)
  - Occupational injury: 0.5% (Employer only)
- BHYT: 4.5% total (Employer 3%, Employee 1.5%)
- BHTN: 2% total (Employer 1%, Employee 1%)
- KPCD: 2% (Employer only)

PIT deductions (per PIT Law):
- Personal deduction: 11,000,000 VND/month
- Dependent deduction: 4,400,000 VND/month/dependent
"""
from decimal import Decimal, ROUND_HALF_UP

from app.extensions import db
from app.models.employee import Employee, Payslip

PIT_PERSONAL_DEDUCTION = Decimal("11000000")
PIT_DEPENDENT_DEDUCTION = Decimal("4400000")

BHXH_EMPLOYEE_RATE = Decimal("0.08")
BHYT_EMPLOYEE_RATE = Decimal("0.015")
BHTN_EMPLOYEE_RATE = Decimal("0.01")

BHXH_EMPLOYER_RATE = Decimal("0.175")
BHYT_EMPLOYER_RATE = Decimal("0.03")
BHTN_EMPLOYER_RATE = Decimal("0.01")
KPCD_RATE = Decimal("0.02")

PIT_BRACKETS = [
    (Decimal("5000000"), Decimal("0.05")),
    (Decimal("10000000"), Decimal("0.10")),
    (Decimal("18000000"), Decimal("0.15")),
    (Decimal("32000000"), Decimal("0.20")),
    (Decimal("52000000"), Decimal("0.25")),
    (Decimal("80000000"), Decimal("0.30")),
    (None, Decimal("0.35")),
]


class PayrollService:
    """Business logic for payroll processing."""

    @staticmethod
    def calc_insurance(insurance_salary):
        """Calculate all insurance contributions.

        Returns dict with employee deductions and employer costs.
        """
        base = Decimal(str(insurance_salary))
        return {
            "bxhs_employee": (base * BHXH_EMPLOYEE_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "bhyt_employee": (base * BHYT_EMPLOYEE_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "bhtn_employee": (base * BHTN_EMPLOYEE_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "bxhs_employer": (base * BHXH_EMPLOYER_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "bhyt_employer": (base * BHYT_EMPLOYER_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "bhtn_employer": (base * BHTN_EMPLOYER_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
            "kpcd": (base * KPCD_RATE).quantize(Decimal("1"), rounding=ROUND_HALF_UP),
        }

    @staticmethod
    def calc_pit(taxable_income, dependents=0):
        """Calculate personal income tax (PIT) using progressive brackets.

        Taxable income = gross - insurance (employee portion) - deductions
        """
        income = Decimal(str(taxable_income))
        deductions = PIT_PERSONAL_DEDUCTION + (PIT_DEPENDENT_DEDUCTION * dependents)
        taxable = max(income - deductions, Decimal("0"))

        if taxable == 0:
            return Decimal("0")

        prev_threshold = Decimal("0")
        tax = Decimal("0")
        for threshold, rate in PIT_BRACKETS:
            if threshold is None:
                tax += (taxable - prev_threshold) * rate
                break
            if taxable <= threshold:
                tax += (taxable - prev_threshold) * rate
                break
            tax += (threshold - prev_threshold) * rate
            prev_threshold = threshold

        return tax.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    @staticmethod
    def create_payslip(employee_id, period, working_days=26, actual_days=26,
                       overtime_hours=0, allowance=0, bonus=0, notes=""):
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise ValueError("Nhân viên không tìm thấy")

        existing = Payslip.query.filter_by(employee_id=employee_id, period=period).first()
        if existing:
            raise ValueError(f"Bảng lương cho {employee.employee_code} kỳ {period} đã tồn tại")

        gross = Decimal(str(employee.gross_salary))
        if actual_days != working_days and working_days > 0:
            gross = (gross * actual_days / working_days).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        allowance = Decimal(str(allowance))
        bonus = Decimal(str(bonus))
        ot_hours = Decimal(str(overtime_hours))

        hourly_rate = (Decimal(str(employee.gross_salary)) / (working_days * 8)) if working_days > 0 else Decimal("0")
        ot_pay = (ot_hours * hourly_rate * Decimal("1.5")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        total_income = gross + ot_pay + allowance + bonus

        ins_salary = employee.insurance_salary if employee.insurance_salary else employee.gross_salary
        ins = PayrollService.calc_insurance(ins_salary)

        total_ins_employee = ins["bxhs_employee"] + ins["bhyt_employee"] + ins["bhtn_employee"]
        taxable_income = total_income - total_ins_employee
        pit = PayrollService.calc_pit(taxable_income, employee.dependents)

        total_deductions = total_ins_employee + pit
        net_salary = total_income - total_deductions

        total_employer = ins["bxhs_employer"] + ins["bhyt_employer"] + ins["bhtn_employer"] + ins["kpcd"]
        total_employer_cost = total_income + total_employer

        payslip = Payslip(
            employee_id=employee_id,
            period=period,
            working_days=working_days,
            actual_days=actual_days,
            gross_salary=gross,
            overtime_hours=ot_hours,
            overtime_pay=ot_pay,
            allowance=allowance,
            bonus=bonus,
            total_income=total_income,
            bhxh_employee=ins["bxhs_employee"],
            bhyt_employee=ins["bhyt_employee"],
            bhtn_employee=ins["bhtn_employee"],
            pit=pit,
            total_deductions=total_deductions,
            net_salary=net_salary,
            bhxh_employer=ins["bxhs_employer"],
            bhyt_employer=ins["bhyt_employer"],
            bhtn_employer=ins["bhtn_employer"],
            kpcd=ins["kpcd"],
            total_employer_cost=total_employer_cost,
            status="draft",
            notes=notes,
        )
        db.session.add(payslip)
        db.session.commit()
        return payslip

    @staticmethod
    def approve_payslip(payslip_id):
        payslip = db.session.get(Payslip, payslip_id)
        if not payslip:
            raise ValueError("Bảng lương không tìm thấy")
        if payslip.status != "draft":
            raise ValueError("Chỉ bảng lương ở trạng thái nháp mới có thể duyệt")
        payslip.status = "approved"
        db.session.commit()
        return payslip

    @staticmethod
    def get_payslips(period=None, employee_id=None, status=None):
        query = Payslip.query
        if period:
            query = query.filter_by(period=period)
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Payslip.period.desc(), Payslip.employee_id).all()

    @staticmethod
    def get_payroll_summary(period):
        payslips = Payslip.query.filter_by(period=period, status="approved").all()
        total_gross = sum(float(p.total_income) for p in payslips)
        total_net = sum(float(p.net_salary) for p in payslips)
        total_bhxh = sum(float(p.bhxh_employee) + float(p.bhxh_employer) for p in payslips)
        total_bhyt = sum(float(p.bhyt_employee) + float(p.bhyt_employer) for p in payslips)
        total_bhtn = sum(float(p.bhtn_employee) + float(p.bhtn_employer) for p in payslips)
        total_kpcd = sum(float(p.kpcd) for p in payslips)
        total_pit = sum(float(p.pit) for p in payslips)
        return {
            "count": len(payslips),
            "total_gross": total_gross,
            "total_net": total_net,
            "total_bhxh": total_bhxh,
            "total_bhyt": total_bhyt,
            "total_bhtn": total_bhtn,
            "total_kpcd": total_kpcd,
            "total_pit": total_pit,
            "total_employer_cost": sum(float(p.total_employer_cost) for p in payslips),
        }


class EmployeeService:
    """Business logic for employee management."""

    @staticmethod
    def get_all(active_only=True):
        query = Employee.query
        if active_only:
            query = query.filter_by(status="active")
        return query.order_by(Employee.full_name).all()

    @staticmethod
    def get_by_id(employee_id):
        return db.session.get(Employee, employee_id)

    @staticmethod
    def get_by_code(code):
        return Employee.get_by_code(code)

    @staticmethod
    def create(employee_code, full_name, hire_date, gross_salary, department="",
               position="", contract_type="indefinite", date_of_birth=None,
               id_number="", address="", phone="", email="", tax_code="",
               bank_account="", bank_name="", dependents=0, is_insured=True,
               insurance_salary=None, salary_allowance=0):
        if not employee_code or not employee_code.strip():
            raise ValueError("Mã nhân viên không được để trống")
        if not full_name or not full_name.strip():
            raise ValueError("Tên nhân viên không được để trống")
        if Employee.get_by_code(employee_code):
            raise ValueError(f"Nhân viên với mã '{employee_code}' đã tồn tại")
        employee = Employee(
            employee_code=employee_code,
            full_name=full_name,
            hire_date=hire_date,
            gross_salary=gross_salary,
            department=department,
            position=position,
            contract_type=contract_type,
            date_of_birth=date_of_birth,
            id_number=id_number,
            address=address,
            phone=phone,
            email=email,
            tax_code=tax_code,
            bank_account=bank_account,
            bank_name=bank_name,
            dependents=dependents,
            is_insured=is_insured,
            insurance_salary=insurance_salary,
            salary_allowance=salary_allowance,
            status="active",
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def update(employee_id, **kwargs):
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise ValueError("Employee not found")
        employee.update(**kwargs)
        db.session.commit()
        return employee

    @staticmethod
    def deactivate(employee_id):
        employee = db.session.get(Employee, employee_id)
        if not employee:
            raise ValueError("Employee not found")
        employee.status = "inactive"
        db.session.commit()
        return employee
