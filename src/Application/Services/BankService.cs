using GL.Application.DTOs;
using GL.Domain.Entities;
using System;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kế toán ngân hàng - B01-B08
    /// </summary>
    public class BankService
    {
        /// <summary>
        /// Tạo bút toán đối chiếu sao kê ngân hàng (B01)
        /// </summary>
        public Transaction CreateBankReconciliationEntry(BankReconciliationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ReconciliationDate,
                Description = $"Đối chiếu sao kê ngân hàng - {request.BankAccountCode}",
            };

            decimal difference = request.BankStatementBalance - request.BookBalance;

            if (Math.Abs(difference) > 0.01m && !string.IsNullOrEmpty(request.DifferenceReason))
            {
                if (difference > 0)
                {
                    transaction.AddLine(request.BankAccountCode, difference, 0, "Tăng do đối chiếu");
                    transaction.AddLine("138", 0, difference, request.DifferenceReason);
                }
                else
                {
                    transaction.AddLine("138", Math.Abs(difference), 0, request.DifferenceReason);
                    transaction.AddLine(request.BankAccountCode, 0, Math.Abs(difference), "Giảm do đối chiếu");
                }
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán chuyển khoản thanh toán (B02)
        /// </summary>
        public Transaction CreateWirePaymentEntry(WirePaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.PaymentDate,
                Description = $"Chuyển khoản thanh toán - {request.SupplierName}",
            };

            decimal totalPayment = request.AmountVnd + request.VatAmountVnd;

            transaction.AddLine("331", totalPayment, 0, $"Phải trả {request.SupplierName}");
            transaction.AddLine("112", 0, totalPayment, "Chuyển khoản");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán giải ngân vay ngân hàng (B03)
        /// </summary>
        public Transaction CreateLoanDrawdownEntry(LoanDrawdownRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.DrawdownDate,
                Description = $"Giải ngân vay - {request.BankName}",
            };

            transaction.AddLine("112", request.LoanAmountVnd, 0, "Nhận giải ngân");
            transaction.AddLine(request.LoanAccountCode, 0, request.LoanAmountVnd, "Vay ngắn hạn");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán trả nợ vay (B04)
        /// </summary>
        public Transaction CreateLoanRepaymentEntry(LoanRepaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RepaymentDate,
                Description = "Trả nợ vay ngân hàng",
            };

            transaction.AddLine(request.LoanAccountCode, request.PrincipalAmountVnd, 0, "Trả gốc vay");
            transaction.AddLine("635", request.InterestAmountVnd, 0, "Chi phí lãi vay");
            transaction.AddLine("112", 0, request.PrincipalAmountVnd + request.InterestAmountVnd, "Thanh toán");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán phí ngân hàng (B05)
        /// </summary>
        public Transaction CreateBankFeeEntry(BankFeeRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.FeeDate,
                Description = $"Phí ngân hàng - {request.FeeDescription}",
            };

            transaction.AddLine(request.ExpenseAccountCode, request.FeeAmountVnd, 0, request.FeeDescription);
            transaction.AddLine("112", 0, request.FeeAmountVnd, "Phí ngân hàng");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán lãi tiền gửi ngân hàng (B06)
        /// </summary>
        public Transaction CreateInterestIncomeEntry(InterestIncomeRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.InterestDate,
                Description = "Lãi tiền gửi ngân hàng",
            };

            decimal netInterest = request.InterestAmountVnd - request.TaxWithheldVnd;

            transaction.AddLine("112", netInterest, 0, "Lãi tiền gửi (sau thuế)");
            if (request.TaxWithheldVnd > 0)
            {
                transaction.AddLine("112", request.TaxWithheldVnd, 0, "Thuế TNCN khấu trừ");
            }
            transaction.AddLine("515", 0, request.InterestAmountVnd, "Lãi tiền gửi");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán đánh giá lại ngoại hối (B08)
        /// </summary>
        public Transaction CreateFxRevaluationEntry(FxRevaluationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RevaluationDate,
                Description = "Đánh giá lại ngoại hối",
            };

            decimal difference = request.NewAmountVnd - request.OriginalAmountVnd;

            if (difference > 0)
            {
                transaction.AddLine(request.BankAccountCode, difference, 0, "Lãi tỷ giá");
                transaction.AddLine("413", 0, difference, "Chênh lệch tỷ giá");
            }
            else if (difference < 0)
            {
                transaction.AddLine("635", Math.Abs(difference), 0, "Lỗ tỷ giá");
                transaction.AddLine(request.BankAccountCode, 0, Math.Abs(difference), "Chênh lệch tỷ giá");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán mở LC (B07)
        /// </summary>
        public Transaction CreateLcOpeningEntry(LcOpeningRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.LcIssueDate,
                Description = $"Mở LC - {request.BankName}",
            };

            transaction.AddLine("144", request.LcAmountVnd, 0, "Ký quỹ LC");
            transaction.AddLine("112", 0, request.LcAmountVnd, "Phí LC trừ tài khoản");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán thanh toán LC
        /// </summary>
        public Transaction CreateLcSettlementEntry(LcSettlementRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.SettlementDate,
                Description = "Thanh toán LC",
            };

            transaction.AddLine("144", request.PaymentAmountVnd, 0, "Giải ký quỹ LC");
            transaction.AddLine("331", 0, request.PaymentAmountVnd, "Phải trả NCC");

            return transaction;
        }
    }
}