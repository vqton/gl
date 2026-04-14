using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class ReportServiceTests
    {
        private readonly ReportService _service;

        public ReportServiceTests()
        {
            _service = new ReportService();
        }

        [Fact]
        public void GenerateBalanceSheetReport_ShouldCalculateAssetsFromTransactions()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("TXN001", "2026-01-15", new[]
                {
                    ("111", 50000000m, 0m),
                    ("112", 30000000m, 0m),
                    ("331", 0m, 80000000m)
                })
            };

            var result = _service.GenerateBalanceSheetReport(transactions, "2026-01", new DateTime(2026, 1, 31));

            Assert.NotNull(result);
            Assert.True(result.TotalAssets > 0);
        }

        [Fact]
        public void GenerateIncomeStatementReport_ShouldCalculateRevenues()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("TXN001", "2026-01-10", new[]
                {
                    ("131", 110000000m, 0m),
                    ("511", 0m, 110000000m)
                }),
                CreateTransaction("TXN002", "2026-01-15", new[]
                {
                    ("632", 70000000m, 0m),
                    ("151", 0m, 70000000m)
                })
            };

            var result = _service.GenerateIncomeStatementReport(transactions, "2026-01", new DateTime(2026, 1, 31));

            Assert.NotNull(result);
            Assert.True(result.TotalRevenue > 0);
        }

        [Fact]
        public void GetAccountBalance_ShouldReturnCorrectBalance()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("TXN001", "2026-01-10", new[]
                {
                    ("111", 10000000m, 0m),
                    ("112", 0m, 10000000m)
                }),
                CreateTransaction("TXN002", "2026-01-15", new[]
                {
                    ("111", 5000000m, 0m),
                    ("131", 0m, 5000000m)
                })
            };

            var balance = _service.GetAccountBalance(transactions, "111");

            Assert.Equal(15000000m, balance);
        }

        private Transaction CreateTransaction(string id, string dateStr, (string, decimal, decimal)[] lines)
        {
            var transaction = new Transaction
            {
                Id = id,
                Date = DateTime.Parse(dateStr),
                Description = $"Test transaction {id}"
            };

            foreach (var (code, debit, credit) in lines)
            {
                transaction.AddLine(code, debit, credit);
            }

            return transaction;
        }
    }
}
