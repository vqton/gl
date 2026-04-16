using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kế toán tổng hợp (GL Central Posting) - G05
    /// Tổng hợp tất cả bút toán từ các module vào sổ cái tổng hợp
    /// </summary>
    public class GLCentralPostingService
    {
        /// <summary>
        /// Tổng hợp bút toán cuối ngày (G05a)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch trong ngày</param>
        /// <param name="workDate">Ngày làm việc</param>
        /// <returns>Bút toán tổng hợp</returns>
        public Transaction CollectDailyTransactions(List<Transaction> transactions, string workDate)
        {
            var result = new Transaction
            {
                Id = $"GL-{workDate}",
                Date = DateTime.Parse(workDate),
                Description = $"Tổng hợp cuối ngày - {workDate}",
            };

            var aggregatedLines = new Dictionary<string, (decimal debit, decimal credit)>();

            foreach (var tx in transactions)
            {
                foreach (var line in tx.Lines)
                {
                    if (!aggregatedLines.ContainsKey(line.AccountCode))
                    {
                        aggregatedLines[line.AccountCode] = (0, 0);
                    }

                    var current = aggregatedLines[line.AccountCode];
                    aggregatedLines[line.AccountCode] = (
                        current.debit + line.DebitAmount,
                        current.credit + line.CreditAmount
                    );
                }
            }

            foreach (var kvp in aggregatedLines)
            {
                var netAmount = Math.Abs(kvp.Value.debit - kvp.Value.credit);
                if (netAmount > 0.01m)
                {
                    if (kvp.Value.debit > kvp.Value.credit)
                    {
                        result.AddLine(kvp.Key, netAmount, 0, "Tổng hợp Nợ");
                    }
                    else
                    {
                        result.AddLine(kvp.Key, 0, netAmount, "Tổng hợp Có");
                    }
                }
            }

            return result;
        }

        /// <summary>
        /// Tạo file xuất sổ cái (G05b)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch</param>
        /// <param name="period">Kỳ kế toán</param>
        /// <returns>Bút toán tổng hợp</returns>
        public Transaction GenerateGeneralLedgerFile(List<Transaction> transactions, string period)
        {
            var result = new Transaction
            {
                Id = $"GL-{period}",
                Date = DateTime.Parse($"{period}-01"),
                Description = $"Sổ cái tổng hợp - Kỳ {period}",
            };

            var aggregatedLines = new Dictionary<string, (decimal debit, decimal credit)>();

            foreach (var tx in transactions)
            {
                foreach (var line in tx.Lines)
                {
                    if (!aggregatedLines.ContainsKey(line.AccountCode))
                    {
                        aggregatedLines[line.AccountCode] = (0, 0);
                    }

                    var current = aggregatedLines[line.AccountCode];
                    aggregatedLines[line.AccountCode] = (
                        current.debit + line.DebitAmount,
                        current.credit + line.CreditAmount
                    );
                }
            }

            foreach (var kvp in aggregatedLines.OrderBy(k => k.Key))
            {
                if (kvp.Value.debit > 0)
                {
                    result.AddLine(kvp.Key, kvp.Value.debit, 0, "Tổng Nợ");
                }
                if (kvp.Value.credit > 0)
                {
                    result.AddLine(kvp.Key, 0, kvp.Value.credit, "Tổng Có");
                }
            }

            return result;
        }

        /// <summary>
        /// Kiểm tra số dư cuối ngày (G05c)
        /// </summary>
        /// <param name="accountBalances">Số dư các tài khoản</param>
        /// <param name="workDate">Ngày làm việc</param>
        /// <returns>Kết quả kiểm tra</returns>
        public DayEndCheckResult CheckDayEndBalances(Dictionary<string, decimal> accountBalances, string workDate)
        {
            var result = new DayEndCheckResult
            {
                WorkDate = workDate,
                IsValid = true,
                Messages = new List<string>()
            };

            decimal totalAssets = 0;
            decimal totalLiabilities = 0;
            decimal totalEquity = 0;

            foreach (var kvp in accountBalances)
            {
                var code = kvp.Key;
                var balance = kvp.Value;

                if (code.StartsWith("1"))
                {
                    totalAssets += balance;
                }
                else if (code.StartsWith("2") && !code.StartsWith("21"))
                {
                    totalLiabilities += balance;
                }
                else if (code == "411" || code == "4211" || code == "4212")
                {
                    totalEquity += balance;
                }
            }

            var netWorth = totalAssets - totalLiabilities;
            if (Math.Abs(netWorth - totalEquity) > 100)
            {
                result.IsValid = false;
                result.Messages.Add($"Chênh lệch: Tài sản {totalAssets:N0} - Nợ phải trả {totalLiabilities:N0} = Vốn chủ sở hữu {totalEquity:N0}");
            }

            return result;
        }

        /// <summary>
        /// Báo cáo chênh lệch (G05d)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch</param>
        /// <returns>Báo cáo chênh lệch</returns>
        public DiscrepancyReport ReportDiscrepancies(List<Transaction> transactions)
        {
            var report = new DiscrepancyReport
            {
                Discrepancies = new List<DiscrepancyItem>()
            };

            foreach (var tx in transactions)
            {
                if (!tx.IsBalanced)
                {
                    decimal totalDebit = tx.Lines.Sum(l => l.DebitAmount);
                    decimal totalCredit = tx.Lines.Sum(l => l.CreditAmount);

                    report.Discrepancies.Add(new DiscrepancyItem
                    {
                        TransactionId = tx.Id,
                        Description = tx.Description,
                        DebitTotal = totalDebit,
                        CreditTotal = totalCredit,
                        Difference = totalDebit - totalCredit,
                    });
                }
            }

            return report;
        }
    }

    /// <summary>
    /// Kết quả kiểm tra cuối ngày
    /// </summary>
    public class DayEndCheckResult
    {
        public string WorkDate { get; set; }
        public bool IsValid { get; set; }
        public List<string> Messages { get; set; }
    }

    /// <summary>
    /// Báo cáo chênh lệch
    /// </summary>
    public class DiscrepancyReport
    {
        public List<DiscrepancyItem> Discrepancies { get; set; }
    }

    /// <summary>
    /// Mục chênh lệch
    /// </summary>
    public class DiscrepancyItem
    {
        public string TransactionId { get; set; }
        public string Description { get; set; }
        public decimal DebitTotal { get; set; }
        public decimal CreditTotal { get; set; }
        public decimal Difference { get; set; }
    }
}