using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class InventoryServiceTests
    {
        private readonly InventoryService _service;

        public InventoryServiceTests()
        {
            _service = new InventoryService();
        }

        [Fact]
        public void CreateInventoryReceiptEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryReceiptRequest
            {
                ReceiptDate = new DateTime(2026, 1, 15),
                InventoryAccount = "156",
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                Quantity = 10,
                UnitPriceVnd = 100000,
                VatRate = 0.1m,
                SupplierId = "NCC001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryReceiptEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
            Assert.Contains(result.Lines, l => l.AccountCode == "1331");
        }

        [Fact]
        public void CreateInventoryReceiptEntry_ShouldCreateBalancedTransaction_ForRawMaterial()
        {
            var request = new InventoryReceiptRequest
            {
                ReceiptDate = new DateTime(2026, 1, 20),
                InventoryAccount = "152",
                ProductId = "NVL001",
                ProductName = "Nguyên vật liệu B",
                Quantity = 50,
                UnitPriceVnd = 50000,
                VatRate = 0.1m,
                SupplierId = "NCC002",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryReceiptEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "152");
        }

        [Fact]
        public void CreateInventoryIssueEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryIssueRequest
            {
                IssueDate = new DateTime(2026, 1, 25),
                InventoryAccount = "156",
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                Quantity = 5,
                UnitCostVnd = 100000,
                Reason = "Bán hàng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryIssueEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "632");
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
        }

        [Fact]
        public void CreateInventoryIssueEntry_ShouldCreateBalancedTransaction_ForProduction()
        {
            var request = new InventoryIssueRequest
            {
                IssueDate = new DateTime(2026, 1, 28),
                InventoryAccount = "152",
                ProductId = "NVL001",
                ProductName = "Nguyên vật liệu B",
                Quantity = 20,
                UnitCostVnd = 50000,
                Reason = "Sản xuất",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryIssueEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "621");
        }

        [Fact]
        public void CreateInventoryTransferEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryTransferRequest
            {
                TransferDate = new DateTime(2026, 1, 30),
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                Quantity = 5,
                UnitCostVnd = 100000,
                FromWarehouse = "KHO A",
                ToWarehouse = "KHO B",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryTransferEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInventoryCountEntry_ShouldCreateBalancedTransaction_WhenOver()
        {
            var request = new InventoryCountRequest
            {
                CountDate = new DateTime(2026, 1, 31),
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                BookQuantity = 100,
                ActualQuantity = 105,
                Reason = "Thừa do đếm sai",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryCountEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
        }

        [Fact]
        public void CreateInventoryCountEntry_ShouldCreateBalancedTransaction_WhenUnder()
        {
            var request = new InventoryCountRequest
            {
                CountDate = new DateTime(2026, 1, 31),
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                BookQuantity = 100,
                ActualQuantity = 95,
                Reason = "Thiếu do mất mát",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryCountEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "138");
        }

        [Fact]
        public void CreateInventoryRevaluationEntry_ShouldCreateBalancedTransaction_WhenDecline()
        {
            var request = new InventoryRevaluationRequest
            {
                RevaluationDate = new DateTime(2026, 12, 31),
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                BookValueVnd = 1000000,
                MarketValueVnd = 800000,
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateInventoryRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "632");
            Assert.Contains(result.Lines, l => l.AccountCode == "2294");
        }

        [Fact]
        public void CreateInventoryProvisionEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryProvisionRequest
            {
                ProvisionDate = new DateTime(2026, 12, 31),
                ProvisionAmountVnd = 200000,
                Reason = "Trích lập dự phòng giảm giá hàng tồn kho",
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateInventoryProvisionEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInventoryWriteOffEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryWriteOffRequest
            {
                WriteOffDate = new DateTime(2026, 1, 31),
                ProductId = "SP001",
                ProductName = "Hàng hóa hư hỏng",
                WriteOffQuantity = 10,
                UnitCostVnd = 100000,
                VatRecoverableVnd = 100000,
                Reason = "Hết hạn sử dụng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryWriteOffEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "811");
        }

        [Fact]
        public void CreateInventoryTransferEntry_ShouldNotCreateEntry_WhenZeroQuantity()
        {
            var request = new InventoryTransferRequest
            {
                TransferDate = new DateTime(2026, 1, 30),
                ProductId = "SP001",
                ProductName = "Hàng hóa A",
                Quantity = 0,
                UnitCostVnd = 100000,
                FromWarehouse = "KHO A",
                ToWarehouse = "KHO B",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInventoryTransferEntry(request);

            Assert.NotNull(result);
            Assert.Equal(0, result.Lines.Count);
        }
    }
}