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
            var request = new RevenueClosingRequest
            {
                ClosingPeriodId = "2026-01",
                ClosingDate = new DateTime(2026, 1, 31),
                Revenue511 = 1000000,
                Revenue515 = 50000,
                Revenue711 = 0,
                ContraRevenue521 = 50000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateRevenueClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateExpenseClosingEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ExpenseClosingRequest
            {
                ClosingPeriodId = "2026-01",
                ClosingDate = new DateTime(2026, 1, 31),
                Expense632 = 700000,
                Expense635 = 10000,
                Expense641 = 50000,
                Expense642 = 80000,
                Expense811 = 0,
                Expense821 = 50000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateExpenseClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateProfitClosingEntry_ShouldCreateTransaction_WhenProfitIsPositive()
        {
            var request = new ProfitClosingRequest
            {
                FiscalYearId = "2026",
                ClosingDate = new DateTime(2026, 12, 31),
                ProfitAfterTaxVnd = 150000,
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateProfitClosingEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenOutputVatGreater()
        {
            var request = new VatDeclarationRequest
            {
                DeclarationPeriodId = "2026-01",
                DeclarationDate = new DateTime(2026, 2, 20),
                OutputVatTotal = 100000,
                InputVatTotal = 70000,
                PaymentMethod = "BANK_TRANSFER",
                BankAccountId = "BANK001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePayrollEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PayrollCalculationRequest
            {
                PayrollId = "PAY001",
                PayrollMonth = new DateTime(2026, 1, 31),
                TotalGrossVnd = 1000000,
                EmployeeDeductionsVnd = 100000,
                NetPayVnd = 900000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePayrollEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFixedAssetPurchaseEntry_ShouldCreateBalancedTransaction()
        {
            var request = new FixedAssetPurchaseRequest
            {
                AssetHandoverId = "AST001",
                HandoverDate = new DateTime(2026, 1, 15),
                AssetType = "TANGIBLE",
                OriginalCostVnd = 120000000,
                VatAmountVnd = 12000000,
                SupplierId = "SUP001",
                PaymentMethod = "BANK_TRANSFER",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFixedAssetPurchaseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateDepreciationEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DepreciationRequest
            {
                DepreciationPeriodId = "2026-01",
                CalculationDate = new DateTime(2026, 1, 31),
                AccountingPeriodId = "2026-01"
            };

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