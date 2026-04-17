using GL.Application.DTOs;
using GL.Application.Services;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Tests for PeriodLockingService (PL01-PL03)
    /// </summary>
    public class PeriodLockingServiceTests
    {
        private readonly PeriodLockingService _service = new PeriodLockingService();

        [Fact]
        public void PL01_OpenPeriod_Success()
        {
            var request = new OpenPeriodRequest("2026-05", "ketoantruong");

            var result = _service.OpenPeriod(request);

            Assert.True(result.IsValid);
            Assert.Equal("OPEN", result.Status);
        }

        [Fact]
        public void PL02_ClosePeriod_Success()
        {
            var openRequest = new OpenPeriodRequest("2026-04", "ketoantruong");
            _service.OpenPeriod(openRequest);

            var closeRequest = new ClosePeriodRequest("2026-04", "ketoantruong", "End of month");

            var result = _service.ClosePeriod(closeRequest);

            Assert.True(result.IsValid);
            Assert.Equal("CLOSED", result.Status);
        }

        [Fact]
        public void PL03_ValidatePeriod_OpenPeriod_AllowsPosting()
        {
            var openRequest = new OpenPeriodRequest("2026-06", "ketoantruong");
            _service.OpenPeriod(openRequest);

            var result = _service.ValidatePeriod(new ValidatePeriodRequest("2026-06"));

            Assert.True(result.IsValid, result.Message);
            Assert.Contains("OPEN", result.Message);
        }

        [Fact]
        public void PL03_ValidatePeriod_ClosedPeriod_RejectsPosting()
        {
            var openRequest = new OpenPeriodRequest("2026-03", "ketoantruong");
            _service.OpenPeriod(openRequest);

            var closeRequest = new ClosePeriodRequest("2026-03", "ketoantruong", null);
            _service.ClosePeriod(closeRequest);

            var result = _service.ValidatePeriod(new ValidatePeriodRequest("2026-03"));

            Assert.False(result.IsValid);
            Assert.Contains("closed", result.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void PL03_ValidatePeriod_NonExistentPeriod_ReturnsError()
        {
            var result = _service.ValidatePeriod(new ValidatePeriodRequest("2099-01"));

            Assert.False(result.IsValid);
            Assert.Contains("does not exist", result.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void PL02_ClosePeriod_Failed_WhenNotOpened()
        {
            var request = new ClosePeriodRequest("2026-07", "ketoantruong", null);

            var result = _service.ClosePeriod(request);

            Assert.False(result.IsValid);
        }
    }
}