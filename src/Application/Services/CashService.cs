using GL.Domain.Entities;
using GL.Application.DTOs;
using System;
using System.Collections.Generic;

namespace GL.Application.Services
{
    /// <summary>
    /// Service xử lý các nghiệp vụ tiền mặt và ngân hàng (T01-T22)
    /// Theo Thông tư 99/2025/TT-BTC và hướng dẫn từ tamkhoatech.vn
    /// </summary>
    public class CashService
    {
        /// <summary>
        /// T01: Rút tiền gửi ngân hàng về nhập quỹ tiền mặt
        /// Nợ 111(1111) / Có 112
        /// </summary>
        public Transaction CreateCashDepositEntry(CashDepositRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Rút tiền ngân hàng về quỹ - {request.FromAccount}"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            transaction.AddLine("112", 0, request.Amount, "Tiền gửi ngân hàng");

            return transaction;
        }

        /// <summary>
        /// T02: Thu tiền bán hàng nhập quỹ
        /// Nợ 111 / Có 511,515,711 + Có 333(33311)
        /// </summary>
        public Transaction CreateCashReceiptFromSaleEntry(CashReceiptFromSaleRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Thu tiền bán hàng từ KH {request.CustomerId}"
            };

            string cashAccount = request.PaymentMethod == "CASH" ? "1111" : "112";
            transaction.AddLine(cashAccount, request.Amount, 0, "Tiền mặt/TK ngân hàng");

            if (request.VatAmount > 0 && request.IsVatDeduction)
            {
                decimal netRevenue = request.Amount - request.VatAmount;
                transaction.AddLine("5111", 0, netRevenue, "Doanh thu bán hàng chưa thuế");
                transaction.AddLine("33311", 0, request.VatAmount, "Thuế GTGT đầu ra");
            }
            else
            {
                transaction.AddLine("5111", 0, request.Amount, "Doanh thu bán hàng (bao gồm VAT)");
            }

            return transaction;
        }

        /// <summary>
        /// T03: Chi tiền mặt mua nguyên vật liệu, CCDC, TSCĐ
        /// Nợ 151,152,153,156,211 / Nợ 133 / Có 111
        /// </summary>
        public Transaction CreateCashPaymentPurchaseEntry(CashPaymentPurchaseRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Mua hàng từ NCC {request.SupplierId}"
            };

            transaction.AddLine(request.InventoryAccount, request.Amount, 0, "Hàng mua/TSCĐ");
            
            if (request.VatAmount > 0 && request.IsVatDeduction)
            {
                transaction.AddLine("1331", request.VatAmount, 0, "Thuế GTGT đầu vào");
            }

