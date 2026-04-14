using System;
using GL.Domain.Entities;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho LaborContract entity
    /// </summary>
    public class LaborContractTests
    {
        [Fact]
        public void IsValid_WithValidData_ReturnsTrue()
        {
            var contract = new LaborContract
            {
                EmployeeId = "EMP001",
                ContractNumber = "HD/2026/001",
                ContractType = ContractType.CóThờiHạn,
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2027, 1, 1),
                BaseSalary = 10_000_000,
                Position = "Kế toán",
                Department = "Tài chính"
            };

            Assert.True(contract.IsValid());
        }

        [Fact]
        public void IsValid_WithEmptyEmployeeId_ReturnsFalse()
        {
            var contract = new LaborContract
            {
                EmployeeId = "",
                ContractNumber = "HD/2026/001",
                ContractType = ContractType.ThửViệc,
                StartDate = new DateTime(2026, 1, 1),
                BaseSalary = 10_000_000
            };

            Assert.False(contract.IsValid());
        }

        [Fact]
        public void IsValid_WithZeroSalary_ReturnsFalse()
        {
            var contract = new LaborContract
            {
                EmployeeId = "EMP001",
                ContractNumber = "HD/2026/001",
                ContractType = ContractType.ThửViệc,
                StartDate = new DateTime(2026, 1, 1),
                BaseSalary = 0
            };

            Assert.False(contract.IsValid());
        }

        [Fact]
        public void IsValid_WithEndDateBeforeStartDate_ReturnsFalse()
        {
            var contract = new LaborContract
            {
                EmployeeId = "EMP001",
                ContractNumber = "HD/2026/001",
                ContractType = ContractType.CóThờiHạn,
                StartDate = new DateTime(2027, 1, 1),
                EndDate = new DateTime(2026, 1, 1),
                BaseSalary = 10_000_000
            };

            Assert.False(contract.IsValid());
        }

        [Fact]
        public void IsExpired_WhenContractEnded_ReturnsTrue()
        {
            var contract = new LaborContract
            {
                StartDate = new DateTime(2024, 1, 1),
                EndDate = new DateTime(2025, 1, 1),
                Status = ContractStatus.HoạtĐộng
            };

            Assert.True(contract.IsExpired());
        }

        [Fact]
        public void IsExpired_WhenContractNotEnded_ReturnsFalse()
        {
            var contract = new LaborContract
            {
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2027, 12, 31),
                Status = ContractStatus.HoạtĐộng
            };

            Assert.False(contract.IsExpired());
        }

        [Fact]
        public void GetDurationMonths_WithDateRange_ReturnsCorrectMonths()
        {
            var contract = new LaborContract
            {
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 12, 31)
            };

            Assert.Equal(11, contract.GetDurationMonths());
        }

        [Fact]
        public void GetDurationMonths_WithoutEndDate_ReturnsMinusOne()
        {
            var contract = new LaborContract
            {
                StartDate = new DateTime(2026, 1, 1),
                EndDate = null
            };

            Assert.Equal(-1, contract.GetDurationMonths());
        }
    }
}