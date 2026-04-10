import pytest
from decimal import Decimal
from datetime import date
from app.services.payroll_service import PayrollService, EmployeeService
from app.models.employee import Employee, Payslip


class TestPayrollService:
    def test_calc_insurance(self, db):
        result = PayrollService.calc_insurance(Decimal("10000000"))
        assert result["bxhs_employee"] == 800000  # 8%
        assert result["bxhs_employer"] == 1750000  # 17.5%
        assert result["bhyt_employee"] == 150000  # 1.5%
        assert result["bhyt_employer"] == 300000  # 3%
        assert result["bhtn_employee"] == 100000  # 1%
        assert result["bhtn_employer"] == 100000  # 1%
        assert result["kpcd"] == 200000  # 2%

    def test_calc_insurance_zero_salary(self, db):
        result = PayrollService.calc_insurance(Decimal("0"))
        assert result["bxhs_employee"] == 0
        assert result["bxhs_employer"] == 0

    def test_calc_pit_no_taxable_income(self, db):
        pit = PayrollService.calc_pit(Decimal("3000000"), dependents=2)
        # With personal deduction 11M + 2*4.4M = 19.8M, 3M < 19.8M so 0
        assert pit == 0

    def test_calc_pit_first_bracket(self, db):
        pit = PayrollService.calc_pit(Decimal("15000000"))
        # Taxable = 15M - 11M = 4M (below 5M bracket)
        # 4M * 5% = 200,000
        assert pit == 200000
        # With personal deduction 11M, 3M < 11M so 0

    def test_calc_pit_above_deduction(self, db):
        pit = PayrollService.calc_pit(Decimal("15000000"))
        # Taxable = 15M - 11M = 4M
        # First bracket: 5M * 5% = 250K, but only 4M so 4M * 5% = 200K
        assert pit == 200000

    def test_calc_pit_multiple_brackets(self, db):
        pit = PayrollService.calc_pit(Decimal("25000000"))
        # Taxable = 25M - 11M = 14M
        # 5M * 5% = 250K
        # 5M * 10% = 500K  
        # 4M * 15% = 600K
        # Total = 1,350,000
        assert pit == 1350000

    def test_calc_pit_with_dependents(self, db):
        pit_no_dep = PayrollService.calc_pit(Decimal("20000000"), dependents=0)
        pit_with_dep = PayrollService.calc_pit(Decimal("20000000"), dependents=1)
        assert pit_with_dep < pit_no_dep