            transaction.AddLine("1111", 0, request.Amount + request.VatAmount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T04: Nộp tiền mặt vào ngân hàng
        /// Nợ 112 / Có 111
        /// </summary>
        public Transaction CreateBankDepositEntry(BankDepositRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Nộp tiền vào TK ngân hàng {request.ToAccount}"
            };

            transaction.AddLine("112", request.Amount, 0, "Tiền gửi ngân hàng");
            transaction.AddLine("1111", 0, request.Amount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T05: Chi tiền mặt trả lương CBCNV
        /// Nợ 334 / Có 111
        /// </summary>
        public Transaction CreatePayrollCashPaymentEntry(CashPayrollPaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.PaymentBatchId ?? Guid.NewGuid().ToString(),
                Date = request.PaymentDate,
                Description = "Chi lương bằng tiền mặt"
            };

            transaction.AddLine("334", request.TotalNetPayVnd, 0, "Phải trả công nhân viên");
            transaction.AddLine("1111", 0, request.TotalNetPayVnd, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T06: Xuất quỹ chi tạm ứng, chi trả nợ
        /// Nợ 141/331/333/334/336/338/341/342 / Có 111
        /// </summary>
        public Transaction CreateAdvancePaymentEntry(AdvancePaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Chi tạm ứng cho {request.PayeeId}"
            };

            transaction.AddLine("141", request.Amount, 0, "Tạm ứng");
            transaction.AddLine("1111", 0, request.Amount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T07: Thu hồi nợ phải thu bằng tiền mặt
        /// Nợ 111 / Có 131,136,138,141
        /// </summary>
        public Transaction CreateReceivableCollectionEntry(ReceivableCollectionRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Thu nợ từ KH {request.CustomerId}"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            transaction.AddLine("131", 0, request.Amount, "Phải thu khách hàng");

            return transaction;
        }

        /// <summary>
        /// T08: Kiểm kê phát hiện thừa tiền mặt
        /// Nợ 111 / Có 338(3381)
        /// </summary>
        public Transaction CreateCashOverageEntry(CashOverageRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? "Phát hiện thừa tiền mặt khi kiểm kê"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            transaction.AddLine("3381", 0, request.Amount, "Phải trả khác - Chờ xử lý");

            return transaction;
        }

        /// <summary>
        /// T09: Kiểm kê phát hiện thiếu tiền mặt
        /// Nợ 138(1381) / Có 111
        /// </summary>
        public Transaction CreateCashShortageEntry(CashShortageRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? "Phát hiện thiếu tiền mặt khi kiểm kê"
            };

            transaction.AddLine("1381", request.Amount, 0, "Phải thu khác - Chờ xử lý");
            transaction.AddLine("1111", 0, request.Amount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T10: Nhận vốn cấp bằng tiền mặt nhập quỹ
        /// Nợ 111 / Có 411
        /// </summary>
        public Transaction CreateCapitalContributionEntry(CapitalContributionRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Nhận vốn góp từ {request.InvestorId}"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            transaction.AddLine("411", 0, request.Amount, "Vốn chủ sở hữu");

            return transaction;
        }

        /// <summary>
        /// T11: Nhận ký quỹ, ký cược bằng tiền mặt
        /// Nợ 111 / Có 344
        /// </summary>
        public Transaction CreateSecurityDepositReceivedEntry(SecurityDepositReceivedRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Nhận ký quỹ từ {request.DepositorId}"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            transaction.AddLine("344", 0, request.Amount, "Nhận thế chấp ký quỹ dài hạn");

            return transaction;
        }

        /// <summary>
        /// T12: Hoàn trả ký quỹ, ký cược bằng tiền mặt
        /// Nợ 344 / Có 111
        /// </summary>
        public Transaction CreateSecurityDepositReturnedEntry(SecurityDepositReturnedRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Hoàn trả ký quỹ cho {request.DepositorId}"
            };

            transaction.AddLine("344", request.Amount, 0, "Nhận thế chấp ký quỹ dài hạn");
            transaction.AddLine("1111", 0, request.Amount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T13: Chi tiền mặt chi trả chi phí kinh doanh
        /// Nợ 627,641,642,635,811 / Nợ 133 / Có 111
        /// </summary>
        public Transaction CreateExpensePaymentEntry(ExpensePaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? "Chi tiền mặt chi phí kinh doanh"
            };

            transaction.AddLine(request.ExpenseAccount, request.Amount, 0, "Chi phí");

            if (request.VatAmount > 0 && request.IsVatDeduction)
            {
                transaction.AddLine("1331", request.VatAmount, 0, "Thuế GTGT đầu vào");
            }

            transaction.AddLine("1111", 0, request.Amount + request.VatAmount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T14: Đi vay bằng tiền mặt
        /// Nợ 111 / Có 341 hoặc 311
        /// </summary>
        public Transaction CreateLoanReceivedEntry(LoanReceivedRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Nhận tiền vay từ {request.LenderId}"
            };

            transaction.AddLine("1111", request.Amount, 0, "Tiền mặt");
            
            string loanAccount = request.LoanType == "LONG_TERM" ? "341" : "311";
            transaction.AddLine(loanAccount, 0, request.Amount, 
                request.LoanType == "LONG_TERM" ? "Vay dài hạn" : "Vay ngắn hạn");

            return transaction;
        }

        /// <summary>
        /// T15: Bán, thu hồi đầu tư nhập quỹ tiền mặt
        /// Nợ 111 / Nợ/Có 635 hoặc 515 / Có 121,128,221,222,244
        /// </summary>
        public Transaction CreateInvestmentSaleEntry(InvestmentSaleRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Bán đầu tư {request.InvestmentAccount}"
            };

            decimal gainLoss = request.SaleAmount - request.CostAmount;

            transaction.AddLine("1111", request.SaleAmount, 0, "Tiền mặt");

            if (gainLoss != 0)
            {
                if (gainLoss > 0)
                    transaction.AddLine("515", 0, gainLoss, "Doanh thu hoạt động tài chính");
                else
                    transaction.AddLine("635", Math.Abs(gainLoss), 0, "Chi phí tài chính");
            }

            transaction.AddLine(request.InvestmentAccount, 0, request.CostAmount, "Đầu tư");

            return transaction;
        }

        /// <summary>
        /// T16: Xuất quỹ tiền mặt chi đầu tư
        /// Nợ 121,228,222,244 / Có 111
        /// </summary>
        public Transaction CreateInvestmentPurchaseEntry(InvestmentPurchaseRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Mua đầu tư {request.InvestmentAccount}"
            };

            transaction.AddLine(request.InvestmentAccount, request.Amount, 0, "Đầu tư");
            transaction.AddLine("1111", 0, request.Amount, "Tiền mặt");

            return transaction;
        }

        /// <summary>
        /// T17: Thu tiền bán hàng bằng ngoại tệ
        /// Nợ 111(1112) theo tỷ giá thực tế / Có 511 / Có 333(3331)
        /// </summary>
        public Transaction CreateForeignCurrencyReceiptEntry(ForeignCurrencyReceiptRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Thu ngoại tệ bán hàng {request.CurrencyCode}"
            };

            decimal vndAmount = request.Amount * request.ExchangeRate;
            decimal netAmount = vndAmount - request.VatAmount;

            transaction.AddLine("1112", vndAmount, 0, $"Tiền mặt {request.CurrencyCode}");
            transaction.AddLine("5111", 0, netAmount, "Doanh thu bán hàng");
            
            if (request.VatAmount > 0)
            {
                transaction.AddLine("33311", 0, request.VatAmount, "Thuế GTGT đầu ra");
            }

            return transaction;
        }

        /// <summary>
        /// T18: Thu hồi nợ ngoại tệ
        /// Nợ 111(1112) / Nợ/Có 635 hoặc 515 / Có 131,136...
        /// </summary>
        public Transaction CreateForeignCurrencyCollectionEntry(ForeignCurrencyCollectionRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Thu hồi nợ ngoại tệ từ {request.CustomerId}"
            };

            decimal receivedVnd = request.Amount * request.ExchangeRate;
            decimal recordedVnd = request.Amount * request.RecordedRate;
            decimal gainLoss = receivedVnd - recordedVnd;

            transaction.AddLine("1112", receivedVnd, 0, $"Tiền mặt {request.CurrencyCode}");

            if (gainLoss != 0)
            {
                if (gainLoss > 0)
                    transaction.AddLine("515", 0, gainLoss, "Lãi chênh lệch tỷ giá");
                else
                    transaction.AddLine("635", Math.Abs(gainLoss), 0, "Lỗ chênh lệch tỷ giá");
            }

            transaction.AddLine("131", 0, recordedVnd, "Phải thu khách hàng");

            return transaction;
        }

        /// <summary>
        /// T19: Xuất ngoại tệ mua vật tư, hàng hóa
        /// Nợ 152,153,156,211,627,641,642 theo tỷ giá thực tế / Nợ 133 / Có 111(1112) theo tỷ giá thực tế
        /// </summary>
        public Transaction CreateForeignCurrencyPaymentEntry(ForeignCurrencyPaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.Description ?? $"Xuất ngoại tệ mua hàng {request.CurrencyCode}"
            };

            decimal paymentVnd = request.Amount * request.ExchangeRate;

            transaction.AddLine(request.ExpenseAccount, paymentVnd, 0, "Chi phí mua hàng");

            if (request.VatAmount > 0)
            {
                transaction.AddLine("1331", request.VatAmount, 0, "Thuế GTGT đầu vào");
            }

            transaction.AddLine("1112", 0, paymentVnd, $"Tiền mặt {request.CurrencyCode}");

            return transaction;
        }

        /// <summary>
        /// T20: Bán ngoại tệ
        /// Nợ 111(1111),131 / Nợ/Có 635 hoặc 515 / Có 111(1112)
        /// </summary>
        public Transaction CreateForeignCurrencySaleEntry(ForeignCurrencySaleRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Bán ngoại tệ {request.CurrencyCode}"
            };

            decimal saleVnd = request.Amount * request.SaleRate;
            decimal recordedVnd = request.Amount * request.RecordedRate;
            decimal gainLoss = saleVnd - recordedVnd;

            transaction.AddLine("1111", saleVnd, 0, "Tiền mặt VND");

            if (gainLoss != 0)
            {
                if (gainLoss > 0)
                    transaction.AddLine("515", 0, gainLoss, "Lãi chênh lệch tỷ giá");
                else
                    transaction.AddLine("635", Math.Abs(gainLoss), 0, "Lỗ chênh lệch tỷ giá");
            }

            transaction.AddLine("1112", 0, recordedVnd, $"Ngoại tệ xuất bán");

            return transaction;
        }

