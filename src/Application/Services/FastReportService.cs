using GL.Domain.Entities;
using GL.Domain.Enums;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service tạo báo cáo tài chính cho FastReport (data layer)
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class FastReportService
    {
        /// <summary>
        /// Lấy dữ liệu Bảng cân đối tài khoản (B01-BN)
        /// </summary>
        public List<TrialBalanceReportData> GetTrialBalanceData(
            List<Transaction> transactions,
            string periodCode,
            DateTime fromDate,
            DateTime toDate)
        {
            var data = new List<TrialBalanceReportData>();
            var balances = CalculateAccountBalances(transactions);

            foreach (var account in ChartOfAccounts.GetAllAccounts())
            {
                var opening = GetOpeningBalance(transactions, account.Code, fromDate);
                var periodTx = transactions.Where(t => t.Date >= fromDate && t.Date <= toDate).ToList();
                var debit = GetDebitTurnover(periodTx, account.Code);
                var credit = GetCreditTurnover(periodTx, account.Code);
                var closing = balances.ContainsKey(account.Code) ? balances[account.Code] : 0;

                if (opening != 0 || debit != 0 || credit != 0 || closing != 0)
                {
                    data.Add(new TrialBalanceReportData
                    {
                        PeriodCode = periodCode,
                        AccountCode = account.Code,
                        AccountName = account.Name,
                        NormalBalance = account.NormalBalance,
                        OpeningBalance = opening,
                        DebitTurnover = debit,
                        CreditTurnover = credit,
                        ClosingBalance = closing
                    });
                }
            }

            return data;
        }

        /// <summary>
        /// Lấy dữ liệu Bảng cân đối kế toán
        /// </summary>
        public List<BalanceSheetReportData> GetBalanceSheetData(
            List<Transaction> transactions,
            string periodCode,
            DateTime reportDate)
        {
            var data = new List<BalanceSheetReportData>();
            var balances = CalculateAccountBalances(transactions);

            foreach (var account in ChartOfAccounts.GetAllAccounts())
            {
                if (!balances.ContainsKey(account.Code) || balances[account.Code] == 0)
                    continue;

                var section = account.Type switch
                {
                    AccountType.Asset => "TÀI SẢN",
                    AccountType.Liability => "NỢ PHẢI TRẢ",
                    AccountType.Equity => "VỐN CHỦ SỞ HỮU",
                    _ => "KHÁC"
                };

                data.Add(new BalanceSheetReportData
                {
                    PeriodCode = periodCode,
                    ReportDate = reportDate,
                    Section = section,
                    AccountCode = account.Code,
                    AccountName = account.Name,
                    Amount = balances[account.Code]
                });
            }

            return data;
        }

        /// <summary>
        /// Lấy dữ liệu Báo cáo kết quả hoạt động kinh doanh
        /// </summary>
        public List<IncomeStatementReportData> GetIncomeStatementData(
            List<Transaction> transactions,
            string periodCode,
            DateTime reportDate)
        {
            var data = new List<IncomeStatementReportData>();
            var balances = CalculateAccountBalances(transactions);

            foreach (var account in ChartOfAccounts.GetAllAccounts())
            {
                if (!balances.ContainsKey(account.Code) || balances[account.Code] == 0)
                    continue;

                var section = account.Type switch
                {
                    AccountType.Revenue => "DOANH THU",
                    AccountType.Expense => "CHI PHÍ",
                    _ => "KHÁC"
                };

                if (section == "KHÁC") continue;

                data.Add(new IncomeStatementReportData
                {
                    PeriodCode = periodCode,
                    ReportDate = reportDate,
                    Section = section,
                    AccountCode = account.Code,
                    AccountName = account.Name,
                    Amount = balances[account.Code]
                });
            }

            return data;
        }

        /// <summary>
        /// Lấy dữ liệu Báo cáo lưu chuyển tiền tệ (B03-BN)
        /// </summary>
        public CashFlowReportData GetCashFlowData(
            List<Transaction> transactions,
            string periodCode,
            string method)
        {
            var cashAccounts = new[] { "111", "112" };
            var revenueAccounts = new[] { "511", "515", "711" };
            var expenseAccounts = new[] { "621", "622", "623", "627", "632" };
            var faAccounts = new[] { "211", "213" };
            var financingAccounts = new[] { "341", "411" };

            decimal operatingIn = 0, operatingOut = 0;
            decimal investingOut = 0, financingIn = 0;

            foreach (var tx in transactions)
            {
                foreach (var line in tx.Lines)
                {
                    var code = line.AccountCode ?? "";
                    if (cashAccounts.Contains(code))
                    {
                        if (line.DebitAmount > 0) operatingIn += line.DebitAmount;
                        if (line.CreditAmount > 0) operatingOut += line.CreditAmount;
                    }
                    else if (revenueAccounts.Contains(code))
                    {
                        if (line.CreditAmount > 0) operatingIn += line.CreditAmount;
                    }
                    else if (expenseAccounts.Any(e => code.StartsWith(e)))
                    {
                        if (line.DebitAmount > 0) operatingOut += line.DebitAmount;
                    }
                    else if (faAccounts.Contains(code))
                    {
                        if (line.CreditAmount > 0) investingOut += line.CreditAmount;
                    }
                    else if (financingAccounts.Contains(code))
                    {
                        if (line.DebitAmount > 0) financingIn += line.DebitAmount;
                    }
                }
            }

            return new CashFlowReportData
            {
                PeriodCode = periodCode,
                Method = method,
                OperatingCashFlow = operatingIn - operatingOut,
                InvestingCashFlow = -investingOut,
                FinancingCashFlow = financingIn,
                NetCashFlow = (operatingIn - operatingOut) - investingOut + financingIn
            };
        }

        /// <summary>
        /// Lấy dữ liệu Sổ cái (General Ledger)
        /// </summary>
        public List<GeneralLedgerReportData> GetGeneralLedgerData(
            List<Transaction> transactions,
            string accountCode,
            DateTime fromDate,
            DateTime toDate)
        {
            var data = new List<GeneralLedgerReportData>();
            var account = ChartOfAccounts.GetAllAccounts().FirstOrDefault(a => a.Code == accountCode);
            if (account == null) return data;

            decimal balance = 0;
            var filtered = transactions
                .Where(t => t.Date >= fromDate && t.Date <= toDate)
                .OrderBy(t => t.Date)
                .ToList();

            foreach (var tx in filtered)
            {
                var line = tx.Lines.FirstOrDefault(l => l.AccountCode == accountCode);
                if (line == null) continue;

                balance += account.NormalBalance == "Debit"
                    ? line.DebitAmount - line.CreditAmount
                    : line.CreditAmount - line.DebitAmount;

                data.Add(new GeneralLedgerReportData
                {
                    AccountCode = accountCode,
                    AccountName = account.Name,
                    TransactionDate = tx.Date,
                    TransactionId = tx.Id,
                    Description = tx.Description,
                    DebitAmount = line.DebitAmount,
                    CreditAmount = line.CreditAmount,
                    Balance = balance
                });
            }

            return data;
        }

        /// <summary>
        /// Lấy dữ liệu Sổ chi tiết (Sub-Ledger 131/331/156)
        /// </summary>
        public List<SubLedgerReportData> GetSubLedgerData(
            List<Transaction> transactions,
            string accountCode,
            string partnerCode,
            DateTime fromDate,
            DateTime toDate)
        {
            var data = new List<SubLedgerReportData>();
            decimal balance = 0;

            var filtered = transactions
                .Where(t => t.Date >= fromDate && t.Date <= toDate)
                .OrderBy(t => t.Date)
                .ToList();

            foreach (var tx in filtered)
            {
                var line = tx.Lines.FirstOrDefault(l => l.AccountCode == accountCode);
                if (line == null) continue;

                var account = ChartOfAccounts.GetAllAccounts().FirstOrDefault(a => a.Code == accountCode);
                if (account != null)
                {
                    balance += account.NormalBalance == "Debit"
                        ? line.DebitAmount - line.CreditAmount
                        : line.CreditAmount - line.DebitAmount;
                }
                else
                {
                    balance += line.DebitAmount - line.CreditAmount;
                }

                data.Add(new SubLedgerReportData
                {
                    AccountCode = accountCode,
                    PartnerCode = partnerCode,
                    TransactionDate = tx.Date,
                    TransactionId = tx.Id,
                    Description = tx.Description,
                    DebitAmount = line.DebitAmount,
                    CreditAmount = line.CreditAmount,
                    Balance = balance
                });
            }

            return data;
        }

        private Dictionary<string, decimal> CalculateAccountBalances(List<Transaction> transactions)
        {
            var balances = new Dictionary<string, decimal>();

            foreach (var tx in transactions)
            {
                foreach (var line in tx.Lines)
                {
                    var code = line.AccountCode;
                    if (string.IsNullOrEmpty(code)) continue;

                    if (!balances.ContainsKey(code))
                        balances[code] = 0;

                    var account = ChartOfAccounts.GetAllAccounts().FirstOrDefault(a => a.Code == code);
                    if (account == null) continue;

                    if (account.NormalBalance == "Debit")
                        balances[code] += line.DebitAmount - line.CreditAmount;
                    else
                        balances[code] += line.CreditAmount - line.DebitAmount;
                }
            }

            return balances;
        }

        private decimal GetOpeningBalance(List<Transaction> transactions, string accountCode, DateTime beforeDate)
        {
            var before = transactions.Where(t => t.Date < beforeDate).ToList();
            return CalculateAccountBalances(before).ContainsKey(accountCode)
                ? CalculateAccountBalances(before)[accountCode]
                : 0;
        }

        private decimal GetDebitTurnover(List<Transaction> transactions, string accountCode)
        {
            return transactions
                .SelectMany(t => t.Lines)
                .Where(l => l.AccountCode == accountCode)
                .Sum(l => l.DebitAmount);
        }

        private decimal GetCreditTurnover(List<Transaction> transactions, string accountCode)
        {
            return transactions
                .SelectMany(t => t.Lines)
                .Where(l => l.AccountCode == accountCode)
                .Sum(l => l.CreditAmount);
        }
    }

    public class TrialBalanceReportData
    {
        public string PeriodCode { get; set; }
        public string AccountCode { get; set; }
        public string AccountName { get; set; }
        public string NormalBalance { get; set; }
        public decimal OpeningBalance { get; set; }
        public decimal DebitTurnover { get; set; }
        public decimal CreditTurnover { get; set; }
        public decimal ClosingBalance { get; set; }
    }

    public class BalanceSheetReportData
    {
        public string PeriodCode { get; set; }
        public DateTime ReportDate { get; set; }
        public string Section { get; set; }
        public string AccountCode { get; set; }
        public string AccountName { get; set; }
        public decimal Amount { get; set; }
    }

    public class IncomeStatementReportData
    {
        public string PeriodCode { get; set; }
        public DateTime ReportDate { get; set; }
        public string Section { get; set; }
        public string AccountCode { get; set; }
        public string AccountName { get; set; }
        public decimal Amount { get; set; }
    }

    public class CashFlowReportData
    {
        public string PeriodCode { get; set; }
        public string Method { get; set; }
        public decimal OperatingCashFlow { get; set; }
        public decimal InvestingCashFlow { get; set; }
        public decimal FinancingCashFlow { get; set; }
        public decimal NetCashFlow { get; set; }
    }

    public class GeneralLedgerReportData
    {
        public string AccountCode { get; set; }
        public string AccountName { get; set; }
        public DateTime TransactionDate { get; set; }
        public string TransactionId { get; set; }
        public string Description { get; set; }
        public decimal DebitAmount { get; set; }
        public decimal CreditAmount { get; set; }
        public decimal Balance { get; set; }
    }

    public class SubLedgerReportData
    {
        public string AccountCode { get; set; }
        public string PartnerCode { get; set; }
        public DateTime TransactionDate { get; set; }
        public string TransactionId { get; set; }
        public string Description { get; set; }
        public decimal DebitAmount { get; set; }
        public decimal CreditAmount { get; set; }
        public decimal Balance { get; set; }
    }
}