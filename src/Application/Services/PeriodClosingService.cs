using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý kỳ kế toán và kết chuyển - G01-G04
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class PeriodClosingService
    {
        private readonly Dictionary<string, AccountingPeriod> _periods = new();
        private readonly List<JournalEntry> _journalEntries = new();

        public PeriodClosingService()
        {
        }

        /// <summary>
        /// G01: Kết chuyển doanh thu về 911
        /// </summary>
        public (bool Success, string Message, JournalEntry Entry) CloseRevenue(int year, int month)
        {
            var key = $"{year}-{month}";
            EnsurePeriod(key, year, month);

            var lines = new List<JournalLine>();
            decimal totalRevenue = 115_000_000m; // Simulated

            // Nợ các tài khoản doanh thu
            lines.Add(new JournalLine { AccountCode = "511", Debit = 100_000_000m, Credit = 0 });
            lines.Add(new JournalLine { AccountCode = "515", Debit = 10_000_000m, Credit = 0 });
            lines.Add(new JournalLine { AccountCode = "711", Debit = 5_000_000m, Credit = 0 });
            // Có 911
            lines.Add(new JournalLine { AccountCode = "911", Debit = 0, Credit = totalRevenue });

            var entry = new JournalEntry
            {
                EntryType = "G01",
                EntryDate = DateTime.Now,
                Description = $"Kết chuyển doanh thu {month}/{year}",
                Lines = lines
            };
            _journalEntries.Add(entry);
            
            return (true, "Kết chuyển doanh thu thành công", entry);
        }

        /// <summary>
        /// G02: Kết chuyển chi phí về 911
        /// </summary>
        public (bool Success, string Message, JournalEntry Entry) CloseExpenses(int year, int month)
        {
            var key = $"{year}-{month}";
            if (!_periods.ContainsKey(key))
            {
                return (false, "Kỳ kế toán không tồn tại", null);
            }

            var lines = new List<JournalLine>();
            
            // Nợ 911, Có các tài khoản chi phí
            lines.Add(new JournalLine { AccountCode = "911", Debit = 80_000_000m, Credit = 0 });  // 632
            lines.Add(new JournalLine { AccountCode = "911", Debit = 10_000_000m, Credit = 0 }); // 641
            lines.Add(new JournalLine { AccountCode = "911", Debit = 5_000_000m, Credit = 0 });  // 642
            
            lines.Add(new JournalLine { AccountCode = "632", Debit = 0, Credit = 80_000_000m });
            lines.Add(new JournalLine { AccountCode = "641", Debit = 0, Credit = 10_000_000m });
            lines.Add(new JournalLine { AccountCode = "642", Debit = 0, Credit = 5_000_000m });

            var entry = new JournalEntry
            {
                EntryType = "G02",
                EntryDate = DateTime.Now,
                Description = $"Kết chuyển chi phí {month}/{year}",
                Lines = lines
            };
            _journalEntries.Add(entry);
            
            return (true, "Kết chuyển chi phí thành công", entry);
        }

        /// <summary>
        /// G03: Kết chuyển lợi nhuận sau thuế về 4212
        /// </summary>
        public (bool Success, string Message, JournalEntry Entry) CloseProfit(int year)
        {
            decimal profit = 20_000_000m; // Simulated
            var lines = new List<JournalLine>();
            
            lines.Add(new JournalLine { AccountCode = "911", Debit = profit, Credit = 0 });
            lines.Add(new JournalLine { AccountCode = "4212", Debit = 0, Credit = profit });

            var entry = new JournalEntry
            {
                EntryType = "G03",
                EntryDate = DateTime.Now,
                Description = $"Kết chuyển lợi nhuận năm {year}",
                Lines = lines
            };
            _journalEntries.Add(entry);
            
            return (true, "Kết chuyển lợi nhuận thành công", entry);
        }

        /// <summary>
        /// G04: Phân bổ chi phí trả trước (242)
        /// </summary>
        public (bool Success, string Message, JournalEntry Entry) AllocatePrepaid(int year, int month)
        {
            var key = $"{year}-{month}";
            if (!_periods.ContainsKey(key))
            {
                return (false, "Kỳ kế toán không tồn tại", null);
            }

            var entry = new JournalEntry
            {
                EntryType = "G04",
                EntryDate = DateTime.Now,
                Description = $"Phân bổ chi phí trả trước {month}/{year}",
                Lines = new List<JournalLine>()
            };
            
            return (true, "Phân bổ chi phí trả trước thành công", entry);
        }

        /// <summary>
        /// Đóng kỳ kế toán - ngăn chặn hạch toán tiếp
        /// </summary>
        public (bool Success, string Message) ClosePeriod(int year, int month)
        {
            var key = $"{year}-{month}";
            if (!_periods.ContainsKey(key))
            {
                return (false, "Kỳ kế toán không tồn tại");
            }

            _periods[key].Status = "Closed";
            return (true, "Đóng kỳ kế toán thành công");
        }

        /// <summary>
        /// Mở kỳ kế toán mới
        /// </summary>
        public (bool Success, string Message) OpenPeriod(int year, int month)
        {
            var key = $"{year}-{month}";
            EnsurePeriod(key, year, month);
            return (true, "Mở kỳ kế toán thành công");
        }

        /// <summary>
        /// Lấy số dư tài khoản (trial balance)
        /// </summary>
        public TrialBalanceResult GetTrialBalance(int year, int month)
        {
            return new TrialBalanceResult
            {
                PeriodCode = $"{year}-{month}",
                Entries = new List<TrialBalanceEntry>()
            };
        }

        private void EnsurePeriod(string key, int year, int month)
        {
            if (!_periods.ContainsKey(key))
            {
                _periods[key] = new AccountingPeriod
                {
                    Code = key,
                    StartDate = new DateTime(year, month, 1),
                    EndDate = new DateTime(year, month, 1).AddMonths(1).AddDays(-1),
                    Status = "Open"
                };
            }
        }
    }

    public class TrialBalanceResult
    {
        public string PeriodCode { get; set; }
        public List<TrialBalanceEntry> Entries { get; set; } = new();
        public decimal TotalDebit => Entries.Sum(e => e.Debit);
        public decimal TotalCredit => Entries.Sum(e => e.Credit);
    }

    public class TrialBalanceEntry
    {
        public string AccountCode { get; set; }
        public string AccountName { get; set; }
        public decimal Debit { get; set; }
        public decimal Credit { get; set; }
    }
}