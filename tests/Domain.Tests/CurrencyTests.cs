using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Test cases for multi-currency functionality
    /// </summary>
    public class CurrencyTests
    {
        [Fact]
        public void Currency_Create_ShouldSetProperties()
        {
            var currency = new Currency
            {
                Code = "USD",
                Name = "US Dollar",
                Symbol = "$",
                ExchangeRate = 24500m,
                IsBaseCurrency = false,
                EffectiveDate = DateTime.Now
            };

            Assert.Equal("USD", currency.Code);
            Assert.Equal("US Dollar", currency.Name);
            Assert.Equal("$", currency.Symbol);
            Assert.Equal(24500m, currency.ExchangeRate);
            Assert.False(currency.IsBaseCurrency);
        }

        [Fact]
        public void Currency_IsValid_ShouldReturnTrue()
        {
            var currency = new Currency
            {
                Code = "USD",
                Name = "US Dollar",
                ExchangeRate = 24500m,
                EffectiveDate = DateTime.Now
            };

            Assert.True(currency.IsValid());
        }

        [Fact]
        public void CurrencyConversion_ConvertToBase_ShouldCalculateCorrectly()
        {
            var conversion = new CurrencyConversion
            {
                FromCurrencyCode = "USD",
                ToCurrencyCode = "VND",
                ExchangeRate = 24500m,
                Amount = 100m,
                ConvertedAmount = 2450000m
            };

            Assert.Equal(2450000m, conversion.ConvertedAmount);
        }

        [Fact]
        public void MultiCurrencyTransaction_Create_ShouldHandleForeignCurrency()
        {
            var transaction = new MultiCurrencyTransaction
            {
                Id = "TX001",
                Date = DateTime.Now,
                Description = "Purchase order payment",
                CurrencyCode = "USD",
                ExchangeRate = 24500m,
                OriginalAmount = 1000m,
                ConvertedAmount = 24500000m
            };

            Assert.Equal("USD", transaction.CurrencyCode);
            Assert.Equal(24500000m, transaction.ConvertedAmount);
            Assert.True(transaction.IsBalanced);
        }
    }
}
