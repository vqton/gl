using System;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tính trợ cấp thôi việc
    /// Theo Bộ luật Lao động 2019, Điều 46
    /// </summary>
    public class SeverancePayCalculator
    {
        /// <summary>
        /// Số tháng làm việc tối thiểu để được hưởng trợ cấp
        /// </summary>
        private const int MinimumMonthsRequired = 12;

        /// <summary>
        /// Số tháng trợ cấp cho mỗi năm làm việc
        /// </summary>
        public const decimal MonthsPerYear = 0.5m; // 0.5 tháng/năm

        /// <summary>
        /// Tính trợ cấp thôi việc
        /// Điều kiện: làm việc từ 12 tháng trở lên
        /// Mức hưởng: 0.5 tháng lương cho mỗi năm làm việc
        /// </summary>
        public (bool Eligible, string Message, decimal Amount, decimal EligibleMonths) 
            CalculateSeverancePay(DateTime startDate, DateTime terminationDate, decimal monthlySalary)
        {
            // Tính số tháng làm việc
            int monthsWorked = ((terminationDate.Year - startDate.Year) * 12) + 
                               (terminationDate.Month - startDate.Month);

            if (monthsWorked < MinimumMonthsRequired)
            {
                return (false, 
                       $"Chưa đủ {MinimumMonthsRequired} tháng làm việc ({monthsWorked} tháng). Không được hưởng trợ cấp thôi việc.",
                       0, 0);
            }

            // Tính số tháng được hưởng (tối đa 12 tháng theo quy định)
            decimal eligibleMonths = Math.Min(monthsWorked / 12m, 12) * 6; // 0.5 tháng * số năm
            
            // Quy đổi: 1 năm = 12 tháng, mỗi năm = 0.5 tháng lương
            // Đơn giản: số năm làm việc * 0.5
            decimal yearsWorked = monthsWorked / 12m;
            eligibleMonths = yearsWorked * MonthsPerYear;
            
            // Mức trần: không quá 12 tháng lương
            eligibleMonths = Math.Min(eligibleMonths, 12);

            decimal amount = monthlySalary * eligibleMonths;

            return (true,
                   $"Đủ điều kiện hưởng trợ cấp thôi việc ({yearsWorked:F1} năm làm việc)",
                   amount,
                   eligibleMonths);
        }

        /// <summary>
        /// Tính trợ cấp mất việc làm (Điều 42 BLLĐ 2019)
        /// Áp dụng khi doanh nghiệp thay đổi cơ cấu, công nghệ...
        /// </summary>
        public (bool Eligible, string Message, decimal Amount) 
            CalculateJobLossAllowance(DateTime startDate, DateTime terminationDate, decimal monthlySalary)
        {
            int monthsWorked = ((terminationDate.Year - startDate.Year) * 12) + 
                               (terminationDate.Month - startDate.Month);

            if (monthsWorked < MinimumMonthsRequired)
            {
                return (false, "Chưa đủ 12 tháng làm việc", 0);
            }

            decimal yearsWorked = monthsWorked / 12m;
            decimal amount = monthlySalary * yearsWorked * 1.5m; // 1.5 tháng/năm

            return (true, "Đủ điều kiện hưởng trợ cấp mất việc làm", amount);
        }

        /// <summary>
        /// Tính trợ cấp thôi việc cho hợp đồng lao động
        /// </summary>
        public (bool Eligible, string Message, decimal Amount) 
            CalculateFromContract(LaborContract contract, DateTime terminationDate)
        {
            if (contract == null)
                return (false, "Hợp đồng lao động không tồn tại", 0);

            var result = CalculateSeverancePay(contract.StartDate, terminationDate, contract.BaseSalary);
            return (result.Eligible, result.Message, result.Amount);
        }

        /// <summary>
        /// Tạo bản ghi trợ cấp thôi việc
        /// </summary>
        public (bool Success, string Message, SeveranceRecord Record)
            CreateSeveranceRecord(string employeeId, string employeeName, DateTime terminationDate, 
                                  int monthsWorked, decimal monthlySalary, string reason)
        {
            var result = CalculateSeverancePay(
                terminationDate.AddMonths(-monthsWorked),
                terminationDate,
                monthlySalary);

            if (!result.Eligible)
            {
                return (false, result.Message, null);
            }

            var record = new SeveranceRecord
            {
                Id = Guid.NewGuid().ToString(),
                EmployeeId = employeeId,
                EmployeeName = employeeName,
                TerminationDate = terminationDate,
                MonthsWorked = monthsWorked,
                MonthlySalary = monthlySalary,
                EligibleMonths = result.EligibleMonths,
                Amount = result.Amount,
                Reason = reason,
                CreatedAt = DateTime.Now
            };

            return (true, "Tạo bản ghi trợ cấp thành công", record);
        }

        /// <summary>
        /// Kiểm tra điều kiện hưởng trợ cấp thôi việc
        /// </summary>
        public (bool Eligible, string Message) CheckEligibility(DateTime startDate, DateTime terminationDate)
        {
            int monthsWorked = ((terminationDate.Year - startDate.Year) * 12) + 
                               (terminationDate.Month - startDate.Month);

            if (monthsWorked < MinimumMonthsRequired)
            {
                return (false, $"Chưa đủ {MinimumMonthsRequired} tháng. Đã làm {monthsWorked} tháng.");
            }

            return (true, "Đủ điều kiện hưởng trợ cấp thôi việc");
        }
    }
}