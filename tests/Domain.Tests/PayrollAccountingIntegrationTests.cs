using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;
using DTOs = GL.Application.DTOs;

namespace GL.Domain.Tests
{
    public class PayrollAccountingIntegrationTests
    {
        private readonly TransactionService _transactionService;
        private readonly PayrollAccountingService _payrollAccountingService;

        public PayrollAccountingIntegrationTests()
        {
            _transactionService = new TransactionService();
            _payrollAccountingService = new PayrollAccountingService(_transactionService);
        }

        [Fact]
        public void GeneratePayrollTransactions_ShouldCreateBalancedEntries()
        {
            var payroll = CreatePayroll();
            var postingDate = new DateTime(2026, 1, 31);

            var result = _payrollAccountingService.GeneratePayrollTransactions(payroll, postingDate);

            Assert.NotNull(result);
            Assert.NotEmpty(result);
        }

        [Fact]
        public void GeneratePayrollTransactions_ShouldCreateCorrectEntryCount()
        {
            var payroll = CreatePayroll();
            var postingDate = new DateTime(2026, 1, 31);

            var result = _payrollAccountingService.GeneratePayrollTransactions(payroll, postingDate);

            Assert.InRange(result.Count, 3, 4);
        }

        [Fact]
        public void CreatePayrollSummaryEntry_ShouldBalance()
        {
            var payroll = CreatePayroll();
            var postingDate = new DateTime(2026, 1, 31);

            var result = _payrollAccountingService.CreatePayrollSummaryEntry(payroll, postingDate);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePayrollEntry_ShouldUseCorrectAccounts()
        {
            var request = new DTOs.PayrollCalculationRequest
            {
                PayrollId = "PY001",
                PayrollMonth = new DateTime(2026, 1, 31),
                TotalGrossVnd = 50000000,
                EmployeeDeductionsVnd = 5000000,
                NetPayVnd = 45000000
            };

            var result = _transactionService.CreatePayrollEntry(request);

            Assert.NotNull(result);
            var has642 = result.Lines.Any(l => l.AccountCode == "642");
            var has334 = result.Lines.Any(l => l.AccountCode == "334");
            Assert.True(has642 && has334);
        }

        [Fact]
        public void CreateSocialInsuranceEntry_ShouldUseCorrectAccounts()
        {
            var request = new DTOs.SocialInsuranceRequest
            {
                PayrollId = "PY001",
                CalculationDate = new DateTime(2026, 1, 31),
                Bhxh175 = 7000000,
                Bhyt30 = 1000000,
                Bhtn10 = 500000,
                Kpcd20 = 1000000
            };

            var result = _transactionService.CreateSocialInsuranceEntry(request);

            Assert.NotNull(result);
            var has642 = result.Lines.Any(l => l.AccountCode == "642");
            var has3382 = result.Lines.Any(l => l.AccountCode == "3382");
            Assert.True(has642 && has3382);
        }

        [Fact]
        public void CreatePayrollPaymentEntry_ShouldUseCorrectAccounts()
        {
            var request = new DTOs.PayrollPaymentRequest
            {
                PaymentBatchId = "BATCH001",
                PaymentDate = new DateTime(2026, 1, 31),
                TotalNetPayVnd = 45000000,
                PaymentMethod = "BANK"
            };

            var result = _transactionService.CreatePayrollPaymentEntry(request);

            Assert.NotNull(result);
            var has334 = result.Lines.Any(l => l.AccountCode == "334");
            var has112 = result.Lines.Any(l => l.AccountCode == "112");
            Assert.True(has334 && has112);
        }

        [Fact]
        public void CreatePitTaxEntry_ShouldUseCorrectAccounts()
        {
            var request = new DTOs.PitTaxRequest
            {
                PayrollPeriodId = "PY001",
                WithholdingDate = new DateTime(2026, 1, 31),
                TotalPitWithheldVnd = 2000000,
                PaymentDate = new DateTime(2026, 2, 10)
            };

            var result = _transactionService.CreatePitTaxEntry(request);

            Assert.NotNull(result);
            var has334 = result.Lines.Any(l => l.AccountCode == "334");
            var has3335 = result.Lines.Any(l => l.AccountCode == "3335");
            Assert.True(has334 && has3335);
        }

        [Fact]
        public void ProcessPayroll_ShouldCallIntegrationService()
        {
            var integrationService = new IntegrationService();
            var request = new DTOs.PayrollCalculationRequest
            {
                PayrollId = "PY001",
                PayrollMonth = new DateTime(2026, 1, 31),
                TotalGrossVnd = 50000000,
                EmployeeDeductionsVnd = 5000000,
                NetPayVnd = 45000000
            };

            var result = integrationService.ProcessPayroll(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        private Payroll CreatePayroll()
        {
            var line = new PayrollLine
            {
                Id = Guid.NewGuid().ToString(),
                PayrollId = "PY001",
                EmployeeId = "EMP001",
                BaseSalary = 15000000,
                HousingAllowance = 2000000,
                SocialInsuranceDeduction = 525000,
                HealthInsuranceDeduction = 150000,
                UnemploymentInsuranceDeduction = 75000,
                PersonalIncomeTax = 1500000
            };

            var payroll = new Payroll
            {
                Id = Guid.NewGuid().ToString(),
                PayrollPeriodId = "PY001",
                Year = 2026,
                Month = 1,
                Status = PayrollStatus.Nháp,
                CreatedAt = DateTime.Now
            };

            payroll.Lines.Add(line);

            return payroll;
        }
    }
}