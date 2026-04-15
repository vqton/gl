using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho SocialInsuranceService
    /// </summary>
    public class SocialInsuranceTests
    {
        private readonly InMemorySocialInsuranceRepository _socialRepo;
        private readonly InMemoryPayrollLineRepositoryTest _payrollLineRepo;
        private readonly SocialInsuranceService _service;

        public SocialInsuranceTests()
        {
            _socialRepo = new InMemorySocialInsuranceRepository();
            _payrollLineRepo = new InMemoryPayrollLineRepositoryTest();
            _service = new SocialInsuranceService(_socialRepo, _payrollLineRepo);
        }

        [Fact]
        public void CreateMonthlyDeclaration_WithValidPeriod_ReturnsSuccess()
        {
            var result = _service.CreateMonthlyDeclaration(2026, 4);

            Assert.True(result.Success);
            Assert.NotNull(result.Declaration);
            Assert.Equal(2026, result.Declaration.Year);
            Assert.Equal(4, result.Declaration.Month);
        }

        [Fact]
        public void CreateMonthlyDeclaration_DuplicatePeriod_ReturnsFalse()
        {
            _service.CreateMonthlyDeclaration(2026, 4);
            var result = _service.CreateMonthlyDeclaration(2026, 4);

            Assert.False(result.Success);
            Assert.Contains("đã tồn tại", result.Message);
        }

        [Fact]
        public void CalculateSocialInsurance_10MillionSalary_ReturnsCorrectAmounts()
        {
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 10_000_000m
            };

            var (bhxh, bhyt, bhtn) = _service.CalculateSocialInsurance(line.BaseSalary);

            Assert.Equal(1_750_000m, bhxh);
            Assert.Equal(300_000m, bhyt);
            Assert.Equal(100_000m, bhtn);
        }

        [Fact]
        public void CalculateSocialInsurance_EmployerContribution_Returns14Percent()
        {
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 20_000_000m
            };

            var (bhxh, bhyt, bhtn) = _service.CalculateEmployerContribution(line.BaseSalary);

            Assert.Equal(2_800_000m, bhxh);
            Assert.Equal(400_000m, bhyt);
            Assert.Equal(100_000m, bhtn);
        }

        [Fact]
        public void CalculateSocialInsurance_CapsAt149Million()
        {
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                BaseSalary = 200_000_000m
            };

            var (bhxh, bhyt, bhtn) = _service.CalculateSocialInsurance(line.BaseSalary);

            Assert.Equal(26_075_000m, bhxh);
            Assert.Equal(4_470_000m, bhyt);
            Assert.Equal(1_490_000m, bhtn);
        }

        [Fact]
        public void GenerateDeclarationReport_WithMultipleEmployees_ReturnsTotals()
        {
            var declaration = _service.CreateMonthlyDeclaration(2026, 4).Declaration;
            Assert.NotNull(declaration);

            _service.AddEmployeeToDeclaration(declaration.Id, "EMP001", "Nguyễn Văn A", 10_000_000m);
            _service.AddEmployeeToDeclaration(declaration.Id, "EMP002", "Trần Thị B", 15_000_000m);

            var report = _service.GenerateDeclarationReport(declaration.Id);

            Assert.Equal(2, report.TotalEmployees);
            Assert.True(report.TotalSalary > 0);
        }

        [Fact]
        public void ExportToXML_ReturnsValidFormat()
        {
            var declaration = _service.CreateMonthlyDeclaration(2026, 4).Declaration;

            var xml = _service.ExportToXML(declaration.Id);

            Assert.Contains("<SoBaoHiem>", xml);
            Assert.Contains("<Nam>2026</Nam>", xml);
            Assert.Contains("<Thang>4</Thang>", xml);
        }
    }

    public class InMemorySocialInsuranceRepository : ISocialInsuranceRepository
    {
        private readonly List<SocialInsuranceDeclaration> _declarations = new();

        public void Add(SocialInsuranceDeclaration declaration)
        {
            _declarations.Add(declaration);
        }

        public SocialInsuranceDeclaration GetById(string id)
        {
            return _declarations.FirstOrDefault(d => d.Id == id);
        }

        public SocialInsuranceDeclaration GetByPeriod(int year, int month)
        {
            return _declarations.FirstOrDefault(d => d.Year == year && d.Month == month);
        }

        public void Update(SocialInsuranceDeclaration declaration)
        {
            var index = _declarations.FindIndex(d => d.Id == declaration.Id);
            if (index >= 0) _declarations[index] = declaration;
        }

        public IEnumerable<SocialInsuranceDeclaration> GetAll()
        {
            return _declarations;
        }

        public void Delete(string id)
        {
            _declarations.RemoveAll(d => d.Id == id);
        }
    }

    public class InMemoryPayrollLineRepositoryTest : IPayrollLineRepository
    {
        private readonly List<PayrollLine> _lines = new();

        public void Add(PayrollLine line)
        {
            _lines.Add(line);
        }

        public PayrollLine GetById(string id)
        {
            return _lines.FirstOrDefault(l => l.Id == id);
        }

        public IEnumerable<PayrollLine> GetByPayrollId(string payrollId)
        {
            return _lines.Where(l => l.PayrollId == payrollId);
        }

        public void AddRange(IEnumerable<PayrollLine> lines)
        {
            _lines.AddRange(lines);
        }

        public void Update(PayrollLine line)
        {
            var index = _lines.FindIndex(l => l.Id == line.Id);
            if (index >= 0) _lines[index] = line;
        }

        public void Delete(string id)
        {
            _lines.RemoveAll(l => l.Id == id);
        }

        public IEnumerable<PayrollLine> GetAll()
        {
            return _lines;
        }
    }
}