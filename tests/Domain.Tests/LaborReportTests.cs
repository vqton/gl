using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class LaborReportTests
    {
        private readonly LaborReportService _service;

        public LaborReportTests()
        {
            _service = new LaborReportService();
        }

        [Fact]
        public void GenerateLaborUsageReport_ShouldCalculateHeadcount()
        {
            var contracts = new List<LaborContract>
            {
                CreateContract("EMP001", new DateTime(2026, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP002", new DateTime(2026, 1, 1), 18000000, ContractType.CóThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP003", new DateTime(2025, 6, 1), 12000000, ContractType.ThửViệc, ContractStatus.HoạtĐộng)
            };

            var result = _service.GenerateLaborUsageReport(contracts, "2026-01");

            Assert.NotNull(result);
            Assert.Equal("2026-01", result.PeriodCode);
            Assert.Equal(3, result.TotalHeadcount);
        }

        [Fact]
        public void GenerateLaborUsageReport_ShouldGroupByContractType()
        {
            var contracts = new List<LaborContract>
            {
                CreateContract("EMP001", new DateTime(2026, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP002", new DateTime(2026, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP003", new DateTime(2026, 1, 1), 12000000, ContractType.CóThờiHạn, ContractStatus.HoạtĐộng)
            };

            var result = _service.GenerateLaborUsageReport(contracts, "2026-01");

            Assert.Equal(2, result.ContractsByType[(int)ContractType.KhôngThờiHạn]);
            Assert.Equal(1, result.ContractsByType[(int)ContractType.CóThờiHạn]);
        }

        [Fact]
        public void GenerateLaborUsageReport_ShouldCalculateTurnover()
        {
            var contracts = new List<LaborContract>
            {
                CreateContract("EMP001", new DateTime(2025, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP002", new DateTime(2025, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HếtHạn),
                CreateContract("EMP003", new DateTime(2025, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.ChấmDứt)
            };

            var result = _service.GenerateLaborUsageReport(contracts, "2026-01");

            Assert.Equal(2, result.TerminatedCount);
        }

        [Fact]
        public void CalculateRecruitmentCount_ShouldCountNewHires()
        {
            var contracts = new List<LaborContract>
            {
                CreateContract("EMP001", new DateTime(2026, 1, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP002", new DateTime(2026, 1, 15), 15000000, ContractType.CóThờiHạn, ContractStatus.HoạtĐộng),
                CreateContract("EMP003", new DateTime(2025, 12, 1), 15000000, ContractType.KhôngThờiHạn, ContractStatus.HoạtĐộng)
            };

            var result = _service.CalculateRecruitmentCount(contracts, new DateTime(2026, 1, 1), new DateTime(2026, 1, 31));

            Assert.Equal(2, result);
        }

        private LaborContract CreateContract(string employeeId, DateTime startDate, decimal salary, ContractType type, ContractStatus status)
        {
            return new LaborContract
            {
                Id = Guid.NewGuid().ToString(),
                EmployeeId = employeeId,
                ContractNumber = "HD" + employeeId,
                ContractType = type,
                StartDate = startDate,
                BaseSalary = salary,
                Status = status,
                CreatedAt = DateTime.Now
            };
        }
    }
}