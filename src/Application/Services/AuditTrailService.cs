using GL.Domain.Entities;
using System;
using System.Collections.Generic;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý Audit Trail (Phase 3)
    /// Theo dõi tất cả các thay đổi trong hệ thống
    /// </summary>
    public class AuditTrailService
    {
        private readonly List<AuditEntry> _auditEntries = new List<AuditEntry>();

        /// <summary>
        /// Ghi lại hành động tạo mới
        /// </summary>
        public void LogCreate(string transactionId, string accountCode, decimal amount, string userId, string description = "")
        {
            var entry = new AuditEntry
            {
                Id = Guid.NewGuid().ToString(),
                TransactionId = transactionId,
                ActionType = "CREATE",
                AccountCode = accountCode,
                Amount = amount,
                ActionDate = DateTime.Now,
                UserId = userId,
                Description = description
            };
            _auditEntries.Add(entry);
        }

        /// <summary>
        /// Ghi lại hành động cập nhật
        /// </summary>
        public void LogUpdate(string transactionId, string accountCode, string oldValue, string newValue, string userId, string description = "")
        {
            var entry = new AuditEntry
            {
                Id = Guid.NewGuid().ToString(),
                TransactionId = transactionId,
                ActionType = "UPDATE",
                AccountCode = accountCode,
                OldValue = oldValue,
                NewValue = newValue,
                ActionDate = DateTime.Now,
                UserId = userId,
                Description = description
            };
            _auditEntries.Add(entry);
        }

        /// <summary>
        /// Ghi lại hành động xóa
        /// </summary>
        public void LogDelete(string transactionId, string userId, string description = "")
        {
            var entry = new AuditEntry
            {
                Id = Guid.NewGuid().ToString(),
                TransactionId = transactionId,
                ActionType = "DELETE",
                ActionDate = DateTime.Now,
                UserId = userId,
                Description = description
            };
            _auditEntries.Add(entry);
        }

        /// <summary>
        /// Ghi lại hành động hạch toán bút toán
        /// </summary>
        public void LogPost(Transaction transaction, string userId)
        {
            foreach (var line in transaction.Lines)
            {
                var entry = new AuditEntry
                {
                    Id = Guid.NewGuid().ToString(),
                    TransactionId = transaction.Id,
                    ActionType = "POST",
                    AccountCode = line.AccountCode,
                    Amount = line.DebitAmount > 0 ? line.DebitAmount : line.CreditAmount,
                    ActionDate = DateTime.Now,
                    UserId = userId,
                    Description = $"Hạch toán bút toán: {transaction.Description}"
                };
                _auditEntries.Add(entry);
            }
        }

        /// <summary>
        /// Ghi lại hành động bỏ hạch toán
        /// </summary>
        public void LogUnpost(Transaction transaction, string userId)
        {
            foreach (var line in transaction.Lines)
            {
                var entry = new AuditEntry
                {
                    Id = Guid.NewGuid().ToString(),
                    TransactionId = transaction.Id,
                    ActionType = "UNPOST",
                    AccountCode = line.AccountCode,
                    Amount = line.DebitAmount > 0 ? line.DebitAmount : line.CreditAmount,
                    ActionDate = DateTime.Now,
                    UserId = userId,
                    Description = $"Bỏ hạch toán bút toán: {transaction.Description}"
                };
                _auditEntries.Add(entry);
            }
        }

        /// <summary>
        /// Lấy tất cả các bản ghi audit
        /// </summary>
        public List<AuditEntry> GetAllEntries()
        {
            return new List<AuditEntry>(_auditEntries);
        }

        /// <summary>
        /// Lấy các bản ghi audit theo mã giao dịch
        /// </summary>
        public List<AuditEntry> GetEntriesByTransactionId(string transactionId)
        {
            var results = new List<AuditEntry>();
            foreach (var entry in _auditEntries)
            {
                if (entry.TransactionId == transactionId)
                    results.Add(entry);
            }
            return results;
        }

        /// <summary>
        /// Lấy các bản ghi audit theo người dùng
        /// </summary>
        public List<AuditEntry> GetEntriesByUserId(string userId)
        {
            var results = new List<AuditEntry>();
            foreach (var entry in _auditEntries)
            {
                if (entry.UserId == userId)
                    results.Add(entry);
            }
            return results;
        }

        /// <summary>
        /// Lấy các bản ghi audit trong khoảng thời gian
        /// </summary>
        public List<AuditEntry> GetEntriesByDateRange(DateTime startDate, DateTime endDate)
        {
            var results = new List<AuditEntry>();
            foreach (var entry in _auditEntries)
            {
                if (entry.ActionDate >= startDate && entry.ActionDate <= endDate)
                    results.Add(entry);
            }
            return results;
        }

        /// <summary>
        /// Lấy các bản ghi audit theo loại hành động
        /// </summary>
        public List<AuditEntry> GetEntriesByActionType(string actionType)
        {
            var results = new List<AuditEntry>();
            foreach (var entry in _auditEntries)
            {
                if (entry.ActionType == actionType)
                    results.Add(entry);
            }
            return results;
        }
    }
}
