using System;

namespace GL.Application.DTOs
{
    public class CashDepositRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal Amount { get; set; }
        public string FromAccount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CashReceiptFromSaleRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CustomerId { get; set; }
        public decimal Amount { get; set; }
        public decimal VatAmount { get; set; }
        public string PaymentMethod { get; set; }
        public bool IsVatDeduction { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CashPaymentPurchaseRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string SupplierId { get; set; }
        public string InventoryAccount { get; set; }
        public decimal Amount { get; set; }
        public decimal VatAmount { get; set; }
        public string Description { get; set; }
        public bool IsVatDeduction { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class BankDepositRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal Amount { get; set; }
        public string ToAccount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO chi lương bằng tiền mặt (T05) - sử dụng lại từ CommonDTOs
    /// </summary>
    public class CashPayrollPaymentRequest
    {
        public string PaymentBatchId { get; set; }
        public DateTime PaymentDate { get; set; }
        public decimal TotalNetPayVnd { get; set; }
        public string PaymentMethod { get; set; }
        public string BankAccountId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class AdvancePaymentRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string PayeeId { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ReceivableCollectionRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CustomerId { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CashOverageRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CashShortageRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CapitalContributionRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string InvestorId { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class SecurityDepositReceivedRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string DepositorId { get; set; }
        public decimal Amount { get; set; }
        public string ContractRef { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class SecurityDepositReturnedRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string DepositorId { get; set; }
        public decimal Amount { get; set; }
        public string ContractRef { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ExpensePaymentRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string ExpenseAccount { get; set; }
        public decimal Amount { get; set; }
        public decimal VatAmount { get; set; }
        public string Description { get; set; }
        public bool IsVatDeduction { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class LoanReceivedRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string LenderId { get; set; }
        public decimal Amount { get; set; }
        public string LoanType { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class InvestmentSaleRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string InvestmentAccount { get; set; }
        public decimal SaleAmount { get; set; }
        public decimal CostAmount { get; set; }
        public string BuyerId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class InvestmentPurchaseRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string InvestmentAccount { get; set; }
        public decimal Amount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ForeignCurrencyReceiptRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal ExchangeRate { get; set; }
        public decimal VatAmount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ForeignCurrencyCollectionRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CustomerId { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal ExchangeRate { get; set; }
        public decimal RecordedRate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ForeignCurrencyPaymentRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal ExchangeRate { get; set; }
        public decimal RecordedRate { get; set; }
        public string ExpenseAccount { get; set; }
        public decimal VatAmount { get; set; }
        public string Description { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ForeignCurrencySaleRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal SaleRate { get; set; }
        public decimal RecordedRate { get; set; }
        public string BuyerId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class ForeignCurrencyAdvanceRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string SupplierId { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal ExchangeRate { get; set; }
        public decimal RecordedRate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    public class CustomerAdvanceRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CustomerId { get; set; }
        public string CurrencyCode { get; set; }
        public decimal Amount { get; set; }
        public decimal ExchangeRate { get; set; }
        public string AccountingPeriodId { get; set; }
    }
}
