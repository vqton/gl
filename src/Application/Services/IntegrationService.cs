using GL.Domain.Entities;
using GL.Domain.Enums;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tích hợp các module kế toán (Phase 3)
    /// Kết nối Tax, Payroll, Fixed Assets, Period Closing modules
    /// </summary>
    public class IntegrationService
    {
        private readonly TransactionService _transactionService;
        private readonly AuditTrailService _auditTrailService;

        public IntegrationService()
        {
            _transactionService = new TransactionService();
            _auditTrailService = new AuditTrailService();
        }

        /// <summary>
        /// Tích hợp quy trình bán hàng hoàn chỉnh
        /// </summary>
        public Transaction ProcessSaleTransaction(string customerAccount, decimal amount, decimal vatRate, DateTime date, string description)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = date,
                Description = description
            };

            decimal vatAmount = amount * vatRate;
            decimal totalAmount = amount + vatAmount;

            transaction.AddLine(customerAccount, totalAmount, 0, "Phải thu khách hàng");
            transaction.AddLine("511", 0, amount, "Doanh thu bán hàng");
            transaction.AddLine("3331", 0, vatAmount, "VAT đầu ra");

            _auditTrailService.LogPost(transaction, "SYSTEM");

            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình mua hàng hoàn chỉnh
        /// </summary>
        public Transaction ProcessPurchaseTransaction(string supplierAccount, decimal amount, decimal vatRate, DateTime date, string description)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = date,
                Description = description
            };

            decimal vatAmount = amount * vatRate;
            decimal totalAmount = amount + vatAmount;

            transaction.AddLine("156", amount, 0, "Hàng hóa");
            transaction.AddLine("1331", vatAmount, 0, "VAT đầu vào");
            transaction.AddLine(supplierAccount, 0, totalAmount, "Phải trả người bán");

            _auditTrailService.LogPost(transaction, "SYSTEM");

            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình thu tiền
        /// </summary>
        public Transaction ProcessCashReceipt(string customerAccount, decimal amount, DateTime date, string description)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = date,
                Description = description
            };

            transaction.AddLine("111", amount, 0, "Tiền mặt");
            transaction.AddLine(customerAccount, 0, amount, "Thu tiền");

            _auditTrailService.LogPost(transaction, "SYSTEM");

            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình chi tiền
        /// </summary>
        public Transaction ProcessCashPayment(string supplierAccount, decimal amount, DateTime date, string description)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = date,
                Description = description
            };

            transaction.AddLine(supplierAccount, amount, 0, "Chi tiền");
            transaction.AddLine("111", 0, amount, "Tiền mặt");

            _auditTrailService.LogPost(transaction, "SYSTEM");

            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình tính lương và các khoản phải trả
        /// </summary>
        public Transaction ProcessPayroll(DTOs.PayrollCalculationRequest request)
        {
            var transaction = _transactionService.CreatePayrollEntry(request);
            _auditTrailService.LogPost(transaction, "SYSTEM");
            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình khấu hao TSCĐ
        /// </summary>
        public Transaction ProcessDepreciation(DTOs.DepreciationRequest request, decimal totalDepreciation, string department)
        {
            var transaction = _transactionService.CreateDepreciationEntry(request, totalDepreciation, department);
            _auditTrailService.LogPost(transaction, "SYSTEM");
            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình kết chuyển cuối kỳ
        /// </summary>
        public List<Transaction> ProcessPeriodClosing(string periodCode, DateTime closingDate, decimal revenue511, decimal revenue515, decimal revenue711, decimal contraRevenue521, decimal expense632, decimal expense635, decimal expense641, decimal expense642, decimal expense811, decimal expense821)
        {
            var transactions = new List<Transaction>();

            var revenueRequest = new DTOs.RevenueClosingRequest
            {
                ClosingPeriodId = periodCode,
                ClosingDate = closingDate,
                Revenue511 = revenue511,
                Revenue515 = revenue515,
                Revenue711 = revenue711,
                ContraRevenue521 = contraRevenue521,
                AccountingPeriodId = periodCode
            };
            var revenueTransaction = _transactionService.CreateRevenueClosingEntry(revenueRequest);
            transactions.Add(revenueTransaction);

            var expenseRequest = new DTOs.ExpenseClosingRequest
            {
                ClosingPeriodId = periodCode,
                ClosingDate = closingDate,
                Expense632 = expense632,
                Expense635 = expense635,
                Expense641 = expense641,
                Expense642 = expense642,
                Expense811 = expense811,
                Expense821 = expense821,
                AccountingPeriodId = periodCode
            };
            var expenseTransaction = _transactionService.CreateExpenseClosingEntry(expenseRequest);
            transactions.Add(expenseTransaction);

            foreach (var txn in transactions)
            {
                _auditTrailService.LogPost(txn, "SYSTEM");
            }

            return transactions;
        }

        /// <summary>
        /// Tích hợp quy trình kê khai thuế GTGT
        /// </summary>
        public Transaction ProcessVatDeclaration(DTOs.VatDeclarationRequest request)
        {
            var transaction = _transactionService.CreateVatDeclarationEntry(request);
            _auditTrailService.LogPost(transaction, "SYSTEM");
            return transaction;
        }

        /// <summary>
        /// Tích hợp quy trình mua TSCĐ
        /// </summary>
        public Transaction ProcessFixedAssetPurchase(DTOs.FixedAssetPurchaseRequest request)
        {
            var transaction = _transactionService.CreateFixedAssetPurchaseEntry(request);
            _auditTrailService.LogPost(transaction, "SYSTEM");
            return transaction;
        }

        /// <summary>
        /// Lấy lịch sử audit của một giao dịch
        /// </summary>
        public List<AuditEntry> GetTransactionAuditHistory(string transactionId)
        {
            return _auditTrailService.GetEntriesByTransactionId(transactionId);
        }

        /// <summary>
        /// Xác nhận bút toán hợp lệ trước khi ghi sổ
        /// </summary>
        public (bool IsValid, string Message) ValidateTransaction(Transaction transaction)
        {
            if (!transaction.IsBalanced)
            {
                return (false, "Bút toán không cân bằng");
            }

            if (transaction.Lines.Count < 2)
            {
                return (false, "Bút toán phải có ít nhất 2 dòng");
            }

            foreach (var line in transaction.Lines)
            {
                var account = ChartOfAccounts.GetAllAccounts()
                    .FirstOrDefault(a => a.Code == line.AccountCode);

                if (account == null)
                {
                    return (false, $"Tài khoản {line.AccountCode} không tồn tại trong danh mục");
                }

                if (!account.AllowPosting)
                {
                    return (false, $"Tài khoản {line.AccountCode} không được phép hạch toán");
                }
            }

            return (true, "Bút toán hợp lệ");
        }
    }
}
