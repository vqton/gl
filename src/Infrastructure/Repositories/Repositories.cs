using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GL.Infrastructure.Repositories
{
    /// <summary>
    /// Repository for Transaction operations
    /// </summary>
    public interface ITransactionRepository
    {
        Task<Transaction> CreateAsync(Transaction transaction);
        Task<Transaction> GetByIdAsync(string id);
        Task<List<Transaction>> GetByDateRangeAsync(DateTime startDate, DateTime endDate);
        Task<List<Transaction>> GetByPeriodAsync(string periodId);
        Task UpdateAsync(Transaction transaction);
        Task DeleteAsync(string id);
    }

    /// <summary>
    /// Repository for Account operations
    /// </summary>
    public interface IAccountRepository
    {
        Task<List<Account>> GetAllAsync();
        Task<Account> GetByCodeAsync(string code);
        Task<bool> ExistsAsync(string code);
        Task<bool> IsPostableAsync(string code);
    }

    /// <summary>
    /// Repository for Accounting Period operations
    /// </summary>
    public interface IAccountingPeriodRepository
    {
        Task<AccountingPeriod> GetCurrentPeriodAsync();
        Task<AccountingPeriod> GetByCodeAsync(string code);
        Task<List<AccountingPeriod>> GetAllAsync();
        Task CreateAsync(AccountingPeriod period);
        Task UpdateStatusAsync(string code, string status);
        Task<bool> IsPeriodOpenAsync(string code);
    }

    /// <summary>
    /// Implementation of Transaction Repository
    /// </summary>
    public class TransactionRepository : ITransactionRepository
    {
        private readonly Data.GLDbContext _context;

        public TransactionRepository(Data.GLDbContext context)
        {
            _context = context;
        }

        public async Task<Transaction> CreateAsync(Transaction transaction)
        {
            _context.Transactions.Add(transaction);
            await _context.SaveChangesAsync();
            return transaction;
        }

        public async Task<Transaction> GetByIdAsync(string id)
        {
            return await Task.FromResult(
                _context.Transactions.FirstOrDefault(t => t.Id == id)
            );
        }

        public async Task<List<Transaction>> GetByDateRangeAsync(DateTime startDate, DateTime endDate)
        {
            return await Task.FromResult(
                _context.Transactions
                    .Where(t => t.Date >= startDate && t.Date <= endDate)
                    .ToList()
            );
        }

        public async Task<List<Transaction>> GetByPeriodAsync(string periodId)
        {
            return await Task.FromResult(
                _context.Transactions
                    .Where(t => t.Description.Contains(periodId))
                    .ToList()
            );
        }

        public async Task UpdateAsync(Transaction transaction)
        {
            _context.Transactions.Update(transaction);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(string id)
        {
            var transaction = await GetByIdAsync(id);
            if (transaction != null)
            {
                _context.Transactions.Remove(transaction);
                await _context.SaveChangesAsync();
            }
        }
    }

    /// <summary>
    /// Implementation of Account Repository
    /// </summary>
    public class AccountRepository : IAccountRepository
    {
        private readonly Data.GLDbContext _context;

        public AccountRepository(Data.GLDbContext context)
        {
            _context = context;
        }

        public async Task<List<Account>> GetAllAsync()
        {
            return await Task.FromResult(ChartOfAccounts.GetAllAccounts());
        }

        public async Task<Account> GetByCodeAsync(string code)
        {
            var accounts = ChartOfAccounts.GetAllAccounts();
            return await Task.FromResult(accounts.FirstOrDefault(a => a.Code == code));
        }

        public async Task<bool> ExistsAsync(string code)
        {
            var accounts = ChartOfAccounts.GetAllAccounts();
            return await Task.FromResult(accounts.Any(a => a.Code == code));
        }

        public async Task<bool> IsPostableAsync(string code)
        {
            return await Task.FromResult(ChartOfAccounts.IsPostable(code));
        }
    }

    /// <summary>
    /// Implementation of Accounting Period Repository
    /// </summary>
    public class AccountingPeriodRepository : IAccountingPeriodRepository
    {
        private readonly Data.GLDbContext _context;

        public AccountingPeriodRepository(Data.GLDbContext context)
        {
            _context = context;
        }

        public async Task<AccountingPeriod> GetCurrentPeriodAsync()
        {
            var currentMonth = DateTime.Now.ToString("yyyy-MM");
            return await GetByCodeAsync(currentMonth);
        }

        public async Task<AccountingPeriod> GetByCodeAsync(string code)
        {
            return await Task.FromResult(
                _context.AccountingPeriods.FirstOrDefault(p => p.Code == code)
            );
        }

        public async Task<List<AccountingPeriod>> GetAllAsync()
        {
            return await Task.FromResult(
                _context.AccountingPeriods.ToList()
            );
        }

        public async Task CreateAsync(AccountingPeriod period)
        {
            _context.AccountingPeriods.Add(period);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateStatusAsync(string code, string status)
        {
            var period = await GetByCodeAsync(code);
            if (period != null)
            {
                period.Status = status;
                _context.AccountingPeriods.Update(period);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> IsPeriodOpenAsync(string code)
        {
            var period = await GetByCodeAsync(code);
            return period?.Status?.ToUpper() == "OPEN";
        }
    }
}