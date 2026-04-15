using System;
using System.Linq;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho PeriodClosingService (G01-G04)
    /// </summary>
    public class PeriodClosingTests
    {
        private readonly PeriodClosingService _service;

        public PeriodClosingTests()
        {
            _service = new PeriodClosingService();
        }

        [Fact]
        public void G01_CloseRevenue_CreatesValidEntry()
        {
            var result = _service.CloseRevenue(2026, 4);

            Assert.True(result.Success);
            Assert.NotNull(result.Entry);
            Assert.Equal("G01", result.Entry.EntryType);
            
            // Check balance: total debits = total credits
            var totalDebit = result.Entry.Lines.Sum(l => l.Debit);
            var totalCredit = result.Entry.Lines.Sum(l => l.Credit);
            Assert.Equal(totalDebit, totalCredit);
        }

        [Fact]
        public void G02_CloseExpenses_CreatesValidEntry()
        {
            // First open the period
            _service.OpenPeriod(2026, 4);
            
            var result = _service.CloseExpenses(2026, 4);

            Assert.True(result.Success);
            Assert.NotNull(result.Entry);
            Assert.Equal("G02", result.Entry.EntryType);
        }

        [Fact]
        public void G03_CloseProfit_CreatesValidEntry()
        {
            var result = _service.CloseProfit(2026);

            Assert.True(result.Success);
            Assert.NotNull(result.Entry);
            Assert.Equal("G03", result.Entry.EntryType);
            
            // Should have 911 and 4212
            var has911 = result.Entry.Lines.Any(l => l.AccountCode == "911");
            var has4212 = result.Entry.Lines.Any(l => l.AccountCode == "4212");
            Assert.True(has911);
            Assert.True(has4212);
        }

        [Fact]
        public void G04_AllocatePrepaid_CreatesEntry()
        {
            _service.OpenPeriod(2026, 4);
            
            var result = _service.AllocatePrepaid(2026, 4);

            Assert.True(result.Success);
            Assert.NotNull(result.Entry);
            Assert.Equal("G04", result.Entry.EntryType);
        }

        [Fact]
        public void ClosePeriod_ChangesStatusToClosed()
        {
            var openResult = _service.OpenPeriod(2026, 4);
            Assert.True(openResult.Success);

            var closeResult = _service.ClosePeriod(2026, 4);
            Assert.True(closeResult.Success);
        }

        [Fact]
        public void OpenPeriod_CreatesNewPeriod()
        {
            var result = _service.OpenPeriod(2026, 5);

            Assert.True(result.Success);
        }

        [Fact]
        public void RunG01G02_InOrder_Success()
        {
            // G01 first
            var g01 = _service.CloseRevenue(2026, 4);
            Assert.True(g01.Success);
            Assert.Equal("G01", g01.Entry?.EntryType);

            // G02 
            var g02 = _service.CloseExpenses(2026, 4);
            Assert.True(g02.Success);
            Assert.Equal("G02", g02.Entry?.EntryType);
        }

        [Fact]
        public void GetTrialBalance_ReturnsResult()
        {
            var trialBalance = _service.GetTrialBalance(2026, 4);

            Assert.NotNull(trialBalance);
            Assert.Equal("2026-4", trialBalance.PeriodCode);
        }
    }
}