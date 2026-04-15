using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho SalesService (S01-S06)
    /// </summary>
    public class SalesTests
    {
        private readonly InMemorySalesRepository _repository;
        private readonly SalesService _service;

        public SalesTests()
        {
            _repository = new InMemorySalesRepository();
            _service = new SalesService(_repository);
        }

        [Fact]
        public void S01_CreateCashSale_BalancesCorrectly()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 11_000_000m }
                },
                TransactionDate = DateTime.Now
            };

            var result = _service.CreateSale(input);

            Assert.True(result.Success);
            Assert.NotNull(result.Sale);
            
            // Verify balance: total debit = total credit
            var totalDebit = result.Sale.Lines.Sum(l => l.Debit);
            var totalCredit = result.Sale.Lines.Sum(l => l.Credit);
            Assert.Equal(totalDebit, totalCredit);
        }

        [Fact]
        public void S01_CreateCashSale_WithVAT_10Percent()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                VatRate = 0.10m,
                TransactionDate = DateTime.Now
            };

            var result = _service.CreateSale(input);

            Assert.True(result.Success);
            Assert.Equal(10_000_000m, result.Sale.SubTotal);     // Net
            Assert.Equal(1_000_000m, result.Sale.VATAmount);    // VAT 10%
            Assert.Equal(11_000_000m, result.Sale.TotalAmount);   // Gross
        }

        [Fact]
        public void S02_CreateCreditSale_SetsCorrectStatus()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Credit,
                CustomerId = "KH001",
                CustomerName = "Công ty ABC",
                PaymentTermDays = 30,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 10, UnitPrice = 5_000_000m }
                },
                TransactionDate = DateTime.Now
            };

            var result = _service.CreateSale(input);

            Assert.True(result.Success);
            Assert.Equal(PaymentStatus.PendingPayment, result.Sale.PaymentStatus);
            Assert.Contains(result.Sale.Lines, l => l.AccountCode == "131");
        }

        [Fact]
        public void S02_CreateCreditSale_SetsOverdueAfter30Days()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Credit,
                CustomerId = "KH001",
                CustomerName = "Công ty ABC",
                PaymentTermDays = 30,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now.AddDays(-35)
            };
            _service.CreateSale(input);

            var overdue = _service.GetOverdueSales();

            Assert.Single(overdue);
        }

        [Fact]
        public void S03_RecordCOGS_FIFO_CalculatesCorrectly()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 2, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now
            };
            var sale = _service.CreateSale(input).Sale;

            var cogsResult = _service.RecordCOGS(sale.Id, "SP001", 2);

            Assert.True(cogsResult.Success);
            Assert.Contains(sale.Lines, l => l.AccountCode == "632");
        }

        [Fact]
        public void S04_ProcessReturn_ReducesRevenue()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now
            };
            var sale = _service.CreateSale(input).Sale;

            var returnInput = new ReturnInput
            {
                SalesId = sale.Id,
                Quantity = 1,
                Reason = "Hàng lỗi",
                ReturnDate = DateTime.Now
            };
            var result = _service.ProcessReturn(returnInput);

            Assert.True(result.Success);
            Assert.Equal(SalesStatus.Returned, result.Sale.Status);
        }

        [Fact]
        public void S05_ApplyDiscount_ValidAmount()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now
            };
            var sale = _service.CreateSale(input).Sale;

            var discountAmount = 500_000m;  // 5%
            var result = _service.ApplyDiscount(sale.Id, discountAmount);

            Assert.True(result.Success);
        }

        [Fact]
        public void S05_ApplyDiscount_Exceeds20Percent_ReturnsFalse()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Cash,
                CustomerName = "Khách lẻ",
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now
            };
            var sale = _service.CreateSale(input).Sale;

            var result = _service.ApplyDiscount(sale.Id, 2_500_000m); // 25%

            Assert.False(result.Success);
        }

        [Fact]
        public void S06_ApplyPaymentDiscount_CalculatesCorrectly()
        {
            var input = new CreateSaleInput
            {
                Type = SalesType.Credit,
                CustomerId = "KH001",
                CustomerName = "Công ty ABC",
                PaymentTermDays = 30,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 10_000_000m }
                },
                TransactionDate = DateTime.Now
            };
            var sale = _service.CreateSale(input).Sale;

            var result = _service.ApplyPaymentDiscount(sale.Id, 0.02m); // 2%

            Assert.True(result.Success);
        }

        [Fact]
        public void GetByCustomer_ReturnsSales()
        {
            _service.CreateSale(new CreateSaleInput { Type = SalesType.Cash, CustomerId = "KH001", CustomerName = "Công ty ABC", Lines = new List<SalesLineInput> { new SalesLineInput { ProductId = "SP001", Quantity = 1, UnitPrice = 5_000_000m } }, TransactionDate = DateTime.Now });
            _service.CreateSale(new CreateSaleInput { Type = SalesType.Cash, CustomerId = "KH001", CustomerName = "Công ty ABC", Lines = new List<SalesLineInput> { new SalesLineInput { ProductId = "SP002", Quantity = 1, UnitPrice = 3_000_000m } }, TransactionDate = DateTime.Now });

            var sales = _service.GetByCustomer("KH001");

            Assert.Equal(2, sales.Count());
        }
    }

    public class InMemorySalesRepository : ISalesRepository
    {
        private readonly List<SalesTransaction> _sales = new();

        public void Add(SalesTransaction sale)
        {
            _sales.Add(sale);
        }

        public SalesTransaction GetById(string id)
        {
            return _sales.FirstOrDefault(s => s.Id == id);
        }

        public IEnumerable<SalesTransaction> GetByCustomer(string customerId)
        {
            return _sales.Where(s => s.CustomerId == customerId);
        }

        public void Update(SalesTransaction sale)
        {
            var index = _sales.FindIndex(s => s.Id == sale.Id);
            if (index >= 0) _sales[index] = sale;
        }

        public IEnumerable<SalesTransaction> GetAll()
        {
            return _sales;
        }

        public void Delete(string id)
        {
            _sales.RemoveAll(s => s.Id == id);
        }
    }
}