using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class PurchaseServiceTests
    {
        private readonly InMemoryPurchaseRepository _repo;
        private readonly PurchaseService _service;

        public PurchaseServiceTests()
        {
            _repo = new InMemoryPurchaseRepository();
            _service = new PurchaseService(_repo);
        }

        [Fact]
        public void P01_CreatePurchaseWithInventory_ShouldCreateBalancedTransaction()
        {
            var request = new PurchaseRequest
            {
                SupplierId = "NCC001",
                TransactionDate = new DateTime(2026, 1, 15),
                InventoryAccount = "156",
                SubTotal = 100000000,
                VatRate = 0.10m,
                PaymentMethod = "CREDIT",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePurchaseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void P02_CreatePurchaseWithoutInventory_ShouldCreateBalancedTransaction()
        {
            var request = new PurchaseRequest
            {
                SupplierId = "NCC001",
                TransactionDate = new DateTime(2026, 1, 15),
                ExpenseAccount = "621",
                SubTotal = 50000000,
                VatRate = 0.10m,
                PaymentMethod = "CASH",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateDirectExpenseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void P03_CreateFreightEntry_ShouldCreateBalancedTransaction()
        {
            var request = new FreightRequest
            {
                TransactionId = " freight001",
                TransactionDate = new DateTime(2026, 1, 15),
                FreightAmount = 5000000,
                FreightAccountCode = "1562",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFreightEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void P04_CreatePurchaseDiscountEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PurchaseDiscountRequest
            {
                TransactionId = "PUR004",
                TransactionDate = new DateTime(2026, 1, 15),
                SupplierId = "NCC001",
                DiscountAmount = 11000000,
                DiscountType = "PURCHASE_DISCOUNT",
                IsCreditNote = true,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePurchaseDiscountEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void P05_CreatePurchaseReturnEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PurchaseReturnRequest
            {
                TransactionId = "PUR005",
                TransactionDate = new DateTime(2026, 1, 15),
                OriginalPurchaseId = "PUR001",
                SupplierId = "NCC001",
                ReturnAmount = 11000000,
                VatAmount = 1000000,
                InventoryAccount = "156",
                IsVatDeductible = true,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePurchaseReturnEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnTrue_WhenBalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN_PUR_TEST",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("156", 100000000, 0, "Debit");
            transaction.AddLine("1331", 10000000, 0, "Debit");
            transaction.AddLine("331", 0, 110000000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.True(result);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnFalse_WhenUnbalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN_PUR_TEST2",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("156", 100000000, 0, "Debit");
            transaction.AddLine("331", 0, 50000000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result);
        }
    }
}