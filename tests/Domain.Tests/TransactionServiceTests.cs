using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class TransactionServiceTests
    {
        private readonly TransactionService _service;

        public TransactionServiceTests()
        {
            _service = new TransactionService();
        }

        [Fact]
        public void CreateRevenueClosingEntry_ShouldCreateBalancedTransaction()
        {
            var request = new RevenueClosingRequest(
                "2026-01",
                new DateTime(2026, 1, 31),
                1000000,
                50000,
                0,
                50000,
                "2026-01"
            );

            var result = _service.CreateRevenueClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateExpenseClosingEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ExpenseClosingRequest(
                "2026-01",
                new DateTime(2026, 1, 31),
                700000,
                10000,
                50000,
                80000,
                0,
                50000,
                "2026-01"
            );

            var result = _service.CreateExpenseClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateProfitClosingEntry_ShouldCreateTransaction_WhenProfitIsPositive()
        {
            var request = new ProfitClosingRequest(
                "2026",
                new DateTime(2026, 12, 31),
                150000,
                "2026-12"
            );

            var result = _service.CreateProfitClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenOutputVatGreater()
        {
            var request = new VatDeclarationRequest(
                "2026-01",
                new DateTime(2026, 2, 20),
                100000,
                70000,
                "BANK_TRANSFER",
                "BANK001",
                "2026-01"
            );

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePayrollEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PayrollCalculationRequest(
                "PAY001",
                new DateTime(2026, 1, 31),
                1000000,
                100000,
                900000,
                "2026-01"
            );

            var result = _service.CreatePayrollEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFixedAssetPurchaseEntry_ShouldCreateBalancedTransaction()
        {
            var request = new FixedAssetPurchaseRequest(
                "AST001",
                new DateTime(2026, 1, 15),
                "TANGIBLE",
                120000000,
                12000000,
                "SUP001",
                "BANK_TRANSFER",
                "2026-01"
            );

            var result = _service.CreateFixedAssetPurchaseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateDepreciationEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DepreciationRequest(
                "2026-01",
                new DateTime(2026, 1, 31),
                "2026-01"
            );

            var result = _service.CreateDepreciationEntry(request, 1000000, "ADMIN");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnTrue_WhenTransactionIsBalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN001",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("111", 1000, 0, "Debit");
            transaction.AddLine("331", 0, 1000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.True(result);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnFalse_WhenTransactionIsUnbalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN002",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("111", 1000, 0, "Debit");
            transaction.AddLine("331", 0, 500, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result);
        }
    }
}