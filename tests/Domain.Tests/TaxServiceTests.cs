using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class TaxServiceTests
    {
        private readonly TaxService _service;

        public TaxServiceTests()
        {
            _service = new TaxService();
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
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenInputVatGreater()
        {
            var request = new VatDeclarationRequest(
                "2026-01",
                new DateTime(2026, 2, 20),
                50000,
                80000,
                "BANK_TRANSFER",
                "BANK001",
                "2026-01"
            );

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenEqual()
        {
            var request = new VatDeclarationRequest(
                "2026-01",
                new DateTime(2026, 2, 20),
                100000,
                100000,
                "BANK_TRANSFER",
                "BANK001",
                "2026-01"
            );

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCitTaxEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CitTaxRequest(
                "2026-01",
                new DateTime(2026, 1, 31),
                1000000,
                0.2m,
                "2026-01"
            );

            var result = _service.CreateCitTaxEntry(request);

            Assert.NotNull(result);
            Assert.Equal(200000, result.Lines[0].DebitAmount);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePitTaxEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PitTaxRequest(
                "2026-01",
                new DateTime(2026, 1, 31),
                150000,
                new DateTime(2026, 2, 15),
                "BANK001",
                "2026-01"
            );

            var result = _service.CreatePitTaxEntry(request);

            Assert.NotNull(result);
            Assert.Equal(150000, result.Lines[0].DebitAmount);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateUnrecoverableVatEntry_ShouldCreateBalancedTransaction_ToExpenseAccount()
        {
            var request = new UnrecoverableVatRequest(
                "INV001",
                new DateTime(2026, 1, 15),
                100000,
                "6411",
                "Hoa don khong hop le",
                "2026-01"
            );

            var result = _service.CreateUnrecoverableVatEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "6411");
            Assert.Contains(result.Lines, l => l.AccountCode == "1331");
        }

        [Fact]
        public void CreateUnrecoverableVatEntry_ShouldCreateBalancedTransaction_ToAdminExpense()
        {
            var request = new UnrecoverableVatRequest(
                "INV002",
                new DateTime(2026, 1, 20),
                50000,
                "6421",
                "Hang khong dung cho SXKD",
                "2026-01"
            );

            var result = _service.CreateUnrecoverableVatEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateDeferredTaxAssetEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DeferredTaxRequest(
                "2026",
                new DateTime(2026, 12, 31),
                50000000,
                "243",
                "2026-12"
            );

            var result = _service.CreateDeferredTaxAssetEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "243");
            Assert.Contains(result.Lines, l => l.AccountCode == "8212");
        }

        [Fact]
        public void CreateDeferredTaxLiabilityEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DeferredTaxRequest(
                "2026",
                new DateTime(2026, 12, 31),
                30000000,
                "347",
                "2026-12"
            );

            var result = _service.CreateDeferredTaxLiabilityEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "8212");
            Assert.Contains(result.Lines, l => l.AccountCode == "347");
        }

        [Fact]
        public void CreateDeferredTaxReversalEntry_ShouldReverseDeferredTaxAsset()
        {
            var request = new DeferredTaxReversalRequest(
                new DateTime(2027, 6, 30),
                20000000,
                "243",
                "Chenh lech giai toa",
                "2027-06"
            );

            var result = _service.CreateDeferredTaxReversalEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFctInvoiceEntry_ShouldCreateBalancedTransaction()
        {
            var request = new FctInvoiceRequest(
                "FCT001",
                new DateTime(2026, 1, 15),
                "0123456789",
                "9876543210",
                1000000,
                0.1m,
                100000,
                "PAID",
                "2026-01"
            );

            var result = _service.CreateFctInvoiceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFctInvoiceEntry_WithMultipleVatRates_ShouldCreateBalancedTransaction()
        {
            var request = new FctInvoiceRequest(
                "FCT002",
                new DateTime(2026, 1, 20),
                "0123456789",
                "9876543210",
                2000000,
                0.05m,
                100000,
                "UNPAID",
                "2026-01"
            );

            var result = _service.CreateFctInvoiceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }
    }
}