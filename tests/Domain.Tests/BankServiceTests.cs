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
            var request = new BankReconciliationRequest(
                new DateTime(2026, 1, 31),
                "112",
                1000000,
                1000500,
                "Bank fee not recorded",
                "2026-01"
            );

            var result = _service.CreateBankReconciliationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateBankReconciliationEntry_ShouldCreateBalancedTransaction_WhenNoDifference()
        {
            var request = new BankReconciliationRequest(
                new DateTime(2026, 1, 31),
                "112",
                1000000,
                1000000,
                null,
                "2026-01"
            );

            var result = _service.CreateBankReconciliationEntry(request);

            Assert.NotNull(result);
            Assert.Equal(0, result.Lines.Count);
        }

        [Fact]
        public void CreateWirePaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new WirePaymentRequest(
                new DateTime(2026, 1, 15),
                "NCC001",
                "Công ty ABC",
                1100000,
                100000,
                "112",
                "2026-01"
            );

            var result = _service.CreateWirePaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
            Assert.Contains(result.Lines, l => l.AccountCode == "112");
        }

        [Fact]
        public void CreateLoanDrawdownEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LoanDrawdownRequest(
                new DateTime(2026, 1, 10),
                10000000,
                "311",
                "Vietcombank",
                0.08m,
                "2026-01"
            );

            var result = _service.CreateLoanDrawdownEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "112");
            Assert.Contains(result.Lines, l => l.AccountCode == "311");
        }

        [Fact]
        public void CreateLoanRepaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LoanRepaymentRequest(
                new DateTime(2026, 1, 20),
                10000000,
                800000,
                "311",
                "2026-01"
            );

            var result = _service.CreateLoanRepaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "311");
            Assert.Contains(result.Lines, l => l.AccountCode == "635");
        }

        [Fact]
        public void CreateBankFeeEntry_ShouldCreateBalancedTransaction()
        {
            var request = new BankFeeRequest(
                new DateTime(2026, 1, 5),
                55000,
                "Phí quản lý tài khoản tháng 1/2026",
                "6421",
                "2026-01"
            );

            var result = _service.CreateBankFeeEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInterestIncomeEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InterestIncomeRequest(
                new DateTime(2026, 1, 31),
                120000,
                "112",
                12000,
                "2026-01"
            );

            var result = _service.CreateInterestIncomeEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFxRevaluationEntry_ShouldCreateBalancedTransaction_WhenGain()
        {
            var request = new FxRevaluationRequest(
                new DateTime(2026, 1, 31),
                "112",
                1000000,
                1020000,
                "2026-01"
            );

            var result = _service.CreateFxRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFxRevaluationEntry_ShouldCreateBalancedTransaction_WhenLoss()
        {
            var request = new FxRevaluationRequest(
                new DateTime(2026, 1, 31),
                "112",
                1000000,
                980000,
                "2026-01"
            );

            var result = _service.CreateFxRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateLcOpeningEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LcOpeningRequest(
                new DateTime(2026, 1, 15),
                5000000,
                "BIDV",
                "2026-01"
            );

            var result = _service.CreateLcOpeningEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateLcSettlementEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LcSettlementRequest(
                new DateTime(2026, 2, 15),
                5000000,
                5000000,
                "2026-02"
            );

            var result = _service.CreateLcSettlementEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }
    }
}