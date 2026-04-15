using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý bán hàng - S01-S06
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class SalesService
    {
        private readonly ISalesRepository _repository;

        public SalesService(ISalesRepository repository)
        {
            _repository = repository;
        }

        /// <summary>
        /// S01: Bán hàng thu tiền ngay (tiền mặt/chuyển khoản)
        /// </summary>
        public (bool Success, string Message, SalesTransaction Sale) CreateCashSale(CreateSaleInput input)
        {
            var sale = BuildSaleFromInput(input, SalesType.Cash);
            
            // Định khoản: Nợ 111/112 / Có 511 / Có 33311
            sale.JournalEntryType = "S01";
            sale.JournalEntryDescription = $"Bán hàng thu tiền - {sale.CustomerName}";

            _repository.Add(sale);
            return (true, "Tạo bán hàng thu tiền thành công", sale);
        }

        /// <summary>
        /// S02: Bán hàng chịu (công nợ phải thu)
        /// </summary>
        public (bool Success, string Message, SalesTransaction Sale) CreateCreditSale(CreateSaleInput input)
        {
            var sale = BuildSaleFromInput(input, SalesType.Credit);
            
            // Tính DueDate
            if (input.PaymentTermDays > 0)
            {
                sale.DueDate = sale.TransactionDate.AddDays(input.PaymentTermDays);
            }

            // Định khoản: Nợ 131 / Có 511 / Có 33311
            sale.JournalEntryType = "S02";
            sale.JournalEntryDescription = $"Bán hàng chịu - {sale.CustomerName}";

            _repository.Add(sale);
            return (true, "Tạo bán hàng chịu thành công", sale);
        }

        /// <summary>
        /// S03: Ghi nhận giá vốn hàng bán
        /// </summary>
        public (bool Success, string Message, decimal COGS) RecordCOGS(COGSInput input)
        {
            var sale = _repository.GetById(input.SaleId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch bán hàng", 0);
            }

            var cogs = input.Quantity * input.UnitCost;
            sale.COGS += cogs;
            _repository.Update(sale);

            return (true, "Ghi nhận giá vốn thành công", cogs);
        }

        /// <summary>
        /// S04: Xử lý hàng bán bị trả lại
        /// </summary>
        public (bool Success, string Message, decimal ReturnAmount) ProcessReturn(ReturnInput input)
        {
            var sale = _repository.GetById(input.SalesId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch bán hàng", 0);
            }

            var returnAmount = input.RefundAmount;
            var vatAmount = returnAmount * 0.10m;
            var netAmount = returnAmount - vatAmount;

            sale.Status = SalesStatus.Returned;
            sale.JournalEntryType = "S04";
            sale.JournalEntryDescription = $"Trả hàng - {input.Reason}";
            _repository.Update(sale);

            return (true, "Xử lý trả hàng thành công", returnAmount);
        }

        /// <summary>
        /// S05: Giảm giá hàng bán (discount percent on sale)
        /// </summary>
        public (bool Success, string Message, SalesTransaction Sale) ApplyDiscount(CreateSaleInput input)
        {
            var sale = BuildSaleFromInput(input, SalesType.Cash);
            sale.DiscountAmount = sale.SubTotal * (input.DiscountPercent / 100);
            
            RecalculateTotals(sale);
            
            _repository.Add(sale);
            return (true, "Áp dụng giảm giá thành công", sale);
        }

        /// <summary>
        /// S06: Chiết khấu thanh toán
        /// </summary>
        public (bool Success, string Message, decimal DiscountAmount) ApplyPaymentDiscount(PaymentInput input)
        {
            var sale = _repository.GetById(input.SaleId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch bán hàng", 0);
            }

            // Check if payment within discount period
            var daysDiff = (input.PaymentDate - sale.TransactionDate).Days;
            decimal discountPercent = 0;
            
            if (daysDiff <= 10) discountPercent = 2;
            else if (daysDiff <= 15) discountPercent = 1;

            var discountAmount = input.Amount * (discountPercent / 100);

            return (true, "Áp dụng chiết khấu thành công", discountAmount);
        }

        /// <summary>
        /// Get all sales
        /// </summary>
        public IEnumerable<SalesTransaction> GetAll()
        {
            return _repository.GetAll();
        }

        private SalesTransaction BuildSaleFromInput(CreateSaleInput input, SalesType type)
        {
            var sale = new SalesTransaction
            {
                Id = Guid.NewGuid().ToString(),
                TransactionNo = GenerateTransactionNo(type),
                TransactionDate = input.TransactionDate == default ? DateTime.Now : input.TransactionDate,
                Type = type,
                CustomerId = input.CustomerId ?? "KH001",
                CustomerName = input.CustomerName ?? "Khách hàng",
                CustomerTaxCode = input.CustomerTaxCode ?? "",
                PaymentTermDays = input.PaymentTermDays,
                VatRate = input.VatRate > 0 ? input.VatRate : 0.10m,
                DiscountPercent = input.DiscountPercent,
                Lines = new List<SalesLine>(),
                Status = SalesStatus.Draft,
                PaymentStatus = PaymentStatus.PendingPayment,
                CreatedAt = DateTime.Now
            };

            if (input.Lines != null)
            {
                foreach (var lineInput in input.Lines)
                {
                    var line = new SalesLine
                    {
                        Id = Guid.NewGuid().ToString(),
                        SalesId = sale.Id,
                        ProductId = lineInput.ProductId ?? "SP001",
                        ProductName = lineInput.ProductName ?? "Sản phẩm",
                        Quantity = lineInput.Quantity,
                        UnitPrice = lineInput.UnitPrice,
                        DiscountPercent = lineInput.DiscountPercent
                    };
                    sale.Lines.Add(line);
                }
            }

            RecalculateTotals(sale);
            return sale;
        }

        private void RecalculateTotals(SalesTransaction sale)
        {
            sale.SubTotal = sale.Lines.Sum(l => l.LineTotal);
            sale.DiscountAmount = sale.Lines.Sum(l => l.DiscountAmount);
            if (sale.DiscountPercent > 0)
            {
                sale.DiscountAmount += sale.SubTotal * (sale.DiscountPercent / 100);
            }
            var netAmount = sale.SubTotal - sale.DiscountAmount;
            sale.VATAmount = netAmount * sale.VatRate;
            sale.TotalAmount = netAmount + sale.VATAmount;
            sale.NetAmount = netAmount;
        }

        private string GenerateTransactionNo(SalesType type)
        {
            var prefix = type switch
            {
                SalesType.Cash => "S-TM",
                SalesType.Credit => "S-CN",
                SalesType.Installment => "S-TG",
                _ => "S"
            };
            return $"{prefix}{DateTime.Now:yyyyMMdd}-{Guid.NewGuid().ToString()[..4].ToUpper()}";
        }
    }

    public class CreateSaleInput
    {
        public string CustomerId { get; set; }
        public string CustomerName { get; set; }
        public string CustomerTaxCode { get; set; }
        public int PaymentTermDays { get; set; }
        public decimal VatRate { get; set; } = 0.10m;
        public DateTime TransactionDate { get; set; }
        public List<SalesLineInput> Lines { get; set; } = new();
public decimal DiscountPercent { get; set; }
    }

    public class COGSInput
    {
        public string SaleId { get; set; }
        public string ProductId { get; set; }
        public decimal Quantity { get; set; }
        public decimal UnitCost { get; set; }
    }

    public class ReturnInput
    {
        public string SalesId { get; set; }
        public DateTime ReturnDate { get; set; }
        public string Reason { get; set; }
        public decimal RefundAmount { get; set; }
    }

    public class PaymentInput
    {
        public string SaleId { get; set; }
        public DateTime PaymentDate { get; set; }
        public decimal Amount { get; set; }
    }

    public interface ISalesRepository
    {
        void Add(SalesTransaction sale);
        SalesTransaction GetById(string id);
        IEnumerable<SalesTransaction> GetAll();
        void Update(SalesTransaction sale);
    }
}
