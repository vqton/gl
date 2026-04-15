using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Thang bảng lương
    /// </summary>
    public class SalaryScale
    {
        public string Id { get; set; }
        public string ScaleCode { get; set; }
        public string ScaleName { get; set; }
        public int EffectiveYear { get; set; }
        public int EffectiveMonth { get; set; }
        public DateTime CreatedAt { get; set; }
        public SalaryScaleStatus Status { get; set; }
        
        public List<SalaryGrade> Grades { get; set; } = new();
        
        public bool IsActive => Status == SalaryScaleStatus.Active;
        public int TotalGrades => Grades.Count;
    }

    /// <summary>
    /// Bậc lương trong thang
    /// </summary>
    public class SalaryGrade
    {
        public string Id { get; set; }
        public string ScaleId { get; set; }
        public int GradeNumber { get; set; }
        public decimal Coefficient { get; set; }
        public decimal BaseSalary { get; set; }
        
        public decimal CalculateSalary(decimal baseSalary)
        {
            return BaseSalary * Coefficient;
        }
    }

    public enum SalaryScaleStatus
    {
        Nháp,
        Active,
        Deprecated
    }
}