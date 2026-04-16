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

    /// <summary>
    /// DTO cho yêu cầu đốichiếu sao kê ngân hàng (B01)
    /// </summary>
    public class BankReconciliationRequest
    {
        public DateTime ReconciliationDate { get; set; }
        public string BankAccountCode { get; set; }
        public decimal BookBalance { get; set; }
        public decimal BankStatementBalance { get; set; }
        public string DifferenceReason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu chuyển khoản thanh toán (B02)
    /// </summary>
    public class WirePaymentRequest
    {
        public DateTime PaymentDate { get; set; }
        public string SupplierId { get; set; }
        public string SupplierName { get; set; }
        public decimal AmountVnd { get; set; }
        public decimal VatAmountVnd { get; set; }
        public string BankAccountCode { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu giải ngân vay ngân hàng (B03)
    /// </summary>
    public class LoanDrawdownRequest
    {
        public DateTime DrawdownDate { get; set; }
        public decimal LoanAmountVnd { get; set; }
        public string LoanAccountCode { get; set; }
        public string BankName { get; set; }
        public decimal InterestRate { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu trả nợ vay (B04)
    /// </summary>
    public class LoanRepaymentRequest
    {
        public DateTime RepaymentDate { get; set; }
        public decimal PrincipalAmountVnd { get; set; }
        public decimal InterestAmountVnd { get; set; }
        public string LoanAccountCode { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu phí ngân hàng (B05)
    /// </summary>
    public class BankFeeRequest
    {
        public DateTime FeeDate { get; set; }
        public decimal FeeAmountVnd { get; set; }
        public string FeeDescription { get; set; }
        public string ExpenseAccountCode { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu lãi tiền gửi (B06)
    /// </summary>
    public class InterestIncomeRequest
    {
        public DateTime InterestDate { get; set; }
        public decimal InterestAmountVnd { get; set; }
        public string BankAccountCode { get; set; }
        public decimal TaxWithheldVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu đánh giá lại ngoại hối (B07)
    /// </summary>
    public class FxRevaluationRequest
    {
        public DateTime RevaluationDate { get; set; }
        public string BankAccountCode { get; set; }
        public decimal OriginalAmountVnd { get; set; }
        public decimal NewAmountVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu mở LC (B07)
    /// </summary>
    public class LcOpeningRequest
    {
        public DateTime LcIssueDate { get; set; }
        public decimal LcAmountVnd { get; set; }
        public string BankName { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu thanh toán LC
    /// </summary>
    public class LcSettlementRequest
    {
        public DateTime SettlementDate { get; set; }
        public decimal OriginalLcAmountVnd { get; set; }
        public decimal PaymentAmountVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu nhập kho hàng mua (I01)
    /// </summary>
    public class InventoryReceiptRequest
    {
        public DateTime ReceiptDate { get; set; }
        public string InventoryAccount { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitPriceVnd { get; set; }
        public decimal VatRate { get; set; }
        public string SupplierId { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu xuất kho hàng bán/sử dụng (I02)
    /// </summary>
    public class InventoryIssueRequest
    {
        public DateTime IssueDate { get; set; }
        public string InventoryAccount { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCostVnd { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu chuyển kho nội bộ (I03)
    /// </summary>
    public class InventoryTransferRequest
    {
        public DateTime TransferDate { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCostVnd { get; set; }
        public string FromWarehouse { get; set; }
        public string ToWarehouse { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu kiểm kê hàng tồn kho (I04)
    /// </summary>
    public class InventoryCountRequest
    {
        public DateTime CountDate { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal BookQuantity { get; set; }
        public decimal ActualQuantity { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu đánh giá hàng tồn kho (I05)
    /// </summary>
    public class InventoryRevaluationRequest
    {
        public DateTime RevaluationDate { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal BookValueVnd { get; set; }
        public decimal MarketValueVnd { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu trích lập dự phòng (I06)
    /// </summary>
    public class InventoryProvisionRequest
    {
        public DateTime ProvisionDate { get; set; }
        public decimal ProvisionAmountVnd { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    /// <summary>
    /// DTO cho yêu cầu xử lý hàng hư hỏng (I07)
    /// </summary>
    public class InventoryWriteOffRequest
    {
        public DateTime WriteOffDate { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal WriteOffQuantity { get; set; }
        public decimal UnitCostVnd { get; set; }
        public decimal VatRecoverableVnd { get; set; }
        public string Reason { get; set; }
        public string AccountingPeriodId { get; set; }
    }

    // ============== COST ACCOUNTING DTOs (C01) ==============

    /// <summary>
    /// DTO cho chi phí nguyên vật liệu trực tiếp (C01a)
    /// </summary>
    public class DirectMaterialCostRequest
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public string WorkOrderId { get; set; }
        public string ProductId { get; set; }
        public decimal MaterialCostVnd { get; set; }
        public string InventoryAccount { get; set; }
    }

    /// <summary>
    /// DTO cho chi phí nhân công trực tiếp (C01b)
    /// </summary>
    public class DirectLaborCostRequest
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public string WorkOrderId { get; set; }
        public decimal LaborCostVnd { get; set; }
        public string SalaryAccount { get; set; }
    }

    /// <summary>
    /// DTO cho chi phí sản xuất chung (C01c)
    /// </summary>
    public class ManufacturingOverheadRequest
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public string WorkOrderId { get; set; }
        public decimal OverheadCostVnd { get; set; }
        public string OverheadAccount { get; set; }
    }

    /// <summary>
    /// DTO cho kết chuyển WIP (C01d)
    /// </summary>
    public class WIPClosingRequest
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public string WorkOrderId { get; set; }
        public decimal TotalWipCostVnd { get; set; }
    }

    /// <summary>
    /// DTO cho tính giá thành đơn vị (C01e)
    /// </summary>
    public class UnitCostCalculationRequest
    {
        public string ProductId { get; set; }
        public string AccountingPeriodId { get; set; }
        public decimal TotalCostVnd { get; set; }
        public int TotalQuantity { get; set; }
        public string Method { get; set; }
    }

    /// <summary>
    /// Kết quả tính giá thành đơn vị
    /// </summary>
    public class UnitCostResult
    {
        public string ProductId { get; set; }
        public string AccountingPeriodId { get; set; }
        public decimal UnitCostVnd { get; set; }
        public decimal TotalCostVnd { get; set; }
        public int TotalQuantity { get; set; }
    }

    /// <summary>
    /// DTO cho phân bổ chi phí SXC (C01f)
    /// </summary>
    public class OverheadAllocationRequest
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public decimal TotalOverheadVnd { get; set; }
        public string AllocationBase { get; set; }
    }

    /// <summary>
    /// Kết quả phân bổ chi phí SXC
    /// </summary>
    public class OverheadAllocationResult
    {
        public string TransactionId { get; set; }
        public string AccountingPeriodId { get; set; }
        public List<OverheadAllocation> Allocations { get; set; }
    }

    /// <summary>
    /// Mục phân bổ chi phí SXC
    /// </summary>
    public class OverheadAllocation
    {
        public string ProductId { get; set; }
        public decimal AllocatedAmount { get; set; }
    }

    // ============== SUBSIDIARY LEDGER DTOs (S01-S03) ==============

    // --- Accounts Receivable (131) ---

    public class CreateAREntryRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string CustomerId { get; set; }
        public decimal AmountVnd { get; set; }
        public decimal NetAmountVnd { get; set; }
        public decimal VatAmountVnd { get; set; }
    }

    public class UpdateARPaymentRequest
    {
        public string TransactionId { get; set; }
        public DateTime PaymentDate { get; set; }
        public string CustomerId { get; set; }
        public decimal PaymentAmountVnd { get; set; }
    }

    public class AginReport
    {
        public string CustomerId { get; set; }
        public DateTime ReportDate { get; set; }
        public List<AgingBucket> AgingDetails { get; set; }
    }

    public class AgingBucket
    {
        public string Bucket { get; set; }
        public decimal AmountVnd { get; set; }
    }

    public class CreateBadDebtProvisionRequest
    {
        public string TransactionId { get; set; }
        public DateTime ProvisionDate { get; set; }
        public decimal ProvisionAmountVnd { get; set; }
    }

    // --- Accounts Payable (331) ---

    public class CreateAPEntryRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string SupplierId { get; set; }
        public decimal AmountVnd { get; set; }
        public decimal VatAmountVnd { get; set; }
        public decimal TotalAmountVnd { get; set; }
    }

    public class UpdateAPPaymentRequest
    {
        public string TransactionId { get; set; }
        public DateTime PaymentDate { get; set; }
        public string SupplierId { get; set; }
        public decimal PaymentAmountVnd { get; set; }
    }

    // --- Inventory (156) ---

    public class UpdateInventoryCardRequest
    {
        public string TransactionId { get; set; }
        public DateTime TransactionDate { get; set; }
        public string ProductId { get; set; }
        public string ProductName { get; set; }
        public string TransactionType { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCostVnd { get; set; }
    }

    public class CalculateIssueCostRequest
    {
        public string ProductId { get; set; }
        public string Method { get; set; }
    }

    // ============== AUDIT TRAIL DTOs (AT01-AT03) ==============

    public class CreateAuditLogRequest
    {
        public string UserId { get; set; }
        public string Action { get; set; }
        public string TableName { get; set; }
        public string RecordId { get; set; }
        public string OldValues { get; set; }
        public string NewValues { get; set; }
        public string IpAddress { get; set; }
        public string Reason { get; set; }
    }

    public class AuditLogResult
    {
        public Guid Id { get; set; }
        public string UserId { get; set; }
        public DateTime Timestamp { get; set; }
        public string Action { get; set; }
        public string TableName { get; set; }
        public string RecordId { get; set; }
        public string OldValues { get; set; }
        public string NewValues { get; set; }
        public string IpAddress { get; set; }
    }

    public class QueryAuditRequest
    {
        public string RecordId { get; set; }
        public string UserId { get; set; }
        public string TableName { get; set; }
        public DateTime? StartDate { get; set; }
        public DateTime? EndDate { get; set; }
    }

    public class AuditReportResult
    {
        public string PeriodId { get; set; }
        public DateTime GeneratedAt { get; set; }
        public int TotalEntries { get; set; }
        public List<AuditLogResult> Entries { get; set; }
    }

    // ============== PERIOD LOCKING DTOs (PL01-PL03) ==============

    public class OpenPeriodRequest
    {
        public string PeriodId { get; set; }
        public string RequestedBy { get; set; }
    }

    public class ClosePeriodRequest
    {
        public string PeriodId { get; set; }
        public string RequestedBy { get; set; }
        public string Reason { get; set; }
    }

    public class ValidatePeriodRequest
    {
        public string PeriodId { get; set; }
    }

    public class PeriodValidationResult
    {
        public bool IsValid { get; set; }
        public string Message { get; set; }
        public string Status { get; set; }
    }
}