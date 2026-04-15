using GL.Application.DTOs;
using GL.Domain.Entities;
using System;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kế toán hàng tồn kho - I01-I07
    /// </summary>
    public class InventoryService
    {
        /// <summary>
        /// Tạo bút toán nhập kho hàng mua (I01)
        /// </summary>
        public Transaction CreateInventoryReceiptEntry(InventoryReceiptRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ReceiptDate,
                Description = $"Nhập kho {request.ProductName}",
            };

            decimal totalAmount = request.Quantity * request.UnitPriceVnd;
            decimal vatAmount = totalAmount * request.VatRate;

            transaction.AddLine(request.InventoryAccount, totalAmount, 0, $"Nhập kho {request.ProductName}");
            if (vatAmount > 0)
            {
                transaction.AddLine("1331", vatAmount, 0, "VAT đầu vào");
            }
            transaction.AddLine("331", 0, totalAmount + vatAmount, $"Phải trả {request.SupplierId}");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán xuất kho hàng bán/sử dụng (I02)
        /// </summary>
        public Transaction CreateInventoryIssueEntry(InventoryIssueRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.IssueDate,
                Description = $"Xuất kho {request.ProductName} - {request.Reason}",
            };

            decimal totalCost = request.Quantity * request.UnitCostVnd;
            string costAccount = request.Reason == "Sản xuất" ? "621" : "632";

            transaction.AddLine(costAccount, totalCost, 0, $"Giá vốn {request.ProductName}");
            transaction.AddLine(request.InventoryAccount, 0, totalCost, $"Xuất kho {request.ProductName}");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán chuyển kho nội bộ (I03)
        /// </summary>
        public Transaction CreateInventoryTransferEntry(InventoryTransferRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.TransferDate,
                Description = $"Chuyển kho {request.ProductName}: {request.FromWarehouse} → {request.ToWarehouse}",
            };

            if (request.Quantity <= 0)
            {
                return transaction;
            }

            decimal totalCost = request.Quantity * request.UnitCostVnd;

            transaction.AddLine("156", 0, totalCost, $"Xuất từ {request.FromWarehouse}");
            transaction.AddLine("156", totalCost, 0, $"Nhập vào {request.ToWarehouse}");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán kiểm kê hàng tồn kho (I04)
        /// </summary>
        public Transaction CreateInventoryCountEntry(InventoryCountRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.CountDate,
                Description = $"Kiểm kê {request.ProductName}",
            };

            decimal difference = (request.ActualQuantity - request.BookQuantity) * request.BookQuantity / request.BookQuantity;

            if (difference > 0)
            {
                transaction.AddLine("156", difference, 0, "Thừa do kiểm kê");
                transaction.AddLine("338", 0, difference, request.Reason);
            }
            else if (difference < 0)
            {
                transaction.AddLine("138", Math.Abs(difference), 0, request.Reason);
                transaction.AddLine("156", 0, Math.Abs(difference), "Thiếu do kiểm kê");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán đánh giá hàng tồn kho (I05)
        /// </summary>
        public Transaction CreateInventoryRevaluationEntry(InventoryRevaluationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RevaluationDate,
                Description = $"Đánh giá hàng tồn kho {request.ProductName}",
            };

            decimal difference = request.MarketValueVnd - request.BookValueVnd;

            if (difference < 0)
            {
                transaction.AddLine("632", Math.Abs(difference), 0, "Trích lập dự phòng giảm giá");
                transaction.AddLine("2294", 0, Math.Abs(difference), "Dự phòng giảm giá hàng tồn kho");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán trích lập dự phòng giảm giá hàng tồn kho (I06)
        /// </summary>
        public Transaction CreateInventoryProvisionEntry(InventoryProvisionRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ProvisionDate,
                Description = $"Trích lập dự phòng hàng tồn kho",
            };

            transaction.AddLine("632", request.ProvisionAmountVnd, 0, request.Reason);
            transaction.AddLine("2294", 0, request.ProvisionAmountVnd, "Dự phòng giảm giá hàng tồn kho");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán xử lý hàng hư hỏng, hết hạn (I07)
        /// </summary>
        public Transaction CreateInventoryWriteOffEntry(InventoryWriteOffRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.WriteOffDate,
                Description = $"Xử lý hàng hư hỏng {request.ProductName}",
            };

            decimal totalCost = request.WriteOffQuantity * request.UnitCostVnd;

            if (request.VatRecoverableVnd > 0)
            {
                transaction.AddLine("811", totalCost, 0, request.Reason);
                transaction.AddLine("1331", request.VatRecoverableVnd, 0, "Khấu trừ VAT");
                transaction.AddLine("156", 0, totalCost + request.VatRecoverableVnd, "Giảm hàng tồn kho");
            }
            else
            {
                transaction.AddLine("811", totalCost, 0, request.Reason);
                transaction.AddLine("156", 0, totalCost, "Giảm hàng tồn kho");
            }

            return transaction;
        }
    }
}