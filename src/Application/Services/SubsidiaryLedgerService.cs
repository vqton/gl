using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ sổ kế toán chi tiết (Subsidiary Ledger) - S01-S03
    /// S01: Phải thu khách hàng (131)
    /// S02: Phải trả người bán (331)
    /// S03: Hàng tồn kho chi tiết (156)
    /// </summary>
    public class SubsidiaryLedgerService
    {
        private readonly Dictionary<string, List<ARTransaction>> _arLedger = new();
        private readonly Dictionary<string, List<APTransaction>> _apLedger = new();
        private readonly Dictionary<string, InventoryCard> _inventoryCards = new();

        // ============== S01: PHẢI THU KHÁCH HÀNG (131) ==============

        /// <summary>
        /// Tạo phiếu công nợ phải thu (S01a)
        /// </summary>
        public Transaction CreateAREntry(CreateAREntryRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = request.TransactionDate,
                Description = $"Công nợ phải thu - {request.CustomerId}",
            };

            transaction.AddLine("131", request.AmountVnd, 0, $"Phải thu KH {request.CustomerId}");
            transaction.AddLine("511", 0, request.NetAmountVnd, "Doanh thu bán hàng");
            transaction.AddLine("33311", 0, request.VatAmountVnd, "VAT đầu ra");

            if (!_arLedger.ContainsKey(request.CustomerId))
                _arLedger[request.CustomerId] = new List<ARTransaction>();

            var arTx = new ARTransaction
            {
                TransactionId = request.TransactionId,
                CustomerId = request.CustomerId,
                TransactionDate = request.TransactionDate,
                AmountVnd = request.AmountVnd,
                BalanceVnd = request.AmountVnd,
            };
            _arLedger[request.CustomerId].Add(arTx);

            return transaction;
        }

        /// <summary>
        /// Cập nhật thanh toán (S01b)
        /// </summary>
        public Transaction UpdateARPayment(UpdateARPaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = request.PaymentDate,
                Description = $"Thu tiền - {request.CustomerId}",
            };

            transaction.AddLine("111", request.PaymentAmountVnd, 0, "Tiền thu");
            transaction.AddLine("131", 0, request.PaymentAmountVnd, $"Thu tiền KH {request.CustomerId}");

            if (_arLedger.ContainsKey(request.CustomerId) && _arLedger[request.CustomerId].Any())
            {
                var customerTxs = _arLedger[request.CustomerId];
                var latest = customerTxs.LastOrDefault();
                if (latest != null)
                {
                    latest.BalanceVnd -= request.PaymentAmountVnd;
                }
            }

            return transaction;
        }

        /// <summary>
        /// Tính tuổi nợ (S01c)
        /// </summary>
        public AgingReport CalculateARAging(string customerId, DateTime reportDate)
        {
            var agingDetails = new List<AgingBucketItem>();

            if (_arLedger.TryGetValue(customerId, out var transactions))
            {
                foreach (var tx in transactions)
                {
                    var days = (reportDate - tx.TransactionDate).Days;
                    var bucket = days <= 30 ? "Current" 
                        : days <= 60 ? "1-30 days" 
                        : days <= 90 ? "31-60 days" 
                        : "Over 90 days";

                    agingDetails.Add(new AgingBucketItem(bucket, tx.BalanceVnd));
                }
            }

            return new AgingReport(customerId, reportDate, agingDetails);
        }

        /// <summary>
        /// Trích dự phòng nợ phải thu khó đòi (S01e)
        /// </summary>
        public Transaction CreateBadDebtProvision(CreateBadDebtProvisionRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = request.ProvisionDate,
                Description = "Trích dự phòng nợ phải thu khó đòi",
            };

            transaction.AddLine("632", request.ProvisionAmountVnd, 0, "Chi phí trích dự phòng");
            transaction.AddLine("2293", 0, request.ProvisionAmountVnd, "Dự phòng nợ phải thu");

            return transaction;
        }

        // ============== S02: PHẢI TRẢ NGƯỜI BÁN (331) ==============

        /// <summary>
        /// Tạo phiếu công nợ phải trả (S02a)
        /// </summary>
        public Transaction CreateAPEntry(CreateAPEntryRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = request.TransactionDate,
                Description = $"Công nợ phải trả - {request.SupplierId}",
            };

            transaction.AddLine("156", request.AmountVnd, 0, "Hàng mua");
            transaction.AddLine("1331", request.VatAmountVnd, 0, "VAT đầu vào");
            transaction.AddLine("331", 0, request.TotalAmountVnd, $"Phải trả {request.SupplierId}");

            if (!_apLedger.ContainsKey(request.SupplierId))
                _apLedger[request.SupplierId] = new List<APTransaction>();

            var apTx = new APTransaction
            {
                TransactionId = request.TransactionId,
                SupplierId = request.SupplierId,
                TransactionDate = request.TransactionDate,
                AmountVnd = request.TotalAmountVnd,
                BalanceVnd = request.TotalAmountVnd,
            };
            _apLedger[request.SupplierId].Add(apTx);

            return transaction;
        }

        /// <summary>
        /// Cập nhật thanh toán (S02b)
        /// </summary>
        public Transaction UpdateAPPayment(UpdateAPPaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId,
                Date = request.PaymentDate,
                Description = $"Trả tiền - {request.SupplierId}",
            };

            transaction.AddLine("331", request.PaymentAmountVnd, 0, $"Trả tiền NCC {request.SupplierId}");
            transaction.AddLine("112", 0, request.PaymentAmountVnd, "Tiền trả");

            if (_apLedger.ContainsKey(request.SupplierId) && _apLedger[request.SupplierId].Any())
            {
                var supplierTxs = _apLedger[request.SupplierId];
                var latest = supplierTxs.LastOrDefault();
                if (latest != null)
                {
                    latest.BalanceVnd -= request.PaymentAmountVnd;
                }
            }

            return transaction;
        }

        // ============== S03: HÀNG TỒN KHO CHI TIẾT (156) ==============

        /// <summary>
        /// Cập nhật thẻ kho (S03a)
        /// </summary>
        public InventoryCard UpdateInventoryCard(UpdateInventoryCardRequest request)
        {
            if (!_inventoryCards.ContainsKey(request.ProductId))
            {
                _inventoryCards[request.ProductId] = new InventoryCard
                {
                    ProductId = request.ProductId,
                    ProductName = request.ProductName,
                    CardLines = new List<InventoryCardLine>(),
                };
            }

            var card = _inventoryCards[request.ProductId];
            card.CardLines.Add(new InventoryCardLine
            {
                TransactionId = request.TransactionId,
                TransactionDate = request.TransactionDate,
                TransactionType = request.TransactionType,
                Quantity = request.Quantity,
                UnitCostVnd = request.UnitCostVnd,
                AmountVnd = request.Quantity * request.UnitCostVnd,
            });

            return card;
        }

        /// <summary>
        /// Tính giá xuất kho (S03b)
        /// </summary>
        public decimal CalculateIssueCost(CalculateIssueCostRequest request)
        {
            if (!_inventoryCards.ContainsKey(request.ProductId))
                return 0;

            var card = _inventoryCards[request.ProductId];
            var issueLines = card.CardLines.Where(l => l.TransactionType == "ISSUE").ToList();

            return request.Method switch
            {
                "FIFO" => issueLines.FirstOrDefault()?.UnitCostVnd ?? 0,
                "AVERAGE" => issueLines.Any() ? issueLines.Average(l => l.UnitCostVnd) : 0,
                _ => issueLines.FirstOrDefault()?.UnitCostVnd ?? 0,
            };
        }

        /// <summary>
        /// Báo cáo tồn kho chi tiết (S03c)
        /// </summary>
        public InventoryCardReport GenerateInventoryReport(string productId)
        {
            var report = new InventoryCardReport
            {
                ProductId = productId,
            };

            if (_inventoryCards.ContainsKey(productId))
            {
                var card = _inventoryCards[productId];
                report.TotalInQuantity = card.CardLines.Where(l => l.TransactionType == "RECEIPT").Sum(l => l.Quantity);
                report.TotalOutQuantity = card.CardLines.Where(l => l.TransactionType == "ISSUE").Sum(l => l.Quantity);
                report.BalanceQuantity = report.TotalInQuantity - report.TotalOutQuantity;
                report.TotalInAmount = card.CardLines.Where(l => l.TransactionType == "RECEIPT").Sum(l => l.AmountVnd);
                report.TotalOutAmount = card.CardLines.Where(l => l.TransactionType == "ISSUE").Sum(l => l.AmountVnd);
            }

            return report;
        }
    }

    // ============== SUBSIDIARY LEDGER CLASSES ==============

    public class ARTransaction
    {
        public string TransactionId { get; set; }
        public string CustomerId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal AmountVnd { get; set; }
        public decimal BalanceVnd { get; set; }
    }

    public class APTransaction
    {
        public string TransactionId { get; set; }
        public string SupplierId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal AmountVnd { get; set; }
        public decimal BalanceVnd { get; set; }
    }

    public class InventoryCard
    {
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public List<InventoryCardLine> CardLines { get; set; }
    }

    public class InventoryCardLine
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string TransactionType { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCostVnd { get; set; }
        public decimal AmountVnd { get; set; }
    }

    public class InventoryCardReport
    {
        public string ProductId { get; set; }
        public decimal TotalInQuantity { get; set; }
        public decimal TotalOutQuantity { get; set; }
        public decimal BalanceQuantity { get; set; }
        public decimal TotalInAmount { get; set; }
        public decimal TotalOutAmount { get; set; }
        public decimal BalanceAmount => TotalInAmount - TotalOutAmount;
    }
}