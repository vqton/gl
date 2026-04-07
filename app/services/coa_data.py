"""Full Chart of Accounts per Circular 99/2025/TT-BTC.

Source: Phụ lục II — Hệ thống tài khoản kế toán áp dụng cho doanh nghiệp lớn
Ref: ketoanthienung.net, Thông tư 99/2025/TT-BTC
"""

CIRCULAR99_COA = [
    # ═══════════════════════════════════════════
    # LOẠI 1 — TÀI SẢN (ASSETS)
    # ═══════════════════════════════════════════

    # ── TK 111 — Tiền mặt ──
    {"code": "111", "name": "Tiền mặt", "level": 1, "type": "asset",
     "name_en": "Cash", "description": "Tiền Việt Nam, ngoại tệ, vàng tiền tệ tại quỹ"},
    {"code": "1111", "name": "Tiền Việt Nam", "level": 2, "type": "asset", "parent_code": "111"},
    {"code": "1112", "name": "Ngoại tệ", "level": 2, "type": "asset", "parent_code": "111"},
    {"code": "1113", "name": "Vàng tiền tệ", "level": 2, "type": "asset", "parent_code": "111"},

    # ── TK 112 — Tiền gửi không kỳ hạn ──
    {"code": "112", "name": "Tiền gửi không kỳ hạn", "level": 1, "type": "asset",
     "name_en": "Demand deposits"},
    {"code": "1121", "name": "Tiền Việt Nam", "level": 2, "type": "asset", "parent_code": "112"},
    {"code": "1122", "name": "Ngoại tệ", "level": 2, "type": "asset", "parent_code": "112"},

    # ── TK 113 — Tiền đang chuyển ──
    {"code": "113", "name": "Tiền đang chuyển", "level": 1, "type": "asset",
     "name_en": "Cash in transit"},

    # ── TK 121 — Chứng khoán kinh doanh ──
    {"code": "121", "name": "Chứng khoán kinh doanh", "level": 1, "type": "asset",
     "name_en": "Trading securities"},

    # ── TK 128 — Đầu tư nắm giữ đến ngày đáo hạn ──
    {"code": "128", "name": "Đầu tư nắm giữ đến ngày đáo hạn", "level": 1, "type": "asset",
     "name_en": "Held-to-maturity investments"},
    {"code": "1281", "name": "Tiền gửi có kỳ hạn", "level": 2, "type": "asset", "parent_code": "128"},
    {"code": "1282", "name": "Trái phiếu, tín phiếu", "level": 2, "type": "asset", "parent_code": "128"},

    # ── TK 131 — Phải thu của khách hàng ──
    {"code": "131", "name": "Phải thu của khách hàng", "level": 1, "type": "asset",
     "name_en": "Trade receivables"},

    # ── TK 133 — Thuế GTGT được khấu trừ ──
    {"code": "133", "name": "Thuế GTGT được khấu trừ", "level": 1, "type": "asset",
     "name_en": "Deductible VAT"},
    {"code": "1331", "name": "Thuế GTGT được khấu trừ của hàng hóa, dịch vụ", "level": 2, "type": "asset", "parent_code": "133"},
    {"code": "1332", "name": "Thuế GTGT được khấu trừ của TSCĐ", "level": 2, "type": "asset", "parent_code": "133"},

    # ── TK 136 — Phải thu nội bộ ──
    {"code": "136", "name": "Phải thu nội bộ", "level": 1, "type": "asset",
     "name_en": "Internal receivables"},
    {"code": "1361", "name": "Phải thu nội bộ về vốn kinh doanh", "level": 2, "type": "asset", "parent_code": "136"},
    {"code": "1368", "name": "Phải thu nội bộ khác", "level": 2, "type": "asset", "parent_code": "136"},

    # ── TK 138 — Phải thu khác ──
    {"code": "138", "name": "Phải thu khác", "level": 1, "type": "asset",
     "name_en": "Other receivables"},
    {"code": "1381", "name": "Tài sản thiếu chờ xử lý", "level": 2, "type": "asset", "parent_code": "138"},
    {"code": "1388", "name": "Phải thu khác", "level": 2, "type": "asset", "parent_code": "138"},

    # ── TK 141 — Tạm ứng ──
    {"code": "141", "name": "Tạm ứng", "level": 1, "type": "asset",
     "name_en": "Advances"},

    # ── TK 151 — Hàng mua đang đi đường ──
    {"code": "151", "name": "Hàng mua đang đi đường", "level": 1, "type": "asset",
     "name_en": "Goods in transit"},

    # ── TK 152 — Nguyên liệu, vật liệu ──
    {"code": "152", "name": "Nguyên liệu, vật liệu", "level": 1, "type": "asset",
     "name_en": "Raw materials"},

    # ── TK 153 — Công cụ, dụng cụ ──
    {"code": "153", "name": "Công cụ, dụng cụ", "level": 1, "type": "asset",
     "name_en": "Tools and supplies"},

    # ── TK 154 — Chi phí sản xuất, kinh doanh dở dang ──
    {"code": "154", "name": "Chi phí sản xuất, kinh doanh dở dang", "level": 1, "type": "asset",
     "name_en": "Work in progress"},

    # ── TK 155 — Thành phẩm ──
    {"code": "155", "name": "Thành phẩm", "level": 1, "type": "asset",
     "name_en": "Finished goods"},

    # ── TK 156 — Hàng hóa ──
    {"code": "156", "name": "Hàng hóa", "level": 1, "type": "asset",
     "name_en": "Merchandise"},
    {"code": "1561", "name": "Giá mua hàng hóa", "level": 2, "type": "asset", "parent_code": "156"},
    {"code": "1562", "name": "Chi phí thu mua hàng hóa", "level": 2, "type": "asset", "parent_code": "156"},

    # ── TK 157 — Hàng gửi đi bán ──
    {"code": "157", "name": "Hàng gửi đi bán", "level": 1, "type": "asset",
     "name_en": "Goods sent for sale"},

    # ── TK 158 — Hàng hóa kho bảo thuế ──
    {"code": "158", "name": "Hàng hóa kho bảo thuế", "level": 1, "type": "asset",
     "name_en": "Bonded warehouse goods"},

    # ── TK 211 — Tài sản cố định hữu hình ──
    {"code": "211", "name": "Tài sản cố định hữu hình", "level": 1, "type": "asset",
     "name_en": "Tangible fixed assets"},
    {"code": "2111", "name": "Nhà cửa, vật kiến trúc", "level": 2, "type": "asset", "parent_code": "211"},
    {"code": "2112", "name": "Máy móc, thiết bị", "level": 2, "type": "asset", "parent_code": "211"},
    {"code": "2113", "name": "Phương tiện vận tải", "level": 2, "type": "asset", "parent_code": "211"},
    {"code": "2114", "name": "Thiết bị, dụng cụ quản lý", "level": 2, "type": "asset", "parent_code": "211"},
    {"code": "2118", "name": "Tài sản cố định khác", "level": 2, "type": "asset", "parent_code": "211"},

    # ── TK 212 — Tài sản cố định thuê tài chính ──
    {"code": "212", "name": "Tài sản cố định thuê tài chính", "level": 1, "type": "asset",
     "name_en": "Finance leased assets"},

    # ── TK 213 — Tài sản cố định vô hình ──
    {"code": "213", "name": "Tài sản cố định vô hình", "level": 1, "type": "asset",
     "name_en": "Intangible fixed assets"},
    {"code": "2131", "name": "Quyền sử dụng đất", "level": 2, "type": "asset", "parent_code": "213"},
    {"code": "2132", "name": "Quyền phát hành", "level": 2, "type": "asset", "parent_code": "213"},
    {"code": "2133", "name": "Bằng sáng chế, giấy phép", "level": 2, "type": "asset", "parent_code": "213"},
    {"code": "2134", "name": "Phần mềm máy tính", "level": 2, "type": "asset", "parent_code": "213"},
    {"code": "2138", "name": "TSCĐ vô hình khác", "level": 2, "type": "asset", "parent_code": "213"},

    # ── TK 214 — Hao mòn tài sản cố định ──
    {"code": "214", "name": "Hao mòn tài sản cố định", "level": 1, "type": "asset",
     "name_en": "Accumulated depreciation"},
    {"code": "2141", "name": "Hao mòn TSCĐ hữu hình", "level": 2, "type": "asset", "parent_code": "214"},
    {"code": "2142", "name": "Hao mòn TSCĐ thuê tài chính", "level": 2, "type": "asset", "parent_code": "214"},
    {"code": "2143", "name": "Hao mòn TSCĐ vô hình", "level": 2, "type": "asset", "parent_code": "214"},

    # ── TK 215 — Tài sản sinh học ──
    {"code": "215", "name": "Tài sản sinh học", "level": 1, "type": "asset",
     "name_en": "Biological assets"},
    {"code": "2151", "name": "Tài sản sinh học cho sản phẩm", "level": 2, "type": "asset", "parent_code": "215"},
    {"code": "2152", "name": "Tài sản sinh học để bán", "level": 2, "type": "asset", "parent_code": "215"},
    {"code": "2153", "name": "Tài sản sinh học khác", "level": 2, "type": "asset", "parent_code": "215"},

    # ── TK 217 — Bất động sản đầu tư ──
    {"code": "217", "name": "Bất động sản đầu tư", "level": 1, "type": "asset",
     "name_en": "Investment property"},

    # ── TK 221 — Đầu tư vào công ty con ──
    {"code": "221", "name": "Đầu tư vào công ty con", "level": 1, "type": "asset",
     "name_en": "Investment in subsidiaries"},

    # ── TK 222 — Đầu tư vào công ty liên doanh, liên kết ──
    {"code": "222", "name": "Đầu tư vào công ty liên doanh, liên kết", "level": 1, "type": "asset",
     "name_en": "Investment in associates"},

    # ── TK 228 — Đầu tư khác ──
    {"code": "228", "name": "Đầu tư khác", "level": 1, "type": "asset",
     "name_en": "Other investments"},
    {"code": "2281", "name": "Đầu tư góp vốn vào đơn vị khác", "level": 2, "type": "asset", "parent_code": "228"},
    {"code": "2282", "name": "Đầu tư vào công cụ nợ", "level": 2, "type": "asset", "parent_code": "228"},
    {"code": "2283", "name": "Cho vay", "level": 2, "type": "asset", "parent_code": "228"},
    {"code": "2288", "name": "Đầu tư khác", "level": 2, "type": "asset", "parent_code": "228"},

    # ── TK 229 — Dự phòng tổn thất tài sản ──
    {"code": "229", "name": "Dự phòng tổn thất tài sản", "level": 1, "type": "asset",
     "name_en": "Provisions for asset impairment"},
    {"code": "2291", "name": "Dự phòng đầu tư chứng khoán", "level": 2, "type": "asset", "parent_code": "229"},
    {"code": "2292", "name": "Dự phòng tổn thất đầu tư đơn vị khác", "level": 2, "type": "asset", "parent_code": "229"},
    {"code": "2293", "name": "Dự phòng phải thu khó đòi", "level": 2, "type": "asset", "parent_code": "229"},
    {"code": "2294", "name": "Dự phòng giảm giá hàng tồn kho", "level": 2, "type": "asset", "parent_code": "229"},
    {"code": "2295", "name": "Dự phòng tổn thất đầu tư khác", "level": 2, "type": "asset", "parent_code": "229"},

    # ── TK 241 — Xây dựng cơ bản dở dang ──
    {"code": "241", "name": "Xây dựng cơ bản dở dang", "level": 1, "type": "asset",
     "name_en": "Construction in progress"},
    {"code": "2411", "name": "Mua sắm TSCĐ", "level": 2, "type": "asset", "parent_code": "241"},
    {"code": "2412", "name": "Xây dựng cơ bản", "level": 2, "type": "asset", "parent_code": "241"},
    {"code": "2413", "name": "Sửa chữa lớn TSCĐ", "level": 2, "type": "asset", "parent_code": "241"},
    {"code": "2414", "name": "Nâng cấp, cải tạo TSCĐ", "level": 2, "type": "asset", "parent_code": "241"},

    # ── TK 242 — Chi phí trả trước ──
    {"code": "242", "name": "Chi phí trả trước", "level": 1, "type": "asset",
     "name_en": "Prepaid expenses"},
    {"code": "2421", "name": "Chi phí trả trước ngắn hạn", "level": 2, "type": "asset", "parent_code": "242"},
    {"code": "2422", "name": "Chi phí trả trước dài hạn", "level": 2, "type": "asset", "parent_code": "242"},

    # ── TK 243 — Tài sản thuế TNDN hoãn lại ──
    {"code": "243", "name": "Tài sản thuế thu nhập doanh nghiệp hoãn lại", "level": 1, "type": "asset",
     "name_en": "Deferred tax assets"},

    # ── TK 244 — Ký cược, ký quỹ ──
    {"code": "244", "name": "Ký cược, ký quỹ", "level": 1, "type": "asset",
     "name_en": "Deposits"},

    # ═══════════════════════════════════════════
    # LOẠI 2 — NỢ PHẢI TRẢ (LIABILITIES)
    # ═══════════════════════════════════════════

    # ── TK 331 — Phải trả cho người bán ──
    {"code": "331", "name": "Phải trả cho người bán", "level": 1, "type": "liability",
     "name_en": "Trade payables"},

    # ── TK 332 — Phải trả cổ tức, lợi nhuận ──
    {"code": "332", "name": "Phải trả cổ tức, lợi nhuận", "level": 1, "type": "liability",
     "name_en": "Dividends payable"},

    # ── TK 333 — Thuế và các khoản phải nộp Nhà nước ──
    {"code": "333", "name": "Thuế và các khoản phải nộp Nhà nước", "level": 1, "type": "liability",
     "name_en": "Taxes payable"},
    {"code": "3331", "name": "Thuế giá trị gia tăng phải nộp", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "33311", "name": "Thuế GTGT đầu ra", "level": 3, "type": "liability", "parent_code": "3331"},
    {"code": "33312", "name": "Thuế GTGT hàng nhập khẩu", "level": 3, "type": "liability", "parent_code": "3331"},
    {"code": "3332", "name": "Thuế tiêu thụ đặc biệt", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3333", "name": "Thuế xuất, nhập khẩu", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3334", "name": "Thuế thu nhập doanh nghiệp", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3335", "name": "Thuế thu nhập cá nhân", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3336", "name": "Thuế tài nguyên", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3337", "name": "Thuế nhà đất, tiền thuê đất", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3338", "name": "Thuế khác", "level": 2, "type": "liability", "parent_code": "333"},
    {"code": "3339", "name": "Phí, lệ phí và khoản phải nộp khác", "level": 2, "type": "liability", "parent_code": "333"},

    # ── TK 334 — Phải trả người lao động ──
    {"code": "334", "name": "Phải trả người lao động", "level": 1, "type": "liability",
     "name_en": "Employee payables"},

    # ── TK 335 — Chi phí phải trả ──
    {"code": "335", "name": "Chi phí phải trả", "level": 1, "type": "liability",
     "name_en": "Accrued expenses"},

    # ── TK 336 — Phải trả nội bộ ──
    {"code": "336", "name": "Phải trả nội bộ", "level": 1, "type": "liability",
     "name_en": "Internal payables"},
    {"code": "3361", "name": "Phải trả nội bộ về vốn kinh doanh", "level": 2, "type": "liability", "parent_code": "336"},
    {"code": "3368", "name": "Phải trả nội bộ khác", "level": 2, "type": "liability", "parent_code": "336"},

    # ── TK 337 — Thanh toán theo tiến độ kế hoạch hợp đồng xây dựng ──
    {"code": "337", "name": "Thanh toán theo tiến độ kế hoạch hợp đồng xây dựng", "level": 1, "type": "liability",
     "name_en": "Construction progress payments"},

    # ── TK 338 — Phải trả, phải nộp khác ──
    {"code": "338", "name": "Phải trả, phải nộp khác", "level": 1, "type": "liability",
     "name_en": "Other payables"},
    {"code": "3381", "name": "Tài sản thừa chờ xử lý", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3382", "name": "Kinh phí công đoàn", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3383", "name": "Bảo hiểm xã hội", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3384", "name": "Bảo hiểm y tế", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3385", "name": "Bảo hiểm trách nhiệm nghề nghiệp", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3386", "name": "Bảo hiểm thất nghiệp", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3387", "name": "Doanh thu chưa thực hiện", "level": 2, "type": "liability", "parent_code": "338"},
    {"code": "3388", "name": "Phải trả, phải nộp khác", "level": 2, "type": "liability", "parent_code": "338"},

    # ── TK 341 — Vay và nợ thuê tài chính ──
    {"code": "341", "name": "Vay và nợ thuê tài chính", "level": 1, "type": "liability",
     "name_en": "Loans and finance lease liabilities"},
    {"code": "3411", "name": "Vay ngắn hạn", "level": 2, "type": "liability", "parent_code": "341"},
    {"code": "3412", "name": "Vay dài hạn", "level": 2, "type": "liability", "parent_code": "341"},

    # ── TK 343 — Trái phiếu phát hành ──
    {"code": "343", "name": "Trái phiếu phát hành", "level": 1, "type": "liability",
     "name_en": "Bonds payable"},

    # ── TK 344 — Nhận ký cược, ký quỹ ngắn hạn ──
    {"code": "344", "name": "Nhận ký cược, ký quỹ ngắn hạn", "level": 1, "type": "liability",
     "name_en": "Short-term deposits received"},

    # ── TK 347 — Thuế thu nhập hoãn lại phải trả ──
    {"code": "347", "name": "Thuế thu nhập hoãn lại phải trả", "level": 1, "type": "liability",
     "name_en": "Deferred tax liabilities"},

    # ── TK 352 — Dự phòng phải trả ──
    {"code": "352", "name": "Dự phòng phải trả", "level": 1, "type": "liability",
     "name_en": "Provisions"},

    # ── TK 353 — Quỹ khen thưởng, phúc lợi ──
    {"code": "353", "name": "Quỹ khen thưởng, phúc lợi", "level": 1, "type": "liability",
     "name_en": "Bonus and welfare funds"},

    # ── TK 356 — Dự phòng phải trả (dài hạn) ──
    {"code": "356", "name": "Dự phòng phải trả dài hạn", "level": 1, "type": "liability",
     "name_en": "Long-term provisions"},

    # ── TK 357 — Quỹ bình ổn giá ──
    {"code": "357", "name": "Quỹ bình ổn giá", "level": 1, "type": "liability",
     "name_en": "Price stabilization fund"},

    # ═══════════════════════════════════════════
    # LOẠI 3 — VỐN CHỦ SỞ HỮU (EQUITY)
    # ═══════════════════════════════════════════

    # ── TK 411 — Vốn đầu tư của chủ sở hữu ──
    {"code": "411", "name": "Vốn đầu tư của chủ sở hữu", "level": 1, "type": "equity",
     "name_en": "Owner's equity"},
    {"code": "4111", "name": "Vốn cổ phần phổ thông có quyền biểu quyết", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4112", "name": "Vốn cổ phần ưu đãi", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4113", "name": "Thặng dư vốn cổ phần", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4114", "name": "Vốn khác của chủ sở hữu", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4115", "name": "Cổ phiếu quỹ", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4116", "name": "Chênh lệch đánh giá lại tài sản", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4117", "name": "Chênh lệch tỷ giá hối đoái", "level": 2, "type": "equity", "parent_code": "411"},
    {"code": "4118", "name": "Vốn khác", "level": 2, "type": "equity", "parent_code": "411"},

    # ── TK 412 — Chênh lệch đánh giá lại tài sản ──
    {"code": "412", "name": "Chênh lệch đánh giá lại tài sản", "level": 1, "type": "equity",
     "name_en": "Revaluation surplus"},

    # ── TK 413 — Chênh lệch tỷ giá hối đoái ──
    {"code": "413", "name": "Chênh lệch tỷ giá hối đoái", "level": 1, "type": "equity",
     "name_en": "Foreign exchange differences"},

    # ── TK 414 — Quỹ đầu tư phát triển ──
    {"code": "414", "name": "Quỹ đầu tư phát triển", "level": 1, "type": "equity",
     "name_en": "Development investment fund"},

    # ── TK 418 — Tài sản, thu nhập chờ phân bổ ──
    {"code": "418", "name": "Tài sản, thu nhập chờ phân bổ", "level": 1, "type": "equity",
     "name_en": "Deferred income"},

    # ── TK 419 — Cổ phiếu ưu đãi biểu quyết ──
    {"code": "419", "name": "Cổ phiếu ưu đãi có quyền biểu quyết", "level": 1, "type": "equity",
     "name_en": "Voting preference shares"},

    # ── TK 421 — Lợi nhuận sau thuế chưa phân phối ──
    {"code": "421", "name": "Lợi nhuận sau thuế chưa phân phối", "level": 1, "type": "equity",
     "name_en": "Retained earnings"},
    {"code": "4211", "name": "Lợi nhuận năm trước", "level": 2, "type": "equity", "parent_code": "421"},
    {"code": "4212", "name": "Lợi nhuận năm nay", "level": 2, "type": "equity", "parent_code": "421"},

    # ═══════════════════════════════════════════
    # LOẠI 4 — DOANH THU (REVENUE)
    # ═══════════════════════════════════════════

    # ── TK 511 — Doanh thu bán hàng và cung cấp dịch vụ ──
    {"code": "511", "name": "Doanh thu bán hàng và cung cấp dịch vụ", "level": 1, "type": "revenue",
     "name_en": "Revenue from sales and services"},
    {"code": "5111", "name": "Doanh thu bán hàng hóa", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5112", "name": "Doanh thu bán thành phẩm", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5113", "name": "Doanh thu cung cấp dịch vụ", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5114", "name": "Doanh thu trợ giá, phụ thu", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5115", "name": "Doanh thu bán BĐS đầu tư", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5117", "name": "Doanh thu kinh doanh BĐS đầu tư", "level": 2, "type": "revenue", "parent_code": "511"},
    {"code": "5118", "name": "Doanh thu khác", "level": 2, "type": "revenue", "parent_code": "511"},

    # ── TK 515 — Doanh thu hoạt động tài chính ──
    {"code": "515", "name": "Doanh thu hoạt động tài chính", "level": 1, "type": "revenue",
     "name_en": "Financial income"},

    # ── TK 521 — Các khoản giảm trừ doanh thu ──
    {"code": "521", "name": "Các khoản giảm trừ doanh thu", "level": 1, "type": "revenue",
     "name_en": "Revenue deductions"},
    {"code": "5211", "name": "Chiết khấu thương mại", "level": 2, "type": "revenue", "parent_code": "521"},
    {"code": "5212", "name": "Hàng bán bị trả lại", "level": 2, "type": "revenue", "parent_code": "521"},
    {"code": "5213", "name": "Giảm giá hàng bán", "level": 2, "type": "revenue", "parent_code": "521"},
    {"code": "5214", "name": "Thuế TTĐB, thuế XK, thuế GTGT theo phương pháp trực tiếp", "level": 2, "type": "revenue", "parent_code": "521"},

    # ═══════════════════════════════════════════
    # LOẠI 5 — CHI PHÍ SẢN XUẤT, KINH DOANH (COSTS)
    # ═══════════════════════════════════════════

    # ── TK 621 — Chi phí nguyên liệu, vật liệu trực tiếp ──
    {"code": "621", "name": "Chi phí nguyên liệu, vật liệu trực tiếp", "level": 1, "type": "expense",
     "name_en": "Direct materials cost"},

    # ── TK 622 — Chi phí nhân công trực tiếp ──
    {"code": "622", "name": "Chi phí nhân công trực tiếp", "level": 1, "type": "expense",
     "name_en": "Direct labor cost"},

    # ── TK 627 — Chi phí sản xuất chung ──
    {"code": "627", "name": "Chi phí sản xuất chung", "level": 1, "type": "expense",
     "name_en": "Manufacturing overhead"},
    {"code": "6271", "name": "Chi phí nhân viên phân xưởng", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6272", "name": "Chi phí vật liệu", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6273", "name": "Chi phí công cụ, dụng cụ", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6274", "name": "Chi phí khấu hao TSCĐ", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6275", "name": "Chi phí dịch vụ mua ngoài", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6277", "name": "Chi phí bằng tiền khác", "level": 2, "type": "expense", "parent_code": "627"},
    {"code": "6278", "name": "Chi phí sản xuất chung khác", "level": 2, "type": "expense", "parent_code": "627"},

    # ── TK 632 — Giá vốn hàng bán ──
    {"code": "632", "name": "Giá vốn hàng bán", "level": 1, "type": "expense",
     "name_en": "Cost of goods sold"},

    # ── TK 635 — Chi phí tài chính ──
    {"code": "635", "name": "Chi phí tài chính", "level": 1, "type": "expense",
     "name_en": "Financial expenses"},

    # ── TK 641 — Chi phí bán hàng ──
    {"code": "641", "name": "Chi phí bán hàng", "level": 1, "type": "expense",
     "name_en": "Selling expenses"},
    {"code": "6411", "name": "Chi phí nhân viên bán hàng", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6412", "name": "Chi phí vật liệu, bao bì", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6413", "name": "Chi phí công cụ, dụng cụ", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6414", "name": "Chi phí khấu hao TSCĐ", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6415", "name": "Chi phí bảo hành", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6417", "name": "Chi phí dịch vụ mua ngoài", "level": 2, "type": "expense", "parent_code": "641"},
    {"code": "6418", "name": "Chi phí bán hàng khác", "level": 2, "type": "expense", "parent_code": "641"},

    # ── TK 642 — Chi phí quản lý doanh nghiệp ──
    {"code": "642", "name": "Chi phí quản lý doanh nghiệp", "level": 1, "type": "expense",
     "name_en": "Administrative expenses"},
    {"code": "6421", "name": "Chi phí nhân viên quản lý", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6422", "name": "Chi phí vật liệu quản lý", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6423", "name": "Chi phí công cụ, dụng cụ", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6424", "name": "Chi phí khấu hao TSCĐ", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6425", "name": "Thuế, phí, lệ phí", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6426", "name": "Chi phí dự phòng", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6427", "name": "Chi phí dịch vụ mua ngoài", "level": 2, "type": "expense", "parent_code": "642"},
    {"code": "6428", "name": "Chi phí quản lý khác", "level": 2, "type": "expense", "parent_code": "642"},

    # ═══════════════════════════════════════════
    # LOẠI 6 — THU NHẬP KHÁC (OTHER INCOME)
    # ═══════════════════════════════════════════

    # ── TK 711 — Thu nhập khác ──
    {"code": "711", "name": "Thu nhập khác", "level": 1, "type": "revenue",
     "name_en": "Other income"},

    # ═══════════════════════════════════════════
    # LOẠI 7 — CHI PHÍ KHÁC (OTHER EXPENSES)
    # ═══════════════════════════════════════════

    # ── TK 811 — Chi phí khác ──
    {"code": "811", "name": "Chi phí khác", "level": 1, "type": "expense",
     "name_en": "Other expenses"},

    # ── TK 821 — Chi phí thuế TNDN ──
    {"code": "821", "name": "Chi phí thuế thu nhập doanh nghiệp", "level": 1, "type": "expense",
     "name_en": "Corporate income tax expense"},
    {"code": "8211", "name": "Chi phí thuế TNDN hiện hành", "level": 2, "type": "expense", "parent_code": "821"},
    {"code": "82111", "name": "Chi phí thuế TNDN hiện hành thông thường", "level": 3, "type": "expense", "parent_code": "8211"},
    {"code": "82112", "name": "Chi phí thuế TNDN bổ sung (tối thiểu toàn cầu)", "level": 3, "type": "expense", "parent_code": "8211"},
    {"code": "8212", "name": "Chi phí thuế TNDN hoãn lại", "level": 2, "type": "expense", "parent_code": "821"},

    # ═══════════════════════════════════════════
    # LOẠI 8 — XÁC ĐỊNH KẾT QUẢ KINH DOANH
    # ═══════════════════════════════════════════

    # ── TK 911 — Xác định kết quả kinh doanh ──
    {"code": "911", "name": "Xác định kết quả kinh doanh", "level": 1, "type": "expense",
     "name_en": "Business results determination"},
]
