using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class BankServiceTests
    {
        private readonly BankService _service;

        public BankServiceTests()
        {
            _service = new BankService();
        }

        [Fact]
        public void CreateBankReconciliationEntry_ShouldCreateBalancedTransaction_WhenAdjustDifference()
        {
            var request = new BankReconciliationRequest
            {
                ReconciliationDate = new DateTime(2026, 1, 31),
                BankAccountCode = "112",
                BookBalance = 1000000,
                BankStatementBalance = 1000500,
                DifferenceReason = "Bank fee not recorded",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateBankReconciliationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateBankReconciliationEntry_ShouldCreateBalancedTransaction_WhenNoDifference()
        {
            var request = new BankReconciliationRequest
            {
                ReconciliationDate = new DateTime(2026, 1, 31),
                BankAccountCode = "112",
                BookBalance = 1000000,
                BankStatementBalance = 1000000,
                DifferenceReason = null,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateBankReconciliationEntry(request);

            Assert.NotNull(result);
            Assert.Equal(0, result.Lines.Count);
        }

        [Fact]
        public void CreateWirePaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new WirePaymentRequest
            {
                PaymentDate = new DateTime(2026, 1, 15),
                SupplierId = "NCC001",
                SupplierName = "Công ty ABC",
                AmountVnd = 1100000,
                VatAmountVnd = 100000,
                BankAccountCode = "112",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateWirePaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
            Assert.Contains(result.Lines, l => l.AccountCode == "112");
        }

        [Fact]
        public void CreateLoanDrawdownEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LoanDrawdownRequest
            {
                DrawdownDate = new DateTime(2026, 1, 10),
                LoanAmountVnd = 10000000,
                LoanAccountCode = "311",
                BankName = "Vietcombank",
                InterestRate = 0.08m,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateLoanDrawdownEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "112");
            Assert.Contains(result.Lines, l => l.AccountCode == "311");
        }

        [Fact]
        public void CreateLoanRepaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LoanRepaymentRequest
            {
                RepaymentDate = new DateTime(2026, 1, 20),
                PrincipalAmountVnd = 10000000,
                InterestAmountVnd = 800000,
                LoanAccountCode = "311",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateLoanRepaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "311");
            Assert.Contains(result.Lines, l => l.AccountCode == "635");
        }

        [Fact]
        public void CreateBankFeeEntry_ShouldCreateBalancedTransaction()
        {
            var request = new BankFeeRequest
            {
                FeeDate = new DateTime(2026, 1, 5),
                FeeAmountVnd = 55000,
                FeeDescription = "Phí quản lý tài khoản tháng 1/2026",
                ExpenseAccountCode = "6421",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateBankFeeEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInterestIncomeEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InterestIncomeRequest
            {
                InterestDate = new DateTime(2026, 1, 31),
                InterestAmountVnd = 120000,
                BankAccountCode = "112",
                TaxWithheldVnd = 12000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInterestIncomeEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFxRevaluationEntry_ShouldCreateBalancedTransaction_WhenGain()
        {
            var request = new FxRevaluationRequest
            {
                RevaluationDate = new DateTime(2026, 1, 31),
                BankAccountCode = "112",
                OriginalAmountVnd = 1000000,
                NewAmountVnd = 1020000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFxRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFxRevaluationEntry_ShouldCreateBalancedTransaction_WhenLoss()
        {
            var request = new FxRevaluationRequest
            {
                RevaluationDate = new DateTime(2026, 1, 31),
                BankAccountCode = "112",
                OriginalAmountVnd = 1000000,
                NewAmountVnd = 980000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFxRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateLcOpeningEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LcOpeningRequest
            {
               LcIssueDate = new DateTime(2026, 1, 15),
               LcAmountVnd = 5000000,
                BankName = "BIDV",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateLcOpeningEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateLcSettlementEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LcSettlementRequest
            {
                SettlementDate = new DateTime(2026, 2, 15),
                OriginalLcAmountVnd = 5000000,
                PaymentAmountVnd = 5000000,
                AccountingPeriodId = "2026-02"
            };

            var result = _service.CreateLcSettlementEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }
    }
}