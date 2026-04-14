using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Bảng lương hàng tháng
    /// </summary>
    public class Payroll
    {
        public string Id { get; set; }
        public string PayrollPeriodId { get; set; }
        public int Year { get; set; }
        public int Month { get; set; }
        public PayrollStatus Status { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ApprovedAt { get; set; }
        public string ApprovedBy { get; set; }
        public List<PayrollLine> Lines { get; set; } = new List<PayrollLine>();

        public decimal TotalGross => Lines.Count > 0 ? Lines.Sum(l => l.GrossSalary) : 0;
        public decimal TotalNet => Lines.Count > 0 ? Lines.Sum(l => l.NetSalary) : 0;
        public decimal TotalDeductions => Lines.Count > 0 ? Lines.Sum(l => l.TotalDeductions) : 0;
    }

    /// <summary>
    /// Dòng lương của một nhân viên trong bảng lương
    /// </summary>
    public class PayrollLine
    {
        public string Id { get; set; }
        public string PayrollId { get; set; }
        public string EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        
        // Lương cơ bản
        public decimal BaseSalary { get; set; }
        
        // Phụ cấp
        public decimal HousingAllowance { get; set; }
        public decimal TransportAllowance { get; set; }
        public decimal MealAllowance { get; set; }
        public decimal OtherAllowances { get; set; }
        
        // Tăng ca
        public decimal OvertimeHours { get; set; }
        public decimal OvertimeRate { get; set; }
        public decimal OvertimeAmount { get; set; }
        
        // Thưởng/Phạt
        public decimal Bonus { get; set; }
        public decimal Penalty { get; set; }
        
        // Tổng lương
        public decimal GrossSalary => BaseSalary + HousingAllowance + TransportAllowance + 
                                     MealAllowance + OtherAllowances + OvertimeAmount + Bonus - Penalty;
        
        // Các khoản khấu trừ
        public decimal SocialInsuranceDeduction { get; set; }
        public decimal HealthInsuranceDeduction { get; set; }
        public decimal UnemploymentInsuranceDeduction { get; set; }
        public decimal UnionDeduction { get; set; }
        public decimal PersonalIncomeTax { get; set; }
        public decimal OtherDeductions { get; set; }
        
        public decimal TotalDeductions => SocialInsuranceDeduction + HealthInsuranceDeduction + 
                                          UnemploymentInsuranceDeduction + UnionDeduction + 
                                          PersonalIncomeTax + OtherDeductions;
        
        public decimal NetSalary => GrossSalary - TotalDeductions;
        
        // Số ngày làm việc
        public int WorkingDays { get; set; }
        public int ActualWorkingDays { get; set; }
        
        public bool IsValid()
        {
            return !string.IsNullOrEmpty(EmployeeId) && GrossSalary >= 0 && NetSalary >= 0;
        }
    }

    public enum PayrollStatus
    {
        Nháp = 1,
        ĐãTính = 2,
        ĐãDuyệt = 3,
        ĐãChiTrả = 4
    }
}