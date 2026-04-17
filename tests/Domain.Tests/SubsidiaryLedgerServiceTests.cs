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
            var request = new CreateAREntryRequest(
                "AR-001",
                DateTime.Today,
                "KH001",
                110000,
                100000,
                10000
            );

            var result = _service.CreateAREntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "131");
        }

        [Fact]
        public void S01b_UpdateARPayment_BalancedEntry()
        {
            var request = new UpdateARPaymentRequest(
                "PAY-001",
                DateTime.Today,
                "KH001",
                110000
            );

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
            var request = new CreateBadDebtProvisionRequest(
                "BDP-001",
                DateTime.Today,
                5000000
            );

            var result = _service.CreateBadDebtProvision(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "2293");
        }

        [Fact]
        public void S02a_CreateAPEntry_BalancedEntry()
        {
            var request = new CreateAPEntryRequest(
                "AP-001",
                DateTime.Today,
                "NCC001",
                100000,
                10000,
                110000
            );

            var result = _service.CreateAPEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "331");
        }

        [Fact]
        public void S02b_UpdateAPPayment_BalancedEntry()
        {
            var request = new UpdateAPPaymentRequest(
                "PAY-002",
                DateTime.Today,
                "NCC001",
                110000
            );

            var result = _service.UpdateAPPayment(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void S03a_UpdateInventoryCard_CreatesCard()
        {
            var request = new UpdateInventoryCardRequest(
                "IC-001",
                DateTime.Today,
                "SP001",
                "Sản phẩm A",
                "RECEIPT",
                100,
                50000
            );

            var result = _service.UpdateInventoryCard(request);

            Assert.NotNull(result);
            Assert.Equal("SP001", result.ProductId);
        }

        [Fact]
        public void S03b_CalculateIssueCost_FIFO()
        {
            var request = new CalculateIssueCostRequest("SP001", "FIFO");

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