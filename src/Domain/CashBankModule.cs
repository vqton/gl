namespace GL.Core.Entities.Modules
{
    /// <summary>
    /// Danh mục Tiền gửi và Ngân hàng (T01-T05) theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public static class CashBankModule
    {
        /// <summary>
        /// Các tài khoản level 1 cho mô-đun Tiền gửi và Ngân hàng (T01-T05)
        /// </summary>
        public static readonly string[] Level1Accounts = new[]
        {
            "111", // Tiền mặt
            "112", // Ngân hàng
            "113", // Kim loại quý
            "114", // Giá trị gặp lại
            "115"  // Các khoản tiền gửi vay
        };
    }
}