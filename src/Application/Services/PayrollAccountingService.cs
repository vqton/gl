using System;
using System.Collections.Generic;
using GL.Domain.Entities;
using GL.Application.DTOs;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tích hợp Payroll với Kế toán - hạch toán tiền lương
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class PayrollAccountingService
    {
        private readonly TransactionService _transactionService;

        public PayrollAccountingService(TransactionService transactionService)
        {
            _transactionService = transactionService;
        }

        /// <summary>
        /// Hạch toán chi phí lương và các khoản trích theo lương
        /// </summary>
        public List<Transaction> GeneratePayrollTransactions(Payroll payroll, DateTime postingDate)
        {
            var transactions = new List<Transaction>();

            foreach (var line in payroll.Lines)
            {
                // 1. Bút toán chi phí lương (L01)
                var payrollEntry = CreatePayrollEntry(line, postingDate);
                transactions.Add(payrollEntry);

                // 2. Bút toán trích BH phần DN (L02)
                var insuranceEntry = CreateInsuranceEntry(line, postingDate);
                if (insuranceEntry != null)
                    transactions.Add(insuranceEntry);

                // 3. Bút toán chi lương (L03)
                var paymentEntry = CreatePaymentEntry(line, postingDate);
                if (paymentEntry != null)
                    transactions.Add(paymentEntry);

                // 4. Bút toán thuế TNCN (X03)
                if (line.PersonalIncomeTax > 0)
                {
                    var pitEntry = CreatePITEntry(line, postingDate);
                    transactions.Add(pitEntry);
                }
            }

            return transactions;
        }

        private Transaction CreatePayrollEntry(PayrollLine line, DateTime postingDate)
        {
            var request = new PayrollCalculationRequest
            {
                PayrollId = "",
                PayrollMonth = postingDate,
                TotalGrossVnd = line.GrossSalary,
                EmployeeDeductionsVnd = line.SocialInsuranceDeduction + line.HealthInsuranceDeduction + line.UnemploymentInsuranceDeduction,
                NetPayVnd = line.NetSalary
            };

            return _transactionService.CreatePayrollEntry(request);
        }

        private Transaction CreateInsuranceEntry(PayrollLine line, DateTime postingDate)
        {
            decimal employerShare = 0;
            decimal insuranceSalary = Math.Max(line.BaseSalary, 2_300_000m);
            if (insuranceSalary > 149_000_000m) insuranceSalary = 149_000_000m;

            // DN đóng: BHXH 14% + BHYT 2% + BHTN 0.5% + KPCĐ 2%
            employerShare = insuranceSalary * 0.185m; // 18.5%

            if (employerShare <= 0) return null;

            var request = new SocialInsuranceRequest
            {
                PayrollId = "",
                CalculationDate = postingDate,
                Bhxh175 = insuranceSalary * 0.14m,  // 14%
                Bhyt30 = insuranceSalary * 0.02m,   // 2%
                Bhtn10 = insuranceSalary * 0.005m,   // 0.5%
                Kpcd20 = insuranceSalary * 0.02m    // 2%
            };

            return _transactionService.CreateSocialInsuranceEntry(request);
        }

        private Transaction CreatePaymentEntry(PayrollLine line, DateTime postingDate)
        {
            if (line.NetSalary <= 0) return null;

            var request = new PayrollPaymentRequest
            {
                PaymentBatchId = "",
                PaymentDate = postingDate,
                TotalNetPayVnd = line.NetSalary,
                PaymentMethod = "BANK"
            };

            return _transactionService.CreatePayrollPaymentEntry(request);
        }

        private Transaction CreatePITEntry(PayrollLine line, DateTime postingDate)
        {
            var request = new PitTaxRequest
            {
                PayrollPeriodId = "",
                WithholdingDate = postingDate,
                TotalPitWithheldVnd = line.PersonalIncomeTax,
                PaymentDate = postingDate
            };

            return _transactionService.CreatePitTaxEntry(request);
        }

        /// <summary>
        /// Tạo bút toán tổng hợp cho toàn bộ bảng lương
        /// </summary>
        public Transaction CreatePayrollSummaryEntry(Payroll payroll, DateTime postingDate)
        {
            decimal totalGross = payroll.TotalGross;
            decimal totalNet = payroll.TotalNet;
            decimal totalPIT = 0;
            decimal totalInsuranceEmployee = 0;
            decimal totalInsuranceEmployer = 0;

            foreach (var line in payroll.Lines)
            {
                totalPIT += line.PersonalIncomeTax;
                decimal insuranceSalary = Math.Max(line.BaseSalary, 2_300_000m);
                if (insuranceSalary > 149_000_000m) insuranceSalary = 149_000_000m;

                totalInsuranceEmployee += insuranceSalary * 0.035m + insuranceSalary * 0.01m + insuranceSalary * 0.005m;
                totalInsuranceEmployer += insuranceSalary * 0.185m;
            }

            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = postingDate,
                Description = $"Tổng hợp lương tháng {postingDate:MM/yyyy}"
            };

            // Chi phí lương
            transaction.AddLine("642", totalGross, 0, "Chi phí lương");
            
            // Phải trả NLĐ
            transaction.AddLine("334", 0, totalNet, "Lương phải trả");
            
            // Thuế TNCN
            if (totalPIT > 0)
                transaction.AddLine("3335", 0, totalPIT, "Thuế TNCN phải nộp");
            
            // BH phần NLĐ
            if (totalInsuranceEmployee > 0)
                transaction.AddLine("3383", 0, totalInsuranceEmployee, "BH phần NLĐ");
            
            // BH phần DN
            if (totalInsuranceEmployer > 0)
            {
                transaction.AddLine("642", totalInsuranceEmployer, 0, "Chi phí BH DN");
                transaction.AddLine("3382", 0, totalInsuranceEmployer, "BH phần DN");
            }

            return transaction;
        }
    }
}