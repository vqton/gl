using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho một ngân sách kế toán
    /// </summary>
    public class Budget
    {
        /// <summary>
        /// Mã ngân sách
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Tên ngân sách
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Năm tài chính
        /// </summary>
        public int FiscalYear { get; set; }

        /// <summary>
        /// Mã kỳ kế toán
        /// </summary>
        public string PeriodCode { get; set; }

        /// <summary>
        /// Tổng số tiền ngân sách
        /// </summary>
        public decimal TotalAmount { get; set; }

        /// <summary>
        /// Trạng thái ngân sách (DRAFT, APPROVED, CLOSED)
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Danh sách các dòng ngân sách
        /// </summary>
        public List<BudgetLine> Lines { get; set; } = new List<BudgetLine>();

        /// <summary>
        /// Kiểm tra tính hợp lệ của ngân sách
        /// </summary>
        /// <returns>True nếu hợp lệ</returns>
        public bool IsValid()
        {
            return !string.IsNullOrEmpty(Id) &&
                   !string.IsNullOrEmpty(Name) &&
                   FiscalYear > 0 &&
                   TotalAmount > 0;
        }
    }

    /// <summary>
    /// Đại diện cho một dòng ngân sách theo tài khoản
    /// </summary>
    public class BudgetLine
    {
        /// <summary>
        /// Mã tài khoản
        /// </summary>
        public string AccountCode { get; set; }

        /// <summary>
        /// Số tiền ngân sách
        /// </summary>
        public decimal BudgetAmount { get; set; }

        /// <summary>
        /// Số tiền thực tế đã chi
        /// </summary>
        public decimal ActualAmount { get; set; }

        /// <summary>
        /// Chênh lệch (ngân sách - thực tế)
        /// </summary>
        public decimal Variance => BudgetAmount - ActualAmount;

        /// <summary>
        /// Tỷ lệ chênh lệch (%)
        /// </summary>
        public decimal VariancePercent => BudgetAmount > 0 ? (Variance / BudgetAmount) * 100 : 0;
    }

    /// <summary>
    /// Đại diện cho dự báo ngân sách
    /// </summary>
    public class BudgetForecast
    {
        /// <summary>
        /// Năm tài chính dự báo
        /// </summary>
        public int FiscalYear { get; set; }

        /// <summary>
        /// Loại dự báo (LINEAR, EXPONENTIAL, SEASONAL)
        /// </summary>
        public string ForecastType { get; set; }

        /// <summary>
        /// Số tiền cơ sở
        /// </summary>
        public decimal BaseAmount { get; set; }

        /// <summary>
        /// Tỷ lệ tăng trưởng (%)
        /// </summary>
        public decimal GrowthRatePercent { get; set; }

        /// <summary>
        /// Số tiền dự báo
        /// </summary>
        public decimal ProjectedAmount { get; set; }
    }
}