class TestEmployeeService:
    def test_get_all_empty(self, db):
        employees = EmployeeService.get_all()
        assert employees == []

    def test_get_all_with_employees(self, db):
        emp = Employee(
            employee_code="NV001",
            full_name="Nguyễn Văn A",
            hire_date=date.today(),
            gross_salary=Decimal("15000000.00"),
            status="active",
        )
        db.session.add(emp)
        db.session.commit()

        employees = EmployeeService.get_all()
        assert len(employees) == 1

    def test_get_by_id(self, db):
        emp = Employee(
            employee_code="NV002",
            full_name="Nguyễn Văn B",
            hire_date=date.today(),
            gross_salary=Decimal("20000000.00"),
            status="active",
        )
        db.session.add(emp)
        db.session.commit()

        found = EmployeeService.get_by_id(emp.id)
        assert found is not None
        assert found.employee_code == "NV002"

    def test_get_by_code(self, db):
        emp = Employee(
            employee_code="NV003",
            full_name="Nguyễn Văn C",
            hire_date=date.today(),
            gross_salary=Decimal("18000000.00"),
            status="active",
        )
        db.session.add(emp)
        db.session.commit()

        found = EmployeeService.get_by_code("NV003")
        assert found is not None

    def test_create_employee(self, db):
        employee = EmployeeService.create(
            employee_code="NV004",
            full_name="Nguyễn Văn D",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
            department="Kế toán",
            position="Kế toán viên",
            dependents=1,
        )
        db.session.commit()

        assert employee.id is not None
        assert employee.employee_code == "NV004"
        assert employee.status == "active"

    def test_create_duplicate_code_raises_error(self, db):
        EmployeeService.create(
            employee_code="NV005",
            full_name="Nhân viên 1",
            hire_date=date.today(),
            gross_salary=Decimal("10000000.00"),
        )
        db.session.commit()

        with pytest.raises(ValueError, match="đã tồn tại"):
            EmployeeService.create(
                employee_code="NV005",
                full_name="Nhân viên 2",
                hire_date=date.today(),
                gross_salary=Decimal("15000000.00"),
            )
        db.session.rollback()

    def test_create_missing_required_fields(self, db):
        with pytest.raises(ValueError, match="Mã nhân viên không được để trống"):
            EmployeeService.create(
                employee_code="",
                full_name="Test Employee",
                hire_date=date.today(),
                gross_salary=Decimal("10000000.00"),
            )
        db.session.rollback()

        with pytest.raises(ValueError, match="Tên nhân viên không được để trống"):
            EmployeeService.create(
                employee_code="NV006",
                full_name="",
                hire_date=date.today(),
                gross_salary=Decimal("10000000.00"),
            )
        db.session.rollback()

    def test_update_employee(self, db):
        employee = EmployeeService.create(
            employee_code="NV007",
            full_name="Employee",
            hire_date=date.today(),
            gross_salary=Decimal("10000000.00"),
        )
        db.session.commit()

        result = EmployeeService.update(employee.id, gross_salary=Decimal("15000000.00"))
        assert float(result.gross_salary) == 15000000

    def test_deactivate_employee(self, db):
        employee = EmployeeService.create(
            employee_code="NV008",
            full_name="Employee",
            hire_date=date.today(),
            gross_salary=Decimal("10000000.00"),
        )
        db.session.commit()

        result = EmployeeService.deactivate(employee.id)
        assert result.status == "inactive"


class TestPayslipService:
    def test_create_payslip(self, db):
        employee = EmployeeService.create(
            employee_code="NV009",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
            dependents=0,
        )
        db.session.commit()

        payslip = PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
            actual_days=26,
        )
        db.session.commit()

        assert payslip.id is not None
        assert payslip.period == "2026-04"
        assert payslip.status == "draft"

    def test_create_payslip_duplicate_period_raises_error(self, db):
        employee = EmployeeService.create(
            employee_code="NV010",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
        )
        db.session.commit()

        PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
        )
        db.session.commit()

        with pytest.raises(ValueError, match="đã tồn tại"):
            PayrollService.create_payslip(
                employee_id=employee.id,
                period="2026-04",
                working_days=26,
            )
        db.session.rollback()

    def test_approve_payslip(self, db):
        employee = EmployeeService.create(
            employee_code="NV011",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
        )
        db.session.commit()

        payslip = PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
        )
        db.session.commit()

        result = PayrollService.approve_payslip(payslip.id)
        assert result.status == "approved"

    def test_approve_non_draft_raises_error(self, db):
        employee = EmployeeService.create(
            employee_code="NV012",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
        )
        db.session.commit()

        payslip = PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
        )
        db.session.commit()

        PayrollService.approve_payslip(payslip.id)

        with pytest.raises(ValueError, match="trạng thái nháp"):
            PayrollService.approve_payslip(payslip.id)
        db.session.rollback()

    def test_get_payslips_by_period(self, db):
        employee = EmployeeService.create(
            employee_code="NV013",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
        )
        db.session.commit()

        PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
        )
        db.session.commit()

        payslips = PayrollService.get_payslips(period="2026-04")
        assert len(payslips) == 1

    def test_get_payroll_summary(self, db):
        employee = EmployeeService.create(
            employee_code="NV014",
            full_name="Test Employee",
            hire_date=date(2026, 1, 1),
            gross_salary=Decimal("15000000.00"),
        )
        db.session.commit()

        payslip = PayrollService.create_payslip(
            employee_id=employee.id,
            period="2026-04",
            working_days=26,
        )
        db.session.commit()

        PayrollService.approve_payslip(payslip.id)

        summary = PayrollService.get_payroll_summary("2026-04")
        assert summary["count"] == 1
        assert summary["total_gross"] > 0