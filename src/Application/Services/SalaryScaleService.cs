using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý thang bảng lương - P1
    /// Theo Nghị định 46/2025/NĐ-CP
    /// </summary>
    public class SalaryScaleService
    {
        private readonly ISalaryScaleRepository _repository;
        
        // Lương cơ sở 2026
        private const decimal BaseSalary_2026 = 2_300_000m;

        public SalaryScaleService(ISalaryScaleRepository repository)
        {
            _repository = repository;
        }

        /// <summary>
        /// Tạo thang bảng lương mới
        /// </summary>
        public (bool Success, string Message, SalaryScale Scale) CreateSalaryScale(
            string code, string name, int year, int month)
        {
            var existing = _repository.GetByCode(code);
            if (existing != null)
            {
                return (false, "Thang bảng lương đã tồn tại", null);
            }

            var scale = new SalaryScale
            {
                Id = Guid.NewGuid().ToString(),
                ScaleCode = code,
                ScaleName = name,
                EffectiveYear = year,
                EffectiveMonth = month,
                Status = SalaryScaleStatus.Nháp,
                CreatedAt = DateTime.Now
            };

            _repository.Add(scale);
            return (true, "Tạo thang bảng lương thành công", scale);
        }

        /// <summary>
        /// Thêm bậc lương
        /// </summary>
        public (bool Success, string Message) AddGrade(string scaleId, int gradeNumber, decimal coefficient, decimal baseSalary)
        {
            var scale = _repository.GetById(scaleId);
            if (scale == null)
            {
                return (false, "Không tìm thấy thang bảng lương");
            }

            if (gradeNumber <= 0 || coefficient <= 0)
            {
                return (false, "Bậc lương và hệ số phải > 0");
            }

            if (scale.Grades.Any(g => g.GradeNumber == gradeNumber))
            {
                return (false, "Bậc lương đã tồn tại");
            }

            var grade = new SalaryGrade
            {
                Id = Guid.NewGuid().ToString(),
                ScaleId = scaleId,
                GradeNumber = gradeNumber,
                Coefficient = coefficient,
                BaseSalary = baseSalary
            };

            scale.Grades.Add(grade);
            _repository.Update(scale);
            
            return (true, "Thêm bậc lương thành công");
        }

        /// <summary>
        /// Tính lương theo bậc
        /// </summary>
        public decimal CalculateSalary(string scaleId, int gradeNumber)
        {
            var scale = _repository.GetById(scaleId);
            if (scale == null) return 0;

            var grade = scale.Grades.FirstOrDefault(g => g.GradeNumber == gradeNumber);
            if (grade == null) return 0;

            return grade.BaseSalary * grade.Coefficient;
        }

        /// <summary>
        /// Lấy danh sách bậc lương
        /// </summary>
        public IEnumerable<SalaryGrade> GetGrades(string scaleId)
        {
            var scale = _repository.GetById(scaleId);
            return scale?.Grades.OrderBy(g => g.GradeNumber) ?? Enumerable.Empty<SalaryGrade>();
        }

        /// <summary>
        /// Kích hoạt thang bảng lương
        /// </summary>
        public (bool Success, string Message) ActivateScale(string scaleId)
        {
            var scale = _repository.GetById(scaleId);
            if (scale == null)
            {
                return (false, "Không tìm thấy thang bảng lương");
            }

            scale.Status = SalaryScaleStatus.Active;
            _repository.Update(scale);
            
            return (true, "Kích hoạt thang bảng lương thành công");
        }

        /// <summary>
        /// Lấy thang bảng lương theo mã
        /// </summary>
        public SalaryScale GetByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        /// <summary>
        /// Tính lương tối thiểu vùng 2026
        /// </summary>
        public decimal GetMinimumWage(int region)
        {
            return region switch
            {
                1 => 6_900_000m,  // Vùng I
                2 => 5_600_000m,  // Vùng II
                3 => 4_800_000m,  // Vùng III
                4 => 4_200_000m,  // Vùng IV
                _ => 4_200_000m
            };
        }
    }
}