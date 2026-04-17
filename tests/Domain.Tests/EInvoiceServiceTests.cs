using GL.Application.Services;
using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class EInvoiceServiceTests
    {
        private readonly EInvoiceService _service;

        public EInvoiceServiceTests()
        {
            _service = new EInvoiceService();
        }

        [Fact]
        public void CreateInvoice_ShouldGenerateInvoiceNumber()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                BuyerTaxCode = "9876543210",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 10, UnitPrice = 110000, VATRate = 10 }
                }
            });

            Assert.NotNull(invoice);
            Assert.NotNull(invoice.InvoiceNumber);
        }

        [Fact]
        public void CreateInvoice_ShouldCalculateTotalAmount()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 10, UnitPrice = 100000, VATRate = 10 }
                }
            });

            Assert.Equal(1100000m, invoice.TotalAmount);
            Assert.Equal(100000m, invoice.VATAmount);
        }

        [Fact]
        public void CreateInvoice_ShouldGenerateXML()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 110000, VATRate = 10 }
                }
            });

            var xml = _service.GenerateXML(invoice);

            Assert.NotNull(xml);
            Assert.Contains("Invoice", xml);
        }

        [Fact]
        public void SignInvoice_ShouldAddSignature()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 110000, VATRate = 10 }
                }
            });

            var signed = _service.SignInvoice(invoice, "pin");

            Assert.True(signed.IsSigned);
        }

        [Fact]
        public void CancelInvoice_ShouldUpdateStatus()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 110000, VATRate = 10 }
                }
            });

            var result = _service.CancelInvoice(invoice.InvoiceNumber, "Ly do huy");

            Assert.True(result.Success);
        }

        [Fact]
        public void AdjustInvoice_ShouldCreateAdjustmentInvoice()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 100000, VATRate = 10 }
                }
            });

            var adjusted = _service.AdjustInvoice(invoice.InvoiceNumber, -10000m, "DECREASE", "Sai don gia");

            Assert.NotNull(adjusted);
            Assert.Equal("ADJUSTMENT", adjusted.Status);
        }

        [Fact]
        public void ReplaceInvoice_ShouldCreateReplacementInvoice()
        {
            var invoice = _service.CreateInvoice(new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 100000, VATRate = 10 }
                }
            });

            var newRequest = new EInvoiceCreateRequest
            {
                InvoiceType = "01GTKT",
                SellerTaxCode = "0123456789",
                BuyerTaxCode = "9876543210",
                Items = new[]
                {
                    new EInvoiceItem { ItemName = "San pham A", Quantity = 1, UnitPrice = 110000, VATRate = 10 }
                }
            };

            var replaced = _service.ReplaceInvoice(invoice.InvoiceNumber, newRequest);

            Assert.NotNull(replaced);
            Assert.Equal("REPLACED", replaced.Status);
        }

        [Fact]
        public void GenerateAdjustmentMinutes_ShouldCreateMinutes()
        {
            var minutes = _service.GenerateAdjustmentMinutes("2601", "Cong ty XYZ", "Cong ty ABC", "Sai don gia", "Dieu chinh giam 10.000");

            Assert.NotNull(minutes);
            Assert.Contains("BIÊN BẢN ĐIỀU CHỈNH", minutes);
            Assert.Contains("2601", minutes);
        }
    }
}