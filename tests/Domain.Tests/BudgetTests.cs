using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Test cases for budgeting functionality
    /// </summary>
    public class BudgetTests
    {
        [Fact]
        public void Budget_Create_ShouldSetProperties()
        {
            var budget = new Budget
            {
                Id = "BUD2026",
                Name = "Budget 2026",
                FiscalYear = 2026,
                PeriodCode = "2026-01",
                Status = "DRAFT"
            };

            Assert.Equal("BUD2026", budget.Id);
            Assert.Equal(2026, budget.FiscalYear);
            Assert.Equal("DRAFT", budget.Status);
        }

        [Fact]
        public void Budget_IsValid_ShouldReturnTrue()
        {
            var budget = new Budget
            {
                Id = "BUD001",
                Name = "Test Budget",
                FiscalYear = 2026,
                TotalAmount = 1000000m
            };

            Assert.True(budget.IsValid());
        }

        [Fact]
        public void BudgetLine_AddAmount_ShouldTrackBudgetLines()
        {
            var line = new BudgetLine
            {
                AccountCode = "642",
                BudgetAmount = 500000m,
                ActualAmount = 350000m
            };

            Assert.Equal("642", line.AccountCode);
            Assert.Equal(150000m, line.Variance);
        }

        [Fact]
        public void BudgetVariance_Calculate_ShouldReturnCorrectValues()
        {
            var budget = new BudgetLine
            {
                AccountCode = "641",
                BudgetAmount = 200000m,
                ActualAmount = 180000m
            };

            Assert.Equal(20000m, budget.Variance);
            Assert.Equal(10m, budget.VariancePercent);
        }

        [Fact]
        public void BudgetForecast_Calculate_ShouldProjectFutureValues()
        {
            var forecast = new BudgetForecast
            {
                FiscalYear = 2027,
                ForecastType = "LINEAR",
                BaseAmount = 1000000m,
                GrowthRatePercent = 10m
            };
            forecast.ProjectedAmount = forecast.BaseAmount * (1 + forecast.GrowthRatePercent / 100);

            Assert.Equal(1100000m, forecast.ProjectedAmount);
        }
    }
}
