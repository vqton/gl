using GL.Application.DTOs;
using GL.Application.Services;
using GL.Domain.Entities;
using System;
using Xunit;

namespace GL.Domain.Tests
{
    public class CashServiceTests
    {
        private readonly CashService _service;

        public CashServiceTests()
        {
            _service = new CashService();
        }

        [Fact]
        public void CreateCashDepositEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashDepositRequest
            {
                TransactionId = "TXN001",
                TransactionDate = new DateTime(2026, 1, 15),
                Amount = 50000000,
                FromAccount = "112",
                Description = "Rút tiền ngân hàng về quỹ",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCashDepositEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
            Assert.Equal(2, result.Lines.Count);
        }

        [Fact]
        public void CreateCashReceiptFromSaleEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashReceiptFromSaleRequest
            {
                TransactionId = "TXN002",
                TransactionDate = new DateTime(2026, 1, 15),
                CustomerId = "KH001",
                Amount = 110000000,
                VatAmount = 10000000,
                PaymentMethod = "CASH",
                IsVatDeduction = true,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCashReceiptFromSaleEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCashPaymentPurchaseEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashPaymentPurchaseRequest
            {
                TransactionId = "TXN003",
                TransactionDate = new DateTime(2026, 1, 15),
                SupplierId = "NCC001",
                InventoryAccount = "156",
                Amount = 100000000,
                VatAmount = 10000000,
                Description = "Mua hàng tiền mặt",
                IsVatDeduction = true,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCashPaymentPurchaseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateBankDepositEntry_ShouldCreateBalancedTransaction()
        {
            var request = new BankDepositRequest
            {
                TransactionId = "TXN004",
                TransactionDate = new DateTime(2026, 1, 15),
                Amount = 30000000,
                ToAccount = "112",
                Description = "Nộp tiền vào ngân hàng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateBankDepositEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreatePayrollCashPaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashPayrollPaymentRequest
            {
                PaymentBatchId = "PAY001",
                PaymentDate = new DateTime(2026, 1, 31),
                TotalNetPayVnd = 50000000,
                PaymentMethod = "CASH",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreatePayrollCashPaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateAdvancePaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new AdvancePaymentRequest
            {
                TransactionId = "TXN005",
                TransactionDate = new DateTime(2026, 1, 15),
                PayeeId = "NV001",
                Amount = 5000000,
                Description = "Chi tạm ứng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateAdvancePaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateReceivableCollectionEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ReceivableCollectionRequest
            {
                TransactionId = "TXN006",
                TransactionDate = new DateTime(2026, 1, 15),
                CustomerId = "KH001",
                Amount = 20000000,
                Description = "Thu nợ khách hàng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateReceivableCollectionEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCashOverageEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashOverageRequest
            {
                TransactionId = "TXN007",
                TransactionDate = new DateTime(2026, 1, 31),
                Amount = 500000,
                Description = "Phát hiện thừa tiền mặt",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCashOverageEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCashShortageEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CashShortageRequest
            {
                TransactionId = "TXN008",
                TransactionDate = new DateTime(2026, 1, 31),
                Amount = 300000,
                Description = "Phát hiện thiếu tiền mặt",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCashShortageEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCapitalContributionEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CapitalContributionRequest
            {
                TransactionId = "TXN009",
                TransactionDate = new DateTime(2026, 1, 15),
                InvestorId = "CSH001",
                Amount = 100000000,
                Description = "Nhận vốn góp",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCapitalContributionEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateSecurityDepositReceivedEntry_ShouldCreateBalancedTransaction()
        {
            var request = new SecurityDepositReceivedRequest
            {
                TransactionId = "TXN010",
                TransactionDate = new DateTime(2026, 1, 15),
                DepositorId = "DV001",
                Amount = 10000000,
                ContractRef = "HDTQ001",
                Description = "Nhận ký quỹ",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateSecurityDepositReceivedEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateSecurityDepositReturnedEntry_ShouldCreateBalancedTransaction()
        {
            var request = new SecurityDepositReturnedRequest
            {
                TransactionId = "TXN011",
                TransactionDate = new DateTime(2026, 12, 31),
                DepositorId = "DV001",
                Amount = 10000000,
                ContractRef = "HDTQ001",
                Description = "Hoàn trả ký quỹ",
                AccountingPeriodId = "2026-12"
            };

            var result = _service.CreateSecurityDepositReturnedEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateExpensePaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ExpensePaymentRequest
            {
                TransactionId = "TXN012",
                TransactionDate = new DateTime(2026, 1, 15),
                ExpenseAccount = "642",
                Amount = 5000000,
                VatAmount = 500000,
                Description = "Chi phí quản lý",
                IsVatDeduction = true,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateExpensePaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateLoanReceivedEntry_ShouldCreateBalancedTransaction()
        {
            var request = new LoanReceivedRequest
            {
                TransactionId = "TXN013",
                TransactionDate = new DateTime(2026, 1, 15),
                LenderId = "BANK001",
                Amount = 100000000,
                LoanType = "LONG_TERM",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateLoanReceivedEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInvestmentSaleEntry_Gain_ShouldCreateBalancedTransaction()
        {
            var request = new InvestmentSaleRequest
            {
                TransactionId = "TXN014",
                TransactionDate = new DateTime(2026, 1, 15),
                InvestmentAccount = "121",
                SaleAmount = 55000000,
                CostAmount = 50000000,
                BuyerId = "B001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInvestmentSaleEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInvestmentSaleEntry_Loss_ShouldCreateBalancedTransaction()
        {
            var request = new InvestmentSaleRequest
            {
                TransactionId = "TXN015",
                TransactionDate = new DateTime(2026, 1, 15),
                InvestmentAccount = "121",
                SaleAmount = 45000000,
                CostAmount = 50000000,
                BuyerId = "B001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInvestmentSaleEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateInvestmentPurchaseEntry_ShouldCreateBalancedTransaction()
        {
            var request = new InvestmentPurchaseRequest
            {
                TransactionId = "TXN016",
                TransactionDate = new DateTime(2026, 1, 15),
                InvestmentAccount = "121",
                Amount = 50000000,
                Description = "Mua chứng khoán",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateInvestmentPurchaseEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateForeignCurrencyReceiptEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ForeignCurrencyReceiptRequest
            {
                TransactionId = "TXN017",
                TransactionDate = new DateTime(2026, 1, 15),
                CurrencyCode = "USD",
                Amount = 1000,
                ExchangeRate = 25000,
                VatAmount = 2500000,
                Description = "Thu ngoại tệ bán hàng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateForeignCurrencyReceiptEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateForeignCurrencyCollectionEntry_Gain_ShouldCreateBalancedTransaction()
        {
            var request = new ForeignCurrencyCollectionRequest
            {
                TransactionId = "TXN018",
                TransactionDate = new DateTime(2026, 1, 15),
                CustomerId = "KH001",
                CurrencyCode = "USD",
                Amount = 1000,
                ExchangeRate = 25500,
                RecordedRate = 25000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateForeignCurrencyCollectionEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateForeignCurrencyPaymentEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ForeignCurrencyPaymentRequest
            {
                TransactionId = "TXN019",
                TransactionDate = new DateTime(2026, 1, 15),
                CurrencyCode = "USD",
                Amount = 1000,
                ExchangeRate = 24500,
                RecordedRate = 25000,
                ExpenseAccount = "156",
                VatAmount = 0,
                Description = "Xuất ngoại tệ mua hàng",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateForeignCurrencyPaymentEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateForeignCurrencySaleEntry_Gain_ShouldCreateBalancedTransaction()
        {
            var request = new ForeignCurrencySaleRequest
            {
                TransactionId = "TXN020",
                TransactionDate = new DateTime(2026, 1, 15),
                CurrencyCode = "USD",
                Amount = 1000,
                SaleRate = 26000,
                RecordedRate = 25000,
                BuyerId = "B001",
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateForeignCurrencySaleEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateForeignCurrencyAdvanceEntry_ShouldCreateBalancedTransaction()
        {
            var request = new ForeignCurrencyAdvanceRequest
            {
                TransactionId = "TXN021",
                TransactionDate = new DateTime(2026, 1, 15),
                SupplierId = "NCC001",
                CurrencyCode = "USD",
                Amount = 500,
                ExchangeRate = 25500,
                RecordedRate = 25000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateForeignCurrencyAdvanceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void CreateCustomerAdvanceEntry_ShouldCreateBalancedTransaction()
        {
            var request = new CustomerAdvanceRequest
            {
                TransactionId = "TXN022",
                TransactionDate = new DateTime(2026, 1, 15),
                CustomerId = "KH001",
                CurrencyCode = "USD",
                Amount = 1000,
                ExchangeRate = 25000,
                AccountingPeriodId = "2026-01"
            };

            var result = _service.CreateCustomerAdvanceEntry(request);

            Assert.NotNull(result);
            Assert.True(result.IsBalanced);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnTrue_WhenTransactionIsBalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN_TEST1",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("1111", 1000000, 0, "Debit");
            transaction.AddLine("112", 0, 1000000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.True(result);
        }

        [Fact]
        public void ValidateTransaction_ShouldReturnFalse_WhenTransactionIsUnbalanced()
        {
            var transaction = new Transaction
            {
                Id = "TXN_TEST2",
                Date = DateTime.Now,
                Description = "Test"
            };
            transaction.AddLine("1111", 1000000, 0, "Debit");
            transaction.AddLine("112", 0, 500000, "Credit");

            var result = _service.ValidateTransaction(transaction);

            Assert.False(result);
        }
    }
}
