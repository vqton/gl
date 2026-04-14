using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tính lương làm thêm giờ (tăng ca)
    /// Theo Bộ luật Lao động 2019, Điều 104
    /// </summary>
    public class OvertimeCalculationService
    {
        // Hệ số tính lương tăng ca
        public const decimal Rate_NormalDay = 1.5m;           // Ngày thường: 150%
        public const decimal Rate_WeeklyDayOff = 2.0m;        // Ngày nghỉ hàng tuần: 200%
        public const decimal Rate_Holiday = 3.0m;             // Ngày lễ, Tết: 300%
        public const decimal Rate_PaidDayOff = 2.0m;          // Ngày nghỉ có lương: 200%

        // Số giờ làm việc chuẩn
        public const int StandardWorkingHoursPerDay = 8;
        public const int StandardWorkingDaysPerMonth = 22;

        /// <summary>
        /// Tính hệ số tăng ca theo loại ngày
        /// </summary>
        public decimal GetRate(OvertimeType type)
        {
            return type switch
            {
                OvertimeType.NormalDay => Rate_NormalDay,
                OvertimeType.WeeklyDayOff => Rate_WeeklyDayOff,
                OvertimeType.Holiday => Rate_Holiday,
                OvertimeType.PaidDayOff => Rate_PaidDayOff,
                _ => Rate_NormalDay
            };
        }

        /// <summary>
        /// Tính lương giờ từ lương tháng
        /// </summary>
        public decimal CalculateHourlyRate(decimal monthlySalary)
        {
            return monthlySalary / (StandardWorkingDaysPerMonth * StandardWorkingHoursPerDay);
        }

        /// <summary>
        /// Tính số tiền tăng ca cho một bản ghi
        /// </summary>
        public decimal CalculateOvertimeAmount(OvertimeRecord record, decimal monthlySalary)
        {
            if (!record.IsValid())
                return 0;

            decimal hourlyRate = CalculateHourlyRate(monthlySalary);
            decimal rate = record.Rate > 0 ? record.Rate : GetRate(record.Type);
            
            record.Rate = rate;
            record.Amount = hourlyRate * record.Hours * rate;
            
            return record.Amount;
        }

        /// <summary>
        /// Tính tổng tiền tăng ca cho danh sách
        /// </summary>
        public decimal CalculateTotalOvertime(IEnumerable<OvertimeRecord> records, decimal monthlySalary)
        {
            decimal total = 0;
            foreach (var record in records)
            {
                total += CalculateOvertimeAmount(record, monthlySalary);
            }
            return total;
        }

        /// <summary>
        /// Tạo bản ghi tăng ca mới
        /// </summary>
        public (bool Success, string Message, OvertimeRecord Record) CreateOvertimeRecord(
            string employeeId, 
            string employeeName,
            DateTime workDate, 
            decimal hours, 
            OvertimeType type,
            string reason = "")
        {
            if (hours <= 0)
                return (false, "Số giờ tăng ca phải lớn hơn 0", null);

            if (hours > 12)
                return (false, "Số giờ tăng ca không được vượt quá 12 giờ/ngày", null);

            var record = new OvertimeRecord
            {
                Id = Guid.NewGuid().ToString(),
                EmployeeId = employeeId,
                EmployeeName = employeeName,
                WorkDate = workDate,
                Hours = hours,
                Type = type,
                Reason = reason,
                Rate = GetRate(type),
                Status = OvertimeStatus.ChờDuyệt,
                CreatedAt = DateTime.Now
            };

            return (true, "Tạo bản ghi tăng ca thành công", record);
        }

        /// <summary>
        /// Duyệt bản ghi tăng ca
        /// </summary>
        public (bool Success, string Message) ApproveOvertime(OvertimeRecord record, string approvedBy)
        {
            if (record == null)
                return (false, "Không tìm thấy bản ghi tăng ca");

            if (record.Status == OvertimeStatus.ĐãDuyệt)
                return (false, "Bản ghi đã được duyệt");

            if (record.Status == OvertimeStatus.TừChối)
                return (false, "Bản ghi đã bị từ chối");

            record.Status = OvertimeStatus.ĐãDuyệt;
            record.ApprovedBy = approvedBy;
            record.ApprovedAt = DateTime.Now;

            return (true, "Duyệt tăng ca thành công");
        }

        /// <summary>
        /// Tính lương tăng ca đêm (thêm 20% cho ca đêm)
        /// </summary>
        public decimal CalculateNightOvertime(decimal hourlyRate, decimal hours, decimal baseRate)
        {
            decimal nightRate = baseRate + 0.2m; // Thêm 20%
            return hourlyRate * hours * nightRate;
        }

        /// <summary>
        /// Lấy danh sách ngày lễ trong năm (Việt Nam)
        /// </summary>
        public bool IsHoliday(DateTime date)
        {
            // Danh sách ngày lễ cố định
            var holidays = new[]
            {
                new DateTime(date.Year, 1, 1),   // Tết Dương lịch
                new DateTime(date.Year, 4, 30), // Ngày Giải phóng
                new DateTime(date.Year, 5, 1),  // Quốc tế Lao động
                new DateTime(date.Year, 9, 2),  // Quốc khánh
            };

            return holidays.Any(h => h.Date == date.Date);
        }

        /// <summary>
        /// Xác định loại tăng ca tự động
        /// </summary>
        public OvertimeType DetermineOvertimeType(DateTime workDate, bool isWeeklyDayOff)
        {
            if (IsHoliday(workDate))
                return OvertimeType.Holiday;
            
            if (isWeeklyDayOff)
                return OvertimeType.WeeklyDayOff;
            
            return OvertimeType.NormalDay;
        }
    }
}