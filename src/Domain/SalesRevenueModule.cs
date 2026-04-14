namespace GL.Core.Entities.Modules
{
    /// <summary>
    /// Danh mục Doanh thu và Bán hàng (S01-S06) theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public static class SalesRevenueModule
    {
        /// <summary>
        /// Các tài khoản level 1 cho mô-đun Doanh thu và Bán hàng (S01-S06)
        /// Đây là 6 tài khoản level 1 đầu tiên trong danh mục 71 tài khoản level 1
        /// </summary>
        public static readonly string[] Level1Accounts = new[]
        {
            "111", // Tiền mặt
            "112", // Ngân hàng
            "131", // Khách hàng
            "133", // Trả trước cho người bán
            "136", // Thuế GTGT đã stems thu
            "138"  // Kho hàng gửi đi mua ra
        };
    }
}