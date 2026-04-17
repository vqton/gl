using System;

namespace GL.Application.DTOs
{
    public class EInvoiceCreateRequest
    {
        public string InvoiceType { get; set; }
        public string SellerTaxCode { get; set; }
        public string SellerName { get; set; }
        public string SellerAddress { get; set; }
        public string BuyerTaxCode { get; set; }
        public string BuyerName { get; set; }
        public string BuyerAddress { get; set; }
        public EInvoiceItem[] Items { get; set; }
    }

    public class EInvoiceItem
    {
        public string ItemName { get; set; }
        public decimal Quantity { get; set; }
        public string UnitName { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal VATRate { get; set; }
    }

    public class EInvoiceResult
    {
        public string InvoiceId { get; set; }
        public string InvoiceNumber { get; set; }
        public string InvoiceType { get; set; }
        public DateTime InvoiceDate { get; set; }
        public string SellerTaxCode { get; set; }
        public string BuyerTaxCode { get; set; }
        public decimal TotalAmount { get; set; }
        public decimal VATAmount { get; set; }
        public bool IsSigned { get; set; }
        public string Status { get; set; }
        public string XMLContent { get; set; }
    }

    public class CancelInvoiceRequest
    {
        public string InvoiceNumber { get; set; }
        public string Reason { get; set; }
    }
}