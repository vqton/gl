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
            var request = new DirectMaterialCostRequest
            {
                TransactionId = "DM-001",
                AccountingPeriodId = "2026-04",
                WorkOrderId = "WO-100",
                ProductId = "SP-001",
                MaterialCostVnd = 5000000,
                InventoryAccount = "152",
            };

            var result = _service.AddDirectMaterialCost(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
            Assert.Contains(result.Lines, l => l.AccountCode == "152");
        }

        [Fact]
        public void C01b_AddDirectLaborCost_BalancedEntry()
        {
            var request = new DirectLaborCostRequest
            {
                TransactionId = "DL-001",
                AccountingPeriodId = "2026-04",
                WorkOrderId = "WO-100",
                LaborCostVnd = 3000000,
                SalaryAccount = "622",
            };

            var result = _service.AddDirectLaborCost(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
        }

        [Fact]
        public void C01c_AddManufacturingOverhead_BalancedEntry()
        {
            var request = new ManufacturingOverheadRequest
            {
                TransactionId = "MO-001",
                AccountingPeriodId = "2026-04",
                WorkOrderId = "WO-100",
                OverheadCostVnd = 2000000,
                OverheadAccount = "627",
            };

            var result = _service.AddManufacturingOverhead(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void C01d_CloseWorkInProgress_TransferToCOGS()
        {
            var request = new WIPClosingRequest
            {
                TransactionId = "WIP-001",
                AccountingPeriodId = "2026-04",
                WorkOrderId = "WO-100",
                TotalWipCostVnd = 10000000,
            };

            var result = _service.CloseWorkInProgress(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Contains(result.Lines, l => l.AccountCode == "631");
            Assert.Contains(result.Lines, l => l.AccountCode == "154");
        }

        [Fact]
        public void C01e_CalculateUnitCost_AverageMethod()
        {
            var request = new UnitCostCalculationRequest
            {
                ProductId = "SP-001",
                AccountingPeriodId = "2026-04",
                TotalCostVnd = 100000000,
                TotalQuantity = 100,
                Method = "AVERAGE",
            };

            var result = _service.CalculateUnitCost(request);

            Assert.Equal(1000000m, result.UnitCostVnd);
        }

        [Fact]
        public void C01f_AllocateOverhead_ToProducts()
        {
            var request = new OverheadAllocationRequest
            {
                TransactionId = "OA-001",
                AccountingPeriodId = "2026-04",
                TotalOverheadVnd = 5000000,
                AllocationBase = "DIRECTLabor",
            };

            var result = _service.AllocateOverhead(request);

            Assert.NotNull(result);
        }
    }
}