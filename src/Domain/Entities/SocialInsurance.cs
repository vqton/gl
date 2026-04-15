using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Tờ khai bảo hiểm xã hội hàng tháng
    /// </summary>
    public class SocialInsuranceDeclaration
    {
        public string Id { get; set; }
        public string DeclarationId { get; set; }
        public int Year { get; set; }
        public int Month { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? SubmittedAt { get; set; }
        public string SubmittedBy { get; set; }
        public SocialInsuranceStatus Status { get; set; }
        
        public List<SocialInsuranceRecord> Records { get; set; } = new();
        
        public int TotalEmployees => Records.Count;
        public decimal TotalSalary => Records.Count > 0 ? Records.Sum(r => r.InsuranceSalary) : 0;
        public decimal TotalBHXH => Records.Count > 0 ? Records.Sum(r => r.BHXH_Employee + r.BHXH_Employer) : 0;
        public decimal TotalBHYT => Records.Count > 0 ? Records.Sum(r => r.BHYT_Employee + r.BHYT_Employer) : 0;
        public decimal TotalBHTN => Records.Count > 0 ? Records.Sum(r => r.BHTN_Employee + r.BHTN_Employer) : 0;
    }

    /// <summary>
    /// Dòng bảo hiểm của một nhân viên
    /// </summary>
    public class SocialInsuranceRecord
    {
        public string Id { get; set; }
        public string DeclarationId { get; set; }
        public string EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string IdCardNumber { get; set; }
        
        // Lương làm căn cứ đóng BH
        public decimal InsuranceSalary { get; set; }
        
        // BHXH: NLĐ 3.5%, DN 14%
        public decimal BHXH_Employee { get; set; }
        public decimal BHXH_Employer { get; set; }
        
        // BHYT: NLĐ 1%, DN 2%
        public decimal BHYT_Employee { get; set; }
        public decimal BHYT_Employer { get; set; }
        
        // BHTN: NLĐ 0.5%, DN 0.5%
        public decimal BHTN_Employee { get; set; }
        public decimal BHTN_Employer { get; set; }
        
        public decimal Total => BHXH_Employee + BHXH_Employer + BHYT_Employee + BHYT_Employer + 
                       BHTN_Employee + BHTN_Employer;
    }

    public enum SocialInsuranceStatus
    {
        Nháp,
        ĐãTính,
        ĐãDuyệt,
        ĐãNộp
    }
}