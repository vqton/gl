using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý Audit Trail (Phase 4)
    /// Theo dõi tất cả các thay đổi trong hệ thống theo TT99/2025 Điều 18
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
            return _auditEntries.Where(e => e.ActionType == actionType).ToList();
        }

        /// <summary>
        /// AT01: Log transaction entry (TT99/2025 Article 18)
        /// </summary>
        public AuditLogResult LogTransaction(CreateAuditLogRequest request)
        {
            var result = new AuditLogResult
            {
                Id = Guid.NewGuid(),
                UserId = request.UserId,
                Timestamp = DateTime.Now,
                Action = request.Action,
                TableName = request.TableName,
                RecordId = request.RecordId,
                OldValues = request.OldValues,
                NewValues = request.NewValues,
                IpAddress = request.IpAddress,
            };

            var entry = new AuditEntry
            {
                Id = result.Id.ToString(),
                TransactionId = request.RecordId,
                ActionType = request.Action,
                ActionDate = result.Timestamp,
                UserId = request.UserId,
                OldValue = request.OldValues,
                NewValue = request.NewValues,
                Description = $"Audit: {request.Action} on {request.TableName}",
            };
            _auditEntries.Add(entry);

            return result;
        }

        /// <summary>
        /// AT02: Query audit history
        /// </summary>
        public List<AuditLogResult> QueryAuditHistory(QueryAuditRequest request)
        {
            var query = _auditEntries.AsEnumerable();

            if (!string.IsNullOrEmpty(request.RecordId))
            {
                query = query.Where(e => e.TransactionId == request.RecordId);
            }

            if (!string.IsNullOrEmpty(request.UserId))
            {
                query = query.Where(e => e.UserId == request.UserId);
            }

            if (!string.IsNullOrEmpty(request.TableName))
            {
                query = query.Where(e => e.Description.Contains(request.TableName));
            }

            if (request.StartDate.HasValue)
            {
                query = query.Where(e => e.ActionDate >= request.StartDate.Value);
            }

            if (request.EndDate.HasValue)
            {
                query = query.Where(e => e.ActionDate <= request.EndDate.Value);
            }

            return query.Select(e => new AuditLogResult
            {
                Id = Guid.Parse(e.Id),
                UserId = e.UserId,
                Timestamp = e.ActionDate,
                Action = e.ActionType,
                RecordId = e.TransactionId,
                OldValues = e.OldValue,
                NewValues = e.NewValue,
            }).ToList();
        }

        /// <summary>
        /// AT03: Generate audit report for period
        /// </summary>
        public AuditReportResult GenerateAuditReport(string periodId)
        {
            var entries = _auditEntries.Where(e => 
                e.ActionDate.Month.ToString() == periodId.Split('-')[1] &&
                e.ActionDate.Year.ToString() == periodId.Split('-')[0]
            ).ToList();

            return new AuditReportResult
            {
                PeriodId = periodId,
                GeneratedAt = DateTime.Now,
                TotalEntries = entries.Count,
                Entries = entries.Select(e => new AuditLogResult
                {
                    Id = Guid.Parse(e.Id),
                    UserId = e.UserId,
                    Timestamp = e.ActionDate,
                    Action = e.ActionType,
                    RecordId = e.TransactionId,
                    OldValues = e.OldValue,
                    NewValues = e.NewValue,
                }).ToList(),
            };
        }
    }
}
