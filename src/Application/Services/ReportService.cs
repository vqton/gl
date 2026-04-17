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
        /// Tạo báo cáo lưu chuyển tiền tệ (B03-BN)
        /// </summary>
        /// <param name="transactions">Danh sách giao dịch trong kỳ</param>
        /// <param name="periodCode">Mã kỳ báo cáo</param>
        /// <param name="method">Phương pháp: DIRECT hoặc INDIRECT</param>
        /// <returns>Báo cáo lưu chuyển tiền tệ</returns>
        public CashFlowReport GenerateCashFlowReport(
            List<Transaction> transactions,
            string periodCode,
            string method)
        {
            var report = new CashFlowReport
            {
                PeriodCode = periodCode,
                ReportDate = System.DateTime.Now,
                Method = method
            };

            var accountBalances = CalculateAccountBalances(transactions);

            report.CashReceivedFromSales = GetAccountBalanceByCode(transactions, "511");
            report.CashPaidToSuppliers = GetAccountBalanceByCode(transactions, "331") + GetAccountBalanceByCode(transactions, "621");
            report.CashPaidToEmployees = GetAccountBalanceByCode(transactions, "622");
            report.TaxPaid = GetAccountBalanceByCode(transactions, "8211");
            report.CashPaidForFixedAssets = GetAccountBalanceByCode(transactions, "211");
            report.CashReceivedFromLoans = GetAccountBalanceByCode(transactions, "341");
            report.DividendsPaid = GetAccountBalanceByCode(transactions, "421");

            decimal operatingIn = 0;
            decimal operatingOut = 0;
            decimal investingOut = 0;
            decimal financingIn = 0;

            foreach (var transaction in transactions)
            {
                foreach (var line in transaction.Lines)
                {
                    var code = line.AccountCode ?? "";
                    var dept = line.DebitAmount;
                    var cred = line.CreditAmount;

                    if (code == "111" || code == "112")
                    {
                        if (dept > 0) operatingIn += dept;
                        if (cred > 0) operatingOut += cred;
                    }
                    else if (code == "511" || code == "515" || code == "711")
                    {
                        if (dept > 0) operatingIn += dept;
                    }
                    else if (code == "632" || code == "621" || code == "622" || code == "635")
                    {
                        if (cred > 0) operatingOut += cred;
                    }
                    else if (code.StartsWith("21"))
                    {
                        if (cred > 0) investingOut += cred;
                    }
                }
            }

            report.OperatingCashFlow = operatingIn - operatingOut;
            report.InvestingCashFlow = -investingOut;
            report.FinancingCashFlow = financingIn;
            report.NetCashFlow = report.OperatingCashFlow + report.InvestingCashFlow + report.FinancingCashFlow;
            report.EndingCash = report.BeginningCash + report.NetCashFlow;

            return report;
        }

        private decimal GetAccountBalanceByCode(List<Transaction> transactions, string accountCode)
        {
            decimal balance = 0;
            var account = ChartOfAccounts.GetAllAccounts().FirstOrDefault(a => a.Code == accountCode);
            if (account == null) return 0;

            foreach (var transaction in transactions)
            {
                foreach (var line in transaction.Lines)
                {
                    if (line.AccountCode != accountCode) continue;
                    if (account.NormalBalance == "Debit")
                        balance += line.DebitAmount - line.CreditAmount;
                    else
                        balance += line.CreditAmount - line.DebitAmount;
                }
            }
            return balance;
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
