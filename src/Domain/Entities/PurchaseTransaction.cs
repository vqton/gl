using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Giao dịch mua hàng - P01-P06
    /// Theo TT99/2025/TT-BTC
    /// </summary>
    public class PurchaseTransaction
    {
        public string Id { get; set; }
        public string TransactionNo { get; set; }
        public DateTime TransactionDate { get; set; }

        public PurchaseType Type { get; set; }
        public string SupplierId { get; set; }
        public string SupplierName { get; set; }
        public string SupplierTaxCode { get; set; }

        public PaymentMethod PaymentMethod { get; set; }
        public int PaymentTermDays { get; set; }
        public DateTime? DueDate { get; set; }

        public PurchaseStatus Status { get; set; }
        public string OriginalPurchaseId { get; set; }

        public decimal VatRate { get; set; }

        public List<PurchaseLine> Lines { get; set; } = new();

        public decimal SubTotal { get; set; }
        public decimal DiscountPercent { get; set; }
        public decimal DiscountAmount { get; set; }
        public decimal NetAmount { get; set; }
        public decimal VATAmount { get; set; }
        public decimal TotalAmount { get; set; }

        public decimal FreightAmount { get; set; }
        public bool IsFreightExpensedDirectly { get; set; }
        public string FreightAccountCode { get; set; }

        public decimal PrincipalAmount { get; set; }
        public decimal InterestAmount { get; set; }

        public string JournalEntryDescription { get; set; }

        public DateTime CreatedAt { get; set; }
        public string CreatedBy { get; set; }

        public void CalculateTotals()
        {
            SubTotal = Lines.Sum(l => l.Quantity * l.UnitPrice);

            if (Type == PurchaseType.Return)
            {
                SubTotal = -SubTotal;
            }

            DiscountAmount = DiscountPercent > 0
                ? SubTotal * DiscountPercent / 100
                : DiscountAmount;

            var netBeforeFreight = SubTotal - DiscountAmount;
            var freight = IsFreightExpensedDirectly ? 0 : FreightAmount;
            if (Type == PurchaseType.Return) freight = -freight;
            NetAmount = netBeforeFreight + freight;

            if (Type == PurchaseType.Return)
            {
                NetAmount = -Math.Abs(NetAmount);
            }

            VATAmount = NetAmount * VatRate;
            TotalAmount = NetAmount + VATAmount;

            if (Type == PurchaseType.Return)
            {
                TotalAmount = -Math.Abs(TotalAmount);
            }

            if (Type == PurchaseType.Installment && InterestAmount > 0)
            {
                TotalAmount = SubTotal + VATAmount + InterestAmount;
                NetAmount = SubTotal + InterestAmount;
            }

            if (IsFreightExpensedDirectly && FreightAmount > 0)
            {
                FreightAccountCode = "641";
            }
        }
    }

    public class PurchaseLine
    {
        public string Id { get; set; }
        public string PurchaseId { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public string Unit { get; set; }

        public decimal Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal DiscountPercent { get; set; }
        public decimal DiscountAmount { get; set; }

        public string AccountCode { get; set; }
        public decimal Debit { get; set; }
        public decimal Credit { get; set; }

        public decimal LineTotal => (Quantity * UnitPrice) - DiscountAmount;
    }

    public enum PurchaseType
    {
        Inventory,
        TransitGoods,
        DirectToCost,
        Consignment,
        Return,
        Installment
    }

    public enum PurchaseStatus
    {
        Draft,
        InTransit,
        PendingInvoice,
        Completed,
        Returned,
        Cancelled
    }

    public enum PaymentMethod
    {
        Cash,
        BankTransfer,
        Credit,
        Installment
    }
}