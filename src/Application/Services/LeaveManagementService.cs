using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý nghỉ phép năm
    /// Theo Bộ luật Lao động 2019, Điều 111
    /// </summary>
    public class LeaveManagementService
    {
        // Số ngày phép theo thâm niên (Điều 111 BLĐ 2019)
        private const int BaseLeaveDays = 12; // Tối thiểu 12 ngày

        /// <summary>
        /// Tính số ngày phép năm theo thâm niên
        /// </summary>
        public int CalculateAnnualLeaveDays(int yearsWorked)
        {
            if (yearsWorked < 1)
                return BaseLeaveDays;
            
            if (yearsWorked < 5)
                return BaseLeaveDays + (yearsWorked - 1); // 13, 14, 15, 16
            
            if (yearsWorked < 10)
                return 16; // 5-9 năm: 16 ngày
            
            if (yearsWorked < 15)
                return 17; // 10-14 năm: 17 ngày
            
            if (yearsWorked < 20)
                return 18; // 15-19 năm: 18 ngày
            
            return 19; // 20+ năm: 19 ngày
        }

        /// <summary>
        /// Tính số ngày phép còn lại
        /// </summary>
        public int CalculateRemainingLeave(int totalDays, int usedDays)
        {
            return Math.Max(0, totalDays - usedDays);
        }

        /// <summary>
        /// Tạo yêu cầu nghỉ phép mới
        /// </summary>
        public (bool Success, string Message, LeaveRequest Request) CreateLeaveRequest(
            string employeeId,
            string employeeName,
            LeaveType type,
            DateTime startDate,
            DateTime endDate,
            string reason = "")
        {
            if (endDate < startDate)
                return (false, "Ngày kết thúc phải lớn hơn ngày bắt đầu", null);

            if (startDate < DateTime.Now.Date)
                return (false, "Ngày bắt đầu không được trước ngày hiện tại", null);

            var request = new LeaveRequest
            {
                Id = Guid.NewGuid().ToString(),
                EmployeeId = employeeId,
                EmployeeName = employeeName,
                Type = type,
                StartDate = startDate,
                EndDate = endDate,
                Reason = reason,
                Status = LeaveStatus.ChờDuyệt,
                CreatedAt = DateTime.Now
            };

            request.CalculateDays();

            return (true, "Tạo yêu cầu nghỉ phép thành công", request);
        }

        /// <summary>
        /// Duyệt yêu cầu nghỉ phép
        /// </summary>
        public (bool Success, string Message) ApproveLeave(LeaveRequest request, string approvedBy)
        {
            if (request == null)
                return (false, "Không tìm thấy yêu cầu nghỉ phép");

            if (request.Status != LeaveStatus.ChờDuyệt)
                return (false, "Yêu cầu đã được xử lý");

            request.Status = LeaveStatus.ĐãDuyệt;
            request.ApprovedBy = approvedBy;
            request.ApprovedAt = DateTime.Now;

            return (true, "Duyệt nghỉ phép thành công");
        }

        /// <summary>
        /// Từ chối yêu cầu nghỉ phép
        /// </summary>
        public (bool Success, string Message) RejectLeave(LeaveRequest request, string rejectedBy, string reason)
        {
            if (request == null)
                return (false, "Không tìm thấy yêu cầu nghỉ phép");

            request.Status = LeaveStatus.TừChối;
            request.ApprovedBy = rejectedBy;
            request.ApprovedAt = DateTime.Now;
            request.Reason = reason;

            return (true, "Từ chối nghỉ phép");
        }

        /// <summary>
        /// Kiểm tra nghỉ phép có lương hay không
        /// </summary>
        public bool IsPaidLeave(LeaveType type)
        {
            return type switch
            {
                LeaveType.AnnualLeave => true,
                LeaveType.PersonalLeave => true,
                LeaveType.SickLeave => true,
                LeaveType.MaternityLeave => true,
                _ => false
            };
        }

        /// <summary>
        /// Tính lương ngày nghỉ
        /// </summary>
        public decimal CalculateDaySalary(decimal monthlySalary, int workingDaysPerMonth = 22)
        {
            return monthlySalary / workingDaysPerMonth;
        }

        /// <summary>
        /// Tính số tiền lương được hưởng khi nghỉ phép
        /// </summary>
        public decimal CalculateLeaveSalary(LeaveRequest request, decimal dailySalary)
        {
            if (!IsPaidLeave(request.Type))
                return 0;

            return dailySalary * request.Days;
        }

        /// <summary>
        /// Lấy danh sách ngày nghỉ lễ trong năm
        /// </summary>
        public List<DateTime> GetHolidays(int year)
        {
            return new List<DateTime>
            {
                new DateTime(year, 1, 1),   // Tết Dương lịch
                new DateTime(year, 4, 30), // Ngày Giải phóng
                new DateTime(year, 5, 1),  // Quốc tế Lao động
                new DateTime(year, 9, 2)   // Quốc khánh
            };
        }

        /// <summary>
        /// Kiểm tra nghỉ phép năm có vượt quá số ngày còn lại không
        /// </summary>
        public (bool Valid, string Message) ValidateLeaveRequest(LeaveRequest request, int remainingLeaveDays)
        {
            if (request.Type == LeaveType.AnnualLeave && request.Days > remainingLeaveDays)
            {
                return (false, $"Số ngày nghỉ phép vượt quá số ngày còn lại ({remainingLeaveDays} ngày)");
            }

            return (true, "Hợp lệ");
        }
    }
}