"""Financial report generation service — Circular 99/2025 compliance.

Generates standard Vietnamese financial statements:
- B01-DN: Balance Sheet (Bảng cân đối kế toán)
- B02-DN: Income Statement (Kết quả hoạt động kinh doanh)
- B03-DN: Cash Flow Statement (Lưu chuyển tiền tệ)
- B09-DN: Notes to financial statements (Thuyết minh BCTC)
"""
from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models.account import Account
from app.models.journal_entry import JournalEntry, JournalEntryLine
from app.models.invoice import Invoice
from app.models.bill import Bill


ACCOUNT_MAP_B01 = {
    "A": {
        "111": "Tiền mặt",
        "112": "Tiền gửi ngân hàng",
        "113": "Tiền đang chuyển",
        "121": "Chứng khoán kinh doanh",
        "123": "Đầu tư nắm giữ đến ngày đáo hạn",
        "131": "Phải thu của khách hàng",
        "133": "Thuế GTGT được khấu trừ",
        "136": "Phải thu nội bộ",
        "138": "Phải thu khác",
        "141": "Tạm ứng",
        "151": "Hàng mua đang đi đường",
        "152": "Nguyên liệu, vật liệu",
        "153": "Công cụ, dụng cụ",
        "154": "Chi phí SXKD dở dang",
        "155": "Thành phẩm",
        "156": "Hàng hóa",
        "157": "Hàng gửi đi bán",
        "211": "TSCĐ hữu hình",
        "212": "TSCĐ thuê tài chính",
        "213": "TSCĐ vô hình",
        "214": "Hao mòn TSCĐ",
        "221": "Đầu tư vào công ty con",
        "222": "Đầu tư vào công ty liên kết",
        "228": "Đầu tư khác",
        "229": "Dự phòng tổn thất tài sản",
        "241": "Xây dựng cơ bản dở dang",
        "242": "Chi phí chờ phân bổ",
    },
    "B": {
        "311": "Vay và nợ thuê tài chính ngắn hạn",
        "331": "Phải trả cho người bán",
        "332": "Phải trả cổ tức, lợi nhuận",
        "333": "Thuế và các khoản phải nộp NN",
        "334": "Phải trả người lao động",
        "335": "Chi phí phải trả",
        "336": "Phải trả nội bộ",
        "338": "Phải trả, phải nộp khác",
        "341": "Vay và nợ thuê tài chính dài hạn",
        "347": "Thuế TNDN hoãn lại phải trả",
        "352": "Dự phòng phải trả",
        "353": "Quỹ khen thưởng, phúc lợi",
        "356": "Quỹ phát triển KH&CN",
        "411": "Vốn đầu tư của chủ sở hữu",
        "412": "Chênh lệch đánh giá lại tài sản",
        "413": "Chênh lệch tỷ giá hối đoái",
        "414": "Quỹ đầu tư phát triển",
        "418": "Các quỹ khác thuộc VCSH",
        "419": "Cổ phiếu mua lại",
        "421": "Lợi nhuận sau thuế chưa phân phối",
    },
}

ACCOUNT_MAP_B02 = {
    "10": "Doanh thu bán hàng và cung cấp dịch vụ",
    "20": "Các khoản giảm trừ doanh thu",
    "30": "Doanh thu thuần về bán hàng và cung cấp dịch vụ",
    "40": "Giá vốn hàng bán",
    "50": "Lợi nhuận gộp",
    "60": "Doanh thu hoạt động tài chính",
    "70": "Chi phí tài chính",
    "80": "Chi phí bán hàng",
    "90": "Chi phí quản lý doanh nghiệp",
    "100": "Lợi nhuận thuần từ hoạt động kinh doanh",
    "110": "Thu nhập khác",
    "120": "Chi phí khác",
    "130": "Lợi nhuận khác",
    "140": "Tổng lợi nhuận kế toán trước thuế",
    "150": "Chi phí thuế TNDN hiện hành",
    "160": "Lợi nhuận sau thuế thu nhập doanh nghiệp",
}


