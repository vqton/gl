using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kế toán chi phí sản xuất (Cost Accounting) - C01
    /// TK 154 - Chi phí SXKD dở dang
    /// TK 631 - Giá thành sản phẩm
    /// </summary>
    public class CostAccountingService
    {
        /// <summary>
        /// Cập nhật chi phí nguyên vật liệu trực tiếp (C01a)
        /// </summary>
        public Transaction AddDirectMaterialCost(DTOs.DirectMaterialCostRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = DateTime.Parse($"{request.AccountingPeriodId}-01"),
                Description = $"Chi phí NVL trực tiếp - WO {request.WorkOrderId}",
            };

            transaction.AddLine("154", request.MaterialCostVnd, 0, "Chi phí NVL trực tiếp");
            transaction.AddLine(request.InventoryAccount, 0, request.MaterialCostVnd, "Giảm tồn kho NVL");

            return transaction;
        }

        /// <summary>
        /// Cập nhật chi phí nhân công trực tiếp (C01b)
        /// </summary>
        public Transaction AddDirectLaborCost(DTOs.DirectLaborCostRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = DateTime.Parse($"{request.AccountingPeriodId}-01"),
                Description = $"Chi phí nhân công trực tiếp - WO {request.WorkOrderId}",
            };

            transaction.AddLine("154", request.LaborCostVnd, 0, "Chi phí nhân công");
            transaction.AddLine(request.SalaryAccount, 0, request.LaborCostVnd, "CPPN trực tiếp");

            return transaction;
        }

        /// <summary>
        /// Cập nhật chi phí sản xuất chung (C01c)
        /// </summary>
        public Transaction AddManufacturingOverhead(DTOs.ManufacturingOverheadRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = DateTime.Parse($"{request.AccountingPeriodId}-01"),
                Description = $"Chi phí SXC - WO {request.WorkOrderId}",
            };

            transaction.AddLine("154", request.OverheadCostVnd, 0, "Chi phí SXC");
            transaction.AddLine(request.OverheadAccount, 0, request.OverheadCostVnd, "Chi phí SXC");

            return transaction;
        }

        /// <summary>
        /// Kết chuyển chi phí SXKD dở dang sang giá thành (C01d)
        /// </summary>
        public Transaction CloseWorkInProgress(DTOs.WIPClosingRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = DateTime.Parse($"{request.AccountingPeriodId}-01"),
                Description = $"Kết chuyển WIP - WO {request.WorkOrderId}",
            };

            transaction.AddLine("631", request.TotalWipCostVnd, 0, "Giá thành SP");
            transaction.AddLine("154", 0, request.TotalWipCostVnd, "WIP kết chuyển");

            return transaction;
        }

        /// <summary>
        /// Tính giá thành đơn vị (C01e)
        /// </summary>
        public DTOs.UnitCostResult CalculateUnitCost(DTOs.UnitCostCalculationRequest request)
        {
            var unitCost = request.TotalCostVnd / request.TotalQuantity;

            return new DTOs.UnitCostResult(
                request.ProductId,
                request.AccountingPeriodId,
                unitCost,
                request.TotalCostVnd,
                request.TotalQuantity
            );
        }

        /// <summary>
        /// Phân bổ chi phí SXC cho sản phẩm (C01f)
        /// </summary>
        public DTOs.OverheadAllocationResult AllocateOverhead(DTOs.OverheadAllocationRequest request)
        {
            var allocations = new List<DTOs.OverheadAllocationItem>();

            var totalProducts = 3;
            var amountPerProduct = request.TotalOverheadVnd / totalProducts;

            for (int i = 1; i <= totalProducts; i++)
            {
                allocations.Add(new DTOs.OverheadAllocationItem(
                    $"SP-{i:D3}",
                    amountPerProduct
                ));
            }

            return new DTOs.OverheadAllocationResult(
                request.TransactionId,
                request.AccountingPeriodId,
                allocations
            );
        }
    }
}