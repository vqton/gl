using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho một giao dịch kế toán (sổ chung) trong hệ thống
    /// </summary>
    public class Transaction
    {
        /// <summary>
        /// Mã giao dịch (số chứng từ)
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Ngày giao dịch
        /// </summary>
        public DateTime Date { get; set; }

        /// <summary>
        /// Diễn giải giao dịch
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Danh sách các dòng帳 trong giao dịch
        /// </summary>
        public List<TransactionLine> Lines { get; set; } = new List<TransactionLine>();

        /// <summary>
        /// Xác định xem giao dịch có cân bằng không (tổng nợ = tổng có)
        /// </summary>
        public bool IsBalanced
        {
            get
            {
                decimal totalDebit = 0;
                decimal totalCredit = 0;

                foreach (var line in Lines)
                {
                    totalDebit += line.DebitAmount;
                    totalCredit += line.CreditAmount;
                }

                return Math.Abs(totalDebit - totalCredit) < 0.001m; // Cho phép sai lệch nhỏ do làm tròn
            }
        }

        /// <summary>
        /// Thêm một dòng帳 vào giao dịch
        /// </summary>
        /// <param name="accountCode">Mã tài khoản</param>
        /// <param name="debitAmount">Số tiền nợ (0 nếu là có)</param>
        /// <param name="creditAmount">Số tiền có (0 nếu là nợ)</param>
        /// <param name="description">Diễn giải cho dòng này (tùy chọn)</param>
        public void AddLine(string accountCode, decimal debitAmount, decimal creditAmount, string description = "")
        {
            // Kiểm tra hợp lệ cơ bản
            if (string.IsNullOrEmpty(accountCode))
                throw new ArgumentException("Mã tài khoản không được để trống");

            if (debitAmount < 0 || creditAmount < 0)
                throw new ArgumentException("Số tiền không được âm");

            if (debitAmount > 0 && creditAmount > 0)
                throw new ArgumentException("Một dòng không thể có cả nợ và có cùng lúc");

            if (debitAmount == 0 && creditAmount == 0)
                throw new ArgumentException("Một dòng phải có entweder nợ hoặc có");

            Lines.Add(new TransactionLine
            {
                AccountCode = accountCode,
                DebitAmount = debitAmount,
                CreditAmount = creditAmount,
                Description = description
            });
        }
    }

    /// <summary>
    /// Đại diện cho một dòng trong giao dịch kế toán
    /// </summary>
    public class TransactionLine
    {
        /// <summary>
        /// Mã tài khoản
        /// </summary>
        public string AccountCode { get; set; }

        /// <summary>
        /// Số tiền nợ
        /// </summary>
        public decimal DebitAmount { get; set; }

        /// <summary>
        /// Số tiền có
        /// </summary>
        public decimal CreditAmount { get; set; }

        /// <summary>
        /// Diễn giải cho dòng này
        /// </summary>
        public string Description { get; set; }
    }
}