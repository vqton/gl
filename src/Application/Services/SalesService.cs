using System;
using System.Collections.Generic;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

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
        /// S01: Tạo giao dịch bán hàng tiền mặt
        /// </summary>
        public (bool Success, string Message, SalesTransaction Sale) CreateSale(CreateSaleInput input)
        {
            if (input.Lines == null || !input.Lines.Any())
            {
                return (false, "Danh sách sản phẩm trống", null);
            }

            var sale = new SalesTransaction
            {
                Id = Guid.NewGuid().ToString(),
                TransactionNo = GenerateTransactionNo(),
                TransactionDate = input.TransactionDate == default ? DateTime.Now : input.TransactionDate,
                Type = input.Type,
                CustomerId = input.CustomerId ?? "",
                CustomerName = input.CustomerName ?? "Khách lẻ",
                CustomerTaxCode = input.CustomerTaxCode ?? "",
                PaymentTermDays = input.PaymentTermDays,
                DueDate = input.PaymentTermDays > 0 ? input.TransactionDate.AddDays(input.PaymentTermDays) : (DateTime?)null,
                VatRate = input.VatRate,
                Status = SalesStatus.PendingPayment,
                PaymentStatus = PaymentStatus.PendingPayment,
                CreatedAt = DateTime.Now,
                Lines = new List<SalesLine>()
            };

            // Process lines and calculate totals
            decimal subTotal = 0;
            foreach (var lineInput in input.Lines)
            {
                var lineTotal = lineInput.Quantity * lineInput.UnitPrice;
                var discountAmount = lineTotal * (lineInput.DiscountPercent / 100);
                subTotal += lineTotal - discountAmount;

                var line = new SalesLine
                {
                    Id = Guid.NewGuid().ToString(),
                    SalesId = sale.Id,
                    ProductId = lineInput.ProductId,
                    ProductName = lineInput.ProductName ?? lineInput.ProductId,
                    Quantity = lineInput.Quantity,
                    UnitPrice = lineInput.UnitPrice,
                    DiscountPercent = lineInput.DiscountPercent,
                    DiscountAmount = discountAmount,
                    AccountCode = input.Type == SalesType.Cash ? "111" : "131"
                };
                sale.Lines.Add(line);
            }

            sale.SubTotal = subTotal;
            sale.DiscountAmount = input.Lines.Sum(l =>
                (l.Quantity * l.UnitPrice) * (l.DiscountPercent / 100));
            sale.VATAmount = (sale.SubTotal - sale.DiscountAmount) * input.VatRate;
            sale.TotalAmount = sale.SubTotal - sale.DiscountAmount + sale.VATAmount;

            // Add journal lines for accounting
            AddJournalLines(sale, input.Type);

            _repository.Add(sale);
            return (true, "Tạo giao dịch bán hàng thành công", sale);
        }

        /// <summary>
        /// S03: Ghi nhận giá vốn hàng bán (COGS)
        /// </summary>
        public (bool Success, string Message) RecordCOGS(string transactionId, string productId, decimal quantity)
        {
            var sale = _repository.GetById(transactionId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch");
            }

            // Calculate COGS (simplified - would need inventory cost)
            decimal cogsPerUnit = 7_000_000m; // Simplified
            sale.COGS = cogsPerUnit * quantity;

            var cogsLine = new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductId = productId,
                ProductName = productId,
                Quantity = quantity,
                UnitPrice = cogsPerUnit,
                AccountCode = "632",  // Giá vốn hàng bán
                Debit = sale.COGS,
                Credit = 0
            };
            sale.Lines.Add(cogsLine);

            _repository.Update(sale);
            return (true, "Ghi nhận giá vốn thành công");
        }

        /// <summary>
        /// S04: Xử lý hàng bán bị trả lại
        /// </summary>
        public (bool Success, string Message, SalesTransaction Sale) ProcessReturn(ReturnInput input)
        {
            var sale = _repository.GetById(input.SalesId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch", null);
            }

            sale.Status = SalesStatus.Returned;
            
            // Add return journal lines
            var returnLine = new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductId = input.ProductId,
                ProductName = "Hàng trả lại",
                Quantity = input.Quantity,
                AccountCode = "5212",  // Hàng bán bị trả lại
                Debit = input.RefundAmount > 0 ? input.RefundAmount : 0,
                Credit = input.RefundAmount > 0 ? 0 : 0
            };
            sale.Lines.Add(returnLine);

            _repository.Update(sale);
            return (true, "Xử lý trả hàng thành công", sale);
        }

        /// <summary>
        /// S05: Giảm giá hàng bán
        /// </summary>
        public (bool Success, string Message) ApplyDiscount(string transactionId, decimal discountAmount)
        {
            var sale = _repository.GetById(transactionId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch");
            }

            // Check: discount <= 20% of total
            if (discountAmount > sale.TotalAmount * 0.20m)
            {
                return (false, "Giảm giá không được vượt quá 20% giá trị giao dịch");
            }

            sale.DiscountAmount += discountAmount;
            sale.TotalAmount -= discountAmount;

            var discountLine = new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductName = "Giảm giá hàng bán",
                AccountCode = "5211",
                Debit = discountAmount,
                Credit = 0
            };
            sale.Lines.Add(discountLine);

            _repository.Update(sale);
            return (true, "Áp dụng giảm giá thành công");
        }

        /// <summary>
        /// S06: Chiết khấu thanh toán
        /// </summary>
        public (bool Success, string Message) ApplyPaymentDiscount(string transactionId, decimal discountPercent)
        {
            var sale = _repository.GetById(transactionId);
            if (sale == null)
            {
                return (false, "Không tìm thấy giao dịch");
            }

            var discountAmount = sale.TotalAmount * discountPercent;
            var discountLine = new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductName = "Chiết khấu thanh toán",
                AccountCode = "5213",
                Debit = discountAmount,
                Credit = 0
            };
            sale.Lines.Add(discountLine);

            _repository.Update(sale);
            return (true, "Áp dụng chiết khấu thành công");
        }

        /// <summary>
        /// Get sales by customer
        /// </summary>
        public IEnumerable<SalesTransaction> GetByCustomer(string customerId)
        {
            return _repository.GetByCustomer(customerId);
        }

        /// <summary>
        /// Get overdue sales
        /// </summary>
        public IEnumerable<SalesTransaction> GetOverdueSales()
        {
            return _repository.GetAll()
                .Where(s => s.Type == SalesType.Credit && 
                          s.PaymentStatus == PaymentStatus.PendingPayment &&
                          s.DueDate.HasValue && 
                          s.DueDate.Value < DateTime.Now);
        }

        /// <summary>
        /// Get sale by ID
        /// </summary>
        public SalesTransaction GetById(string id)
        {
            return _repository.GetById(id);
        }

        private string GenerateTransactionNo()
        {
            return $"S{DateTime.Now:yyyyMMdd}-{Guid.NewGuid().ToString()[..8].ToUpper()}";
        }

        private void AddJournalLines(SalesTransaction sale, SalesType type)
        {
            // Debit: 111 (cash) or 131 (receivable)
            var debitAccount = type == SalesType.Cash ? "111" : "131";
            
            // Add debit line
            sale.Lines.Add(new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductName = type == SalesType.Cash ? "Tiền mặt" : "Phải thu KH",
                AccountCode = debitAccount,
                Debit = sale.TotalAmount,
                Credit = 0
            });

            // Credit: 511 (revenue) + 33311 (VAT output)
            sale.Lines.Add(new SalesLine
            {
                Id = Guid.NewGuid().ToString(),
                SalesId = sale.Id,
                ProductName = "Doanh thu bán hàng",
                AccountCode = "511",
                Debit = 0,
                Credit = sale.SubTotal - sale.DiscountAmount
            });

            if (sale.VATAmount > 0)
            {
                sale.Lines.Add(new SalesLine
                {
                    Id = Guid.NewGuid().ToString(),
                    SalesId = sale.Id,
                    ProductName = "VAT đầu ra",
                    AccountCode = "33311",
                    Debit = 0,
                    Credit = sale.VATAmount
                });
            }
        }
    }
}