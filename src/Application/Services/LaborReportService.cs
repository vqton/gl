using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    public class LaborReportService
    {
        public LaborUsageReport GenerateLaborUsageReport(List<LaborContract> contracts, string periodCode)
        {
            var report = new LaborUsageReport
            {
                PeriodCode = periodCode,
                ReportDate = DateTime.Now
            };

            var activeContracts = contracts.Where(c => c.Status == ContractStatus.HoạtĐộng).ToList();
            var expiredContracts = contracts.Where(c => c.Status == ContractStatus.HếtHạn).ToList();
            var terminatedContracts = contracts.Where(c => c.Status == ContractStatus.ChấmDứt).ToList();

            report.TotalHeadcount = activeContracts.Count;
            report.TerminatedCount = expiredContracts.Count + terminatedContracts.Count;

            report.ContractsByType = contracts
                .GroupBy(c => (int)c.ContractType)
                .ToDictionary(g => g.Key, g => g.Count());

            report.TotalBaseSalary = activeContracts.Sum(c => c.BaseSalary);
            if (activeContracts.Count > 0)
                report.AverageSalary = activeContracts.Average(c => c.BaseSalary);

            return report;
        }

        public int CalculateRecruitmentCount(List<LaborContract> contracts, DateTime startDate, DateTime endDate)
        {
            return contracts.Count(c => 
                c.Status == ContractStatus.HoạtĐộng &&
                c.StartDate >= startDate && 
                c.StartDate <= endDate);
        }

        public int CalculateTerminationCount(List<LaborContract> contracts, DateTime startDate, DateTime endDate)
        {
            return contracts.Count(c => 
                (c.Status == ContractStatus.HếtHạn || 
                 c.Status == ContractStatus.ChấmDứt) &&
                c.UpdatedAt.HasValue &&
                c.UpdatedAt.Value >= startDate && 
                c.UpdatedAt.Value <= endDate);
        }
    }

    public class LaborUsageReport
    {
        public string PeriodCode { get; set; }
        public DateTime ReportDate { get; set; }
        public int TotalHeadcount { get; set; }
        public int TerminatedCount { get; set; }
        public Dictionary<int, int> ContractsByType { get; set; } = new();
        public decimal TotalBaseSalary { get; set; }
        public decimal AverageSalary { get; set; }
    }
}