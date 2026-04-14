using System;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho một loại tiền tệ trong hệ thống
    /// </summary>
    public class Currency
    {
        /// <summary>
        /// Mã tiền tệ (ISO 4217, ví dụ: USD, EUR, VND)
        /// </summary>
        public string Code { get; set; }

        /// <summary>
        /// Tên tiền tệ
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Ký hiệu tiền tệ
        /// </summary>
        public string Symbol { get; set; }

        /// <summary>
        /// Tỷ giá so với tiền tệ cơ sở
        /// </summary>
        public decimal ExchangeRate { get; set; }

        /// <summary>
        /// Có phải là tiền tệ cơ sở không
        /// </summary>
        public bool IsBaseCurrency { get; set; }

        /// <summary>
        /// Ngày hiệu lực của tỷ giá
        /// </summary>
        public DateTime EffectiveDate { get; set; }

        /// <summary>
        /// Kiểm tra tính hợp lệ của tiền tệ
        /// </summary>
        /// <returns>True nếu hợp lệ</returns>
        public bool IsValid()
        {
            return !string.IsNullOrEmpty(Code) &&
                   !string.IsNullOrEmpty(Name) &&
                   ExchangeRate > 0;
        }
    }

    /// <summary>
    /// Đại diện cho một giao dịch quy đổi tiền tệ
    /// </summary>
    public class CurrencyConversion
    {
        /// <summary>
        /// Mã tiền tệ nguồn
        /// </summary>
        public string FromCurrencyCode { get; set; }

        /// <summary>
        /// Mã tiền tệ đích
        /// </summary>
        public string ToCurrencyCode { get; set; }

        /// <summary>
        /// Tỷ giá quy đổi
        /// </summary>
        public decimal ExchangeRate { get; set; }

        /// <summary>
        /// Số tiền gốc
        /// </summary>
        public decimal Amount { get; set; }

        /// <summary>
        /// Số tiền sau quy đổi
        /// </summary>
        public decimal ConvertedAmount { get; set; }

        /// <summary>
        /// Ngày quy đổi
        /// </summary>
        public DateTime ConversionDate { get; set; }
    }

    /// <summary>
    /// Đại diện cho giao dịch đa tiền tệ
    /// </summary>
    public class MultiCurrencyTransaction : Transaction
    {
        /// <summary>
        /// Mã tiền tệ (khác VND)
        /// </summary>
        public string CurrencyCode { get; set; }

        /// <summary>
        /// Tỷ giá tại thời điểm giao dịch
        /// </summary>
        public decimal ExchangeRate { get; set; }

        /// <summary>
        /// Số tiền gốc (ngoại tệ)
        /// </summary>
        public decimal OriginalAmount { get; set; }

        /// <summary>
        /// Số tiền quy đổi ra VND
        /// </summary>
        public decimal ConvertedAmount { get; set; }
    }
}