class ReportService:
    """Financial report generation."""

    @staticmethod
    def _get_balance(account_code, period, status="posted"):
        """Get debit and credit balance for an account up to a period."""
        debit_q = (
            db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.debit_amount), 0))
            .join(JournalEntry)
            .filter(
                JournalEntryLine.account_code.like(f"{account_code}%"),
                JournalEntry.accounting_period <= period,
                JournalEntry.status == status,
            )
        )
        credit_q = (
            db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.credit_amount), 0))
            .join(JournalEntry)
            .filter(
                JournalEntryLine.account_code.like(f"{account_code}%"),
                JournalEntry.accounting_period <= period,
                JournalEntry.status == status,
            )
        )
        return debit_q.scalar(), credit_q.scalar()

    @staticmethod
    def _get_period_balance(account_code, period, status="posted"):
        """Get debit and credit for a specific period only."""
        debit_q = (
            db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.debit_amount), 0))
            .join(JournalEntry)
            .filter(
                JournalEntryLine.account_code.like(f"{account_code}%"),
                JournalEntry.accounting_period == period,
                JournalEntry.status == status,
            )
        )
        credit_q = (
            db.session.query(db.func.coalesce(db.func.sum(JournalEntryLine.credit_amount), 0))
            .join(JournalEntry)
            .filter(
                JournalEntryLine.account_code.like(f"{account_code}%"),
                JournalEntry.accounting_period == period,
                JournalEntry.status == status,
            )
        )
        return debit_q.scalar(), credit_q.scalar()

    @staticmethod
    def generate_b01(period):
        """Generate Balance Sheet (Bảng cân đối kế toán) — B01-DN.

        Assets = Liabilities + Equity
        """
        rows = []
        total_assets = Decimal("0")
        total_liabilities = Decimal("0")
        total_equity = Decimal("0")

        asset_accounts = [
            ("111", "Tiền mặt"),
            ("112", "Tiền gửi ngân hàng"),
            ("113", "Tiền đang chuyển"),
            ("121", "Chứng khoán kinh doanh"),
            ("123", "Đầu tư nắm giữ đến ngày đáo hạn"),
            ("131", "Phải thu của khách hàng"),
            ("133", "Thuế GTGT được khấu trừ"),
            ("136", "Phải thu nội bộ"),
            ("138", "Phải thu khác"),
            ("141", "Tạm ứng"),
            ("151", "Hàng mua đang đi đường"),
            ("152", "Nguyên liệu, vật liệu"),
            ("153", "Công cụ, dụng cụ"),
            ("154", "Chi phí SXKD dở dang"),
            ("155", "Thành phẩm"),
            ("156", "Hàng hóa"),
            ("157", "Hàng gửi đi bán"),
            ("211", "TSCĐ hữu hình"),
            ("212", "TSCĐ thuê tài chính"),
            ("213", "TSCĐ vô hình"),
            ("214", "Hao mòn TSCĐ"),
            ("221", "Đầu tư vào công ty con"),
            ("222", "Đầu tư vào công ty liên kết"),
            ("228", "Đầu tư khác"),
            ("229", "Dự phòng tổn thất tài sản"),
            ("241", "Xây dựng cơ bản dở dang"),
            ("242", "Chi phí chờ phân bổ"),
        ]

        for code, name in asset_accounts:
            debit, credit = ReportService._get_balance(code, period)
            balance = debit - credit
            total_assets += balance
            rows.append({
                "code": code,
                "name": name,
                "beginning": 0,
                "ending": float(balance),
                "section": "A",
            })

        liability_accounts = [
            ("311", "Vay và nợ thuê tài chính ngắn hạn"),
            ("331", "Phải trả cho người bán"),
            ("332", "Phải trả cổ tức, lợi nhuận"),
            ("333", "Thuế và các khoản phải nộp NN"),
            ("334", "Phải trả người lao động"),
            ("335", "Chi phí phải trả"),
            ("336", "Phải trả nội bộ"),
            ("338", "Phải trả, phải nộp khác"),
            ("341", "Vay và nợ thuê tài chính dài hạn"),
            ("347", "Thuế TNDN hoãn lại phải trả"),
            ("352", "Dự phòng phải trả"),
            ("353", "Quỹ khen thưởng, phúc lợi"),
            ("356", "Quỹ phát triển KH&CN"),
        ]

        for code, name in liability_accounts:
            debit, credit = ReportService._get_balance(code, period)
            balance = credit - debit
            total_liabilities += balance
            rows.append({
                "code": code,
                "name": name,
                "beginning": 0,
                "ending": float(balance),
                "section": "B",
            })

        equity_accounts = [
            ("411", "Vốn đầu tư của chủ sở hữu"),
            ("412", "Chênh lệch đánh giá lại tài sản"),
            ("413", "Chênh lệch tỷ giá hối đoái"),
            ("414", "Quỹ đầu tư phát triển"),
            ("418", "Các quỹ khác thuộc VCSH"),
            ("419", "Cổ phiếu mua lại"),
            ("421", "Lợi nhuận sau thuế chưa phân phối"),
        ]

        for code, name in equity_accounts:
            debit, credit = ReportService._get_balance(code, period)
            balance = credit - debit
            total_equity += balance
            rows.append({
                "code": code,
                "name": name,
                "beginning": 0,
                "ending": float(balance),
                "section": "C",
            })

        return {
            "period": period,
            "report_name": "BẢNG CÂN ĐỐI KẾ TOÁN",
            "report_code": "B01-DN",
            "rows": rows,
            "total_assets": float(total_assets),
            "total_liabilities": float(total_liabilities),
            "total_equity": float(total_equity),
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def generate_b02(period):
        """Generate Income Statement (Kết quả hoạt động kinh doanh) — B02-DN."""
        this_period = period
        year = period.split("-")[0]

        revenue_d, revenue_c = ReportService._get_period_balance("511", this_period)
        revenue_d_y, revenue_c_y = ReportService._get_balance("511", f"{year}-12")

        reduction_d, reduction_c = ReportService._get_period_balance("521", this_period)
        net_revenue = revenue_c - revenue_d - (reduction_d - reduction_c)

        cogs_d, cogs_c = ReportService._get_period_balance("632", this_period)
        gross_profit = net_revenue - (cogs_d - cogs_c)

        fin_rev_d, fin_rev_c = ReportService._get_period_balance("515", this_period)
        fin_exp_d, fin_exp_c = ReportService._get_period_balance("635", this_period)

        sell_exp_d, sell_exp_c = ReportService._get_period_balance("641", this_period)
        mgmt_exp_d, mgmt_exp_c = ReportService._get_period_balance("642", this_period)

        op_profit = gross_profit + (fin_rev_c - fin_rev_d) - (fin_exp_d - fin_exp_c) - \
                    (sell_exp_d - sell_exp_c) - (mgmt_exp_d - mgmt_exp_c)

        other_inc_d, other_inc_c = ReportService._get_period_balance("711", this_period)
        other_exp_d, other_exp_c = ReportService._get_period_balance("811", this_period)

        total_profit = op_profit + (other_inc_c - other_inc_d) - (other_exp_d - other_exp_c)

        cit_d, cit_c = ReportService._get_period_balance("821", this_period)
        net_profit = total_profit - (cit_d - cit_c)

        rows = [
            {"code": "10", "name": "Doanh thu bán hàng và cung cấp dịch vụ",
             "this_period": float(revenue_c - revenue_d), "prev_year": 0},
            {"code": "20", "name": "Các khoản giảm trừ doanh thu",
             "this_period": float(reduction_d - reduction_c), "prev_year": 0},
            {"code": "30", "name": "Doanh thu thuần",
             "this_period": float(net_revenue), "prev_year": 0},
            {"code": "40", "name": "Giá vốn hàng bán",
             "this_period": float(cogs_d - cogs_c), "prev_year": 0},
            {"code": "50", "name": "Lợi nhuận gộp",
             "this_period": float(gross_profit), "prev_year": 0},
            {"code": "60", "name": "Doanh thu hoạt động tài chính",
             "this_period": float(fin_rev_c - fin_rev_d), "prev_year": 0},
            {"code": "70", "name": "Chi phí tài chính",
             "this_period": float(fin_exp_d - fin_exp_c), "prev_year": 0},
            {"code": "80", "name": "Chi phí bán hàng",
             "this_period": float(sell_exp_d - sell_exp_c), "prev_year": 0},
            {"code": "90", "name": "Chi phí quản lý doanh nghiệp",
             "this_period": float(mgmt_exp_d - mgmt_exp_c), "prev_year": 0},
            {"code": "100", "name": "Lợi nhuận thuần từ HĐKD",
             "this_period": float(op_profit), "prev_year": 0},
            {"code": "110", "name": "Thu nhập khác",
             "this_period": float(other_inc_c - other_inc_d), "prev_year": 0},
            {"code": "120", "name": "Chi phí khác",
             "this_period": float(other_exp_d - other_exp_c), "prev_year": 0},
            {"code": "130", "name": "Lợi nhuận khác",
             "this_period": float((other_inc_c - other_inc_d) - (other_exp_d - other_exp_c)), "prev_year": 0},
            {"code": "140", "name": "Tổng lợi nhuận kế toán trước thuế",
             "this_period": float(total_profit), "prev_year": 0},
            {"code": "150", "name": "Chi phí thuế TNDN",
             "this_period": float(cit_d - cit_c), "prev_year": 0},
            {"code": "160", "name": "Lợi nhuận sau thuế TNDN",
             "this_period": float(net_profit), "prev_year": 0},
        ]

        return {
            "period": period,
            "report_name": "BÁO CÁO KẾT QUẢ HOẠT ĐỘNG KINH DOANH",
            "report_code": "B02-DN",
            "rows": rows,
            "net_profit": float(net_profit),
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def generate_b03(period):
        """Generate Cash Flow Statement (Lưu chuyển tiền tệ) — B03-DN.

        Simplified version based on journal entries affecting cash accounts (111, 112, 113).
        """
        cash_accounts = ("111", "112", "113")
        cash_debit = Decimal("0")
        cash_credit = Decimal("0")

        for acc in cash_accounts:
            d, c = ReportService._get_period_balance(acc, period)
            cash_debit += d
            cash_credit += c

        net_cash_flow = cash_debit - cash_credit

        rows = [
            {"code": "01", "name": "Lưu chuyển tiền từ hoạt động kinh doanh", "amount": float(cash_debit)},
            {"code": "02", "name": "Tiền thu từ bán hàng, cung cấp dịch vụ", "amount": 0},
            {"code": "03", "name": "Tiền chi trả cho người cung cấp", "amount": 0},
            {"code": "04", "name": "Tiền chi trả cho người lao động", "amount": 0},
            {"code": "05", "name": "Tiền chi trả lãi vay", "amount": 0},
            {"code": "06", "name": "Tiền chi nộp thuế TNDN", "amount": 0},
            {"code": "07", "name": "Tiền thu khác từ hoạt động kinh doanh", "amount": 0},
            {"code": "08", "name": "Tiền chi khác từ hoạt động kinh doanh", "amount": 0},
            {"code": "20", "name": "Lưu chuyển tiền thuần từ hoạt động kinh doanh",
             "amount": float(cash_debit - cash_credit)},
            {"code": "21", "name": "Lưu chuyển tiền từ hoạt động đầu tư", "amount": 0},
            {"code": "31", "name": "Lưu chuyển tiền từ hoạt động tài chính", "amount": 0},
            {"code": "50", "name": "Lưu chuyển tiền thuần trong kỳ", "amount": float(net_cash_flow)},
        ]

        return {
            "period": period,
            "report_name": "BÁO CÁO LƯU CHUYỂN TIỀN TỆ",
            "report_code": "B03-DN",
            "rows": rows,
            "net_cash_flow": float(net_cash_flow),
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def generate_b09(period):
        """Generate Notes to Financial Statements (Thuyết minh BCTC) — B09-DN."""
        accounts = Account.query.order_by(Account.code).all()
        account_details = []
        for acc in accounts:
            d, c = ReportService._get_balance(acc.code, period)
            if d != 0 or c != 0:
                account_details.append({
                    "code": acc.code,
                    "name": acc.name,
                    "type": acc.account_type,
                    "debit": float(d),
                    "credit": float(c),
                    "balance": float(d - c),
                })

        invoice_count = Invoice.query.filter(
            Invoice.accounting_period == period
        ).count()
        bill_count = Bill.query.filter(
            Bill.accounting_period == period
        ).count()
        je_count = JournalEntry.query.filter(
            JournalEntry.accounting_period == period,
            JournalEntry.status == "posted",
        ).count()

        return {
            "period": period,
            "report_name": "THUYẾT MINH BÁO CÁO TÀI CHÍNH",
            "report_code": "B09-DN",
            "account_details": account_details,
            "statistics": {
                "total_accounts": len(account_details),
                "invoices": invoice_count,
                "bills": bill_count,
                "journal_entries": je_count,
            },
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_dashboard_summary(period):
        """Dashboard KPIs for the main dashboard."""
        b01 = ReportService.generate_b01(period)
        b02 = ReportService.generate_b02(period)

        pending_invoices = Invoice.query.filter_by(status="draft").count()
        pending_bills = Bill.query.filter_by(status="draft").count()
        pending_approvals = Invoice.query.filter_by(status="submitted").count()
        pending_bill_approvals = Bill.query.filter_by(status="submitted").count()

        from app.models.employee import Payslip
        pending_payslips = Payslip.query.filter_by(status="draft", period=period).count()

        return {
            "period": period,
            "total_assets": b01["total_assets"],
            "total_liabilities": b01["total_liabilities"],
            "total_equity": b01["total_equity"],
            "net_profit": b02["net_profit"],
            "pending_invoices": pending_invoices,
            "pending_bills": pending_bills,
            "pending_approvals": pending_approvals,
            "pending_bill_approvals": pending_bill_approvals,
            "pending_payslips": pending_payslips,
        }
