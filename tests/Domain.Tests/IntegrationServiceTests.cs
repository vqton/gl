using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class IntegrationServiceTests
    {
        private readonly IntegrationService _service;

        public IntegrationServiceTests()
        {
            _service = new IntegrationService();
        }

        [Fact]
        public void ProcessSaleTransaction_ShouldCreateBalancedTransaction()
        {
            var result = _service.ProcessSaleTransaction("131", 100000000, 0.1m, DateTime.Now, "Bán hàng");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ProcessPurchaseTransaction_ShouldCreateBalancedTransaction()
        {
            var result = _service.ProcessPurchaseTransaction("331", 70000000, 0.1m, DateTime.Now, "Mua hàng");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ProcessCashReceipt_ShouldCreateBalancedTransaction()
        {
            var result = _service.ProcessCashReceipt("131", 50000000, DateTime.Now, "Thu tiền");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ProcessCashPayment_ShouldCreateBalancedTransaction()
        {
            var result = _service.ProcessCashPayment("331", 30000000, DateTime.Now, "Chi tiền");

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ProcessPeriodClosing_ShouldReturnMultipleTransactions()
        {
            var result = _service.ProcessPeriodClosing(
                "2026-01",
                new DateTime(2026, 1, 31),
                100000000, 5000000, 0, 5000000,
                70000000, 1000000, 15000000, 20000000, 0, 5000000);

            Assert.NotNull(result);
            Assert.Equal(2, result.Count);
            Assert.All(result, t => Assert.True(t.IsBalanced));
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnTrue_WhenValid()
        {
            var transaction = new Transaction
            {
                Id = "TXN001",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("111", 1000000, 0, "Nợ");
            transaction.AddLine("331", 0, 1000000, "Có");

            var (isValid, message) = _service.ValidateTransaction(transaction);

            Assert.True(isValid);
            Assert.Equal("Bút toán hợp lệ", message);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnFalse_WhenUnbalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN002",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("111", 1000000, 0, "Nợ");
            transaction.AddLine("331", 0, 500000, "Có");

            var (isValid, message) = _service.ValidateTransaction(transaction);

            Assert.False(isValid);
            Assert.Equal("Bút toán không cân bằng", message);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnFalse_WhenInvalidAccount()
        {
            var transaction = new Transaction
            {
                Id = "TXN003",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("999", 1000000, 0, "Tài khoản không tồn tại");
            transaction.AddLine("331", 0, 1000000, "Có");

            var (isValid, message) = _service.ValidateTransaction(transaction);

            Assert.False(isValid);
            Assert.Contains("không tồn tại", message);
        }

        [Fact]
        public void GetTransactionAuditHistory_ShouldReturnEntries()
        {
            _service.ProcessSaleTransaction("131", 100000000, 0.1m, DateTime.Now, "Test");

            var history = _service.GetTransactionAuditHistory("TX001");

            Assert.NotNull(history);
        }
    }
}
