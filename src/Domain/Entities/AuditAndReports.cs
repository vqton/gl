using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Theo dõi tất cả các thay đổi và giao dịch trong hệ thống kế toán
    /// </summary>
    public class AuditEntry
    {
        /// <summary>
        /// Mã bản ghi audit
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Mã giao dịch liên quan
        /// </summary>
        public string TransactionId { get; set; }

        /// <summary>
        /// Loại hành động (CREATE, UPDATE, DELETE, POST, UNPOST)
        /// </summary>
        public string ActionType { get; set; }

        /// <summary>
        /// Mã tài khoản liên quan
        /// </summary>
        public string AccountCode { get; set; }

        /// <summary>
        /// Số tiền (nếu có)
        /// </summary>
        public decimal Amount { get; set; }

        /// <summary>
        /// Ngày thực hiện hành động
        /// </summary>
        public DateTime ActionDate { get; set; }

        /// <summary>
        /// Người thực hiện hành động
        /// </summary>
        public string UserId { get; set; }

        /// <summary>
        /// Mô tả chi tiết hành động
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Giá trị cũ (cho UPDATE)
        /// </summary>
        public string OldValue { get; set; }

        /// <summary>
        /// Giá trị mới (cho UPDATE)
        /// </summary>
        public string NewValue { get; set; }

        /// <summary>
        /// Địa IP của người dùng
        /// </summary>
        public string IpAddress { get; set; }
    }

    /// <summary>
    /// Báo cáo tài chính - Bảng cân đối kế toán (BCĐKT)
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class BalanceSheetReport
    {
        /// <summary>
        /// Mã kỳ báo cáo
        /// </summary>
        public string PeriodCode { get; set; }

        /// <summary>
        /// Ngày lập báo cáo
        /// </summary>
        public DateTime ReportDate { get; set; }

        /// <summary>
        /// Danh sách tài sản
        /// </summary>
        public List<BalanceSheetLine> Assets { get; set; } = new List<BalanceSheetLine>();

        /// <summary>
        /// Danh sách nợ phải trả
        /// </summary>
        public List<BalanceSheetLine> Liabilities { get; set; } = new List<BalanceSheetLine>();

        /// <summary>
        /// Danh sách vốn chủ sở hữu
        /// </summary>
        public List<BalanceSheetLine> Equities { get; set; } = new List<BalanceSheetLine>();

        /// <summary>
        /// Thêm tài sản vào báo cáo
        /// </summary>
        public void AddAsset(string code, string name, decimal amount)
        {
            Assets.Add(new BalanceSheetLine { Code = code, Name = name, Amount = amount });
        }

        /// <summary>
        /// Thêm nợ phải trả vào báo cáo
        /// </summary>
        public void AddLiability(string code, string name, decimal amount)
        {
            Liabilities.Add(new BalanceSheetLine { Code = code, Name = name, Amount = amount });
        }

        /// <summary>
        /// Thêm vốn chủ sở hữu vào báo cáo
        /// </summary>
        public void AddEquity(string code, string name, decimal amount)
        {
            Equities.Add(new BalanceSheetLine { Code = code, Name = name, Amount = amount });
        }

        /// <summary>
        /// Tổng tài sản
        /// </summary>
        public decimal TotalAssets
        {
            get
            {
                decimal total = 0;
                foreach (var item in Assets)
                    total += item.Amount;
                return total;
            }
        }

        /// <summary>
        /// Tổng nợ phải trả
        /// </summary>
        public decimal TotalLiabilities
        {
            get
            {
                decimal total = 0;
                foreach (var item in Liabilities)
                    total += item.Amount;
                return total;
            }
        }

        /// <summary>
        /// Tổng vốn chủ sở hữu
        /// </summary>
        public decimal TotalEquity
        {
            get
            {
                decimal total = 0;
                foreach (var item in Equities)
                    total += item.Amount;
                return total;
            }
        }

        /// <summary>
        /// Kiểm tra báo cáo có cân bằng không
        /// </summary>
        public bool IsBalanced
        {
            get
            {
                return Math.Abs(TotalAssets - (TotalLiabilities + TotalEquity)) < 0.01m;
            }
        }
    }

    /// <summary>
    /// Dòng trong báo cáo tài chính
    /// </summary>
    public class BalanceSheetLine
    {
        /// <summary>
        /// Mã tài khoản
        /// </summary>
        public string Code { get; set; }

        /// <summary>
        /// Tên tài khoản
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Số tiền
        /// </summary>
        public decimal Amount { get; set; }
    }

    /// <summary>
    /// Báo cáo kết quả hoạt động kinh doanh (BCKQHĐKD)
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class IncomeStatementReport
    {
        /// <summary>
        /// Mã kỳ báo cáo
        /// </summary>
        public string PeriodCode { get; set; }

        /// <summary>
        /// Ngày lập báo cáo
        /// </summary>
        public DateTime ReportDate { get; set; }

        /// <summary>
        /// Danh sách doanh thu
        /// </summary>
        public List<IncomeStatementLine> Revenues { get; set; } = new List<IncomeStatementLine>();

        /// <summary>
        /// Danh sách chi phí
        /// </summary>
        public List<IncomeStatementLine> Expenses { get; set; } = new List<IncomeStatementLine>();

        /// <summary>
        /// Thêm doanh thu vào báo cáo
        /// </summary>
        public void AddRevenue(string code, string name, decimal amount)
        {
            Revenues.Add(new IncomeStatementLine { Code = code, Name = name, Amount = amount });
        }

        /// <summary>
        /// Thêm chi phí vào báo cáo
        /// </summary>
        public void AddExpense(string code, string name, decimal amount)
        {
            Expenses.Add(new IncomeStatementLine { Code = code, Name = name, Amount = amount });
        }

        /// <summary>
        /// Tổng doanh thu
        /// </summary>
        public decimal TotalRevenue
        {
            get
            {
                decimal total = 0;
                foreach (var item in Revenues)
                    total += item.Amount;
                return total;
            }
        }

        /// <summary>
        /// Tổng chi phí
        /// </summary>
        public decimal TotalExpenses
        {
            get
            {
                decimal total = 0;
                foreach (var item in Expenses)
                    total += item.Amount;
                return total;
            }
        }

        /// <summary>
        /// Lợi nhuận gộp (Doanh thu thuần - Giá vốn hàng bán)
        /// </summary>
        public decimal GrossProfit
        {
            get
            {
                decimal revenue = 0;
                decimal cogs = 0;
                foreach (var item in Revenues)
                {
                    if (item.Code == "511")
                        revenue += item.Amount;
                    if (item.Code == "521")
                        revenue -= item.Amount;
                }
                foreach (var item in Expenses)
                {
                    if (item.Code == "632")
                        cogs += item.Amount;
                }
                return revenue - cogs;
            }
        }

        /// <summary>
        /// Lợi nhuận ròng (Tổng doanh thu - Tổng chi phí)
        /// </summary>
        public decimal NetProfit
        {
            get
            {
                return TotalRevenue - TotalExpenses;
            }
        }
    }

    /// <summary>
    /// Dòng trong báo cáo kết quả hoạt động kinh doanh
    /// </summary>
    public class IncomeStatementLine
    {
        /// <summary>
        /// Mã tài khoản
        /// </summary>
        public string Code { get; set; }

        /// <summary>
        /// Tên tài khoản
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Số tiền
        /// </summary>
        public decimal Amount { get; set; }
    }
}