        /// <summary>
        /// T21: Ứng trước cho nhà cung cấp bằng ngoại tệ
        /// Nợ 331 theo tỷ giá thực tế / Có 111(1112) theo tỷ giá thực tế
        /// </summary>
        public Transaction CreateForeignCurrencyAdvanceEntry(ForeignCurrencyAdvanceRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Ứng trước cho NCC {request.SupplierId} bằng ngoại tệ"
            };

            decimal paymentVnd = request.Amount * request.ExchangeRate;

            transaction.AddLine("331", paymentVnd, 0, "Phải trả người bán");
            transaction.AddLine("1112", 0, paymentVnd, $"Tiền mặt {request.CurrencyCode}");

            return transaction;
        }

        /// <summary>
        /// T22: Thu tiền đặt trước của người mua bằng ngoại tệ
        /// Nợ 111(1112) / Có 131
        /// </summary>
        public Transaction CreateCustomerAdvanceEntry(CustomerAdvanceRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Thu tiền đặt trước từ KH {request.CustomerId}"
            };

            decimal vndAmount = request.Amount * request.ExchangeRate;

            transaction.AddLine("1112", vndAmount, 0, $"Tiền mặt {request.CurrencyCode}");
            transaction.AddLine("131", 0, vndAmount, "Phải thu khách hàng");

            return transaction;
        }

        /// <summary>
        /// Validate transaction is balanced
        /// </summary>
        public bool ValidateTransaction(Transaction transaction)
        {
            return transaction.IsBalanced;
        }
    }
}
