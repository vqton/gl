using System;
using System.Linq;
using GL.Domain.Entities;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho Payroll entity
    /// </summary>
    public class PayrollTests
    {
        [Fact]
        public void PayrollLine_IsValid_WithValidData_ReturnsTrue()
        {
            var line = new PayrollLine
            {
                EmployeeId = "EMP001",
                EmployeeName = "Nguyễn Văn A",
                BaseSalary = 10_000_000,
                HousingAllowance = 1_000_000,
                WorkingDays = 22,
                ActualWorkingDays = 22
            };

            Assert.True(line.IsValid());
        }

        [Fact]
        public void PayrollLine_GrossSalary_CalculatesCorrectly()
        {
            var line = new PayrollLine
            {
                BaseSalary = 10_000_000,
                HousingAllowance = 1_000_000,
                TransportAllowance = 500_000,
                MealAllowance = 500_000,
                OvertimeAmount = 1_000_000,
                Bonus = 2_000_000,
                Penalty = 0
            };

            Assert.Equal(15_000_000, line.GrossSalary);
        }

        [Fact]
        public void PayrollLine_NetSalary_CalculatesCorrectly()
        {
            var line = new PayrollLine
            {
                BaseSalary = 10_000_000,
                HousingAllowance = 2_000_000,
                TransportAllowance = 500_000,
                MealAllowance = 500_000,
                OvertimeAmount = 500_000,
                Bonus = 1_500_000,
                SocialInsuranceDeduction = 350_000,
                HealthInsuranceDeduction = 100_000,
                UnemploymentInsuranceDeduction = 50_000,
                PersonalIncomeTax = 500_000,
                OtherDeductions = 0
            };

            Assert.Equal(14_000_000, line.NetSalary);
        }

        [Fact]
        public void PayrollLine_TotalDeductions_SumsCorrectly()
        {
            var line = new PayrollLine
            {
                SocialInsuranceDeduction = 350_000,
                HealthInsuranceDeduction = 100_000,
                UnemploymentInsuranceDeduction = 50_000,
                UnionDeduction = 100_000,
                PersonalIncomeTax = 500_000,
                OtherDeductions = 100_000
            };

            Assert.Equal(1_200_000, line.TotalDeductions);
        }

        [Fact]
        public void Payroll_TotalGross_SumsAllLines()
        {
            var payroll = new Payroll
            {
                Lines = new System.Collections.Generic.List<PayrollLine>
                {
                    new PayrollLine { BaseSalary = 10_000_000 },
                    new PayrollLine { BaseSalary = 15_000_000 },
                    new PayrollLine { BaseSalary = 12_000_000 }
                }
            };

            Assert.Equal(37_000_000, payroll.TotalGross);
        }

        [Fact]
        public void Payroll_TotalNet_SumsAllLines()
        {
            var payroll = new Payroll
            {
                Lines = new System.Collections.Generic.List<PayrollLine>
                {
                    new PayrollLine { BaseSalary = 9_000_000 },
                    new PayrollLine { BaseSalary = 13_000_000 },
                    new PayrollLine { BaseSalary = 10_000_000 }
                }
            };

            Assert.Equal(32_000_000, payroll.TotalNet);
        }
    }
}