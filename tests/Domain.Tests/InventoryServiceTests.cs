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
            var request = new InventoryReceiptRequest(
                new DateTime(2026, 1, 15),
                "156",
                "SP001",
                "Hàng hóa A",
                10,
                100000,
                0.1m,
                "NCC001",
                "2026-01"
            );

            var result = _service.CreateInventoryReceiptEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
            Assert.Contains(result.Lines, l => l.AccountCode == "1331");
        }

        [Fact]
        public void CreateInventoryReceiptEntry_ShouldCreateBalancedTransaction_ForRawMaterial()
        {
            var request = new InventoryReceiptRequest(
                new DateTime(2026, 1, 20),
                "152",
                "NVL001",
                "Nguyên vật liệu B",
                50,
                50000,
                0.1m,
                "NCC002",
                "2026-01"
            );

            var result = _service.CreateInventoryReceiptEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "152");
        }

        [Fact]
        public void CreateInventoryIssueEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryIssueRequest(
                new DateTime(2026, 1, 25),
                "156",
                "SP001",
                "Hàng hóa A",
                5,
                100000,
                "Bán hàng",
                "2026-01"
            );

            var result = _service.CreateInventoryIssueEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "632");
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
        }

        [Fact]
        public void CreateInventoryIssueEntry_ShouldCreateBalancedTransaction_ForProduction()
        {
            var request = new InventoryIssueRequest(
                new DateTime(2026, 1, 28),
                "152",
                "NVL001",
                "Nguyên vật liệu B",
                20,
                50000,
                "Sản xuất",
                "2026-01"
            );

            var result = _service.CreateInventoryIssueEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "621");
        }

        [Fact]
        public void CreateInventoryTransferEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryTransferRequest(
                new DateTime(2026, 1, 30),
                "SP001",
                "Hàng hóa A",
                5,
                100000,
                "KHO A",
                "KHO B",
                "2026-01"
            );

            var result = _service.CreateInventoryTransferEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInventoryCountEntry_ShouldCreateBalancedTransaction_WhenOver()
        {
            var request = new InventoryCountRequest(
                new DateTime(2026, 1, 31),
                "SP001",
                "Hàng hóa A",
                100,
                105,
                "Thừa do đếm sai",
                "2026-01"
            );

            var result = _service.CreateInventoryCountEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "156");
        }

        [Fact]
        public void CreateInventoryCountEntry_ShouldCreateBalancedTransaction_WhenUnder()
        {
            var request = new InventoryCountRequest(
                new DateTime(2026, 1, 31),
                "SP001",
                "Hàng hóa A",
                100,
                95,
                "Thiếu do mất mát",
                "2026-01"
            );

            var result = _service.CreateInventoryCountEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "138");
        }

        [Fact]
        public void CreateInventoryRevaluationEntry_ShouldCreateBalancedTransaction_WhenDecline()
        {
            var request = new InventoryRevaluationRequest(
                new DateTime(2026, 12, 31),
                "SP001",
                "Hàng hóa A",
                1000000,
                800000,
                "2026-12"
            );

            var result = _service.CreateInventoryRevaluationEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "632");
            Assert.Contains(result.Lines, l => l.AccountCode == "2294");
        }

        [Fact]
        public void CreateInventoryProvisionEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryProvisionRequest(
                new DateTime(2026, 12, 31),
                200000,
                "Trích lập dự phòng giảm giá hàng tồn kho",
                "2026-12"
            );

            var result = _service.CreateInventoryProvisionEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInventoryWriteOffEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InventoryWriteOffRequest(
                new DateTime(2026, 1, 31),
                "SP001",
                "Hàng hóa hư hỏng",
                10,
                100000,
                100000,
                "Hết hạn sử dụng",
                "2026-01"
            );

            var result = _service.CreateInventoryWriteOffEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "811");
        }

        [Fact]
        public void CreateInventoryTransferEntry_ShouldNotCreateEntry_WhenZeroQuantity()
        {
            var request = new InventoryTransferRequest(
                new DateTime(2026, 1, 30),
                "SP001",
                "Hàng hóa A",
                0,
                100000,
                "KHO A",
                "KHO B",
                "2026-01"
            );

            var result = _service.CreateInventoryTransferEntry(request);

            Assert.NotNull(result);
            Assert.Equal(0, result.Lines.Count);
        }
    }
}