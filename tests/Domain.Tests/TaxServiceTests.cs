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
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenInputVatGreater()
        {
            var request = new VatDeclarationRequest
            {
                DeclarationPeriodId = "2026-01",
                DeclarationDate = new DateTime(2026, 2, 20),
                OutputVatTotal = 50000,
                InputVatTotal = 80000,
                PaymentMethod = "BANK_TRANSFER",
                BankAccountId = "BANK001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateVatDeclarationEntry_ShouldCreateBalancedTransaction_WhenEqual()
        {
            var request = new VatDeclarationRequest
            {
                DeclarationPeriodId = "2026-01",
                DeclarationDate = new DateTime(2026, 2, 20),
                OutputVatTotal = 100000,
                InputVatTotal = 100000,
                PaymentMethod = "BANK_TRANSFER",
                BankAccountId = "BANK001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateVatDeclarationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCitTaxEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CitTaxRequest
            {
                TaxPeriodId = "2026-01",
                CalculationDate = new DateTime(2026, 1, 31),
                TaxableIncomeVnd = 1000000,
                CitRate = 0.2m,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCitTaxEntry(request);

            Assert.NotNull(result);
            Assert.Equal(200000, result.Lines[0].DebitAmount);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePitTaxEntry_ShouldCreateBalancedTransaction()
        {
            var request = new PitTaxRequest
            {
                PayrollPeriodId = "2026-01",
                WithholdingDate = new DateTime(2026, 1, 31),
                TotalPitWithheldVnd = 150000,
                PaymentDate = new DateTime(2026, 2, 15),
                BankAccountId = "BANK001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePitTaxEntry(request);

            Assert.NotNull(result);
            Assert.Equal(150000, result.Lines[0].DebitAmount);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateUnrecoverableVatEntry_ShouldCreateBalancedTransaction_ToExpenseAccount()
        {
            var request = new UnrecoverableVatRequest
            {
                InvoiceId = "INV001",
                RecognitionDate = new DateTime(2026, 1, 15),
                VatAmountVnd = 100000,
                ExpenseAccountCode = "6411",
                Reason = "Hoa don khong hop le",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateUnrecoverableVatEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "6411");
            Assert.Contains(result.Lines, l => l.AccountCode == "1331");
        }

        [Fact]
        public void CreateUnrecoverableVatEntry_ShouldCreateBalancedTransaction_ToAdminExpense()
        {
            var request = new UnrecoverableVatRequest
            {
                InvoiceId = "INV002",
                RecognitionDate = new DateTime(2026, 1, 20),
                VatAmountVnd = 50000,
                ExpenseAccountCode = "6421",
                Reason = "Hang khong dung cho SXKD",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateUnrecoverableVatEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateDeferredTaxAssetEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DeferredTaxRequest
            {
                FiscalYearId = "2026",
                RecognitionDate = new DateTime(2026, 12, 31),
                DeferredTaxAssetVnd = 50000000,
                TaxCode = "243",
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateDeferredTaxAssetEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "243");
            Assert.Contains(result.Lines, l => l.AccountCode == "8212");
        }

        [Fact]
        public void CreateDeferredTaxLiabilityEntry_ShouldCreateBalancedTransaction()
        {
            var request = new DeferredTaxRequest
            {
                FiscalYearId = "2026",
                RecognitionDate = new DateTime(2026, 12, 31),
                DeferredTaxAssetVnd = 30000000,
                TaxCode = "347",
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateDeferredTaxLiabilityEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "8212");
            Assert.Contains(result.Lines, l => l.AccountCode == "347");
        }

        [Fact]
        public void CreateDeferredTaxReversalEntry_ShouldReverseDeferredTaxAsset()
        {
            var request = new DeferredTaxReversalRequest
            {
                ReversalDate = new DateTime(2027, 6, 30),
                ReversalAmountVnd = 20000000,
                OriginalDeferredTaxCode = "243",
                Reason = "Chenh lech giai toa",
                AccountingPeriodId = "2027-06"
            };

            var result = _service.CreateDeferredTaxReversalEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFctInvoiceEntry_ShouldCreateBalancedTransaction()
        {
            var request = new FctInvoiceRequest
            {
                InvoiceId = "FCT001",
                InvoiceDate = new DateTime(2026, 1, 15),
                SellerTaxCode = "0123456789",
                BuyerTaxCode = "9876543210",
                TotalBeforeVatVnd = 1000000,
                VatRate = 0.1m,
                VatAmountVnd = 100000,
                PaymentStatus = "PAID",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFctInvoiceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateFctInvoiceEntry_WithMultipleVatRates_ShouldCreateBalancedTransaction()
        {
            var request = new FctInvoiceRequest
            {
                InvoiceId = "FCT002",
                InvoiceDate = new DateTime(2026, 1, 20),
                SellerTaxCode = "0123456789",
                BuyerTaxCode = "9876543210",
                TotalBeforeVatVnd = 2000000,
                VatRate = 0.05m,
                VatAmountVnd = 100000,
                PaymentStatus = "UNPAID",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateFctInvoiceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }
    }
}