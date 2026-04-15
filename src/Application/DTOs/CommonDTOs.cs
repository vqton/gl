using System;

namespace GL.Application.DTOs
{
    /// <summary>
    /// DTO cho yêu cầu kê khai và nộp thuế GTGT (X01)
    /// </summary>
    public class VatDeclarationRequest
    {
        public string DeclarationPeriodId { get; set; }
        public DateTime DeclarationDate { get; set; }
        public decimal OutputVatTotal { get; set; }
        public decimal InputVatTotal { get; set; }
        public string PaymentMethod { get; set; }
        public string BankAccountId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu hạch toán chi phí thuế TNDN (X02)
    /// </summary>
    public class CitTaxRequest
    {
        public string TaxPeriodId { get; set; }
        public DateTime CalculationDate { get; set; }
        public decimal TaxableIncomeVnd { get; set; }
        public decimal CitRate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu hạch toán và nộp thuế TNCN (X03)
    /// </summary>
    public class PitTaxRequest
    {
        public string PayrollPeriodId { get; set; }
        public DateTime WithholdingDate { get; set; }
        public decimal TotalPitWithheldVnd { get; set; }
        public DateTime PaymentDate { get; set; }
        public string BankAccountId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu tính lương và các khoản phải trả NLĐ (L01)
    /// </summary>
    public class PayrollCalculationRequest
    {
        public string PayrollId { get; set; }
        public DateTime PayrollMonth { get; set; }
        public decimal TotalGrossVnd { get; set; }
        public decimal EmployeeDeductionsVnd { get; set; }
        public decimal NetPayVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu trích bảo hiểm xã hội phần doanh nghiệp (L02)
    /// </summary>
    public class SocialInsuranceRequest
    {
        public string PayrollId { get; set; }
        public DateTime CalculationDate { get; set; }
        public decimal Bhxh175 { get; set; }
        public decimal Bhyt30 { get; set; }
        public decimal Bhtn10 { get; set; }
        public decimal Kpcd20 { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu chi lương cho người lao động (L03)
    /// </summary>
    public class PayrollPaymentRequest
    {
        public string PaymentBatchId { get; set; }
        public DateTime PaymentDate { get; set; }
        public decimal TotalNetPayVnd { get; set; }
        public string PaymentMethod { get; set; }
        public string BankTransferFileRef { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu mua tài sản cố định (A01)
    /// </summary>
    public class FixedAssetPurchaseRequest
    {
        public string AssetHandoverId { get; set; }
        public DateTime HandoverDate { get; set; }
        public string AssetType { get; set; }
        public decimal OriginalCostVnd { get; set; }
        public decimal VatAmountVnd { get; set; }
        public string SupplierId { get; set; }
        public string PaymentMethod { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu trích khấu hao TSCĐ hàng tháng (A02)
    /// </summary>
    public class DepreciationRequest
    {
        public string DepreciationPeriodId { get; set; }
        public DateTime CalculationDate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu kết chuyển doanh thu (G01)
    /// </summary>
    public class RevenueClosingRequest
    {
        public string ClosingPeriodId { get; set; }
        public DateTime ClosingDate { get; set; }
        public decimal Revenue511 { get; set; }
        public decimal Revenue515 { get; set; }
        public decimal Revenue711 { get; set; }
        public decimal ContraRevenue521 { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu kết chuyển chi phí (G02)
    /// </summary>
    public class ExpenseClosingRequest
    {
        public string ClosingPeriodId { get; set; }
        public DateTime ClosingDate { get; set; }
        public decimal Expense632 { get; set; }
        public decimal Expense635 { get; set; }
        public decimal Expense641 { get; set; }
        public decimal Expense642 { get; set; }
        public decimal Expense811 { get; set; }
        public decimal Expense821 { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu kết chuyển lợi nhuận sau thuế (G03)
    /// </summary>
    public class ProfitClosingRequest
    {
        public string FiscalYearId { get; set; }
        public DateTime ClosingDate { get; set; }
        public decimal ProfitAfterTaxVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu hạch toán VAT đầu vào không được khấu trừ (X04)
    /// </summary>
    public class UnrecoverableVatRequest
    {
        public string InvoiceId { get; set; }
        public DateTime RecognitionDate { get; set; }
        public decimal VatAmountVnd { get; set; }
        public string ExpenseAccountCode { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu ghi nhận thuế TNDN hoãn lại (X05)
    /// </summary>
    public class DeferredTaxRequest
    {
        public string FiscalYearId { get; set; }
        public DateTime RecognitionDate { get; set; }
        public decimal DeferredTaxAssetVnd { get; set; }
        public string TaxCode { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu đảo thuế TNDN hoãn lại
    /// </summary>
    public class DeferredTaxReversalRequest
    {
        public DateTime ReversalDate { get; set; }
        public decimal ReversalAmountVnd { get; set; }
        public string OriginalDeferredTaxCode { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu tạo hóa đơn điện tử (FCT)
    /// </summary>
    public class FctInvoiceRequest
    {
        public string InvoiceId { get; set; }
        public DateTime InvoiceDate { get; set; }
        public string SellerTaxCode { get; set; }
        public string BuyerTaxCode { get; set; }
        public decimal TotalBeforeVatVnd { get; set; }
        public decimal VatRate { get; set; }
        public decimal VatAmountVnd { get; set; }
        public string PaymentStatus { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu phân bổ chi phí trả trước (G04)
    /// </summary>
    public class PrepaidExpenseAllocationRequest
    {
        public string AllocationPeriodId { get; set; }
        public DateTime AllocationDate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu kiểm tra COA đầy đủ
    /// </summary>
    public class CoaValidationRequest
    {
        public string AccountCode { get; set; }
        public GL.Domain.Enums.AccountType AccountType { get; set; }
        public decimal DebitAmount { get; set; }
        public decimal CreditAmount { get; set; }
        public string ParentCode { get; set; }
    }

    /// <summary>
    /// Kết quả kiểm tra COA
    /// </summary>
    public class CoaValidationResult
    {
        public bool IsValid { get; set; }
        public string ErrorMessage { get; set; }
    }
}