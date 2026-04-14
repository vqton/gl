using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GL.Application.Services
{
    /// <summary>
    /// Service xử lý các nghiệp vụ kế toán tổng hợp (Phase 2)
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class TransactionService
    {
        /// <summary>
        /// Tạo bút toán kết chuyển doanh thu (G01)
        /// </summary>
        /// <param name="request">Yêu cầu kết chuyển doanh thu</param>
        /// <returns>Bút toán kết chuyển</returns>
        public Transaction CreateRevenueClosingEntry(DTOs.RevenueClosingRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ClosingDate,
                Description = $"Kết chuyển doanh thu - Kỳ {request.ClosingPeriodId}",
            };

            decimal totalRevenue = request.Revenue511 + request.Revenue515 + request.Revenue711;
            decimal netRevenue = totalRevenue - request.ContraRevenue521;

            if (request.Revenue511 > 0)
                transaction.AddLine("511", request.Revenue511, 0, "Kết chuyển doanh thu bán hàng");
            if (request.Revenue515 > 0)
                transaction.AddLine("515", request.Revenue515, 0, "Kết chuyển doanh thu hoạt động tài chính");
            if (request.Revenue711 > 0)
                transaction.AddLine("711", request.Revenue711, 0, "Kết chuyển thu nhập khác");

            if (request.ContraRevenue521 > 0)
                transaction.AddLine("521", 0, request.ContraRevenue521, "Kết chuyển giảm trừ doanh thu");

            if (netRevenue > 0)
                transaction.AddLine("911", 0, netRevenue, "Doanh thu thuần");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán kết chuyển chi phí (G02)
        /// </summary>
        /// <param name="request">Yêu cầu kết chuyển chi phí</param>
        /// <returns>Bút toán kết chuyển</returns>
        public Transaction CreateExpenseClosingEntry(DTOs.ExpenseClosingRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ClosingDate,
                Description = $"Kết chuyển chi phí - Kỳ {request.ClosingPeriodId}",
            };

            decimal totalExpenses = request.Expense632 + request.Expense635 + request.Expense641 + 
                                request.Expense642 + request.Expense811 + request.Expense821;

            if (totalExpenses > 0)
                transaction.AddLine("911", totalExpenses, 0, "Kết chuyển tổng chi phí");

            if (request.Expense632 > 0)
                transaction.AddLine("632", 0, request.Expense632, "Giá vốn hàng bán");
            if (request.Expense635 > 0)
                transaction.AddLine("635", 0, request.Expense635, "Chi phí tài chính");
            if (request.Expense641 > 0)
                transaction.AddLine("641", 0, request.Expense641, "Chi phí bán hàng");
            if (request.Expense642 > 0)
                transaction.AddLine("642", 0, request.Expense642, "Chi phí quản lý doanh nghiệp");
            if (request.Expense811 > 0)
                transaction.AddLine("811", 0, request.Expense811, "Chi phí khác");
            if (request.Expense821 > 0)
                transaction.AddLine("821", 0, request.Expense821, "Chi phí thuế TNDN");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán kết chuyển lợi nhuận sau thuế (G03)
        /// </summary>
        /// <param name="request">Yêu cầu kết chuyển lợi nhuận</param>
        /// <returns>Bút toán kết chuyển</returns>
        public Transaction CreateProfitClosingEntry(DTOs.ProfitClosingRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ClosingDate,
                Description = $"Kết chuyển lợi nhuận sau thuế - Năm {request.FiscalYearId}",
            };

            if (request.ProfitAfterTaxVnd > 0)
            {
                transaction.AddLine("911", request.ProfitAfterTaxVnd, 0, "Kết chuyển lãi");
                transaction.AddLine("4212", 0, request.ProfitAfterTaxVnd, "Lợi nhuận sau thuế chưa phân phối");
            }
            else if (request.ProfitAfterTaxVnd < 0)
            {
                transaction.AddLine("911", 0, Math.Abs(request.ProfitAfterTaxVnd), "Kết chuyển lỗ");
                transaction.AddLine("4212", Math.Abs(request.ProfitAfterTaxVnd), 0, "Lỗ năm nay");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán kê khai và nộp thuế GTGT (X01)
        /// </summary>
        /// <param name="request">Yêu cầu kê khai VAT</param>
        /// <returns>Bút toán VAT</returns>
        public Transaction CreateVatDeclarationEntry(DTOs.VatDeclarationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.DeclarationDate,
                Description = $"Kê khai và nộp thuế GTGT - Kỳ {request.DeclarationPeriodId}",
            };

            decimal vatToOffset = Math.Min(request.OutputVatTotal, request.InputVatTotal);
            decimal netVatPayable = Math.Max(0, request.OutputVatTotal - request.InputVatTotal);

            if (vatToOffset > 0)
            {
                transaction.AddLine("33311", vatToOffset, 0, "Bù trừ VAT đầu ra");
                transaction.AddLine("1331", 0, vatToOffset, "Bù trừ VAT đầu vào");
            }

            if (netVatPayable > 0)
            {
                transaction.AddLine("3331", 0, netVatPayable, "VAT còn phải nộp");
                transaction.AddLine("112", netVatPayable, 0, "Nộp ngân sách");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán chi phí thuế TNDN (X02)
        /// </summary>
        /// <param name="request">Yêu cầu tính thuế TNDN</param>
        /// <returns>Bút toán thuế TNDN</returns>
        public Transaction CreateCitTaxEntry(DTOs.CitTaxRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.CalculationDate,
                Description = $"Hạch toán chi phí thuế TNDN - Kỳ {request.TaxPeriodId}",
            };

            decimal taxAmount = request.TaxableIncomeVnd * request.CitRate;

            transaction.AddLine("8211", taxAmount, 0, "Chi phí thuế TNDN hiện hành");
            transaction.AddLine("3334", 0, taxAmount, "Thuế TNDN phải nộp");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán thuế TNCN từ tiền lương (X03)
        /// </summary>
        /// <param name="request">Yêu cầu tính thuế TNCN</param>
        /// <returns>Bút toán thuế TNCN</returns>
        public Transaction CreatePitTaxEntry(DTOs.PitTaxRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.WithholdingDate,
                Description = $"Hạch toán thuế TNCN từ lương - Kỳ {request.PayrollPeriodId}",
            };

            transaction.AddLine("334", request.TotalPitWithheldVnd, 0, "Khấu trừ TNCN từ lương");
            transaction.AddLine("3335", 0, request.TotalPitWithheldVnd, "Thuế TNCN phải nộp");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán tính lương (L01)
        /// </summary>
        /// <param name="request">Yêu cầu tính lương</param>
        /// <returns>Bút toán lương</returns>
        public Transaction CreatePayrollEntry(DTOs.PayrollCalculationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.PayrollMonth,
                Description = $"Tính lương và các khoản phải trả - Tháng {request.PayrollMonth:yyyy-MM}",
            };

            transaction.AddLine("642", request.TotalGrossVnd, 0, "Chi phí lương");
            transaction.AddLine("334", 0, request.NetPayVnd, "Lương phải trả");
            
            if (request.EmployeeDeductionsVnd > 0)
                transaction.AddLine("3383", 0, request.EmployeeDeductionsVnd, "BHXH/BHYT/BHTN phần NLĐ");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán trích bảo hiểm xã hội phần doanh nghiệp (L02)
        /// </summary>
        /// <param name="request">Yêu cầu tính bảo hiểm</param>
        /// <returns>Bút toán bảo hiểm</returns>
        public Transaction CreateSocialInsuranceEntry(DTOs.SocialInsuranceRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.CalculationDate,
                Description = $"Trích BHXH phần doanh nghiệp - Kỳ {request.PayrollId}",
            };

            decimal totalContribution = request.Bhxh175 + request.Bhyt30 + request.Bhtn10 + request.Kpcd20;

            if (totalContribution > 0)
            {
                transaction.AddLine("642", totalContribution, 0, "CP BHXH DN");
                transaction.AddLine("3382", 0, totalContribution, "Trích theo lương phải nộp");
            }

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán chi lương (L03)
        /// </summary>
        /// <param name="request">Yêu cầu chi lương</param>
        /// <returns>Bút toán chi lương</returns>
        public Transaction CreatePayrollPaymentEntry(DTOs.PayrollPaymentRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.PaymentDate,
                Description = $"Chi lương cho người lao động - Batch {request.PaymentBatchId}",
            };

            string cashAccount = request.PaymentMethod == "CASH" ? "111" : "112";

            transaction.AddLine("334", request.TotalNetPayVnd, 0, "Lương phải trả");
            transaction.AddLine(cashAccount, 0, request.TotalNetPayVnd, "Tiền thanh toán");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán mua tài sản cố định (A01)
        /// </summary>
        /// <param name="request">Yêu cầu mua TSCĐ</param>
        /// <returns>Bút toán mua TSCĐ</returns>
        public Transaction CreateFixedAssetPurchaseEntry(DTOs.FixedAssetPurchaseRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.HandoverDate,
                Description = $"Mua tài sản cố định - {request.AssetHandoverId}",
            };

            string assetAccount = request.AssetType switch
            {
                "TANGIBLE" => "211",
                "INTANGIBLE" => "213",
                "LEASED" => "212",
                _ => "211"
            };

            string cashAccount = request.PaymentMethod == "CASH" ? "111" : "331";

            transaction.AddLine(assetAccount, request.OriginalCostVnd, 0, "Nguyên giá TSCĐ");
            transaction.AddLine("1332", request.VatAmountVnd, 0, "VAT TSCĐ đầu vào");
            transaction.AddLine(cashAccount, 0, request.OriginalCostVnd + request.VatAmountVnd, "Phải trả/Thanh toán");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán khấu hao TSCĐ hàng tháng (A02)
        /// </summary>
        /// <param name="request">Yêu cầu tính khấu hao</param>
        /// <param name="totalDepreciation">Tổng khấu hao</param>
        /// <param name="department">Bộ phận phân bổ</param>
        /// <returns>Bút toán khấu hao</returns>
        public Transaction CreateDepreciationEntry(DTOs.DepreciationRequest request, decimal totalDepreciation, string department)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.CalculationDate,
                Description = $"Trích khấu hao TSCĐ - Kỳ {request.DepreciationPeriodId}",
            };

            string expenseAccount = department switch
            {
                "PRODUCTION" => "627",
                "SALES" => "641",
                "ADMIN" => "642",
                _ => "642"
            };

            string depreciationAccount = department == "PRODUCTION" ? "2141" : "2143";

            transaction.AddLine(expenseAccount, totalDepreciation, 0, "Chi phí khấu hao");
            transaction.AddLine(depreciationAccount, 0, totalDepreciation, "Hao mòn lũy kế");

            return transaction;
        }

        /// <summary>
        /// Kiểm tra bút toán có cân bằng không
        /// </summary>
        /// <param name="transaction">Bút toán cần kiểm tra</param>
        /// <returns>True nếu cân bằng</returns>
        public bool ValidateTransaction(Transaction transaction)
        {
            return transaction.IsBalanced;
        }
    }
}