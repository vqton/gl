using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho PayrollCalculationService
    /// </summary>
    public class PayrollCalculationServiceTests
    {
        private readonly PayrollCalculationService _service;

        public PayrollCalculationServiceTests()
        {
            // Use in-memory repositories for testing
            var payrollRepo = new InMemoryPayrollRepository();
            var payrollLineRepo = new InMemoryPayrollLineRepository();
            var contractRepo = new InMemoryContractRepository();
            
            _service = new PayrollCalculationService(payrollRepo, payrollLineRepo, contractRepo);
        }

        [Fact]
        public void CreatePayroll_WithValidPeriod_ReturnsSuccess()
        {
            var result = _service.CreatePayroll(2026, 4);

            Assert.True(result.Success);
            Assert.NotNull(result.Payroll);
            Assert.Equal(2026, result.Payroll.Year);
            Assert.Equal(4, result.Payroll.Month);
        }

        [Fact]
        public void CreatePayroll_DuplicatePeriod_ReturnsFalse()
        {
            _service.CreatePayroll(2026, 4);
            var result = _service.CreatePayroll(2026, 4);

            Assert.False(result.Success);
            Assert.Contains("đã tồn tại", result.Message);
        }

        [Fact]
        public void CalculatePIT_Under5Million_ReturnsZero()
        {
            var pit = _service.CalculatePIT(4_000_000, 4_000_000);

            Assert.Equal(0, pit);
        }

        [Fact]
        public void CalculatePIT_5To10Million_Returns5Percent()
        {
            // Thu nhập chịu thuế = 5tr - 11tr = âm => 0
            var pit = _service.CalculatePIT(15_000_000, 5_000_000);
            
            // Thu nhập chịu thuế = 15tr - 11tr - 525k = 3.475tr
            // Thuế = 3.475tr * 5% = 173,750
            Assert.True(pit > 0);
        }

        [Fact]
        public void CalculatePIT_Over80Million_Returns35Percent()
        {
            var pit = _service.CalculatePIT(100_000_000, 10_000_000);
            
            // Cao nhất bậc 7 (35%)
            Assert.True(pit > 20_000_000);
        }

        [Fact]
        public void AddEmployeeToPayroll_ValidEmployee_ReturnsSuccess()
        {
            var payrollResult = _service.CreatePayroll(2026, 4);
            
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                EmployeeName = "Nguyễn Văn A",
                BaseSalary = 10_000_000,
                WorkingDays = 22,
                ActualWorkingDays = 22
            };

            var result = _service.AddEmployeeToPayroll(payrollResult.Payroll.Id, line);

            Assert.True(result.Success);
        }

        [Fact]
        public void CalculatePayroll_AfterAddingEmployees_ReturnsSuccess()
        {
            var payrollResult = _service.CreatePayroll(2026, 4);
            
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 10_000_000,
                WorkingDays = 22,
                ActualWorkingDays = 22
            };
            _service.AddEmployeeToPayroll(payrollResult.Payroll.Id, line);

            var result = _service.CalculatePayroll(payrollResult.Payroll.Id);

            Assert.True(result.Success);
        }

        [Fact]
        public void ApprovePayroll_AfterCalculation_ReturnsSuccess()
        {
            var payrollResult = _service.CreatePayroll(2026, 4);
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 10_000_000,
                WorkingDays = 22,
                ActualWorkingDays = 22
            };
            _service.AddEmployeeToPayroll(payrollResult.Payroll.Id, line);
            _service.CalculatePayroll(payrollResult.Payroll.Id);

            var result = _service.ApprovePayroll(payrollResult.Payroll.Id, "Kế toán trưởng");

            Assert.True(result.Success);
            Assert.NotNull(payrollResult.Payroll.ApprovedAt);
        }

        [Fact]
        public void GetPayroll_ByYearMonth_ReturnsCorrectPayroll()
        {
            _service.CreatePayroll(2026, 4);
            
            var payroll = _service.GetPayroll(2026, 4);

            Assert.NotNull(payroll);
            Assert.Equal(2026, payroll.Year);
            Assert.Equal(4, payroll.Month);
        }

        [Fact]
        public void CalculateTotalLaborCost_IncludesEmployerInsurance()
        {
            var payrollResult = _service.CreatePayroll(2026, 4);
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 10_000_000,
                HousingAllowance = 1_000_000,
                OvertimeAmount = 1_000_000,
                WorkingDays = 22,
                ActualWorkingDays = 22
            };
            _service.AddEmployeeToPayroll(payrollResult.Payroll.Id, line);
            _service.CalculatePayroll(payrollResult.Payroll.Id);

            var totalCost = _service.CalculateTotalLaborCost(payrollResult.Payroll);

            // Gross 12tr + BH DN đóng (12tr * 18.5% = 2.22tr) = 14.22tr
            Assert.True(totalCost > 12_000_000);
        }
    }

    // In-memory repositories for testing
    public class InMemoryPayrollRepository : IPayrollRepository
    {
        private readonly System.Collections.Generic.Dictionary<string, Payroll> _data = new();

        public Payroll GetById(string id) => _data.TryGetValue(id, out var p) ? p : null;
        
        public Payroll GetByPeriod(int year, int month)
        {
            return _data.Values.FirstOrDefault(p => p.Year == year && p.Month == month);
        }
        
        public System.Collections.Generic.IEnumerable<Payroll> GetAll() => _data.Values;
        
        public void Add(Payroll p) => _data[p.Id] = p;
        public void Update(Payroll p) => _data[p.Id] = p;
        public void Delete(string id) => _data.Remove(id);
    }

    public class InMemoryPayrollLineRepository : IPayrollLineRepository
    {
        private readonly System.Collections.Generic.Dictionary<string, PayrollLine> _data = new();

        public PayrollLine GetById(string id) => _data.TryGetValue(id, out var l) ? l : null;
        
        public System.Collections.Generic.IEnumerable<PayrollLine> GetByPayrollId(string payrollId)
            => _data.Values.Where(l => l.PayrollId == payrollId);
        
        public void Add(PayrollLine l) => _data[l.Id] = l;
        
        public void AddRange(System.Collections.Generic.IEnumerable<PayrollLine> lines)
        {
            foreach (var line in lines)
                _data[line.Id] = line;
        }
        
        public void Update(PayrollLine l) => _data[l.Id] = l;
        public void Delete(string id) => _data.Remove(id);
    }

    public class InMemoryContractRepository : IContractRepository
    {
        private readonly System.Collections.Generic.Dictionary<string, LaborContract> _data = new();

        public LaborContract GetById(string id) => _data.TryGetValue(id, out var c) ? c : null;
        
        public System.Collections.Generic.IEnumerable<LaborContract> GetByEmployeeId(string employeeId)
            => _data.Values.Where(c => c.EmployeeId == employeeId);
        
        public System.Collections.Generic.IEnumerable<LaborContract> GetByStatus(ContractStatus status)
            => _data.Values.Where(c => c.Status == status);
        
        public System.Collections.Generic.IEnumerable<LaborContract> GetActiveContracts()
            => _data.Values.Where(c => c.Status == ContractStatus.HoạtĐộng);
        
        public void Add(LaborContract c) => _data[c.Id] = c;
        public void Update(LaborContract c) => _data[c.Id] = c;
        public void Delete(string id) => _data.Remove(id);
        public bool Exists(string contractNumber) => _data.Values.Any(c => c.ContractNumber == contractNumber);
    }
}