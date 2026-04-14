using System;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Bản ghi làm thêm giờ - ghi nhận số giờ tăng ca của nhân viên
    /// Theo Bộ luật Lao động 2019
    /// </summary>
    public class OvertimeRecord
    {
        public string Id { get; set; }
        public string EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public DateTime WorkDate { get; set; }
        
        /// <summary>
        /// Số giờ tăng ca
        /// </summary>
        public decimal Hours { get; set; }
        
        /// <summary>
        /// Loại ngày làm thêm
        /// </summary>
        public OvertimeType Type { get; set; }
        
        /// <summary>
        /// Lý do tăng ca
        /// </summary>
        public string Reason { get; set; }
        
        /// <summary>
        /// Hệ số tính lương (1.5, 2.0, 3.0)
        /// </summary>
        public decimal Rate { get; set; }
        
        /// <summary>
        /// Số tiền tăng ca
        /// </summary>
        public decimal Amount { get; set; }
        
        /// <summary>
        /// Trạng thái duyệt
        /// </summary>
        public OvertimeStatus Status { get; set; }
        
        public string ApprovedBy { get; set; }
        public DateTime? ApprovedAt { get; set; }
        public DateTime CreatedAt { get; set; }

        public bool IsValid()
        {
            return !string.IsNullOrEmpty(EmployeeId) && 
                   WorkDate != default && 
                   Hours > 0;
        }

        public decimal CalculateAmount(decimal hourlyRate)
        {
            Amount = hourlyRate * Hours * Rate;
            return Amount;
        }
    }

    public enum OvertimeType
    {
        /// <summary>Ngày thường</summary>
        NormalDay = 1,
        
        /// <summary>Ngày nghỉ hàng tuần</summary>
        WeeklyDayOff = 2,
        
        /// <summary>Ngày lễ, Tết</summary>
        Holiday = 3,
        
        /// <summary>Ngày nghỉ có lương</summary>
        PaidDayOff = 4
    }

    public enum OvertimeStatus
    {
        ChờDuyệt = 1,
        ĐãDuyệt = 2,
        TừChối = 3
    }

    /// <summary>
    /// Yêu cầu nghỉ phép của nhân viên
    /// </summary>
    public class LeaveRequest
    {
        public string Id { get; set; }
        public string EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public LeaveType Type { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        
        /// <summary>Số ngày nghỉ</summary>
        public int Days { get; set; }
        
        public string Reason { get; set; }
        public LeaveStatus Status { get; set; }
        public string ApprovedBy { get; set; }
        public DateTime? ApprovedAt { get; set; }
        public DateTime CreatedAt { get; set; }

        public bool IsValid()
        {
            return !string.IsNullOrEmpty(EmployeeId) && 
                   EndDate >= StartDate;
        }

        public int CalculateDays()
        {
            Days = (EndDate - StartDate).Days + 1;
            return Days;
        }
    }

    public enum LeaveType
    {
        /// <summary>Nghỉ phép năm</summary>
        AnnualLeave = 1,
        
        /// <summary>Nghỉ việc riêng có lương</summary>
        PersonalLeave = 2,
        
        /// <summary>Nghỉ việc riêng không lương</summary>
        UnpaidLeave = 3,
        
        /// <summary>Nghỉ ốm</summary>
        SickLeave = 4,
        
        /// <summary>Nghỉ thai sản</summary>
        MaternityLeave = 5,
        
        /// <summary>Nghỉ chế độ khác</summary>
        Other = 6
    }

    public enum LeaveStatus
    {
        ChờDuyệt = 1,
        ĐãDuyệt = 2,
        TừChối = 3,
        ĐãHủy = 4
    }

    /// <summary>
    /// Bản ghi trợ cấp thôi việc
    /// </summary>
    public class SeveranceRecord
    {
        public string Id { get; set; }
        public string EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public DateTime TerminationDate { get; set; }
        
        /// <summary>Số tháng làm việc</summary>
        public int MonthsWorked { get; set; }
        
        /// <summary>Mức lương tính trợ cấp</summary>
        public decimal MonthlySalary { get; set; }
        
        /// <summary>Số tháng được hưởng</summary>
        public decimal EligibleMonths { get; set; }
        
        /// <summary>Số tiền trợ cấp</summary>
        public decimal Amount { get; set; }
        
        public string Reason { get; set; }
        public string CreatedBy { get; set; }
        public DateTime CreatedAt { get; set; }

        public bool IsValid()
        {
            return !string.IsNullOrEmpty(EmployeeId) && 
                   TerminationDate != default &&
                   MonthlySalary > 0;
        }
    }
}