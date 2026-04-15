using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using Xunit;

namespace GL.Domain.Tests
{
    public class CoaValidationServiceTests
    {
        private readonly CoaValidationService _service;

        public CoaValidationServiceTests()
        {
            _service = new CoaValidationService();
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnTrue_WhenValid3DigitCode()
        {
            var result = _service.ValidateAccountCode("111");

            Assert.True(result.IsValid);
            Assert.Null(result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnTrue_WhenValid4DigitCode()
        {
            var result = _service.ValidateAccountCode("1111");

            Assert.True(result.IsValid);
            Assert.Null(result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnFalse_WhenCodeHasLetters()
        {
            var result = _service.ValidateAccountCode("11A");

            Assert.False(result.IsValid);
            Assert.Contains("numeric", result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnFalse_WhenCodeTooShort()
        {
            var result = _service.ValidateAccountCode("1");

            Assert.False(result.IsValid);
            Assert.Contains("3", result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnFalse_WhenCodeTooLong()
        {
            var result = _service.ValidateAccountCode("11111");

            Assert.False(result.IsValid);
            Assert.Contains("4", result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountCode_ShouldReturnFalse_WhenCodeStartsWithZero()
        {
            var result = _service.ValidateAccountCode("011");

            Assert.False(result.IsValid);
            Assert.Contains("zero", result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountExists_ShouldReturnTrue_WhenFoundInCoa()
        {
            var result = _service.ValidateAccountExists("111");

            Assert.True(result.IsValid);
        }

        [Fact]
        public void ValidateAccountExists_ShouldReturnFalse_WhenNotFound()
        {
            var result = _service.ValidateAccountExists("999");

            Assert.False(result.IsValid);
            Assert.Contains("not found", result.ErrorMessage);
        }

        [Fact]
        public void ValidateAccountType_ShouldReturnTrue_WhenAssetCode()
        {
            var result = _service.ValidateAccountType("111", GL.Domain.Enums.AccountType.Asset);

            Assert.True(result.IsValid);
        }

        [Fact]
        public void ValidateAccountType_ShouldReturnFalse_WhenMismatch()
        {
            var result = _service.ValidateAccountType("111", GL.Domain.Enums.AccountType.Liability);

            Assert.False(result.IsValid);
            Assert.Contains("type", result.ErrorMessage);
        }

        [Fact]
        public void ValidateParentChild_ShouldReturnTrue_WhenValidParent()
        {
            var result = _service.ValidateParentChild("111", "1111");

            Assert.True(result.IsValid);
        }

        [Fact]
        public void ValidateParentChild_ShouldReturnFalse_WhenParentNotExist()
        {
            var result = _service.ValidateParentChild("999", "1111");

            Assert.False(result.IsValid);
        }

        [Fact]
        public void ValidateParentChild_ShouldReturnFalse_WhenReversed()
        {
            var result = _service.ValidateParentChild("1111", "111");

            Assert.False(result.IsValid);
            Assert.Contains("not found", result.ErrorMessage);
        }

        [Fact]
        public void ValidateNormalBalance_ShouldReturnTrue_WhenCorrectDirection()
        {
            var result = _service.ValidateNormalBalance("111", 1000, 0);

            Assert.True(result.IsValid);
        }

        [Fact]
        public void ValidateNormalBalance_ShouldReturnTrue_WhenCreditToAsset()
        {
            var result = _service.ValidateNormalBalance("111", 0, 500);

            Assert.False(result.IsValid);
            Assert.Contains("credit", result.ErrorMessage);
        }

        [Fact]
        public void ValidateNormalBalance_ShouldReturnTrue_WhenDebitToLiability()
        {
            var result = _service.ValidateNormalBalance("331", 500, 0);

            Assert.False(result.IsValid);
            Assert.Contains("debit", result.ErrorMessage);
        }

        [Fact]
        public void ValidateFullAccount_ShouldPassAllChecks()
        {
            var request = new CoaValidationRequest
            {
                AccountCode = "111",
                AccountType = GL.Domain.Enums.AccountType.Asset,
                DebitAmount = 1000,
                CreditAmount = 0,
                ParentCode = null
            };

            var result = _service.ValidateFullAccount(request);

            Assert.True(result.IsValid);
        }

        [Fact]
        public void ValidateFullAccount_ShouldFail_WhenCodeInvalid()
        {
            var request = new CoaValidationRequest
            {
                AccountCode = "1A1",
                AccountType = GL.Domain.Enums.AccountType.Asset,
                DebitAmount = 1000,
                CreditAmount = 0,
                ParentCode = null
            };

            var result = _service.ValidateFullAccount(request);

            Assert.False(result.IsValid);
        }

        [Fact]
        public void ValidateFullAccount_ShouldFail_WhenTypeMismatch()
        {
            var request = new CoaValidationRequest
            {
                AccountCode = "331",
                AccountType = GL.Domain.Enums.AccountType.Asset,
                DebitAmount = 1000,
                CreditAmount = 0,
                ParentCode = null
            };

            var result = _service.ValidateFullAccount(request);

            Assert.False(result.IsValid);
        }
    }
}