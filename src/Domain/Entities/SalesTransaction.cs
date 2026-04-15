using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Giao dịch bán hàng - S01-S06
    /// Theo TT99/2025/TT-BTC
    /// </summary>
    public class SalesTransaction
    {
        public string Id { get; set; }
        public string TransactionNo { get; set; }
        public DateTime TransactionDate { get; set; }
        
        public SalesType Type { get; set; }
        public string CustomerId { get; set; }
        public string CustomerName { get; set; }
        public string CustomerTaxCode { get; set; }
        
        // Payment terms
        public int PaymentTermDays { get; set; }
        public DateTime? DueDate { get; set; }
        
        // VAT
        public decimal VatRate { get; set; }
        
        // Items
        public List<SalesLine> Lines { get; set; } = new();
        
        // Totals
        public decimal SubTotal { get; set; }
        public decimal DiscountAmount { get; set; }
        public decimal VATAmount { get; set; }
        public decimal TotalAmount { get; set; }
        public decimal COGS { get; set; }
        
        // Status
        public SalesStatus Status { get; set; }
        public PaymentStatus PaymentStatus { get; set; }
        
        public DateTime CreatedAt { get; set; }
        public string CreatedBy { get; set; }
    }

    /// <summary>
    /// Dòng chi tiết bán hàng
    /// </summary>
    public class SalesLine
    {
        public string Id { get; set; }
        public string SalesId { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public string Unit { get; set; }
        
        public decimal Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal DiscountPercent { get; set; }
        public decimal DiscountAmount { get; set; }
        
        // For journal entry
        public string AccountCode { get; set; }
        public decimal Debit { get; set; }
        public decimal Credit { get; set; }
        
        public decimal LineTotal => (Quantity * UnitPrice) - DiscountAmount;
    }

    public enum SalesType
    {
        Cash,
        Credit,
        Installment,
        Consignment
    }

    public enum SalesStatus
    {
        Draft,
        PendingPayment,
        Paid,
        PartiallyPaid,
        Overdue,
        Returned,
        Cancelled
    }

    public enum PaymentStatus
    {
        PendingPayment,
        Paid,
        PartiallyPaid,
        Overdue
    }

    /// <summary>
    /// Input để tạo giao dịch bán hàng
    /// </summary>
    public class CreateSaleInput
    {
        public SalesType Type { get; set; }
        public string CustomerId { get; set; }
        public string CustomerName { get; set; }
        public string CustomerTaxCode { get; set; }
        
        public int PaymentTermDays { get; set; }
        public decimal VatRate { get; set; } = 0.10m;
        
        public DateTime TransactionDate { get; set; }
        public List<SalesLineInput> Lines { get; set; }
    }

    public class SalesLineInput
    {
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal DiscountPercent { get; set; }
    }

    /// <summary>
    /// Input để xử lý trả hàng
    /// </summary>
    public class ReturnInput
    {
        public string SalesId { get; set; }
        public string ProductId { get; set; }
        public decimal Quantity { get; set; }
        public string Reason { get; set; }
        public DateTime ReturnDate { get; set; }
        public decimal RefundAmount { get; set; }
    }
}