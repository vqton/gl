using System;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho một kỳ kế toán trong hệ thống
    /// </summary>
    public class AccountingPeriod
    {
        /// <summary>
        /// Mã kỳ kế toán (định dạng: 2026-01)
        /// </summary>
        public string Code { get; set; }

        /// <summary>
        /// Ngày bắt đầu kỳ
        /// </summary>
        public DateTime StartDate { get; set; }

        /// <summary>
        /// Ngày kết thúc kỳ
        /// </summary>
        public DateTime EndDate { get; set; }

        /// <summary>
        /// Trạng thái kỳ kế toán (OPEN, CLOSED, LOCKED)
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Xác định xem đây có phải là cuối năm tài chính không
        /// </summary>
        public bool IsFiscalYearEnd { get; set; }

        /// <summary>
        /// Kiểm tra xem kỳ kế toán có đang mở không
        /// </summary>
        /// <returns>True nếu kỳ đang mở</returns>
        public bool IsOpen()
        {
            return Status?.ToUpper() == "OPEN";
        }

        /// <summary>
        /// Kiểm tra tính hợp lệ của kỳ kế toán
        /// </summary>
        /// <returns>True nếu kỳ hợp lệ</returns>
        public bool IsValid()
        {
            return !string.IsNullOrEmpty(Code) &&
                   StartDate != default &&
                   EndDate != default &&
                   StartDate <= EndDate &&
                   !string.IsNullOrEmpty(Status);
        }
    }
}