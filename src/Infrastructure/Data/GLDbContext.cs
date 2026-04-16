using GL.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace GL.Infrastructure.Data
{
    /// <summary>
    /// DbContext cho hệ thống kế toán GL
    /// MariaDB + Entity Framework Core
    /// </summary>
    public class GLDbContext : DbContext
    {
        public GLDbContext(DbContextOptions<GLDbContext> options) : base(options)
        {
        }

        public DbSet<Transaction> Transactions => Set<Transaction>();
        public DbSet<TransactionLine> TransactionLines => Set<TransactionLine>();
        public DbSet<AccountEntity> Accounts => Set<AccountEntity>();
        public DbSet<AccountingPeriod> AccountingPeriods => Set<AccountingPeriod>();

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

            // TransactionLine configuration - embedded in Transaction
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

            // Seed COA data
            SeedCOA(modelBuilder);
        }

        private void SeedCOA(ModelBuilder modelBuilder)
        {
            var accounts = ChartOfAccounts.GetAllAccounts();
            
            modelBuilder.Entity<AccountEntity>().HasData(
                accounts.Select(a => new AccountEntity
                {
                    Code = a.Code,
                    Name = a.Name,
                    Level = a.Level,
                    Type = a.Type,
                    NormalBalance = a.NormalBalance ?? string.Empty,
                    ParentCode = a.ParentCode ?? string.Empty,
                    IsPostable = a.IsPostable
                }).ToArray()
            );
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
        public Domain.Enums.AccountType Type { get; set; }
        public string NormalBalance { get; set; } = string.Empty;
        public string ParentCode { get; set; } = string.Empty;
        public bool IsPostable { get; set; }
    }
}