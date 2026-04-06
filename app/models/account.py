from app.extensions import db
from app.models.base import BaseModel


class Account(BaseModel):
    __tablename__ = "accounts"

    code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255), default="")
    level = db.Column(db.Integer, nullable=False, default=1)
    parent_code = db.Column(db.String(10), db.ForeignKey("accounts.code"), nullable=True)
    account_type = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, default="")
    is_system = db.Column(db.Boolean, default=True, nullable=False)

    parent = db.relationship("Account", remote_side=[code], backref="children")
    journal_lines = db.relationship("JournalEntryLine", backref="account", lazy="dynamic")

    @property
    def is_asset(self):
        return self.account_type == "asset"

    @property
    def is_liability(self):
        return self.account_type == "liability"

    @property
    def is_equity(self):
        return self.account_type == "equity"

    @property
    def is_revenue(self):
        return self.account_type == "revenue"

    @property
    def is_expense(self):
        return self.account_type == "expense"

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def get_by_type(cls, account_type):
        return cls.query.filter_by(account_type=account_type).order_by(cls.code).all()

    @classmethod
    def get_all_level1(cls):
        return cls.query.filter_by(level=1).order_by(cls.code).all()

    def __repr__(self):
        return f"<Account {self.code} - {self.name}>"

    @classmethod
    def get_circular99_accounts(cls):
        return [
            {"code": "111", "name": "Tiền mặt", "level": 1, "type": "asset"},
            {"code": "112", "name": "Tiền gửi không kỳ hạn", "level": 1, "type": "asset"},
            {"code": "113", "name": "Tiền đang chuyển", "level": 1, "type": "asset"},
            {"code": "121", "name": "Chứng khoán kinh doanh", "level": 1, "type": "asset"},
            {"code": "128", "name": "Đầu tư nắm giữ đến ngày đáo hạn", "level": 1, "type": "asset"},
            {"code": "131", "name": "Phải thu của khách hàng", "level": 1, "type": "asset"},
            {"code": "133", "name": "Thuế GTGT được khấu trừ", "level": 1, "type": "asset"},
            {"code": "1331", "name": "Thuế GTGT được khấu trừ của hàng hóa, dịch vụ", "level": 2, "type": "asset"},
            {"code": "1332", "name": "Thuế GTGT được khấu trừ của TSCĐ", "level": 2, "type": "asset"},
            {"code": "136", "name": "Phải thu nội bộ", "level": 1, "type": "asset"},
            {"code": "138", "name": "Phải thu khác", "level": 1, "type": "asset"},
            {"code": "141", "name": "Tạm ứng", "level": 1, "type": "asset"},
            {"code": "151", "name": "Hàng mua đang đi đường", "level": 1, "type": "asset"},
            {"code": "152", "name": "Nguyên liệu, vật liệu", "level": 1, "type": "asset"},
            {"code": "153", "name": "Công cụ, dụng cụ", "level": 1, "type": "asset"},
            {"code": "154", "name": "Chi phí sản xuất, kinh doanh dở dang", "level": 1, "type": "asset"},
            {"code": "155", "name": "Sản phẩm", "level": 1, "type": "asset"},
            {"code": "156", "name": "Hàng hóa", "level": 1, "type": "asset"},
            {"code": "157", "name": "Hàng gửi đi bán", "level": 1, "type": "asset"},
            {"code": "211", "name": "Tài sản cố định hữu hình", "level": 1, "type": "asset"},
            {"code": "212", "name": "Tài sản cố định thuê tài chính", "level": 1, "type": "asset"},
            {"code": "213", "name": "Tài sản cố định vô hình", "level": 1, "type": "asset"},
            {"code": "214", "name": "Hao mòn tài sản cố định", "level": 1, "type": "asset"},
            {"code": "221", "name": "Đầu tư vào công ty con", "level": 1, "type": "asset"},
            {"code": "222", "name": "Đầu tư vào công ty liên doanh, liên kết", "level": 1, "type": "asset"},
            {"code": "228", "name": "Đầu tư khác", "level": 1, "type": "asset"},
            {"code": "229", "name": "Dự phòng tổn thất tài sản", "level": 1, "type": "asset"},
            {"code": "241", "name": "Xây dựng cơ bản dở dang", "level": 1, "type": "asset"},
            {"code": "242", "name": "Chi phí chờ phân bổ", "level": 1, "type": "asset"},
            {"code": "331", "name": "Phải trả cho người bán", "level": 1, "type": "liability"},
            {"code": "332", "name": "Phải trả cổ tức, lợi nhuận", "level": 1, "type": "liability"},
            {"code": "333", "name": "Thuế và các khoản phải nộp Nhà nước", "level": 1, "type": "liability"},
            {"code": "3331", "name": "Thuế giá trị gia tăng phải nộp", "level": 2, "type": "liability"},
            {"code": "33311", "name": "Thuế GTGT đầu ra", "level": 3, "type": "liability"},
            {"code": "33312", "name": "Thuế GTGT hàng nhập khẩu", "level": 3, "type": "liability"},
            {"code": "3334", "name": "Thuế thu nhập doanh nghiệp", "level": 2, "type": "liability"},
            {"code": "3335", "name": "Thuế thu nhập cá nhân", "level": 2, "type": "liability"},
            {"code": "334", "name": "Phải trả người lao động", "level": 1, "type": "liability"},
            {"code": "335", "name": "Chi phí phải trả", "level": 1, "type": "liability"},
            {"code": "336", "name": "Phải trả nội bộ", "level": 1, "type": "liability"},
            {"code": "338", "name": "Phải trả, phải nộp khác", "level": 1, "type": "liability"},
            {"code": "3383", "name": "Bảo hiểm xã hội", "level": 2, "type": "liability"},
            {"code": "3384", "name": "Bảo hiểm y tế", "level": 2, "type": "liability"},
            {"code": "3386", "name": "Bảo hiểm thất nghiệp", "level": 2, "type": "liability"},
            {"code": "341", "name": "Vay và nợ thuê tài chính", "level": 1, "type": "liability"},
            {"code": "411", "name": "Vốn đầu tư của chủ sở hữu", "level": 1, "type": "equity"},
            {"code": "421", "name": "Lợi nhuận sau thuế chưa phân phối", "level": 1, "type": "equity"},
            {"code": "511", "name": "Doanh thu bán hàng và cung cấp dịch vụ", "level": 1, "type": "revenue"},
            {"code": "515", "name": "Doanh thu hoạt động tài chính", "level": 1, "type": "revenue"},
            {"code": "521", "name": "Các khoản giảm trừ doanh thu", "level": 1, "type": "revenue"},
            {"code": "621", "name": "Chi phí nguyên liệu, vật liệu trực tiếp", "level": 1, "type": "expense"},
            {"code": "622", "name": "Chi phí nhân công trực tiếp", "level": 1, "type": "expense"},
            {"code": "627", "name": "Chi phí sản xuất chung", "level": 1, "type": "expense"},
            {"code": "632", "name": "Giá vốn hàng bán", "level": 1, "type": "expense"},
            {"code": "635", "name": "Chi phí tài chính", "level": 1, "type": "expense"},
            {"code": "641", "name": "Chi phí bán hàng", "level": 1, "type": "expense"},
            {"code": "642", "name": "Chi phí quản lý doanh nghiệp", "level": 1, "type": "expense"},
            {"code": "711", "name": "Thu nhập khác", "level": 1, "type": "revenue"},
            {"code": "811", "name": "Chi phí khác", "level": 1, "type": "expense"},
            {"code": "821", "name": "Chi phí thuế thu nhập doanh nghiệp", "level": 1, "type": "expense"},
            {"code": "911", "name": "Xác định kết quả kinh doanh", "level": 1, "type": "expense"},
        ]
