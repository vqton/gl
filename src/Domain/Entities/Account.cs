using System;
using System.Collections.Generic;
using GL.Domain.Enums;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho một tài khoản kế toán trong hệ thống
    /// </summary>
    public class Account
    {
        /// <summary>
        /// Mã tài khoản (ví dụ: 111, 112, 211, etc.)
        /// </summary>
        public string Code { get; set; }

        /// <summary>
        /// Tên tài khoản
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Loại tài khoản (Asset, Liability, Equity, Revenue, Expense)
        /// </summary>
        public AccountType Type { get; set; }

        /// <summary>
        /// Số dư bình thường (Debit hoặc Credit)
        /// </summary>
        public string NormalBalance { get; set; }

        /// <summary>
        /// Mã tài khoản cha (null nếu là tài khoản gốc)
        /// </summary>
        public string ParentCode { get; set; }

        /// <summary>
        /// Danh sách tài khoản con
        /// </summary>
        public List<Account> Children { get; set; } = new List<Account>();

        /// <summary>
        /// Xác định xem tài khoản có thể được sử dụng để hạch toán không
        /// </summary>
        public bool AllowPosting => Children.Count == 0;

        /// <summary>
        /// Kiểm tra xem tài khoản có hợp lệ trước khi hạch toán không
        /// </summary>
        /// <returns>True nếu tài khoản hợp lệ để hạch toán</returns>
        public bool IsValidForPosting()
        {
            return !string.IsNullOrEmpty(Code) && 
                   !string.IsNullOrEmpty(Name) && 
                   Type != 0 &&
                   !string.IsNullOrEmpty(NormalBalance) &&
                   AllowPosting;
        }
    }
}