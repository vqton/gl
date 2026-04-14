using GL.Domain.Entities;
using GL.Domain.Enums;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Tests cho Audit Trail functionality
    /// </summary>
    public class AuditTrailTests
    {
        [Fact]
        public void AuditEntry_ShouldHaveRequiredProperties()
        {
            var auditEntry = new AuditEntry
            {
                Id = "AUD001",
                TransactionId = "TXN001",
                ActionType = "CREATE",
                AccountCode = "111",
                Amount = 1000000,
                ActionDate = DateTime.Now,
                UserId = "USER001"
            };

            Assert.NotNull(auditEntry.Id);
            Assert.NotNull(auditEntry.TransactionId);
            Assert.Equal("CREATE", auditEntry.ActionType);
        }

        [Fact]
        public void AuditEntry_ShouldTrackCreateAction()
        {
            var auditEntry = new AuditEntry
            {
                Id = "AUD001",
                TransactionId = "TXN001",
                ActionType = "CREATE",
                Description = "Tạo mới bút toán"
            };

            Assert.Equal("CREATE", auditEntry.ActionType);
            Assert.Contains("Tạo", auditEntry.Description);
        }

        [Fact]
        public void AuditEntry_ShouldTrackUpdateAction()
        {
            var auditEntry = new AuditEntry
            {
                Id = "AUD002",
                TransactionId = "TXN001",
                ActionType = "UPDATE",
                OldValue = "1000000",
                NewValue = "1500000",
                Description = "Cập nhật số tiền"
            };

            Assert.Equal("UPDATE", auditEntry.ActionType);
            Assert.Equal("1000000", auditEntry.OldValue);
            Assert.Equal("1500000", auditEntry.NewValue);
        }

        [Fact]
        public void AuditEntry_ShouldTrackDeleteAction()
        {
            var auditEntry = new AuditEntry
            {
                Id = "AUD003",
                TransactionId = "TXN001",
                ActionType = "DELETE",
                Description = "Xóa bút toán"
            };

            Assert.Equal("DELETE", auditEntry.ActionType);
        }
    }

    /// <summary>
    /// Tests cho Financial Reports
    /// </summary>
    public class FinancialReportTests
    {
        [Fact]
        public void BalanceSheetReport_ShouldCalculateAssetsCorrectly()
        {
            var report = new BalanceSheetReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddAsset("111", "Tiền mặt", 50000000);
            report.AddAsset("112", "Tiền gửi ngân hàng", 100000000);
            report.AddAsset("131", "Phải thu khách hàng", 30000000);

            var totalAssets = report.TotalAssets;

            Assert.Equal(180000000m, totalAssets);
        }

        [Fact]
        public void BalanceSheetReport_ShouldCalculateLiabilitiesCorrectly()
        {
            var report = new BalanceSheetReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddLiability("331", "Phải trả người bán", 40000000);
            report.AddLiability("3331", "Thuế GTGT phải nộp", 5000000);
            report.AddLiability("334", "Phải trả người lao động", 15000000);

            var totalLiabilities = report.TotalLiabilities;

            Assert.Equal(60000000m, totalLiabilities);
        }

        [Fact]
        public void BalanceSheetReport_ShouldCalculateEquityCorrectly()
        {
            var report = new BalanceSheetReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddEquity("341", "Vốn góp của chủ sở hữu", 100000000);
            report.AddEquity("4212", "Lợi nhuận sau thuế chưa phân phối", 20000000);

            var totalEquity = report.TotalEquity;

            Assert.Equal(120000000m, totalEquity);
        }

        [Fact]
        public void BalanceSheetReport_ShouldVerifyBalance()
        {
            var report = new BalanceSheetReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddAsset("111", "Tiền mặt", 50000000);
            report.AddAsset("112", "Tiền gửi ngân hàng", 100000000);

            report.AddLiability("331", "Phải trả người bán", 40000000);
            report.AddEquity("341", "Vốn góp", 110000000);

            var isBalanced = report.IsBalanced;

            Assert.True(isBalanced);
        }

        [Fact]
        public void IncomeStatementReport_ShouldCalculateRevenues()
        {
            var report = new IncomeStatementReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddRevenue("511", "Doanh thu bán hàng", 150000000);
            report.AddRevenue("515", "Doanh thu hoạt động tài chính", 5000000);
            report.AddRevenue("711", "Thu nhập khác", 2000000);

            var totalRevenue = report.TotalRevenue;

            Assert.Equal(157000000m, totalRevenue);
        }

        [Fact]
        public void IncomeStatementReport_ShouldCalculateExpenses()
        {
            var report = new IncomeStatementReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddExpense("632", "Giá vốn hàng bán", 80000000);
            report.AddExpense("635", "Chi phí tài chính", 5000000);
            report.AddExpense("641", "Chi phí bán hàng", 15000000);
            report.AddExpense("642", "Chi phí quản lý doanh nghiệp", 25000000);

            var totalExpenses = report.TotalExpenses;

            Assert.Equal(125000000m, totalExpenses);
        }

        [Fact]
        public void IncomeStatementReport_ShouldCalculateNetProfit()
        {
            var report = new IncomeStatementReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddRevenue("511", "Doanh thu bán hàng", 150000000);
            report.AddRevenue("515", "Doanh thu hoạt động tài chính", 5000000);

            report.AddExpense("632", "Giá vốn hàng bán", 80000000);
            report.AddExpense("641", "Chi phí bán hàng", 15000000);
            report.AddExpense("642", "Chi phí quản lý doanh nghiệp", 25000000);

            var netProfit = report.NetProfit;

            Assert.Equal(35000000m, netProfit);
        }

        [Fact]
        public void IncomeStatementReport_ShouldCalculateGrossProfit()
        {
            var report = new IncomeStatementReport
            {
                PeriodCode = "2026-01",
                ReportDate = new DateTime(2026, 1, 31)
            };

            report.AddRevenue("511", "Doanh thu bán hàng", 150000000);
            report.AddRevenue("521", "Giảm trừ doanh thu", 5000000);

            report.AddExpense("632", "Giá vốn hàng bán", 80000000);

            var grossProfit = report.GrossProfit;

            Assert.Equal(65000000m, grossProfit);
        }
    }
}
