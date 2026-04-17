using GL.Application.Services;
using GL.Application.DTOs;
using GL.Domain.Entities;
using Xunit;

namespace GL.Domain.Tests
{
    public class CostAccountingServiceTests
    {
        private readonly CostAccountingService _service = new CostAccountingService();

        [Fact]
        public void C01a_AddDirectMaterialCost_BalancedEntry()
        {
            var request = new DirectMaterialCostRequest(
                "DM-001",
                "2026-04",
                "WO-100",
                "SP-001",
                5000000,
                "152"
            );

            var result = _service.AddDirectMaterialCost(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
            Assert.Contains(result.Lines, l => l.AccountCode == "152");
        }

        [Fact]
        public void C01b_AddDirectLaborCost_BalancedEntry()
        {
            var request = new DirectLaborCostRequest(
                "DL-001",
                "2026-04",
                "WO-100",
                3000000,
                "622"
            );

            var result = _service.AddDirectLaborCost(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
        }

        [Fact]
        public void C01c_AddManufacturingOverhead_BalancedEntry()
        {
            var request = new ManufacturingOverheadRequest(
                "MO-001",
                "2026-04",
                "WO-100",
                2000000,
                "627"
            );

            var result = _service.AddManufacturingOverhead(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void C01d_CloseWorkInProgress_TransferToCOGS()
        {
            var request = new WIPClosingRequest(
                "WIP-001",
                "2026-04",
                "WO-100",
                10000000
            );

            var result = _service.CloseWorkInProgress(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "631");
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
        }

        [Fact]
        public void C01e_CalculateUnitCost_AverageMethod()
        {
            var request = new UnitCostCalculationRequest(
                "SP-001",
                "2026-04",
                100000000,
                100,
                "AVERAGE"
            );

            var result = _service.CalculateUnitCost(request);

            Assert.Equal(1000000m, result.UnitCostVnd);
        }

        [Fact]
        public void C01f_AllocateOverhead_ToProducts()
        {
            var request = new OverheadAllocationRequest(
                "OA-001",
                "2026-04",
                5000000,
                "DIRECTLabor"
            );

            var result = _service.AllocateOverhead(request);

            Assert.NotNull(result);
        }
    }
}