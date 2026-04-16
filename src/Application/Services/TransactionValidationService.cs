using GL.Domain.Entities;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ xác thực bút toán trước khi ghi sổ
    /// Kiểm tra tất cả tài khoản trong bút toán theo TT99/2025
    /// </summary>
    public class TransactionValidationService
    {
        private readonly CoaValidationService _coaService = new CoaValidationService();

        /// <summary>
        /// Kiểm tra toàn bộ bút toán trước khi ghi sổ
        /// </summary>
        public TransactionValidationResult ValidateTransaction(Transaction transaction)
        {
            var result = new TransactionValidationResult
            {
                IsValid = true,
                Errors = new List<string>()
            };

            if (transaction.Lines == null || transaction.Lines.Count == 0)
            {
                result.IsValid = false;
                result.Errors.Add("Transaction has no lines");
                return result;
            }

            // Check transaction is balanced
            if (!transaction.IsBalanced)
            {
                result.IsValid = false;
                result.Errors.Add("Transaction is not balanced (total debit != total credit)");
            }

            // Validate each line
            foreach (var line in transaction.Lines)
            {
                // Validate account code format
                var codeResult = _coaService.ValidateAccountCode(line.AccountCode);
                if (!codeResult.IsValid)
                {
                    result.IsValid = false;
                    result.Errors.Add($"Line [{line.AccountCode}]: {codeResult.ErrorMessage}");
                    continue;
                }

                // Validate account exists
                var existsResult = _coaService.ValidateAccountExists(line.AccountCode);
                if (!existsResult.IsValid)
                {
                    result.IsValid = false;
                    result.Errors.Add($"Line [{line.AccountCode}]: {existsResult.ErrorMessage}");
                    continue;
                }

                // Validate account is postable (level 3-4)
                var postableResult = _coaService.ValidateAccountIsPostable(line.AccountCode);
                if (!postableResult.IsValid)
                {
                    result.IsValid = false;
                    result.Errors.Add($"Line [{line.AccountCode}]: {postableResult.ErrorMessage}");
                }
            }

            // Check minimum lines (at least 2 lines for double-entry)
            if (transaction.Lines.Count < 2)
            {
                result.IsValid = false;
                result.Errors.Add("Transaction must have at least 2 lines (double-entry)");
            }

            return result;
        }

        /// <summary>
        /// Kiểm tra một tài khoản đơn lẻ có hợp lệ không
        /// </summary>
        public bool IsValidAccountCode(string accountCode)
        {
            var codeResult = _coaService.ValidateAccountCode(accountCode);
            if (!codeResult.IsValid) return false;

            var existsResult = _coaService.ValidateAccountExists(accountCode);
            if (!existsResult.IsValid) return false;

            var postableResult = _coaService.ValidateAccountIsPostable(accountCode);
            return postableResult.IsValid;
        }

        /// <summary>
        /// Lấy thông tin tài khoản
        /// </summary>
        public Account GetAccountInfo(string accountCode)
        {
            var accounts = ChartOfAccounts.GetAllAccounts();
            return accounts.FirstOrDefault(a => a.Code == accountCode);
        }
    }

    /// <summary>
    /// Kết quả kiểm tra bút toán
    /// </summary>
    public class TransactionValidationResult
    {
        public bool IsValid { get; set; }
        public List<string> Errors { get; set; }
        public string Summary => IsValid ? "Valid" : $"{Errors.Count} error(s) found";
    }
}