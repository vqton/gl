using GL.Domain.Entities;
using GL.Domain.Enums;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class AccountTests
    {
        [Fact]
        public void Account_ShouldBeValidForPosting_WhenHasNoChildren()
        {
            var account = new Account
            {
                Code = "111",
                Name = "Tiền mặt",
                Type = AccountType.Asset,
                NormalBalance = "Debit"
            };

            var result = account.IsValidForPosting();

            Assert.True(result);
        }

        [Fact]
        public void Account_ShouldNotBeValidForPosting_WhenHasChildren()
        {
            var account = new Account
            {
                Code = "11",
                Name = "Tài sản",
                Type = AccountType.Asset,
                NormalBalance = "Debit"
            };
            account.Children.Add(new Account { Code = "111", Name = "Tiền mặt", Type = AccountType.Asset, NormalBalance = "Debit" });

            var result = account.IsValidForPosting();

            Assert.False(result);
        }

        [Fact]
        public void Account_ShouldNotBeValidForPosting_WhenMissingRequiredFields()
        {
            var account = new Account
            {
                Code = "111",
                Name = "",
                Type = AccountType.Asset,
                NormalBalance = "Debit"
            };

            var result = account.IsValidForPosting();

            Assert.False(result);
        }
    }

    public class TransactionTests
    {
        [Fact]
        public void Transaction_AddLine_ShouldIncreaseLineCount()
        {
            var transaction = new Transaction
            {
                Id = "TXN001",
                Date = DateTime.Now,
                Description = "Test transaction"
            };

            transaction.AddLine("111", 1000m, 0m, "Test debit line");

            Assert.Single(transaction.Lines);
        }

        [Fact]
        public void Transaction_AddMultipleLines_ShouldHaveCorrectCount()
        {
            var transaction = new Transaction
            {
                Id = "TXN002",
                Date = DateTime.Now,
                Description = "Test transaction"
            };

            transaction.AddLine("111", 1000m, 0m, "Debit line");
            transaction.AddLine("331", 0m, 1000m, "Credit line");

            Assert.Equal(2, transaction.Lines.Count);
        }

        [Fact]
        public void Transaction_IsBalanced_ShouldReturnTrueForBalancedTransaction()
        {
            var transaction = new Transaction
            {
                Id = "TXN003",
                Date = DateTime.Now,
                Description = "Balanced transaction"
            };
            transaction.AddLine("111", 1000m, 0m, "Debit line");
            transaction.AddLine("331", 0m, 1000m, "Credit line");

            var result = transaction.IsBalanced;

            Assert.True(result);
        }

        [Fact]
        public void Transaction_IsBalanced_ShouldReturnFalseForUnbalancedTransaction()
        {
            var transaction = new Transaction
            {
                Id = "TXN004",
                Date = DateTime.Now,
                Description = "Unbalanced transaction"
            };
            transaction.AddLine("111", 1000m, 0m, "Debit line");
            transaction.AddLine("331", 0m, 500m, "Credit line");

            var result = transaction.IsBalanced;

            Assert.False(result);
        }

        [Fact]
        public void Transaction_AddLine_ShouldThrowException_WhenBothDebitAndCreditAreZero()
        {
            var transaction = new Transaction
            {
                Id = "TXN005",
                Date = DateTime.Now,
                Description = "Test transaction"
            };

            Assert.Throws<System.ArgumentException>(() =>
                transaction.AddLine("111", 0m, 0m, "Invalid line"));
        }

        [Fact]
        public void Transaction_AddLine_ShouldThrowException_WhenBothDebitAndCreditArePositive()
        {
            var transaction = new Transaction
            {
                Id = "TXN006",
                Date = DateTime.Now,
                Description = "Test transaction"
            };

            Assert.Throws<System.ArgumentException>(() =>
                transaction.AddLine("111", 500m, 500m, "Invalid line"));
        }
    }

    public class AccountingPeriodTests
    {
        [Fact]
        public void AccountingPeriod_IsOpen_WhenStatusIsOpen()
        {
            var period = new AccountingPeriod
            {
                Code = "2026-01",
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 1, 31),
                Status = "OPEN"
            };

            var result = period.IsOpen();

            Assert.True(result);
        }

        [Fact]
        public void AccountingPeriod_IsOpen_WhenStatusIsClosed()
        {
            var period = new AccountingPeriod
            {
                Code = "2026-01",
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 1, 31),
                Status = "CLOSED"
            };

            var result = period.IsOpen();

            Assert.False(result);
        }

        [Fact]
        public void AccountingPeriod_IsValid_WhenAllFieldsProvided()
        {
            var period = new AccountingPeriod
            {
                Code = "2026-01",
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 1, 31),
                Status = "OPEN"
            };

            var result = period.IsValid();

            Assert.True(result);
        }

        [Fact]
        public void AccountingPeriod_IsValid_WhenMissingCode()
        {
            var period = new AccountingPeriod
            {
                Code = "",
                StartDate = new DateTime(2026, 1, 1),
                EndDate = new DateTime(2026, 1, 31),
                Status = "OPEN"
            };

            var result = period.IsValid();

            Assert.False(result);
        }

        [Fact]
        public void AccountingPeriod_IsValid_WhenEndDateBeforeStartDate()
        {
            var period = new AccountingPeriod
            {
                Code = "2026-01",
                StartDate = new DateTime(2026, 1, 31),
                EndDate = new DateTime(2026, 1, 1),
                Status = "OPEN"
            };

            var result = period.IsValid();

            Assert.False(result);
        }
    }

    public class ChartOfAccountsTests
    {
        [Fact]
        public void GetAllAccounts_ShouldReturnTT99Accounts()
        {
            var accounts = GL.Domain.Entities.ChartOfAccounts.GetAllAccounts();

            Assert.NotNull(accounts);
            Assert.True(accounts.Count > 0);
        }

        [Fact]
        public void GetAllAccounts_ShouldIncludeMainAccounts()
        {
            var accounts = GL.Domain.Entities.ChartOfAccounts.GetAllAccounts();

            var has111 = accounts.Exists(a => a.Code == "111");
            var has112 = accounts.Exists(a => a.Code == "112");
            var has511 = accounts.Exists(a => a.Code == "511");
            var has642 = accounts.Exists(a => a.Code == "642");

            Assert.True(has111, "Should have account 111");
            Assert.True(has112, "Should have account 112");
            Assert.True(has511, "Should have account 511");
            Assert.True(has642, "Should have account 642");
        }

        [Fact]
        public void GetAllAccounts_ShouldHaveAtLeast50Accounts()
        {
            var accounts = GL.Domain.Entities.ChartOfAccounts.GetAllAccounts();

            Assert.True(accounts.Count >= 50, $"Expected at least 50 accounts, got {accounts.Count}");
        }
    }
}