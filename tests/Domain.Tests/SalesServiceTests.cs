using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho SalesService (S01-S06)
    /// </summary>
    public class SalesServiceTests
    {
        private readonly InMemorySalesRepository _repo;
        private readonly SalesService _service;

        public SalesServiceTests()
        {
            _repo = new InMemorySalesRepository();
            _service = new SalesService(_repo);
        }

        [Fact]
        public void S01_CreateCashSale_WithValidInput_ReturnsSuccess()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                CustomerName = "Công ty ABC",
                TransactionDate = new DateTime(2026, 4, 15),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 10, UnitPrice = 1_000_000m }
                }
            };

            var result = _service.CreateCashSale(input);

            Assert.True(result.Success);
            Assert.NotNull(result.Sale);
            Assert.Equal("KH001", result.Sale.CustomerId);
        }

        [Fact]
        public void S01_CreateCashSale_WithVAT_CalculatesCorrectly()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                VatRate = 0.10m,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 1, UnitPrice = 1_000_000m }
                }
            };

            var result = _service.CreateCashSale(input);

            Assert.True(result.Success);
            Assert.Equal(1_000_000m, result.Sale.NetAmount);
            Assert.Equal(100_000m, result.Sale.VATAmount);
            Assert.Equal(1_100_000m, result.Sale.TotalAmount);
        }

        [Fact]
        public void S01_CreateCashSale_UpdatesJournalEntry()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 1, UnitPrice = 1_100_000m }
                }
            };

            var result = _service.CreateCashSale(input);

            Assert.Equal("S01", result.Sale.JournalEntryType);
            Assert.Contains("Bán hàng thu tiền", result.Sale.JournalEntryDescription);
        }

        [Fact]
        public void S02_CreateCreditSale_WithPaymentTerm_ReturnsSuccess()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                CustomerName = "Công ty ABC",
                TransactionDate = new DateTime(2026, 4, 15),
                PaymentTermDays = 30,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 10, UnitPrice = 1_000_000m }
                }
            };

            var result = _service.CreateCreditSale(input);

            Assert.True(result.Success);
            Assert.Equal(SalesType.Credit, result.Sale.Type);
            Assert.Equal(new DateTime(2026, 5, 15), result.Sale.DueDate);
        }

        [Fact]
        public void S02_CreateCreditSale_JournalEntryFor131()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 1, UnitPrice = 1_100_000m }
                }
            };

            var result = _service.CreateCreditSale(input);

            Assert.Equal("S02", result.Sale.JournalEntryType);
        }

        [Fact]
        public void S03_RecordCOGS_WithInventory_ReturnsCorrectCost()
        {
            var saleInput = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 5, UnitPrice = 1_000_000m }
                }
            };
            var sale = _service.CreateCashSale(saleInput).Sale;

            var cogsInput = new COGSInput
            {
                SaleId = sale.Id,
                ProductId = "SP001",
                Quantity = 5,
                UnitCost = 700_000m
            };

            var result = _service.RecordCOGS(cogsInput);

            Assert.True(result.Success);
            Assert.Equal(3_500_000m, result.COGS);
        }

        [Fact]
        public void S04_ProcessSalesReturn_ReducesRevenue()
        {
            var saleInput = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 10, UnitPrice = 1_000_000m }
                }
            };
            var sale = _service.CreateCashSale(saleInput).Sale;

            var returnInput = new ReturnInput
            {
                SalesId = sale.Id,
                ReturnDate = new DateTime(2026, 4, 20),
                Reason = "Hàng kém chất lượng",
                RefundAmount = 2_200_000m
            };

            var result = _service.ProcessReturn(returnInput);

            Assert.True(result.Success);
            Assert.Equal(2_200_000m, result.ReturnAmount);
            Assert.Equal(SalesStatus.Returned, sale.Status);
        }

        [Fact]
        public void S05_ApplyDiscount_WithValidAmount_ReturnsSuccess()
        {
            var input = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 15),
                DiscountPercent = 10,
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 1, UnitPrice = 1_000_000m }
                }
            };

            var result = _service.ApplyDiscount(input);

            Assert.True(result.Success);
            Assert.Equal(100_000m, result.Sale.DiscountAmount);
            Assert.Equal(990_000m, result.Sale.TotalAmount);
        }

        [Fact]
        public void S06_ApplyPaymentDiscount_WithinDiscountPeriod_ReturnsDiscount()
        {
            var saleInput = new CreateSaleInput
            {
                CustomerId = "KH001",
                TransactionDate = new DateTime(2026, 4, 1),
                Lines = new List<SalesLineInput>
                {
                    new SalesLineInput { ProductId = "SP001", ProductName = "Sản phẩm A", Quantity = 1, UnitPrice = 10_000_000m }
                }
            };
            var sale = _service.CreateCashSale(saleInput).Sale;

            var paymentInput = new PaymentInput
            {
                SaleId = sale.Id,
                PaymentDate = new DateTime(2026, 4, 10),
                Amount = 11_000_000m
            };

            var result = _service.ApplyPaymentDiscount(paymentInput);

            Assert.True(result.Success);
            Assert.Equal(220_000m, result.DiscountAmount);
        }

        [Fact]
        public void GetAllSales_ReturnsAll()
        {
            _service.CreateCashSale(new CreateSaleInput { CustomerId = "A", TransactionDate = DateTime.Now, Lines = new List<SalesLineInput> { new() { ProductId = "P1", ProductName = "P", Quantity = 1, UnitPrice = 100 } } });
            _service.CreateCashSale(new CreateSaleInput { CustomerId = "B", TransactionDate = DateTime.Now, Lines = new List<SalesLineInput> { new() { ProductId = "P2", ProductName = "P", Quantity = 1, UnitPrice = 200 } } });

            var sales = _service.GetAll();

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

        public IEnumerable<SalesTransaction> GetAll()
        {
            return _sales;
        }

        public void Update(SalesTransaction sale)
        {
            var index = _sales.FindIndex(s => s.Id == sale.Id);
            if (index >= 0) _sales[index] = sale;
        }
    }
}