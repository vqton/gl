using System;
using System.Collections.Generic;

namespace GL.Application.DTOs
{
    #region TAX DTOs (X01-X05) - Thue

    /// <summary>
    /// Yêu cầu kê khai và nộp thuế GTGT
    /// </summary>
    /// <remarks>X01 - Tờ khai thuế GTGT</remarks>
    public sealed record VatDeclarationRequest(
        string DeclarationPeriodId,
        DateTime DeclarationDate,
        decimal OutputVatTotal,
        decimal InputVatTotal,
        string PaymentMethod,
        string BankAccountId,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu hạch toán chi phí thuế TNDN
    /// </summary>
    /// <remarks>X02 - Chi phí thuế TNDN</remarks>
    public sealed record CitTaxRequest(
        string TaxPeriodId,
        DateTime CalculationDate,
        decimal TaxableIncomeVnd,
        decimal CitRate,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu hạch toán và nộp thuế TNCN
    /// </summary>
    /// <remarks>X03 - Thuế TNCN khấu trừ</remarks>
    public sealed record PitTaxRequest(
        string PayrollPeriodId,
        DateTime WithholdingDate,
        decimal TotalPitWithheldVnd,
        DateTime PaymentDate,
        string BankAccountId,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu hạch toán VAT đầu vào không được khấu trừ
    /// </summary>
    /// <remarks>X04 - VAT không được khấu trừ</remarks>
    public sealed record UnrecoverableVatRequest(
        string InvoiceId,
        DateTime RecognitionDate,
        decimal VatAmountVnd,
        string ExpenseAccountCode,
        string Reason,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu ghi nhận thuế TNDN hoãn lại
    /// </summary>
    /// <remarks>X05 - Thuế hoãn lại</remarks>
    public sealed record DeferredTaxRequest(
        string FiscalYearId,
        DateTime RecognitionDate,
        decimal DeferredTaxAssetVnd,
        string TaxCode,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu đảo thuế TNDN hoãn lại
    /// </summary>
    public sealed record DeferredTaxReversalRequest(
        DateTime ReversalDate,
        decimal ReversalAmountVnd,
        string OriginalDeferredTaxCode,
        string Reason,
        string AccountingPeriodId
    );

    #endregion

    #region PAYROLL DTOs (L01-L07) - Tien luong

    /// <summary>
    /// Yêu cầu tính lương và các khoản phải trả NLĐ
    /// </summary>
    /// <remarks>L01 - Tính lương</remarks>
    public sealed record PayrollCalculationRequest(
        string PayrollId,
        DateTime PayrollMonth,
        decimal TotalGrossVnd,
        decimal EmployeeDeductionsVnd,
        decimal NetPayVnd,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu trích bảo hiểm xã hội phần doanh nghiệp
    /// </summary>
    /// <remarks>L02 - Trích BHXH doanh nghiệp</remarks>
    public sealed record SocialInsuranceRequest(
        string PayrollId,
        DateTime CalculationDate,
        decimal Bhxh175,
        decimal Bhyt30,
        decimal Bhtn10,
        decimal Kpcd20,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu chi lương cho người lao động
    /// </summary>
    /// <remarks>L03 - Chi lương</remarks>
    public sealed record PayrollPaymentRequest(
        string PaymentBatchId,
        DateTime PaymentDate,
        decimal TotalNetPayVnd,
        string PaymentMethod,
        string BankTransferFileRef,
        string AccountingPeriodId
    );

    #endregion

    #region FIXED ASSETS DTOs (A01-A06) - Tai san co dinh

    /// <summary>
    /// Yêu cầu mua tài sản cố định
    /// </summary>
    /// <remarks>A01 - Mua TSCĐ</remarks>
    public sealed record FixedAssetPurchaseRequest(
        string AssetHandoverId,
        DateTime HandoverDate,
        string AssetType,
        decimal OriginalCostVnd,
        decimal VatAmountVnd,
        string SupplierId,
        string PaymentMethod,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu trích khấu hao TSCĐ hàng tháng
    /// </summary>
    /// <remarks>A02 - Khấu hao TSCĐ</remarks>
    public sealed record DepreciationRequest(
        string DepreciationPeriodId,
        DateTime CalculationDate,
        string AccountingPeriodId
    );

    #endregion

    #region PERIOD CLOSING DTOs (G01-G04) - Ket chuyen

    /// <summary>
    /// Yêu cầu kết chuyển doanh thu
    /// </summary>
    /// <remarks>G01 - Kết chuyển doanh thu</remarks>
    public sealed record RevenueClosingRequest(
        string ClosingPeriodId,
        DateTime ClosingDate,
        decimal Revenue511,
        decimal Revenue515,
        decimal Revenue711,
        decimal ContraRevenue521,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu kết chuyển chi phí
    /// </summary>
    /// <remarks>G02 - Kết chuyển chi phí</remarks>
    public sealed record ExpenseClosingRequest(
        string ClosingPeriodId,
        DateTime ClosingDate,
        decimal Expense632,
        decimal Expense635,
        decimal Expense641,
        decimal Expense642,
        decimal Expense811,
        decimal Expense821,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu kết chuyển lợi nhuận sau thuế
    /// </summary>
    /// <remarks>G03 - Kết chuyển lợi nhuận</remarks>
    public sealed record ProfitClosingRequest(
        string FiscalYearId,
        DateTime ClosingDate,
        decimal ProfitAfterTaxVnd,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu phân bổ chi phí trả trước
    /// </summary>
    /// <remarks>G04 - Phân bổ CPPT</remarks>
    public sealed record PrepaidExpenseAllocationRequest(
        string AllocationPeriodId,
        DateTime AllocationDate,
        string AccountingPeriodId
    );

    #endregion

    #region BANK DTOs (B01-B08) - Ngan hang

    /// <summary>
    /// Yêu cầu đối chiếu sao kê ngân hàng
    /// </summary>
    /// <remarks>B01 - Đối chiếu NH</remarks>
    public sealed record BankReconciliationRequest(
        DateTime ReconciliationDate,
        string BankAccountCode,
        decimal BookBalance,
        decimal BankStatementBalance,
        string DifferenceReason,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu chuyển khoản thanh toán
    /// </summary>
    /// <remarks>B02 - Chuyển khoản</remarks>
    public sealed record WirePaymentRequest(
        DateTime PaymentDate,
        string SupplierId,
        string SupplierName,
        decimal AmountVnd,
        decimal VatAmountVnd,
        string BankAccountCode,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu giải ngân vay ngân hàng
    /// </summary>
    /// <remarks>B03 - Giải ngân</remarks>
    public sealed record LoanDrawdownRequest(
        DateTime DrawdownDate,
        decimal LoanAmountVnd,
        string LoanAccountCode,
        string BankName,
        decimal InterestRate,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu trả nợ vay
    /// </summary>
    /// <remarks>B04 - Trả nợ vay</remarks>
    public sealed record LoanRepaymentRequest(
        DateTime RepaymentDate,
        decimal PrincipalAmountVnd,
        decimal InterestAmountVnd,
        string LoanAccountCode,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu phí ngân hàng
    /// </summary>
    /// <remarks>B05 - Phí NH</remarks>
    public sealed record BankFeeRequest(
        DateTime FeeDate,
        decimal FeeAmountVnd,
        string FeeDescription,
        string ExpenseAccountCode,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu lãi tiền gửi
    /// </summary>
    /// <remarks>B06 - Lãi tiền gửi</remarks>
    public sealed record InterestIncomeRequest(
        DateTime InterestDate,
        decimal InterestAmountVnd,
        string BankAccountCode,
        decimal TaxWithheldVnd,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu đánh giá lại ngoại hối
    /// </summary>
    /// <remarks>B07 - Đánh giá FX</remarks>
    public sealed record FxRevaluationRequest(
        DateTime RevaluationDate,
        string BankAccountCode,
        decimal OriginalAmountVnd,
        decimal NewAmountVnd,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu mở LC
    /// </summary>
    /// <remarks>B08 - Mở LC</remarks>
    public sealed record LcOpeningRequest(
        DateTime LcIssueDate,
        decimal LcAmountVnd,
        string BankName,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu thanh toán LC
    /// </summary>
    public sealed record LcSettlementRequest(
        DateTime SettlementDate,
        decimal OriginalLcAmountVnd,
        decimal PaymentAmountVnd,
        string AccountingPeriodId
    );

    #endregion

    #region INVENTORY DTOs (I01-I07) - Ton kho

    /// <summary>
    /// Yêu cầu nhập kho hàng mua
    /// </summary>
    /// <remarks>I01 - Nhập kho</remarks>
    public sealed record InventoryReceiptRequest(
        DateTime ReceiptDate,
        string InventoryAccount,
        string ProductId,
        string ProductName,
        decimal Quantity,
        decimal UnitPriceVnd,
        decimal VatRate,
        string SupplierId,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu xuất kho hàng bán/sử dụng
    /// </summary>
    /// <remarks>I02 - Xuất kho</remarks>
    public sealed record InventoryIssueRequest(
        DateTime IssueDate,
        string InventoryAccount,
        string ProductId,
        string ProductName,
        decimal Quantity,
        decimal UnitCostVnd,
        string Reason,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu chuyển kho nội bộ
    /// </summary>
    /// <remarks>I03 - Chuyển kho</remarks>
    public sealed record InventoryTransferRequest(
        DateTime TransferDate,
        string ProductId,
        string ProductName,
        decimal Quantity,
        decimal UnitCostVnd,
        string FromWarehouse,
        string ToWarehouse,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu kiểm kê hàng tồn kho
    /// </summary>
    /// <remarks>I04 - Kiểm kê</remarks>
    public sealed record InventoryCountRequest(
        DateTime CountDate,
        string ProductId,
        string ProductName,
        decimal BookQuantity,
        decimal ActualQuantity,
        string Reason,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu đánh giá hàng tồn kho
    /// </summary>
    /// <remarks>I05 - Đánh giá</remarks>
    public sealed record InventoryRevaluationRequest(
        DateTime RevaluationDate,
        string ProductId,
        string ProductName,
        decimal BookValueVnd,
        decimal MarketValueVnd,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu trích lập dự phòng
    /// </summary>
    /// <remarks>I06 - Dự phòng</remarks>
    public sealed record InventoryProvisionRequest(
        DateTime ProvisionDate,
        decimal ProvisionAmountVnd,
        string Reason,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu xử lý hàng hư hỏng
    /// </summary>
    /// <remarks>I07 - Xử lý hàng</remarks>
    public sealed record InventoryWriteOffRequest(
        DateTime WriteOffDate,
        string ProductId,
        string ProductName,
        decimal WriteOffQuantity,
        decimal UnitCostVnd,
        decimal VatRecoverableVnd,
        string Reason,
        string AccountingPeriodId
    );

    #endregion

    #region COST ACCOUNTING DTOs (C01) - Gia thanh

    /// <summary>
    /// Yêu cầu chi phí nguyên vật liệu trực tiếp
    /// </summary>
    public sealed record DirectMaterialCostRequest(
        string TransactionId,
        string AccountingPeriodId,
        string WorkOrderId,
        string ProductId,
        decimal MaterialCostVnd,
        string InventoryAccount
    );

    /// <summary>
    /// Yêu cầu chi phí nhân công trực tiếp
    /// </summary>
    public sealed record DirectLaborCostRequest(
        string TransactionId,
        string AccountingPeriodId,
        string WorkOrderId,
        decimal LaborCostVnd,
        string SalaryAccount
    );

    /// <summary>
    /// Yêu cầu chi phí sản xuất chung
    /// </summary>
    public sealed record ManufacturingOverheadRequest(
        string TransactionId,
        string AccountingPeriodId,
        string WorkOrderId,
        decimal OverheadCostVnd,
        string OverheadAccount
    );

    /// <summary>
    /// Yêu cầu kết chuyển WIP
    /// </summary>
    public sealed record WIPClosingRequest(
        string TransactionId,
        string AccountingPeriodId,
        string WorkOrderId,
        decimal TotalWipCostVnd
    );

    /// <summary>
    /// Yêu cầu tính giá thành đơn vị
    /// </summary>
    public sealed record UnitCostCalculationRequest(
        string ProductId,
        string AccountingPeriodId,
        decimal TotalCostVnd,
        int TotalQuantity,
        string Method
    );

    /// <summary>
    /// Kết quả tính giá thành đơn vị
    /// </summary>
    public sealed record UnitCostResult(
        string ProductId,
        string AccountingPeriodId,
        decimal UnitCostVnd,
        decimal TotalCostVnd,
        int TotalQuantity
    );

    /// <summary>
    /// Yêu cầu phân bổ chi phí SXC
    /// </summary>
    public sealed record OverheadAllocationRequest(
        string TransactionId,
        string AccountingPeriodId,
        decimal TotalOverheadVnd,
        string AllocationBase
    );

    /// <summary>
    /// Kết quả phân bổ chi phí SXC
    /// </summary>
    public sealed record OverheadAllocationResult(
        string TransactionId,
        string AccountingPeriodId,
        List<OverheadAllocationItem> Allocations
    );

    /// <summary>
    /// Mục phân bổ chi phí SXC
    /// </summary>
    public sealed record OverheadAllocationItem(
        string ProductId,
        decimal AllocatedAmount
    );

    #endregion

    #region SUBSIDIARY LEDGER DTOs (S01-S03) - So chi tiet

    // --- Accounts Receivable (131) ---

    /// <summary>
    /// Yêu cầu tạo dòng phải thu (131)
    /// </summary>
    public sealed record CreateAREntryRequest(
        string TransactionId,
        DateTime TransactionDate,
        string CustomerId,
        decimal AmountVnd,
        decimal NetAmountVnd,
        decimal VatAmountVnd
    );

    /// <summary>
    /// Yêu cầu cập nhật thanh toán phải thu
    /// </summary>
    public sealed record UpdateARPaymentRequest(
        string TransactionId,
        DateTime PaymentDate,
        string CustomerId,
        decimal PaymentAmountVnd
    );

    /// <summary>
    /// Báo cáo công nợ phải thu theo kỳ hạn
    /// </summary>
    public sealed record AgingReport(
        string CustomerId,
        DateTime ReportDate,
        List<AgingBucketItem> AgingDetails
    );

    /// <summary>
    /// Khoản công nợ theo kỳ hạn
    /// </summary>
    public sealed record AgingBucketItem(
        string Bucket,
        decimal AmountVnd
    );

    /// <summary>
    /// Yêu cầu trích lập dự phòng phải thu khó đòi
    /// </summary>
    public sealed record CreateBadDebtProvisionRequest(
        string TransactionId,
        DateTime ProvisionDate,
        decimal ProvisionAmountVnd
    );

    // --- Accounts Payable (331) ---

    /// <summary>
    /// Yêu cầu tạo dòng phải trả (331)
    /// </summary>
    public sealed record CreateAPEntryRequest(
        string TransactionId,
        DateTime TransactionDate,
        string SupplierId,
        decimal AmountVnd,
        decimal VatAmountVnd,
        decimal TotalAmountVnd
    );

    /// <summary>
    /// Yêu cầu cập nhật thanh toán phải trả
    /// </summary>
    public sealed record UpdateAPPaymentRequest(
        string TransactionId,
        DateTime PaymentDate,
        string SupplierId,
        decimal PaymentAmountVnd
    );

    // --- Inventory (156) ---

    /// <summary>
    /// Yêu cầu cập nhật thẻ kho (156)
    /// </summary>
    public sealed record UpdateInventoryCardRequest(
        string TransactionId,
        DateTime TransactionDate,
        string ProductId,
        string ProductName,
        string TransactionType,
        decimal Quantity,
        decimal UnitCostVnd
    );

    /// <summary>
    /// Yêu cầu tính giá xuất kho
    /// </summary>
    public sealed record CalculateIssueCostRequest(
        string ProductId,
        string Method
    );

    #endregion

    #region AUDIT TRAIL DTOs (AT01-AT03) - Kiem toan

    /// <summary>
    /// Yêu cầu tạo log kiểm toán
    /// </summary>
    public sealed record CreateAuditLogRequest(
        string UserId,
        string Action,
        string TableName,
        string RecordId,
        string? OldValues,
        string? NewValues,
        string? IpAddress,
        string? Reason
    );

    /// <summary>
    /// Kết quả log kiểm toán
    /// </summary>
    public sealed record AuditLogResult(
        Guid Id,
        string UserId,
        DateTime Timestamp,
        string Action,
        string TableName,
        string RecordId,
        string? OldValues,
        string? NewValues,
        string? IpAddress
    );

    /// <summary>
    /// Yêu cầu truy vấn audit trail
    /// </summary>
    public sealed record QueryAuditRequest(
        string? RecordId,
        string? UserId,
        string? TableName,
        DateTime? StartDate,
        DateTime? EndDate
    );

    /// <summary>
    /// Kết quả báo cáo audit
    /// </summary>
    public sealed record AuditReportResult(
        string? PeriodId,
        DateTime GeneratedAt,
        int TotalEntries,
        List<AuditLogResult> Entries
    );

    #endregion

    #region PERIOD LOCKING DTOs (PL01-PL03) - Khoa ky

    /// <summary>
    /// Yêu cầu mở kỳ kế toán
    /// </summary>
    public sealed record OpenPeriodRequest(
        string PeriodId,
        string RequestedBy
    );

    /// <summary>
    /// Yêu cầu đóng kỳ kế toán
    /// </summary>
    public sealed record ClosePeriodRequest(
        string PeriodId,
        string RequestedBy,
        string? Reason
    );

    /// <summary>
    /// Yêu cầu kiểm tra kỳ kế toán
    /// </summary>
    public sealed record ValidatePeriodRequest(
        string PeriodId
    );

    /// <summary>
    /// Kết quả kiểm tra kỳ kế toán
    /// </summary>
    public sealed record PeriodValidationResult(
        bool IsValid,
        string Message,
        string Status
    );

    #endregion

    #region GENERAL DTOs - Chung

    /// <summary>
    /// Yêu cầu tạo hóa đơn điện tử (FCT)
    /// </summary>
    public sealed record FctInvoiceRequest(
        string InvoiceId,
        DateTime InvoiceDate,
        string SellerTaxCode,
        string BuyerTaxCode,
        decimal TotalBeforeVatVnd,
        decimal VatRate,
        decimal VatAmountVnd,
        string PaymentStatus,
        string AccountingPeriodId
    );

    /// <summary>
    /// Yêu cầu kiểm tra COA đầy đủ
    /// </summary>
    public sealed record CoaValidationRequest(
        string AccountCode,
        GL.Domain.Enums.AccountType AccountType,
        decimal DebitAmount,
        decimal CreditAmount,
        string? ParentCode
    );

    /// <summary>
    /// Kết quả kiểm tra COA
    /// </summary>
    public sealed record CoaValidationResult(
        bool IsValid,
        string? ErrorMessage
    );

    #endregion
}