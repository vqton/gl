using GL.Domain.Enums;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Danh mục tài khoản theo Thông tư 99/2025/TT-BTC
    /// 71 tài khoản cấp 1, 101 tài khoản cấp 2
    /// Hiệu lực: 01/01/2026
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
                // ========== LOẠI TÀI KHOẢN TÀI SẢN ==========
                
                // Nhóm 1: Tài sản ngắn hạn (111-159)
                new Account { Code = "111", Name = "Tiền mặt", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "112", Name = "Tiền gửi không kỳ hạn", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "113", Name = "Tiền đang chuyển", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "121", Name = "Chứng khoán kinh doanh", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "128", Name = "Đầu tư nắm giữ đến ngày đáo hạn", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "1281", Name = "Tiền gửi có kỳ hạn", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "128" },
                new Account { Code = "1282", Name = "Trái phiếu", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "128" },
                new Account { Code = "1283", Name = "Cho vay", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "128" },
                new Account { Code = "1288", Name = "Các khoản đầu tư khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "128" },
                new Account { Code = "131", Name = "Phải thu của khách hàng", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "133", Name = "Thuế GTGT được khấu trừ", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "1331", Name = "Thuế GTGT được khấu trừ của hàng hóa, dịch vụ", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "133" },
                new Account { Code = "1332", Name = "Thuế GTGT được khấu trừ của TSCĐ", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "133" },
                new Account { Code = "136", Name = "Phải thu nội bộ", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "1361", Name = "Vốn kinh doanh ở đơn vị trực thuộc", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "136" },
                new Account { Code = "1362", Name = "Phải thu nội bộ về chênh lệch tỷ giá", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "136" },
                new Account { Code = "1363", Name = "Phải thu nội bộ về chi phí đi vay", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "136" },
                new Account { Code = "1368", Name = "Phải thu nội bộ khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "136" },
                new Account { Code = "138", Name = "Phải thu khác", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "1381", Name = "Tài sản thiếu chờ xử lý", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "138" },
                new Account { Code = "1383", Name = "Thuế TTĐB của hàng nhập khẩu", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "138" },
                new Account { Code = "1388", Name = "Phải thu khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "138" },
                new Account { Code = "141", Name = "Tạm ứng", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "151", Name = "Hàng mua đang đi đường", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "152", Name = "Nguyên liệu, vật liệu", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "153", Name = "Công cụ, dụng cụ", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "154", Name = "Chi phí sản xuất, kinh doanh dở dang", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "155", Name = "Sản phẩm", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "156", Name = "Hàng hóa", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "157", Name = "Hàng gửi đi bán", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "158", Name = "Nguyên liệu, vật tư tại kho bảo thuế", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "171", Name = "Giao dịch mua, bán lại trái phiếu chính phủ", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },

                // Nhóm 2: Tài sản dài hạn (211-249)
                new Account { Code = "211", Name = "Tài sản cố định hữu hình", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "212", Name = "Tài sản cố định thuê tài chính", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "213", Name = "Tài sản cố định vô hình", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "214", Name = "Hao mòn tài sản cố định", Level = 1, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "2141", Name = "Hao mòn TSCĐ hữu hình", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "214" },
                new Account { Code = "2142", Name = "Hao mòn TSCĐ thuê tài chính", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "214" },
                new Account { Code = "2143", Name = "Hao mòn TSCĐ vô hình", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "214" },
                new Account { Code = "2147", Name = "Hao mòn BĐSĐT", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "214" },
                new Account { Code = "215", Name = "Tài sản sinh học", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "217", Name = "Bất động sản đầu tư", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "221", Name = "Đầu tư vào công ty con", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "222", Name = "Đầu tư vào công ty liên doanh, liên kết", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "228", Name = "Đầu tư khác", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "2281", Name = "Đầu tư góp vốn vào đơn vị khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "228" },
                new Account { Code = "2288", Name = "Đầu tư khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "228" },
                new Account { Code = "229", Name = "Dự phòng tổn thất tài sản", Level = 1, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "2291", Name = "Dự phòng giảm giá chứng khoán kinh doanh", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "229" },
                new Account { Code = "2292", Name = "Dự phòng tổn thất đầu tư vào đơn vị khác", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "229" },
                new Account { Code = "2293", Name = "Dự phòng phải thu khó đòi", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "229" },
                new Account { Code = "2294", Name = "Dự phòng giảm giá hàng tồn kho", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "229" },
                new Account { Code = "2295", Name = "Dự phòng tổn thất tài sản sinh học", Level = 2, Type = AccountType.Asset, NormalBalance = "Credit", IsPostable = true, ParentCode = "229" },
                new Account { Code = "241", Name = "Xây dựng cơ bản dở dang", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "2411", Name = "Mua sắm TSCĐ", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "241" },
                new Account { Code = "2412", Name = "Xây dựng cơ bản", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "241" },
                new Account { Code = "2413", Name = "Sửa chữa, bảo dưỡng định kỳ TSCĐ", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "241" },
                new Account { Code = "2414", Name = "Nâng cấp, cải tạo TSCĐ", Level = 2, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true, ParentCode = "241" },
                new Account { Code = "242", Name = "Chi phí chờ phân bổ", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "243", Name = "Tài sản thuế thu nhập hoãn lại", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "244", Name = "Ký quỹ, ký cược", Level = 1, Type = AccountType.Asset, NormalBalance = "Debit", IsPostable = true },

                // ========== LOẠI TÀI KHOẢN NỢ PHẢI TRẢ ==========

                new Account { Code = "331", Name = "Phải trả cho người bán", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "332", Name = "Phải trả cổ tức, lợi nhuận", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "333", Name = "Thuế và các khoản phải nộp Nhà nước", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3331", Name = "Thuế giá trị gia tăng phải nộp", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "33311", Name = "Thuế GTGT đầu ra", Level = 3, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "3331" },
                new Account { Code = "33312", Name = "Thuế GTGT hàng nhập khẩu", Level = 3, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "3331" },
                new Account { Code = "3332", Name = "Thuế tiêu thụ đặc biệt", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3333", Name = "Thuế xuất, nhập khẩu", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3334", Name = "Thuế thu nhập doanh nghiệp", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3335", Name = "Thuế thu nhập cá nhân", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3336", Name = "Thuế tài nguyên", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3337", Name = "Thuế nhà đất, tiền thuê đất", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3338", Name = "Thuế bảo vệ môi trường và các loại thuế khác", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "3339", Name = "Phí, lệ phí và các khoản phải nộp khác", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "333" },
                new Account { Code = "334", Name = "Phải trả người lao động", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "335", Name = "Chi phí phải trả", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "336", Name = "Phải trả nội bộ", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3361", Name = "Phải trả nội bộ về vốn kinh doanh", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "336" },
                new Account { Code = "3362", Name = "Phải trả nội bộ về chênh lệch tỷ giá", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "336" },
                new Account { Code = "3363", Name = "Phải trả nội bộ về chi phí đi vay", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "336" },
                new Account { Code = "3368", Name = "Phải trả nội bộ khác", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "336" },
                new Account { Code = "337", Name = "Thanh toán theo tiến độ hợp đồng xây dựng", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "338", Name = "Phải trả, phải nộp khác", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3381", Name = "Tài sản thừa chờ giải quyết", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3382", Name = "Kinh phí công đoàn", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3383", Name = "Bảo hiểm xã hội", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3384", Name = "Bảo hiểm y tế", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3386", Name = "Bảo hiểm thất nghiệp", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3387", Name = "Doanh thu chờ phân bổ", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "3388", Name = "Phải trả, phải nộp khác", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "338" },
                new Account { Code = "341", Name = "Vay và nợ thuê tài chính", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3411", Name = "Các khoản đi vay", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "341" },
                new Account { Code = "3412", Name = "Nợ thuê tài chính", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "341" },
                new Account { Code = "343", Name = "Trái phiếu phát hành", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3431", Name = "Trái phiếu thường", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "343" },
                new Account { Code = "3432", Name = "Trái phiếu chuyển đổi", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "343" },
                new Account { Code = "344", Name = "Nhận ký quỹ, ký cược", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "347", Name = "Thuế thu nhập hoãn lại phải trả", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "352", Name = "Dự phòng phải trả", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3521", Name = "Dự phòng bảo hành sản phẩm, hàng hóa", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "352" },
                new Account { Code = "3522", Name = "Dự phòng bảo hành công trình xây dựng", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "352" },
                new Account { Code = "3523", Name = "Dự phòng tái cơ cấu doanh nghiệp", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "352" },
                new Account { Code = "3525", Name = "Dự phòng phải trả khác", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "352" },
                new Account { Code = "353", Name = "Quỹ khen thưởng, phúc lợi", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "3531", Name = "Quỹ khen thưởng", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "353" },
                new Account { Code = "3532", Name = "Quỹ phúc lợi", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "353" },
                new Account { Code = "3533", Name = "Quỹ phúc lợi đã hình thành TSCĐ", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "353" },
                new Account { Code = "3534", Name = "Quỹ thưởng ban quản lý điều hành công ty", Level = 2, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true, ParentCode = "353" },
                new Account { Code = "356", Name = "Quỹ phát triển khoa học và công nghệ", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "357", Name = "Quỹ bình ổn giá", Level = 1, Type = AccountType.Liability, NormalBalance = "Credit", IsPostable = false },

                // ========== LOẠI TÀI KHOẢN VỐN CHỦ SỞ HỮU ==========

                new Account { Code = "411", Name = "Vốn đầu tư của chủ sở hữu", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "4111", Name = "Vốn góp của chủ sở hữu", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "411" },
                new Account { Code = "4112", Name = "Thặng dư vốn", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "411" },
                new Account { Code = "4113", Name = "Quyền chọn chuyển đổi trái phiếu", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "411" },
                new Account { Code = "4118", Name = "Vốn khác", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "411" },
                new Account { Code = "412", Name = "Chênh lệch đánh giá lại tài sản", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "413", Name = "Chênh lệch tỷ giá hối đoái", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "414", Name = "Quỹ đầu tư phát triển", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "418", Name = "Các quỹ khác thuộc vốn chủ sở hữu", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "419", Name = "Cổ phiếu mua lại của chính mình", Level = 1, Type = AccountType.Equity, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "421", Name = "Lợi nhuận sau thuế chưa phân phối", Level = 1, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "4211", Name = "Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối năm trước", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "421" },
                new Account { Code = "4212", Name = "Lợi nhuận sau thuế chưa phân phối năm nay", Level = 2, Type = AccountType.Equity, NormalBalance = "Credit", IsPostable = true, ParentCode = "421" },

                // ========== LOẠI TÀI KHOẢN DOANH THU ==========

                new Account { Code = "511", Name = "Doanh thu bán hàng và cung cấp dịch vụ", Level = 1, Type = AccountType.Revenue, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "515", Name = "Doanh thu hoạt động tài chính", Level = 1, Type = AccountType.Revenue, NormalBalance = "Credit", IsPostable = true },
                new Account { Code = "521", Name = "Các khoản giảm trừ doanh thu", Level = 1, Type = AccountType.Revenue, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "5211", Name = "Chiết khấu thương mại", Level = 2, Type = AccountType.Revenue, NormalBalance = "Debit", IsPostable = true, ParentCode = "521" },
                new Account { Code = "5212", Name = "Hàng bán bị trả lại", Level = 2, Type = AccountType.Revenue, NormalBalance = "Debit", IsPostable = true, ParentCode = "521" },
                new Account { Code = "5213", Name = "Giảm giá hàng bán", Level = 2, Type = AccountType.Revenue, NormalBalance = "Debit", IsPostable = true, ParentCode = "521" },

                // ========== LOẠI TÀI KHOẢN CHI PHÍ ==========

                new Account { Code = "621", Name = "Chi phí nguyên liệu, vật liệu trực tiếp", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "622", Name = "Chi phí nhân công trực tiếp", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "623", Name = "Chi phí sử dụng máy thi công", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "627", Name = "Chi phí sản xuất chung", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "6271", Name = "Chi phí nhân viên phân xưởng", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6272", Name = "Chi phí vật liệu", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6273", Name = "Chi phí dụng cụ sản xuất", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6274", Name = "Chi phí khấu hao TSCĐ", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6275", Name = "Thuế, phí, lệ phí", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6277", Name = "Chi phí dịch vụ mua ngoài", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "6278", Name = "Chi phí bằng tiền khác", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "627" },
                new Account { Code = "632", Name = "Giá vốn hàng bán", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "635", Name = "Chi phí tài chính", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "641", Name = "Chi phí bán hàng", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "6411", Name = "Chi phí nhân viên", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6412", Name = "Chi phí vật liệu, bao bì", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6413", Name = "Chi phí dụng cụ, đồ dùng", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6414", Name = "Chi phí khấu hao TSCĐ", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6415", Name = "Thuế, phí, lệ phí", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6417", Name = "Chi phí dịch vụ mua ngoài", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "6418", Name = "Chi phí bằng tiền khác", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "641" },
                new Account { Code = "642", Name = "Chi phí quản lý doanh nghiệp", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "6421", Name = "Chi phí nhân viên quản lý", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6422", Name = "Chi phí vật liệu quản lý", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6423", Name = "Chi phí đồ dùng văn phòng", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6424", Name = "Chi phí khấu hao TSCĐ", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6425", Name = "Thuế, phí và lệ phí", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6426", Name = "Chi phí dự phòng", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6427", Name = "Chi phí dịch vụ mua ngoài", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },
                new Account { Code = "6428", Name = "Chi phí bằng tiền khác", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "642" },

                // ========== LOẠI TÀI KHOẢN THU NHẬP KHÁC ==========

                new Account { Code = "711", Name = "Thu nhập khác", Level = 1, Type = AccountType.Revenue, NormalBalance = "Credit", IsPostable = true },

                // ========== LOẠI TÀI KHOẢN CHI PHÍ KHÁC ==========

                new Account { Code = "811", Name = "Chi phí khác", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },

                // ========== TÀI KHOẢN XÁC ĐỊNH KẾT QUẢ ==========

                new Account { Code = "821", Name = "Chi phí thuế thu nhập doanh nghiệp", Level = 1, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true },
                new Account { Code = "8211", Name = "Chi phí thuế TNDN hiện hành", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "821" },
                new Account { Code = "8212", Name = "Chi phí thuế TNDN hoãn lại", Level = 2, Type = AccountType.Expense, NormalBalance = "Debit", IsPostable = true, ParentCode = "821" },
                new Account { Code = "911", Name = "Xác định kết quả kinh doanh", Level = 1, Type = AccountType.Expense, NormalBalance = "Credit", IsPostable = true },
            };
        }

        /// <summary>
        /// Kiểm tra tài khoản có thể ghi sổ (postable) không
        /// </summary>
        public static bool IsPostable(string accountCode)
        {
            var account = GetAllAccounts().FirstOrDefault(a => a.Code == accountCode);
            return account?.IsPostable ?? false;
        }
    }
}