using System;

namespace GL.Application.DTOs
{
    public class PurchaseRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string SupplierId { get; set; }
        public string InventoryAccount { get; set; }
        public string ExpenseAccount { get; set; }
        public decimal SubTotal { get; set; }
        public decimal VatRate { get; set; }
        public string PaymentMethod { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class FreightRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal FreightAmount { get; set; }
        public string FreightAccountCode { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class PurchaseDiscountRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string SupplierId { get; set; }
        public decimal DiscountAmount { get; set; }
        public string DiscountType { get; set; }
        public bool IsCreditNote { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class PurchaseReturnRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string OriginalPurchaseId { get; set; }
        public string SupplierId { get; set; }
        public decimal ReturnAmount { get; set; }
        public decimal VatAmount { get; set; }
        public string InventoryAccount { get; set; }
        public bool IsVatDeductible { get; set; }
        public string AccountingPeriodId { get; set; }
    }
}