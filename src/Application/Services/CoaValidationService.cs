using GL.Application.DTOs;
using GL.Domain.Entities;
using GL.Domain.Enums;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kiểm tra và xác thực tài khoản kế toán (COA)
    /// </summary>
    public class CoaValidationService
    {
        private static readonly Dictionary<string, Account> _coaCache;

        static CoaValidationService()
        {
            _coaCache = ChartOfAccounts.GetAllAccounts().ToDictionary(a => a.Code);
        }

        /// <summary>
        /// Kiểm tra mã tài khoản có đúng định dạng không
        /// </summary>
        /// <param name="accountCode">Mã tài khoản</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateAccountCode(string accountCode)
        {
            if (string.IsNullOrEmpty(accountCode))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = "Account code cannot be empty" };
            }

            if (accountCode.Length < 3 || accountCode.Length > 4)
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = "Account code must be 3-4 digits" };
            }

            if (!accountCode.All(char.IsDigit))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = "Account code must be numeric" };
            }

            if (accountCode.StartsWith("0"))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = "Account code cannot start with zero" };
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }

        /// <summary>
        /// Kiểm tra tài khoản có tồn tại trong danh mục không
        /// </summary>
        /// <param name="accountCode">Mã tài khoản</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateAccountExists(string accountCode)
        {
            if (_coaCache.ContainsKey(accountCode))
            {
                return new CoaValidationResult { IsValid = true, ErrorMessage = null };
            }

            return new CoaValidationResult { IsValid = false, ErrorMessage = $"Account {accountCode} not found in Chart of Accounts" };
        }

        /// <summary>
        /// Kiểm tra loại tài khoản có khớp không
        /// </summary>
        /// <param name="accountCode">Mã tài khoản</param>
        /// <param name="expectedType">Loại tài khoản mong đợi</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateAccountType(string accountCode, AccountType expectedType)
        {
            if (!_coaCache.TryGetValue(accountCode, out var account))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Account {accountCode} not found" };
            }

            if (account.Type != expectedType)
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Account type mismatch: expected {expectedType}, got {account.Type}" };
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }

        /// <summary>
        /// Kiểm tra quan hệ cha-con giữa các tài khoản
        /// </summary>
        /// <param name="parentCode">Mã tài khoản cha</param>
        /// <param name="childCode">Mã tài khoản con</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateParentChild(string parentCode, string childCode)
        {
            if (!_coaCache.ContainsKey(parentCode))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Parent account {parentCode} not found" };
            }

            if (!childCode.StartsWith(parentCode))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Child account {childCode} does not belong to parent {parentCode}" };
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }

        /// <summary>
        /// Kiểm tra tài khoản có thể ghi sổ không (cấp 3-4 theo TT99)
        /// </summary>
        public CoaValidationResult ValidateAccountIsPostable(string accountCode)
        {
            if (!_coaCache.TryGetValue(accountCode, out var account))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Account {accountCode} not found" };
            }

            if (!account.IsPostable)
            {
                return new CoaValidationResult { 
                    IsValid = false, 
                    ErrorMessage = $"Account {accountCode} ({account.Name}) is not postable. Only level 3-4 accounts can be used for journaling." 
                };
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }

        /// <summary>
        /// Kiểm tra chiều số dư bình thường có đúng không
        /// </summary>
        /// <param name="accountCode">Mã tài khoản</param>
        /// <param name="debitAmount">Số tiền nợ</param>
        /// <param name="creditAmount">Số tiền có</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateNormalBalance(string accountCode, decimal debitAmount, decimal creditAmount)
        {
            if (!_coaCache.TryGetValue(accountCode, out var account))
            {
                return new CoaValidationResult { IsValid = false, ErrorMessage = $"Account {accountCode} not found" };
            }

            bool isDebitNormal = account.NormalBalance == "Debit";

            if (isDebitNormal)
            {
                if (creditAmount > 0 && debitAmount == 0)
                {
                    return new CoaValidationResult { IsValid = false, ErrorMessage = "Cannot credit to debit-normal account" };
                }
            }
            else
            {
                if (debitAmount > 0 && creditAmount == 0)
                {
                    return new CoaValidationResult { IsValid = false, ErrorMessage = "Cannot debit to credit-normal account" };
                }
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }

        /// <summary>
        /// Kiểm tra đầy đủ tất cả các quy tắc COA
        /// </summary>
        /// <param name="request">Yêu cầu kiểm tra COA</param>
        /// <returns>Kết quả kiểm tra</returns>
        public CoaValidationResult ValidateFullAccount(CoaValidationRequest request)
        {
            var codeResult = ValidateAccountCode(request.AccountCode);
            if (!codeResult.IsValid) return codeResult;

            var existsResult = ValidateAccountExists(request.AccountCode);
            if (!existsResult.IsValid) return existsResult;

            var typeResult = ValidateAccountType(request.AccountCode, request.AccountType);
            if (!typeResult.IsValid) return typeResult;

            var balanceResult = ValidateNormalBalance(request.AccountCode, request.DebitAmount, request.CreditAmount);
            if (!balanceResult.IsValid) return balanceResult;

            if (!string.IsNullOrEmpty(request.ParentCode))
            {
                var parentResult = ValidateParentChild(request.ParentCode, request.AccountCode);
                if (!parentResult.IsValid) return parentResult;
            }

            return new CoaValidationResult { IsValid = true, ErrorMessage = null };
        }
    }
}