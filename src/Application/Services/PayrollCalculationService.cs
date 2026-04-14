using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tính lương hàng tháng - P0
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class PayrollCalculationService
    {
        private readonly IPayrollRepository _payrollRepository;
        private readonly IPayrollLineRepository _payrollLineRepository;
        private readonly IContractRepository _contractRepository;

        // Tỷ lệ bảo hiểm 2026
        private const decimal BHXH_Rate = 0.175m;      // 17.5%
        private const decimal BHXH_Employee = 0.035m;  // NLĐ: 3.5%
        private const decimal BHXH_Employer = 0.14m;   // DN: 14%
        
        private const decimal BHYT_Rate = 0.03m;       // 3%
        private const decimal BHYT_Employee = 0.01m;   // NLĐ: 1%
        private const decimal BHYT_Employer = 0.02m;   // DN: 2%
        
        private const decimal BHTN_Rate = 0.01m;       // 1%
        private const decimal BHTN_Employee = 0.005m;  // NLĐ: 0.5%
        private const decimal BHTN_Employer = 0.005m; // DN: 0.5%
        
        private const decimal KPCĐ_Rate = 0.02m;       // 2% (DN: 2%)

        // Mức lương tối thiểu vùng 2026
        private const decimal MinWage_V1 = 6_900_000m;
        private const decimal MinWage_V2 = 5_600_000m;
        private const decimal MinWage_V3 = 4_800_000m;
        private const decimal MinWage_V4 = 4_200_000m;

        // Mức lương cơ sở
        private const decimal BaseSalary_Current = 2_300_000m;

        // Giảm trừ gia cảnh
        private const decimal Deduction_Standard = 11_000_000m;  // 11 triệu
        private const decimal Deduction_Dependent = 4_400_000m;  // 4.4 triệu/người

        public PayrollCalculationService(
            IPayrollRepository payrollRepository,
            IPayrollLineRepository payrollLineRepository,
            IContractRepository contractRepository)
        {
            _payrollRepository = payrollRepository;
            _payrollLineRepository = payrollLineRepository;
            _contractRepository = contractRepository;
        }

        /// <summary>
        /// Tạo bảng lương mới cho kỳ
        /// </summary>
        public (bool Success, string Message, Payroll Payroll) CreatePayroll(int year, int month)
        {
            var existing = _payrollRepository.GetByPeriod(year, month);
            if (existing != null)
            {
                return (false, "Bảng lương đã tồn tại", null);
            }

            var payroll = new Payroll
            {
                Id = Guid.NewGuid().ToString(),
                PayrollPeriodId = $"{year}{month:D2}",
                Year = year,
                Month = month,
                Status = PayrollStatus.Nháp,
                CreatedAt = DateTime.Now
            };

            _payrollRepository.Add(payroll);
            return (true, "Tạo bảng lương thành công", payroll);
        }

        /// <summary>
        /// Thêm nhân viên vào bảng lương
        /// </summary>
        public (bool Success, string Message) AddEmployeeToPayroll(string payrollId, PayrollLine line)
        {
            var payroll = _payrollRepository.GetById(payrollId);
            if (payroll == null)
            {
                return (false, "Không tìm thấy bảng lương");
            }

            if (payroll.Status != PayrollStatus.Nháp)
            {
                return (false, "Không thể thêm nhân viên vào bảng lương đã được duyệt");
            }

            line.Id = Guid.NewGuid().ToString();
            line.PayrollId = payrollId;
            
            // Tính các khoản khấu trừ
            CalculateDeductions(line);
            
            _payrollLineRepository.Add(line);
            payroll.Lines.Add(line);
            _payrollRepository.Update(payroll);
            
            return (true, "Thêm nhân viên thành công");
        }

        /// <summary>
        /// Tính toàn bộ bảng lương
        /// </summary>
        public (bool Success, string Message) CalculatePayroll(string payrollId)
        {
            var payroll = _payrollRepository.GetById(payrollId);
            if (payroll == null)
            {
                return (false, "Không tìm thấy bảng lương");
            }

            foreach (var line in payroll.Lines)
            {
                CalculateDeductions(line);
                _payrollLineRepository.Update(line);
            }

            payroll.Status = PayrollStatus.ĐãTính;
            _payrollRepository.Update(payroll);
            
            return (true, "Tính lương thành công");
        }

        /// <summary>
        /// Tính các khoản khấu trừ
        /// </summary>
        private void CalculateDeductions(PayrollLine line)
        {
            // Tính lương làm thêm
            if (line.OvertimeHours > 0 && line.OvertimeRate > 0)
            {
                decimal hourlyRate = line.BaseSalary / (22 * 8); // 22 ngày, 8h/ngày
                line.OvertimeAmount = line.OvertimeHours * hourlyRate * line.OvertimeRate;
            }

            // Lương làm căn cứ đóng BH
            decimal insuranceSalary = Math.Max(line.BaseSalary, BaseSalary_Current);
            if (insuranceSalary > 149_000_000m)
                insuranceSalary = 149_000_000m; // Tối đa 149 triệu

            // Khấu trừ BHXH (NLĐ: 3.5%)
            line.SocialInsuranceDeduction = Math.Round(insuranceSalary * BHXH_Employee, 0);
            
            // Khấu trừ BHYT (NLĐ: 1%)
            line.HealthInsuranceDeduction = Math.Round(insuranceSalary * BHYT_Employee, 0);
            
            // Khấu trừ BHTN (NLĐ: 0.5%)
            line.UnemploymentInsuranceDeduction = Math.Round(insuranceSalary * BHTN_Employee, 0);
            
            // Kinh phí công đoàn (NLĐ: không trích)
            line.UnionDeduction = 0;
            
            // Tính thuế TNCN
            line.PersonalIncomeTax = CalculatePIT(line.GrossSalary, insuranceSalary);
        }

        /// <summary>
        /// Tính thuế TNCN theo biểu lũy tiến
        /// </summary>
        public decimal CalculatePIT(decimal grossSalary, decimal insuranceSalary)
        {
            // Thu nhập chịu thuế = Lương - Giảm trừ - BH
            decimal taxableIncome = grossSalary - Deduction_Standard - 
                                   insuranceSalary * (BHXH_Employee + BHYT_Employee + BHTN_Employee);
            
            if (taxableIncome <= 0)
                return 0;

            // Biểu thuế lũy tiến
            var taxBrackets = new[]
            {
                (0m, 5_000_000m, 0.05m, 0m),
                (5_000_000m, 10_000_000m, 0.10m, 250_000m),
                (10_000_000m, 18_000_000m, 0.15m, 750_000m),
                (18_000_000m, 32_000_000m, 0.20m, 1_650_000m),
                (32_000_000m, 52_000_000m, 0.25m, 4_850_000m),
                (52_000_000m, 80_000_000m, 0.30m, 9_850_000m),
                (80_000_000m, decimal.MaxValue, 0.35m, 18_550_000m)
            };

            decimal tax = 0;
            foreach (var (min, max, rate, deduction) in taxBrackets)
            {
                if (taxableIncome > min)
                {
                    decimal taxableInBracket = Math.Min(taxableIncome, max) - min;
                    tax += taxableInBracket * rate;
                }
            }

            return Math.Round(tax, 0);
        }

        /// <summary>
        /// Duyệt bảng lương
        /// </summary>
        public (bool Success, string Message) ApprovePayroll(string payrollId, string approvedBy)
        {
            var payroll = _payrollRepository.GetById(payrollId);
            if (payroll == null)
            {
                return (false, "Không tìm thấy bảng lương");
            }

            if (payroll.Status != PayrollStatus.ĐãTính)
            {
                return (false, "Bảng lương chưa được tính");
            }

            payroll.Status = PayrollStatus.ĐãDuyệt;
            payroll.ApprovedAt = DateTime.Now;
            payroll.ApprovedBy = approvedBy;
            
            _payrollRepository.Update(payroll);
            return (true, "Duyệt bảng lương thành công");
        }

        /// <summary>
        /// Lấy bảng lương theo kỳ
        /// </summary>
        public Payroll GetPayroll(int year, int month)
        {
            return _payrollRepository.GetByPeriod(year, month);
        }

        /// <summary>
        /// Tính tổng chi phí lương cho doanh nghiệp (bao gồm BH DN đóng)
        /// </summary>
        public decimal CalculateTotalLaborCost(Payroll payroll)
        {
            decimal total = 0;
            foreach (var line in payroll.Lines)
            {
                decimal insuranceSalary = Math.Max(line.BaseSalary, BaseSalary_Current);
                if (insuranceSalary > 149_000_000m)
                    insuranceSalary = 149_000_000m;

                // DN đóng: BHXH 14% + BHYT 2% + BHTN 0.5% + KPCĐ 2%
                decimal employerInsurance = insuranceSalary * (BHXH_Employer + BHYT_Employer + BHTN_Employer + KPCĐ_Rate);
                total += line.GrossSalary + employerInsurance;
            }
            return total;
        }
    }
}