using GL.Domain.Entities;
using GL.Domain.Enums;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tạo báo cáo tài chính (Phase 3)
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class ReportService
    {
        /// <summary>
        /// Tạo báo cáo Bảng cân đối kế toán (BCĐKT)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch trong kỳ</param>
        /// <param name="periodCode">Mã kỳ báo cáo</param>
        /// <param name="reportDate">Ngày lập báo cáo</param>
        /// <returns>Báo cáo BCĐKT</returns>
        public BalanceSheetReport GenerateBalanceSheetReport(
            List<Transaction> transactions,
            string periodCode,
            System.DateTime reportDate)
        {
            var report = new BalanceSheetReport
            {
                PeriodCode = periodCode,
                ReportDate = reportDate
            };

            var accountBalances = CalculateAccountBalances(transactions);

            foreach (var account in ChartOfAccounts.GetAllAccounts())
            {
                if (!accountBalances.ContainsKey(account.Code))
                    continue;

                var balance = accountBalances[account.Code];
                if (balance == 0)
                    continue;

                switch (account.Type)
                {
                    case AccountType.Asset:
                        if (balance > 0)
                            report.AddAsset(account.Code, account.Name, balance);
                        break;
                    case AccountType.Liability:
                        if (balance > 0)
                            report.AddLiability(account.Code, account.Name, balance);
                        break;
                    case AccountType.Equity:
                        if (balance > 0)
                            report.AddEquity(account.Code, account.Name, balance);
                        break;
                }
            }

            return report;
        }

        /// <summary>
        /// Tạo báo cáo Kết quả hoạt động kinh doanh (BCKQHĐKD)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch trong kỳ</param>
        /// <param name="periodCode">Mã kỳ báo cáo</param>
        /// <param name="reportDate">Ngày lập báo cáo</param>
        /// <returns>Báo cáo BCKQHĐKD</returns>
        public IncomeStatementReport GenerateIncomeStatementReport(
            List<Transaction> transactions,
            string periodCode,
            System.DateTime reportDate)
        {
            var report = new IncomeStatementReport
            {
                PeriodCode = periodCode,
                ReportDate = reportDate
            };

            var accountBalances = CalculateAccountBalances(transactions);

            foreach (var account in ChartOfAccounts.GetAllAccounts())
            {
                if (!accountBalances.ContainsKey(account.Code))
                    continue;

                var balance = accountBalances[account.Code];
                if (balance == 0)
                    continue;

                switch (account.Type)
                {
                    case AccountType.Revenue:
                        if (balance > 0)
                            report.AddRevenue(account.Code, account.Name, balance);
                        break;
                    case AccountType.Expense:
                        if (balance > 0)
                            report.AddExpense(account.Code, account.Name, balance);
                        break;
                }
            }

            return report;
        }

        /// <summary>
        /// Tính số dư các tài khoản từ danh sách giao dịch
        /// </summary>
        private Dictionary<string, decimal> CalculateAccountBalances(List<Transaction> transactions)
        {
            var balances = new Dictionary<string, decimal>();

            foreach (var transaction in transactions)
            {
                foreach (var line in transaction.Lines)
                {
                    if (!balances.ContainsKey(line.AccountCode))
                        balances[line.AccountCode] = 0;

                    var account = ChartOfAccounts.GetAllAccounts()
                        .FirstOrDefault(a => a.Code == line.AccountCode);

                    if (account == null)
                        continue;

                    if (account.NormalBalance == "Debit")
                    {
                        balances[line.AccountCode] += line.DebitAmount - line.CreditAmount;
                    }
                    else
                    {
                        balances[line.AccountCode] += line.CreditAmount - line.DebitAmount;
                    }
                }
            }

            return balances;
        }

        /// <summary>
        /// Lấy số dư cuối kỳ của một tài khoản
        /// </summary>
        public decimal GetAccountBalance(List<Transaction> transactions, string accountCode)
        {
            decimal balance = 0;

            var account = ChartOfAccounts.GetAllAccounts()
                .FirstOrDefault(a => a.Code == accountCode);

            if (account == null)
                return 0;

            foreach (var transaction in transactions)
            {
                var line = transaction.Lines.FirstOrDefault(l => l.AccountCode == accountCode);
                if (line == null)
                    continue;

                if (account.NormalBalance == "Debit")
                {
                    balance += line.DebitAmount - line.CreditAmount;
                }
                else
                {
                    balance += line.CreditAmount - line.DebitAmount;
                }
            }

            return balance;
        }
    }
}
