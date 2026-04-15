using System;
using System.Collections.Generic;
using Xunit;
using GL.Domain.Entities;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Tests nghiệp vụ mua hàng - P01-P06
    /// Theo TT99/2025/TT-BTC
    /// </summary>
    public class PurchaseTests
    {
        #region P01 - Mua hàng nhập kho

        [Fact]
        public void P01a_PurchaseWithInvoice_Balanced()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P001",
                TransactionNo = "PO-001",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                SupplierId = "NCC01",
                SupplierName = "Công ty ABC",
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        ProductName = "Hàng hóa A",
                        Quantity = 10,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(1000000m, purchase.SubTotal);
            Assert.Equal(100000m, purchase.VATAmount);
            Assert.Equal(1100000m, purchase.TotalAmount);
        }

        [Fact]
        public void P01a_PurchaseWithInvoice_WithVAT()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P001",
                TransactionNo = "PO-001",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 5,
                        UnitPrice = 200000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(1000000m, purchase.SubTotal);
            Assert.Equal(100000m, purchase.VATAmount);
            Assert.Equal(1100000m, purchase.TotalAmount);
        }

        [Fact]
        public void P01b_PurchaseInvoiceFirst_Track151()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P002",
                TransactionNo = "PO-002",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.TransitGoods,
                Status = PurchaseStatus.InTransit,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP02",
                        Quantity = 20,
                        UnitPrice = 50000,
                        AccountCode = "151"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(PurchaseStatus.InTransit, purchase.Status);
            Assert.Equal("151", purchase.Lines[0].AccountCode);
        }

        [Fact]
        public void P01c_PurchaseGoodsFirst_TempPrice()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P003",
                TransactionNo = "PO-003",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                Status = PurchaseStatus.PendingInvoice,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP03",
                        Quantity = 15,
                        UnitPrice = 80000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(PurchaseStatus.PendingInvoice, purchase.Status);
            Assert.Equal(1200000m, purchase.SubTotal);
        }

        #endregion

        #region P02 - Mua hàng không qua kho

        [Fact]
        public void P02_PurchaseDirectToCost_NoInventory()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P004",
                TransactionNo = "PO-004",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.DirectToCost,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP04",
                        ProductName = "Vật tư tiêu hao",
                        Quantity = 1,
                        UnitPrice = 500000,
                        AccountCode = "621"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(PurchaseType.DirectToCost, purchase.Type);
            Assert.Equal("621", purchase.Lines[0].AccountCode);
            Assert.Equal(550000m, purchase.TotalAmount);
        }

        [Fact]
        public void P02b_ConsignmentPurchase_Track157()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P005",
                TransactionNo = "PO-005",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Consignment,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP05",
                        Quantity = 30,
                        UnitPrice = 30000,
                        AccountCode = "157"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal("157", purchase.Lines[0].AccountCode);
            Assert.Equal(990000m, purchase.TotalAmount);
        }

        #endregion

        #region P03 - Chi phí mua hàng

        [Fact]
        public void P03_PurchaseWithFreight_IncludeInCost()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P006",
                TransactionNo = "PO-006",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                FreightAmount = 100000,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 10,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(1000000m, purchase.SubTotal);
            Assert.Equal(1100000m, purchase.NetAmount);
            Assert.Equal(1210000m, purchase.TotalAmount);
        }

        [Fact]
        public void P03_FreightSmall_ExpenseDirect()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P007",
                TransactionNo = "PO-007",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                FreightAmount = 50000,
                VatRate = 0.10m,
                IsFreightExpensedDirectly = true,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 10,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.True(purchase.IsFreightExpensedDirectly);
            Assert.Equal("641", purchase.FreightAccountCode);
        }

        #endregion

        #region P04 - Chiết khấu TM & Giảm giá

        [Fact]
        public void P04a_TradeDiscount_Applied()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P008",
                TransactionNo = "PO-008",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                VatRate = 0.10m,
                DiscountPercent = 10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 10,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(10m, purchase.DiscountPercent);
            Assert.Equal(100000m, purchase.DiscountAmount);
            Assert.Equal(900000m, purchase.NetAmount);
        }

        [Fact]
        public void P04b_PurchaseDiscount_Applied()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P009",
                TransactionNo = "PO-009",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                VatRate = 0.10m,
                DiscountAmount = 50000,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 5,
                        UnitPrice = 200000,
                        AccountCode = "1561"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(50000m, purchase.DiscountAmount);
            Assert.Equal(950000m, purchase.NetAmount);
            Assert.Equal(1045000m, purchase.TotalAmount);
        }

        #endregion

        #region P05 - Trả lại hàng mua

        [Fact]
        public void P05_PurchaseReturn_ReducePayable()
        {
            var originalPurchase = new PurchaseTransaction
            {
                Id = "P010",
                TransactionNo = "PO-010",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 10,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };
            originalPurchase.CalculateTotals();

            var returnTransaction = new PurchaseTransaction
            {
                Id = "PR001",
                TransactionNo = "PT-001",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Return,
                OriginalPurchaseId = "P010",
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        ProductName = "Hàng hóa A - Trả lại",
                        Quantity = 2,
                        UnitPrice = 100000,
                        AccountCode = "1561"
                    }
                }
            };
            returnTransaction.CalculateTotals();

            Assert.Equal(PurchaseType.Return, returnTransaction.Type);
            Assert.Equal("P010", returnTransaction.OriginalPurchaseId);
            Assert.Equal(-200000m, returnTransaction.SubTotal);
            Assert.Equal(-220000m, returnTransaction.TotalAmount);
        }

        #endregion

        #region P06 - Mua hàng trả góp

        [Fact]
        public void P06_InstallmentPurchase_SplitInterest()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P011",
                TransactionNo = "PO-011",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Installment,
                PrincipalAmount = 10000000m,
                InterestAmount = 1000000m,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP06",
                        ProductName = "Máy móc trả góp",
                        Quantity = 1,
                        UnitPrice = 10000000m,
                        AccountCode = "211"
                    }
                }
            };

            purchase.CalculateTotals();

            Assert.Equal(PurchaseType.Installment, purchase.Type);
            Assert.Equal(10000000m, purchase.PrincipalAmount);
            Assert.Equal(1000000m, purchase.InterestAmount);
            Assert.Equal(12000000m, purchase.TotalAmount);
        }

        #endregion

        #region Journal Entry Validation

        [Fact]
        public void P01_JournalEntry_DebitEqualsCredit()
        {
            var purchase = new PurchaseTransaction
            {
                Id = "P012",
                TransactionNo = "PO-012",
                TransactionDate = DateTime.Today,
                Type = PurchaseType.Inventory,
                PaymentMethod = PaymentMethod.Cash,
                VatRate = 0.10m,
                Lines = new List<PurchaseLine>
                {
                    new PurchaseLine
                    {
                        ProductId = "SP01",
                        Quantity = 5,
                        UnitPrice = 100000,
                        AccountCode = "1561",
                        Debit = 500000
                    }
                }
            };
            purchase.CalculateTotals();

            var totalDebit = purchase.Lines.Sum(l => l.Debit) + purchase.VATAmount;
            var totalCredit = purchase.TotalAmount;

            Assert.Equal(totalDebit, totalCredit);
        }

        #endregion
    }
}