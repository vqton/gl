using GL.Domain.Enums;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Danh mục tài khoản theo Thông tư 99/2025/TT-BTC (71 tài khoản cấp 1)
    /// </summary>
    public static class ChartOfAccounts
    {
        /// <summary>
        /// Lấy toàn bộ danh mục tài khoản TT99
        /// </summary>
        public static List<Account> GetAllAccounts()
        {
            return new List<Account>
            {
// Nhóm 1: Tài sản ngắn hạn (100-159)
                new Account { Code = "111", Name = "Tiền mặt", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "112", Name = "Tiền gửi ngân hàng", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "113", Name = "Tiền gửi kho bạc nhà nước", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "114", Name = "Tiền gửi của Ngân sách nhà nước", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "115", Name = "Tiền đang chuyển", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "121", Name = "Chứng khoán kinh doanh", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "122", Name = "Dự phòng giảm giá chứng khoán kinh doanh", Type = AccountType.Asset, NormalBalance = "Credit" },
                new Account { Code = "128", Name = "Các khoản đầu tư ngắn hạn khác", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "129", Name = "Dự phòng giảm giá đầu tư ngắn hạn khác", Type = AccountType.Asset, NormalBalance = "Credit" },
                new Account { Code = "131", Name = "Phải thu khách hàng", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "132", Name = "Phải thu nội bộ", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "1331", Name = "Thuế GTGT được khấu trừ", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "136", Name = "Phải thu khác", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "138", Name = "Dự phòng phải thu khó đòi", Type = AccountType.Asset, NormalBalance = "Credit" },
                new Account { Code = "139", Name = "Giao dịch mua bán lô tài sản phi tiền tệ", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "141", Name = "Tạm ứng", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "142", Name = "Chi phí trả trước", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "143", Name = "Cầm cố, ký quỹ, ký cược ngắn hạn", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "151", Name = "Giá trị hàng hóa tồn kho", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "152", Name = "Nguyên liệu, vật liệu", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "153", Name = "Công cụ, dụng cụ", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "154", Name = "Chi phí sx kinh doanh dở dang", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "155", Name = "Thành phẩm", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "156", Name = "Hàng hóa", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "157", Name = "Hàng gửi đi bán", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "158", Name = "Hàng tồn kho được hướng dẫn ghi nhận theo Báo cáo tài chính quốc tế", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "159", Name = "Dự phòng giảm giá hàng tồn kho", Type = AccountType.Asset, NormalBalance = "Credit" },

                // Nhóm 2: Tài sản dài hạn (200-259)
                new Account { Code = "211", Name = "Tài sản cố định hữu hình", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "212", Name = "Tài sản cố định thuê tài chính", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "213", Name = "Tài sản cố định vô hình", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "214", Name = "Hao mòn lũy kế tài sản cố định", Type = AccountType.Asset, NormalBalance = "Credit" },
                new Account { Code = "215", Name = "Bất động sản đầu tư", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "221", Name = "Góp vốn liên doanh", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "222", Name = "Vốn góp liên doanh", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "228", Name = "Đầu tư dài hạn khác", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "229", Name = "Dự phòng giảm giá đầu tư dài hạn", Type = AccountType.Asset, NormalBalance = "Credit" },
                new Account { Code = "231", Name = "Phải thu dài hạn", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "232", Name = "Vốn kinh doanh ở đơn vị trực thuộc", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "243", Name = "Tài sản thuế TNDN hoãn lại", Type = AccountType.Asset, NormalBalance = "Debit" },
                new Account { Code = "333", Name = "Thuế và các khoản phải nộp nhà nước", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "3331", Name = "Thuế GTGT đầu ra phải nộp", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "33311", Name = "Thuế GTGT đầu ra", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "3334", Name = "Thuế thu nhập doanh nghiệp", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "3335", Name = "Thuế thu nhập cá nhân", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "334", Name = "Phải trả người lao động", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "335", Name = "Chi phí phải trả", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "336", Name = "Phải trả nội bộ", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "337", Name = "Nhận ký quỹ, ký cược dài hạn", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "338", Name = "Phải trả khác", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "3382", Name = "Kinh phí công đoàn", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "3383", Name = "Bảo hiểm xã hội", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "347", Name = "Thuế TNDN hoãn lại phải trả", Type = AccountType.Liability, NormalBalance = "Credit" },
                new Account { Code = "341", Name = "Vốn góp của chủ sở hữu", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "342", Name = "Thặng dư vốn cổ phần", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "411", Name = "Vốn đầu tư của chủ sở hữu", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "412", Name = "Chênh lệch đánh giá lại tài sản", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "413", Name = "Chênh lệch tỷ giá hối đoái", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "414", Name = "Quỹ đầu tư phát triển", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "415", Name = "Quỹ hỗ trợ sắp xếp doanh nghiệp", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "421", Name = "Lợi nhuận sau thuế chưa phân phối", Type = AccountType.Equity, NormalBalance = "Credit" },
                new Account { Code = "4212", Name = "Lợi nhuận sau thuế chưa phân phối", Type = AccountType.Equity, NormalBalance = "Credit" },

                // Nhóm 5: Doanh thu (500-539)
                new Account { Code = "511", Name = "Doanh thu bán hàng", Type = AccountType.Revenue, NormalBalance = "Credit" },
                new Account { Code = "5111", Name = "Doanh thu bán hàng", Type = AccountType.Revenue, NormalBalance = "Credit" },
                new Account { Code = "515", Name = "Doanh thu hoạt động tài chính", Type = AccountType.Revenue, NormalBalance = "Credit" },
                new Account { Code = "521", Name = "Giảm trừ doanh thu", Type = AccountType.Revenue, NormalBalance = "Debit" },
                new Account { Code = "522", Name = "Hàng bán bị trả lại", Type = AccountType.Revenue, NormalBalance = "Debit" },
                new Account { Code = "531", Name = "Doanh thu bán hàng trực tiếp", Type = AccountType.Revenue, NormalBalance = "Credit" },
                new Account { Code = "532", Name = "Giảm giá hàng bán", Type = AccountType.Revenue, NormalBalance = "Debit" },
                new Account { Code = "711", Name = "Thu nhập khác", Type = AccountType.Revenue, NormalBalance = "Credit" },

                // Nhóm 6: Chi phí sản xuất kinh doanh (600-639)
                new Account { Code = "621", Name = "Giá trị hàng hóa", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "622", Name = "Giá thành sản phẩm tiền lương", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "623", Name = "Giá thành sản phẩm tiền công", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "624", Name = "Giá thành sản phẩm vật liệu", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "625", Name = "Giá thành sản phẩm máy móc", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "627", Name = "Chi phí sản xuất và quản lý", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "632", Name = "Giá vốn hàng bán", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "635", Name = "Chi phí tài chính", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "641", Name = "Chi phí bán hàng", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "6411", Name = "Chi phí bán hàng", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "642", Name = "Chi phí quản lý doanh nghiệp", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "6421", Name = "Chi phí quản lý doanh nghiệp", Type = AccountType.Expense, NormalBalance = "Debit" },

                // Nhóm 8: Chi phí khác (800-829)
                new Account { Code = "811", Name = "Chi phí khác", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "8211", Name = "Chi phí thuế TNDN hiện hành", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "8212", Name = "Chi phí thuế TNDN hoãn lại", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "821", Name = "Chi phí thuế thu nhập doanh nghiệp", Type = AccountType.Expense, NormalBalance = "Debit" },
                new Account { Code = "911", Name = "Xác định kết quả kinh doanh", Type = AccountType.Expense, NormalBalance = "Credit" },

                // Nhóm 3: Phải trả người bán và các khoản phải trả
                new Account { Code = "331", Name = "Phải trả người bán", Type = AccountType.Liability, NormalBalance = "Credit" },
            };
        }
    }
}