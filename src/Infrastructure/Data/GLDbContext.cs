using GL.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace GL.Infrastructure.Data
{
    /// <summary>
    /// DbContext cho hệ thống kế toán GL
    /// SQL Server / MariaDB / PostgreSQL with EF Core
    /// </summary>
    public class GLDbContext : DbContext
    {
        public GLDbContext(DbContextOptions<GLDbContext> options) : base(options)
        {
        }

        // Core Entities
        public DbSet<Transaction> Transactions => Set<Transaction>();
        public DbSet<TransactionLine> TransactionLines => Set<TransactionLine>();
        public DbSet<AccountEntity> Accounts => Set<AccountEntity>();
        public DbSet<AccountingPeriod> AccountingPeriods => Set<AccountingPeriod>();
        
        // Transaction Entities
        public DbSet<SalesTransaction> SalesTransactions => Set<SalesTransaction>();
        public DbSet<PurchaseTransaction> PurchaseTransactions => Set<PurchaseTransaction>();

        // User & Role Entities
        public DbSet<User> Users => Set<User>();
        public DbSet<Role> Roles => Set<Role>();
        public DbSet<UserRole> UserRoles => Set<UserRole>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Transaction configuration
            modelBuilder.Entity<Transaction>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).HasMaxLength(50);
                entity.Property(e => e.Description).HasMaxLength(500);
            });

            // TransactionLine configuration
            modelBuilder.Entity<TransactionLine>(entity =>
            {
                entity.Property(e => e.AccountCode).HasMaxLength(20);
                entity.Property(e => e.Description).HasMaxLength(200);
                entity.Property(e => e.DebitAmount).HasPrecision(18, 2);
                entity.Property(e => e.CreditAmount).HasPrecision(18, 2);
            });

            // Account configuration
            modelBuilder.Entity<AccountEntity>(entity =>
            {
                entity.HasKey(e => e.Code);
                entity.Property(e => e.Code).HasMaxLength(20);
                entity.Property(e => e.Name).HasMaxLength(200);
                entity.Property(e => e.NormalBalance).HasMaxLength(10);
            });

            // AccountingPeriod configuration
            modelBuilder.Entity<AccountingPeriod>(entity =>
            {
                entity.HasKey(e => e.Code);
                entity.Property(e => e.Code).HasMaxLength(20);
                entity.Property(e => e.Status).HasMaxLength(20);
            });

            // SalesTransaction configuration
            modelBuilder.Entity<SalesTransaction>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).HasMaxLength(50);
            });

            // PurchaseTransaction configuration
            modelBuilder.Entity<PurchaseTransaction>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).HasMaxLength(50);
            });
        }

        /// <summary>
        /// Seed COA data - gọi sau khi tạo database
        /// Sử dụng cho production deployment
        /// </summary>
        public void SeedCOA()
        {
            var accounts = ChartOfAccounts.GetAllAccounts();
            foreach (var a in accounts)
            {
                if (!Accounts.Any(acc => acc.Code == a.Code))
                {
                    Accounts.Add(new AccountEntity
                    {
                        Code = a.Code,
                        Name = a.Name,
                        Level = a.Level,
                        Type = a.Type,
                        NormalBalance = a.NormalBalance ?? string.Empty,
                        ParentCode = a.ParentCode ?? string.Empty,
                        IsPostable = a.IsPostable
                    });
                }
            }
            SaveChanges();
        }

        /// <summary>
        /// Seed Accounting Periods - tạo kỳ kế toán mặc định
        /// </summary>
        public void SeedAccountingPeriods()
        {
            var currentYear = DateTime.Now.Year;
            for (int month = 1; month <= 12; month++)
            {
                var periodCode = $"{currentYear}-{month:D2}";
                if (!AccountingPeriods.Any(p => p.Code == periodCode))
                {
                    AccountingPeriods.Add(new AccountingPeriod
                    {
                        Code = periodCode,
                        StartDate = new DateTime(currentYear, month, 1),
                        EndDate = new DateTime(currentYear, month, 1).AddMonths(1).AddDays(-1),
                        Status = month == DateTime.Now.Month ? "OPEN" : "CLOSED"
                    });
                }
            }
            SaveChanges();
        }
    }

    /// <summary>
    /// Entity for database - maps from domain Account
    /// </summary>
    public class AccountEntity
    {
        public string Code { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public int Level { get; set; }
        public GL.Domain.Enums.AccountType Type { get; set; }
        public string NormalBalance { get; set; } = string.Empty;
        public string ParentCode { get; set; } = string.Empty;
        public bool IsPostable { get; set; }
    }
}
