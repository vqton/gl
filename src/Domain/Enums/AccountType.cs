namespace GL.Domain.Enums
{
    /// <summary>
    /// Loại tài khoản kế toán theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public enum AccountType
    {
        /// <summary>
        /// Tài sản
        /// </summary>
        Asset = 1,

        /// <summary>
        /// Nợ phải trả
        /// </summary>
        Liability = 2,

        /// <summary>
        /// Vốn chủ sở hữu
        /// </summary>
        Equity = 3,

        /// <summary>
        /// Doanh thu
        /// </summary>
        Revenue = 4,

        /// <summary>
        /// Chi phí
        /// </summary>
        Expense = 5
    }
}