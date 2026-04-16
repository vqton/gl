using GL.Application.Services;
using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class SubsidiaryLedgerServiceTests
    {
        private readonly SubsidiaryLedgerService _service = new();

        [Fact]
        public void S01a_CreateAREntry_BalancedEntry()
        {
            var request = new CreateAREntryRequest
            {
                TransactionId = "AR-001",
                TransactionDate = DateTime.Today,
                CustomerId = "KH001",
                AmountVnd = 110000,
                NetAmountVnd = 100000,
                VatAmountVnd = 10000,
            };

            var result = _service.CreateAREntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "131");
        }

        [Fact]
        public void S01b_UpdateARPayment_BalancedEntry()
        {
            var request = new UpdateARPaymentRequest
            {
                TransactionId = "PAY-001",
                PaymentDate = DateTime.Today,
                CustomerId = "KH001",
                PaymentAmountVnd = 110000,
            };

            var result = _service.UpdateARPayment(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "111");
        }

        [Fact]
        public void S01c_CalculateARAging_ReturnsReport()
        {
            var result = _service.CalculateARAging("KH001", DateTime.Today);

            Assert.NotNull(result);
            Assert.Equal("KH001", result.CustomerId);
        }

        [Fact]
        public void S01e_CreateBadDebtProvision_BalancedEntry()
        {
            var request = new CreateBadDebtProvisionRequest
            {
                TransactionId = "BDP-001",
                ProvisionDate = DateTime.Today,
                ProvisionAmountVnd = 5000000,
            };

            var result = _service.CreateBadDebtProvision(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "2293");
        }

        [Fact]
        public void S02a_CreateAPEntry_BalancedEntry()
        {
            var request = new CreateAPEntryRequest
            {
                TransactionId = "AP-001",
                TransactionDate = DateTime.Today,
                SupplierId = "NCC001",
                AmountVnd = 100000,
                VatAmountVnd = 10000,
                TotalAmountVnd = 110000,
            };

            var result = _service.CreateAPEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
        }

        [Fact]
        public void S02b_UpdateAPPayment_BalancedEntry()
        {
            var request = new UpdateAPPaymentRequest
            {
                TransactionId = "PAY-002",
                PaymentDate = DateTime.Today,
                SupplierId = "NCC001",
                PaymentAmountVnd = 110000,
            };

            var result = _service.UpdateAPPayment(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void S03a_UpdateInventoryCard_CreatesCard()
        {
            var request = new UpdateInventoryCardRequest
            {
                TransactionId = "IC-001",
                TransactionDate = DateTime.Today,
                ProductId = "SP001",
                ProductName = "Sản phẩm A",
                TransactionType = "RECEIPT",
                Quantity = 100,
                UnitCostVnd = 50000,
            };

            var result = _service.UpdateInventoryCard(request);

            Assert.NotNull(result);
            Assert.Equal("SP001", result.ProductId);
        }

        [Fact]
        public void S03b_CalculateIssueCost_FIFO()
        {
            var request = new CalculateIssueCostRequest
            {
                ProductId = "SP001",
                Method = "FIFO",
            };

            var result = _service.CalculateIssueCost(request);

            Assert.True(result >= 0);
        }

        [Fact]
        public void S03c_GenerateInventoryReport_ReturnsReport()
        {
            var result = _service.GenerateInventoryReport("SP001");

            Assert.NotNull(result);
        }
    }
}