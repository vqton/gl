namespace GL.Core.Entities.Modules
{
    /// <summary>
    /// Danh mục Mua hàng và Hàng tồn kho (P01-P05) theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public static class PurchasingInventoryModule
    {
        /// <summary>
        /// Các tài khoản level 1 cho mô-đun Mua hàng và Hàng tồn kho (P01-P05)
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