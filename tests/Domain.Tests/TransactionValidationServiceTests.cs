using GL.Application.Services;
using GL.Domain.Entities;
using Xunit;

namespace GL.Domain.Tests
{
    public class TransactionValidationServiceTests
    {
        private readonly TransactionValidationService _service = new TransactionValidationService();

        [Fact]
        public void ValidateTransaction_ValidEntry_ReturnsValid()
        {
            var transaction = new Transaction
            {
                Id = "TX-001",
                Date = System.DateTime.Today,
                Description = "Test transaction"
            };
            transaction.AddLine("111", 100000, 0, "Debit");
            transaction.AddLine("511", 0, 100000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.True(result.IsValid, result.Summary);
        }

        [Fact]
        public void ValidateTransaction_Unbalanced_ReturnsInvalid()
        {
            var transaction = new Transaction
            {
                Id = "TX-002",
                Date = System.DateTime.Today,
                Description = "Unbalanced transaction"
            };
            transaction.AddLine("111", 100000, 0, "Debit");
            transaction.AddLine("511", 0, 99000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result.IsValid);
            Assert.Contains(result.Errors, e => e.Contains("balanced"));
        }

        [Fact]
        public void ValidateTransaction_InvalidAccount_ReturnsInvalid()
        {
            var transaction = new Transaction
            {
                Id = "TX-003",
                Date = System.DateTime.Today,
                Description = "Invalid account"
            };
            transaction.AddLine("111", 100000, 0, "Debit");
            transaction.AddLine("999", 0, 100000, "Invalid account");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result.IsValid);
            Assert.Contains(result.Errors, e => e.Contains("not found"));
        }

        [Fact]
        public void ValidateTransaction_Level1Account_ReturnsInvalid()
        {
            var transaction = new Transaction
            {
                Id = "TX-004",
                Date = System.DateTime.Today,
                Description = "Using level 1 account"
            };
            transaction.AddLine("111", 100000, 0, "Debit");
            transaction.AddLine("11", 0, 100000, "Invalid level");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result.IsValid);
        }

        [Fact]
        public void IsValidAccountCode_Valid_ReturnsTrue()
        {
            var result = _service.IsValidAccountCode("111");
            Assert.True(result);
        }

        [Fact]
        public void IsValidAccountCode_Invalid_ReturnsFalse()
        {
            var result = _service.IsValidAccountCode("999");
            Assert.False(result);
        }

        [Fact]
        public void GetAccountInfo_ReturnsAccount()
        {
            var account = _service.GetAccountInfo("111");
            
            Assert.NotNull(account);
            Assert.Equal("Tiền mặt", account.Name);
            Assert.Equal(1, account.Level);
        }
    }
}