using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý Period Locking (Phase 4)
    /// Kiểm soát việc mở/đóng kỳ kế toán theo TT99/2025
    /// </summary>
    /// <remarks>
    /// PL01: Open period - Cho phép ghi bút toán trong kỳ
    /// PL02: Close period - Khóa kỳ, ngăn ghi bổ sung
    /// PL03: Validate period - Kiểm tra trước khi ghi bút toán
    /// </remarks>
    public class PeriodLockingService
    {
        private readonly Dictionary<string, AccountingPeriod> _periods = new();

        /// <summary>
        /// Khởi tạo với kỳ hiện tại
        /// </summary>
        public PeriodLockingService()
        {
            var currentPeriod = new AccountingPeriod
            {
                Code = DateTime.Now.ToString("yyyy-MM"),
                StartDate = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1),
                EndDate = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1).AddMonths(1).AddDays(-1),
                Status = "OPEN",
                IsFiscalYearEnd = false
            };
            _periods[currentPeriod.Code] = currentPeriod;
        }

        /// <summary>
        /// Mở kỳ kế toán cho phép ghi nhận nghiệp vụ
        /// </summary>
        /// <param name="request">Yêu cầu mở kỳ</param>
        /// <returns>Kết quả mở kỳ</returns>
        /// <exception cref="ArgumentNullException">Khi request null</exception>
        /// <exception cref="ArgumentException">Khi định dạng periodId không hợp lệ</exception>
        public PeriodValidationResult OpenPeriod(OpenPeriodRequest request)
        {
            if (_periods.ContainsKey(request.PeriodId))
            {
                var existing = _periods[request.PeriodId];
                if (existing.Status == "OPEN")
                {
                    return new PeriodValidationResult
                    {
                        IsValid = false,
                        Message = $"Period {request.PeriodId} is already open",
                        Status = existing.Status
                    };
                }
            }

            var parts = request.PeriodId.Split('-');
            var year = int.Parse(parts[0]);
            var month = int.Parse(parts[1]);

            var period = new AccountingPeriod
            {
                Code = request.PeriodId,
                StartDate = new DateTime(year, month, 1),
                EndDate = new DateTime(year, month, 1).AddMonths(1).AddDays(-1),
                Status = "OPEN",
                IsFiscalYearEnd = month == 12
            };

            _periods[request.PeriodId] = period;

            return new PeriodValidationResult
            {
                IsValid = true,
                Message = $"Period {request.PeriodId} opened successfully",
                Status = "OPEN"
            };
        }

        /// <summary>
        /// Đóng kỳ kế toán, ngăn ghi bổ sung
        /// </summary>
        /// <param name="request">Yêu cầu đóng kỳ</param>
        /// <returns>Kết quả đóng kỳ</returns>
        /// <remarks>
        /// Chỉ đóng được kỳ đang ở trạng thái OPEN.
        /// Sau khi đóng, không thể ghi bút toán mới vào kỳ này.
        /// </remarks>
        public PeriodValidationResult ClosePeriod(ClosePeriodRequest request)
        {
            if (!_periods.ContainsKey(request.PeriodId))
            {
                return new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} not found",
                    Status = "NOT_FOUND"
                };
            }

            var period = _periods[request.PeriodId];
            
            if (period.Status == "CLOSED")
            {
                return new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} is already closed",
                    Status = "CLOSED"
                };
            }

            if (period.Status != "OPEN")
            {
                return new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} cannot be closed from status {period.Status}",
                    Status = period.Status
                };
            }

            period.Status = "CLOSED";
            _periods[request.PeriodId] = period;

            return new PeriodValidationResult
            {
                IsValid = true,
                Message = $"Period {request.PeriodId} closed successfully. Reason: {request.Reason ?? "N/A"}",
                Status = "CLOSED"
            };
        }

        /// <summary>
        /// PL03: Validate period before posting
        /// </summary>
        public PeriodValidationResult ValidatePeriod(ValidatePeriodRequest request)
        {
            if (!_periods.ContainsKey(request.PeriodId))
            {
                return new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} does not exist. Please create the period first.",
                    Status = "NOT_FOUND"
                };
            }

            var period = _periods[request.PeriodId];

            return period.Status switch
            {
                "OPEN" => new PeriodValidationResult
                {
                    IsValid = true,
                    Message = $"Period {request.PeriodId} is OPEN. Posting allowed.",
                    Status = "OPEN"
                },
                "CLOSED" => new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} is CLOSED. Posting not allowed.",
                    Status = "CLOSED"
                },
                "LOCKED" => new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} is LOCKED. Contact administrator.",
                    Status = "LOCKED"
                },
                _ => new PeriodValidationResult
                {
                    IsValid = false,
                    Message = $"Period {request.PeriodId} has unknown status: {period.Status}",
                    Status = period.Status
                }
            };
        }

        /// <summary>
        /// Get all periods
        /// </summary>
        public List<AccountingPeriod> GetAllPeriods()
        {
            return _periods.Values.ToList();
        }

        /// <summary>
        /// Get period by ID
        /// </summary>
        public AccountingPeriod GetPeriod(string periodId)
        {
            return _periods.ContainsKey(periodId) ? _periods[periodId] : null;
        }
    }
}