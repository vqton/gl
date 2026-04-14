using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class AuditTrailServiceTests
    {
        private readonly AuditTrailService _service;

        public AuditTrailServiceTests()
        {
            _service = new AuditTrailService();
        }

        [Fact]
        public void LogCreate_ShouldAddEntry()
        {
            _service.LogCreate("TXN001", "111", 1000000, "USER001", "Tạo bút toán");

            var entries = _service.GetAllEntries();

            Assert.Single(entries);
            Assert.Equal("CREATE", entries[0].ActionType);
        }

        [Fact]
        public void LogUpdate_ShouldAddEntry()
        {
            _service.LogUpdate("TXN001", "111", "1000000", "1500000", "USER001", "Cập nhật số tiền");

            var entries = _service.GetAllEntries();

            Assert.Single(entries);
            Assert.Equal("UPDATE", entries[0].ActionType);
            Assert.Equal("1000000", entries[0].OldValue);
            Assert.Equal("1500000", entries[0].NewValue);
        }

        [Fact]
        public void LogDelete_ShouldAddEntry()
        {
            _service.LogDelete("TXN001", "USER001", "Xóa bút toán");

            var entries = _service.GetAllEntries();

            Assert.Single(entries);
            Assert.Equal("DELETE", entries[0].ActionType);
        }

        [Fact]
        public void LogPost_ShouldAddMultipleEntries_ForEachTransactionLine()
        {
            var transaction = new Transaction
            {
                Id = "TXN001",
                Date = DateTime.Now,
                Description = "Test transaction"
            };
            transaction.AddLine("111", 1000000, 0, "Debit");
            transaction.AddLine("331", 0, 1000000, "Credit");

            _service.LogPost(transaction, "USER001");

            var entries = _service.GetAllEntries();

            Assert.Equal(2, entries.Count);
            Assert.All(entries, e => Assert.Equal("POST", e.ActionType));
        }

        [Fact]
        public void GetEntriesByTransactionId_ShouldReturnMatchingEntries()
        {
            _service.LogCreate("TXN001", "111", 1000000, "USER001");
            _service.LogCreate("TXN002", "112", 500000, "USER001");
            _service.LogCreate("TXN001", "331", 1000000, "USER001");

            var entries = _service.GetEntriesByTransactionId("TXN001");

            Assert.Equal(2, entries.Count);
        }

        [Fact]
        public void GetEntriesByUserId_ShouldReturnMatchingEntries()
        {
            _service.LogCreate("TXN001", "111", 1000000, "USER001");
            _service.LogCreate("TXN002", "112", 500000, "USER002");

            var entries = _service.GetEntriesByUserId("USER001");

            Assert.Single(entries);
        }

        [Fact]
        public void GetEntriesByDateRange_ShouldReturnMatchingEntries()
        {
            var now = DateTime.Now;
            _service.LogCreate("TXN001", "111", 1000000, "USER001");

            var entries = _service.GetEntriesByDateRange(now.AddMinutes(-1), now.AddMinutes(1));

            Assert.Single(entries);
        }

        [Fact]
        public void GetEntriesByActionType_ShouldReturnMatchingEntries()
        {
            _service.LogCreate("TXN001", "111", 1000000, "USER001");
            _service.LogDelete("TXN002", "USER001");

            var entries = _service.GetEntriesByActionType("CREATE");

            Assert.Single(entries);
        }
    }
}
