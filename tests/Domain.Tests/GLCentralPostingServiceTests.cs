using GL.Application.Services;
using GL.Domain.Entities;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Tests for GL Central Posting Service (G05)
    /// </summary>
    public class GLCentralPostingServiceTests
    {
        private readonly GLCentralPostingService _service = new GLCentralPostingService();

        [Fact]
        public void G05a_CollectDailyTransactions_BalancedEntry()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("Nợ 111 / Có 112", 1000000, "111", 1000000, "112", 1000000),
                CreateTransaction("Nợ 156 / Có 131", 500000, "156", 500000, "131", 500000),
            };

            var result = _service.CollectDailyTransactions(transactions, "2026-04-15");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced, "Tổng hợp phải cân bằng");
        }

        [Fact]
        public void G05a_CollectDailyTransactions_TotalDebitEqualsTotalCredit()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("Nợ 111 / Có 511", 200000, "111", 200000, "511", 200000),
                CreateTransaction("Nợ 632 / Có 156", 150000, "632", 150000, "156", 150000),
            };

            var result = _service.CollectDailyTransactions(transactions, "2026-04-15");

            decimal totalDebit = result.Lines.Sum(l => l.DebitAmount);
            decimal totalCredit = result.Lines.Sum(l => l.CreditAmount);

            Assert.Equal(totalDebit, totalCredit);
        }

        [Fact]
        public void G05b_GenerateGeneralLedgerFile_ContainsAllAccounts()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("Nợ 111", 100000, "111", 100000, "112", 100000),
                CreateTransaction("Nợ 156", 50000, "156", 50000, "331", 50000),
                CreateTransaction("Nợ 641", 30000, "641", 30000, "112", 30000),
            };

            var result = _service.GenerateGeneralLedgerFile(transactions, "2026-04");

            Assert.Contains(result.Lines, l => l.AccountCode == "111");
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
            Assert.Contains(result.Lines, l => l.AccountCode == "641");
        }

        [Fact]
        public void G05c_CheckDayEndBalances_ValidDayEnd()
        {
            var accountBalances = new Dictionary<string, decimal>
            {
                {"111", 18000000},
                {"211", 10000000},
                {"331", 2000000},
                {"411", 26000000},
            };

            var result = _service.CheckDayEndBalances(accountBalances, "2026-04-15");

            Assert.NotNull(result);
            Assert.True(result.IsValid, "Số dư cuối ngày phải hợp lệ");
        }

        [Fact]
        public void G05d_ReportDiscrepancies_NoDiscrepancy()
        {
            var transactions = new List<Transaction>
            {
                CreateTransaction("Nợ 111 / Có 112", 1000000, "111", 1000000, "112", 1000000),
            };

            var result = _service.ReportDiscrepancies(transactions);

            Assert.Empty(result.Discrepancies);
        }

        [Fact]
        public void G05d_ReportDiscrepancies_DetectUnbalanced()
        {
            var transaction = new Transaction
            {
                Id = "TEST-001",
                Date = System.DateTime.Today,
                Description = "Bút toán không cân",
            };
            transaction.AddLine("111", 100000, 0, "Test");
            transaction.AddLine("112", 0, 99000, "Test");

            var transactions = new List<Transaction> { transaction };

            var result = _service.ReportDiscrepancies(transactions);

            Assert.NotEmpty(result.Discrepancies);
        }

        private Transaction CreateTransaction(string desc, decimal amount, string debitAcct, decimal debitAmt, string creditAcct, decimal creditAmt)
        {
            return new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = System.DateTime.Today,
                Description = desc,
            }.Also(t =>
            {
                t.AddLine(debitAcct, debitAmt, 0, "Nợ");
                t.AddLine(creditAcct, 0, creditAmt, "Có");
            });
        }
    }

    public static class TransactionExtensions
    {
        public static Transaction Also(this Transaction t, Action<Transaction> action)
        {
            action(t);
            return t;
        }
    }
}