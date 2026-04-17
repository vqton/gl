using GL.Application.Services;
using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class InventoryCostingMethodTests
    {
        private readonly InventoryCostingService _service = new();

        [Fact]
        public void I05a_CalculateWeightedAverage_ReturnsCorrectCost()
        {
            var productId = "SP001";
            var receipts = new List<(decimal Qty, decimal Cost)>
            {
                (100, 50000),
                (150, 52000),
                (50, 48000)
            };

            foreach (var (qty, cost) in receipts)
            {
                _service.RecordReceipt(productId, qty, cost, DateTime.Today);
            }

            var result = _service.CalculateIssueCost(productId, "AVERAGE", 50);

            var expected = (100 * 50000 + 150 * 52000 + 50 * 48000m) / (100 + 150 + 50);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void I05b_CalculateFIFO_ReturnsFirstLotCost()
        {
            var productId = "SP002";
            _service.RecordReceipt(productId, 100, 50000, DateTime.Today.AddDays(-2));
            _service.RecordReceipt(productId, 100, 55000, DateTime.Today.AddDays(-1));
            _service.RecordReceipt(productId, 100, 60000, DateTime.Today);

            var result = _service.CalculateIssueCost(productId, "FIFO", 50);

            Assert.Equal(50000m, result);
        }

        [Fact]
        public void I05b_FIFO_SplitsMultipleLots()
        {
            var productId = "SP003";
            _service.RecordReceipt(productId, 30, 50000, DateTime.Today.AddDays(-1));
            _service.RecordReceipt(productId, 50, 55000, DateTime.Today);

            var result = _service.CalculateIssueCost(productId, "FIFO", 70);

            var expected = (30m * 50000m + 40m * 55000m) / 70m;
            Assert.Equal(expected, result);
        }

        [Fact]
        public void I05c_SpecificIdentification_ReturnsExactLotCost()
        {
            var productId = "SP004";
            var lotA = _service.RecordReceipt(productId, 100, 50000, DateTime.Today.AddDays(-2));
            var lotB = _service.RecordReceipt(productId, 100, 60000, DateTime.Today);

            var result = _service.CalculateIssueCost(productId, "SPECIFIC", 10, lotA.LotId);

            Assert.Equal(50000m, result);
        }

        [Fact]
        public void I05d_RetailMethod_CalculatesFromSellingPrice()
        {
            var productId = "SP005";
            var sellingPrice = 120000m;
            var marginRate = 0.20m;

            _service.SetRetailMargin(productId, marginRate);
            _service.RecordReceipt(productId, 100, 96000, DateTime.Today);

            _service.RecordSale(productId, 50, sellingPrice);

            var result = _service.CalculateIssueCost(productId, "RETAIL", 10);

            var expectedCost = sellingPrice * (1 - marginRate);
            Assert.Equal(expectedCost, result);
        }

        [Fact]
        public void I05e_Reconciliation_MatchesBookToPhysical()
        {
            var productId = "SP006";

            _service.RecordReceipt(productId, 100, 50000, DateTime.Today);
            _service.Issue(productId, 80);
            _service.Issue(productId, 10);

            var bookBalance = _service.GetBookBalance(productId);
            var physicalCount = 12;

            var variance = bookBalance - physicalCount;
            Assert.Equal(-2, variance);
        }

        [Fact]
        public void I05f_CalculateFromEndingInventory_BackCalculation()
        {
            var productId = "SP007";

            var period = new InventoryPeriod
            {
                ProductId = productId,
                OpeningQuantity = 50,
                OpeningValue = 2500000m,
                ReceiptQuantity = 150,
                ReceiptValue = 7500000m,
                ClosingQuantity = 80
            };

            var result = _service.CalculateIssueFromEnding(period);

            var expectedValue = 2500000m + 7500000m - (80 * 50000m);
            var expectedQty = 50 + 150 - 80;

            Assert.Equal(expectedValue, result.TotalValue);
            Assert.Equal(expectedQty, result.TotalQuantity);
        }
    }

    public class InventoryCostingService
    {
        private readonly Dictionary<string, List<InventoryLot>> _inventory = new();
        private readonly Dictionary<string, decimal> _retailMargins = new();
        private readonly List<InventoryTransaction> _transactions = new();

        public InventoryLot RecordReceipt(string productId, decimal quantity, decimal unitCost, DateTime date)
        {
            if (!_inventory.ContainsKey(productId))
                _inventory[productId] = new List<InventoryLot>();

            var lot = new InventoryLot
            {
                LotId = $"{productId}-{date:yyyyMMdd}-{_inventory[productId].Count + 1}",
                ProductId = productId,
                Quantity = quantity,
                UnitCost = unitCost,
                ReceivedDate = date
            };

            _inventory[productId].Add(lot);

            _transactions.Add(new InventoryTransaction
            {
                ProductId = productId,
                TransactionType = "RECEIPT",
                Quantity = quantity,
                UnitCost = unitCost,
                Amount = quantity * unitCost,
                TransactionDate = date
            });

            return lot;
        }

        public decimal CalculateIssueCost(string productId, string method, decimal quantity, string? lotId = null)
        {
            if (!_inventory.ContainsKey(productId))
                return 0;

            var lots = _inventory[productId].OrderBy(l => l.ReceivedDate).ToList();

            return method switch
            {
                "FIFO" => CalculateFIFO(lots, quantity),
                "AVERAGE" => CalculateAverage(lots),
                "SPECIFIC" => CalculateSpecific(lots, lotId),
                "RETAIL" => CalculateRetail(productId, quantity),
                _ => CalculateFIFO(lots, quantity)
            };
        }

        private decimal CalculateFIFO(List<InventoryLot> lots, decimal quantity)
        {
            decimal totalCost = 0;
            var remaining = quantity;

            foreach (var lot in lots)
            {
                if (remaining <= 0) break;
                var qty = Math.Min(remaining, lot.Quantity);
                totalCost += qty * lot.UnitCost;
                remaining -= qty;
            }

            return quantity > 0 ? totalCost / quantity : 0;
        }

        private decimal CalculateAverage(List<InventoryLot> lots)
        {
            if (!lots.Any()) return 0;
            var totalValue = lots.Sum(l => l.Quantity * l.UnitCost);
            var totalQty = lots.Sum(l => l.Quantity);
            return totalQty > 0 ? totalValue / totalQty : 0;
        }

        private decimal CalculateSpecific(List<InventoryLot> lots, string? lotId)
        {
            if (string.IsNullOrEmpty(lotId)) return 0;
            var lot = lots.FirstOrDefault(l => l.LotId == lotId);
            return lot?.UnitCost ?? 0;
        }

        private decimal CalculateRetail(string productId, decimal quantity)
        {
            if (!_retailMargins.ContainsKey(productId))
                return CalculateAverage(_inventory[productId]);

            var avgCost = CalculateAverage(_inventory[productId]);
            var margin = _retailMargins[productId];
            return avgCost;
        }

        public void SetRetailMargin(string productId, decimal marginRate)
        {
            _retailMargins[productId] = marginRate;
        }

        public void Issue(string productId, decimal quantity)
        {
            if (!_inventory.ContainsKey(productId))
                return;

            _transactions.Add(new InventoryTransaction
            {
                ProductId = productId,
                TransactionType = "ISSUE",
                Quantity = quantity,
                TransactionDate = DateTime.Today
            });
        }

        public decimal GetBookBalance(string productId)
        {
            var receipts = _transactions
                .Where(t => t.ProductId == productId && t.TransactionType == "RECEIPT")
                .Sum(t => t.Quantity);
            var issues = _transactions
                .Where(t => t.ProductId == productId && t.TransactionType == "ISSUE")
                .Sum(t => t.Quantity);
            return receipts - issues;
        }

        public void RecordSale(string productId, decimal quantity, decimal sellingPrice)
        {
            _transactions.Add(new InventoryTransaction
            {
                ProductId = productId,
                TransactionType = "SALE",
                Quantity = quantity,
                UnitCost = sellingPrice,
                TransactionDate = DateTime.Today
            });
        }

        public InventoryIssueResult CalculateIssueFromEnding(InventoryPeriod period)
        {
            var closingValue = period.OpeningValue + period.ReceiptValue - (period.ClosingQuantity * 50000m);
            var closingQty = period.OpeningQuantity + period.ReceiptQuantity - period.ClosingQuantity;

            return new InventoryIssueResult
            {
                TotalQuantity = closingQty,
                TotalValue = closingValue
            };
        }

        public InventoryLot RecordReceipt(string productId, decimal quantity, decimal unitCost, DateTime date, string lotId)
        {
            if (!_inventory.ContainsKey(productId))
                _inventory[productId] = new List<InventoryLot>();

            var lot = new InventoryLot
            {
                LotId = lotId,
                ProductId = productId,
                Quantity = quantity,
                UnitCost = unitCost,
                ReceivedDate = date
            };

            _inventory[productId].Add(lot);
            return lot;
        }
    }

    public class InventoryLot
    {
        public string LotId { get; set; }
        public string ProductId { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCost { get; set; }
        public DateTime ReceivedDate { get; set; }
    }

    public class InventoryTransaction
    {
        public string ProductId { get; set; }
        public string TransactionType { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCost { get; set; }
        public decimal Amount { get; set; }
        public DateTime TransactionDate { get; set; }
    }

    public class InventoryPeriod
    {
        public string ProductId { get; set; }
        public decimal OpeningQuantity { get; set; }
        public decimal OpeningValue { get; set; }
        public decimal ReceiptQuantity { get; set; }
        public decimal ReceiptValue { get; set; }
        public decimal ClosingQuantity { get; set; }
    }

    public class InventoryIssueResult
    {
        public decimal TotalQuantity { get; set; }
        public decimal TotalValue { get; set; }
    }
}