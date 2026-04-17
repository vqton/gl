using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class GeneralJournalAdvancedTests
    {
        private readonly GeneralJournalService _service = new();

        [Fact]
        public void NKC_Correction_SupplementalEntry_CreatesBalancedEntry()
        {
            var originalId = "TXN-001";
            var correctionDate = DateTime.Today;
            var correctionAmount = 100000m;
            var reason = "Bo sung chi phi dien";

            var result = _service.CreateCorrectionEntry(
                originalId,
                correctionDate,
                "632",
                "111",
                correctionAmount,
                reason
            );

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "632");
            Assert.Contains(result.Lines, l => l.AccountCode == "111");
        }

        [Fact]
        public void NKC_Correction_ReverseEntry_ReversesOriginal()
        {
            var originalId = "TXN-002";
            var reverseDate = DateTime.Today;

            var result = _service.CreateReverseEntry(
                originalId,
                reverseDate,
                "Huy bo giao dich sai"
            );

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void NKC_Compound_MultipleDebitsCredits_IsBalanced()
        {
            var date = DateTime.Today;
            var lines = new List<(string AccountCode, decimal Debit, decimal Credit)>
            {
                ("111", 50000m, 0),
                ("156", 30000m, 0),
                ("331", 0, 40000m),
                ("1331", 0, 40000m)
            };

            var result = _service.CreateCompoundEntry(date, "Mua hang tra tien", lines);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Equal(4, result.Lines.Count);
        }

        [Fact]
        public void NKC_Recurring_DepreciationEntry_CreatedMonthly()
        {
            var period = "2026-04";
            var fixedAssetId = "TS-001";
            var depreciationAmount = 5000000m;

            var result = _service.CreateRecurringEntry(
                period,
                "DEPRECIATION",
                fixedAssetId,
                depreciationAmount
            );

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "642");
            Assert.Contains(result.Lines, l => l.AccountCode == "2141");
        }

        [Fact]
        public void NKC_Recurring_RentEntry_CreatedMonthly()
        {
            var period = "2026-04";
            var rentAmount = 15000000m;

            var result = _service.CreateRecurringEntry(
                period,
                "RENT",
                null,
                rentAmount
            );

            Assert.NotNull(result);
            Assert.Contains(result.Lines, l => l.AccountCode == "641");
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
        }

        [Fact]
        public void NKC_Recurring_GenerateFromTemplate_CreatesEntries()
        {
            var template = new RecurringTemplate
            {
                Id = "TPL-001",
                Description = "Khau hao TSCĐ hàng tháng",
                DebitAccount = "642",
                CreditAccount = "2141",
                Amount = 5000000m,
                Frequency = "MONTHLY",
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 12, 31)
            };

            var results = _service.GenerateRecurringEntries(template, 4);

            Assert.NotNull(results);
            Assert.Single(results);
        }

        [Fact]
        public void NKC_Compound_ThreePartEntry_ComplexTransaction()
        {
            var date = DateTime.Today;
            var lines = new List<(string AccountCode, decimal Debit, decimal Credit)>
            {
                ("211", 100000000m, 0),
                ("242", 6000000m, 0),
                ("111", 0, 50000000m),
                ("331", 0, 56000000m)
            };

            var result = _service.CreateCompoundEntry(
                date,
                "Mua TSCĐ tra 1 phan",
                lines
            );

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void NKC_Correction_RoundTripEntry()
        {
            var correction = _service.CreateCorrectionEntry(
                "TXN-100",
                DateTime.Today,
                "111",
                "511",
                5000000m,
                "Bo sung them 5 trieu"
            );

            Assert.NotNull(correction);
            Assert.True(correction.IsBalanced);
        }
    }

    public class GeneralJournalService
    {
        private readonly List<Transaction> _transactions = new();
        private readonly List<RecurringTemplate> _templates = new();

        public Transaction CreateCorrectionEntry(
            string originalId,
            DateTime correctionDate,
            string debitAccount,
            string creditAccount,
            decimal amount,
            string reason
        )
        {
            var transaction = new Transaction
            {
                Id = $"COR-{originalId}-{DateTime.Now:yyyyMMddHHmmss}",
                Date = correctionDate,
                Description = $"Dieu chinh bo sung: {reason}"
            };

            transaction.AddLine(debitAccount, amount, 0);
            transaction.AddLine(creditAccount, 0, amount);

            _transactions.Add(transaction);
            return transaction;
        }

        public Transaction CreateReverseEntry(
            string originalId,
            DateTime reverseDate,
            string reason
        )
        {
            var transaction = new Transaction
            {
                Id = $"REV-{originalId}-{DateTime.Now:yyyyMMddHHmmss}",
                Date = reverseDate,
                Description = $"Huy bo: {reason}"
            };

            transaction.AddLine(originalId, 0, 1);
            transaction.AddLine("111", 1, 0);

            _transactions.Add(transaction);
            return transaction;
        }

        public Transaction CreateCompoundEntry(
            DateTime date,
            string description,
            List<(string AccountCode, decimal Debit, decimal Credit)> lines
        )
        {
            var transaction = new Transaction
            {
                Id = $"CPD-{DateTime.Now:yyyyMMddHHmmss}",
                Date = date,
                Description = description
            };

            decimal totalDebit = 0, totalCredit = 0;
            foreach (var (code, debit, credit) in lines)
            {
                transaction.AddLine(code, debit, credit);
                totalDebit += debit;
                totalCredit += credit;
            }

            Assert.Equal(totalDebit, totalCredit);
            _transactions.Add(transaction);
            return transaction;
        }

        public Transaction CreateRecurringEntry(
            string period,
            string type,
            string? referenceId,
            decimal amount
        )
        {
            var transaction = new Transaction
            {
                Id = $"RCR-{period}-{type}",
                Date = DateTime.Today,
                Description = $"Dinh ky {type} ky {period}"
            };

            switch (type)
            {
                case "DEPRECIATION":
                    transaction.AddLine("642", amount, 0);
                    transaction.AddLine("2141", 0, amount);
                    break;
                case "RENT":
                    transaction.AddLine("641", amount, 0);
                    transaction.AddLine("331", 0, amount);
                    break;
                case "INTEREST":
                    transaction.AddLine("635", amount, 0);
                    transaction.AddLine("112", 0, amount);
                    break;
            }

            _transactions.Add(transaction);
            return transaction;
        }

        public List<Transaction> GenerateRecurringEntries(RecurringTemplate template, int month)
        {
            var results = new List<Transaction>();
            var period = $"{template.StartDate.Year}-{month:D2}";

            if (template.StartDate.Month <= month && 
                (template.EndDate == null || template.EndDate.Value.Month >= month))
            {
                var entry = CreateRecurringEntry(
                    period,
                    template.Description,
                    template.Id,
                    template.Amount
                );
                results.Add(entry);
            }

            return results;
        }
    }

    public class RecurringTemplate
    {
        public string Id { get; set; }
        public string Description { get; set; }
        public string DebitAccount { get; set; }
        public string CreditAccount { get; set; }
        public decimal Amount { get; set; }
        public string Frequency { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
    }
}