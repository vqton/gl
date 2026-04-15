using GL.Application.DTOs;
using GL.Domain.Entities;

namespace GL.Application.Services
{
    /// <summary>
    /// Dịch vụ kế toán thuế - X01-X05
    /// </summary>
    public class TaxService
    {
        /// <summary>
        /// Tạo bút toán kê khai và nộp thuế GTGT (X01)
        /// </summary>
        /// <param name="request">Yêu cầu kê khai VAT</param>
        /// <returns>Bút toán VAT</returns>
        public Transaction CreateVatDeclarationEntry(VatDeclarationRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.DeclarationDate,
                Description = $"Kê khai và nộp thuế GTGT - Kỳ {request.DeclarationPeriodId}",
            };

            decimal vatToOffset = System.Math.Min(request.OutputVatTotal, request.InputVatTotal);
            decimal netVatPayable = System.Math.Max(0, request.OutputVatTotal - request.InputVatTotal);

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
        public Transaction CreateCitTaxEntry(CitTaxRequest request)
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
        public Transaction CreatePitTaxEntry(PitTaxRequest request)
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
        /// Tạo bút toán VAT đầu vào không được khấu trừ (X04)
        /// </summary>
        /// <param name="request">Yêu cầu VAT không được khấu trừ</param>
        /// <returns>Bút toán VAT không được khấu trừ</returns>
        public Transaction CreateUnrecoverableVatEntry(UnrecoverableVatRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RecognitionDate,
                Description = $"VAT đầu vào không được khấu trừ - Hóa đơn {request.InvoiceId}",
            };

            transaction.AddLine(request.ExpenseAccountCode, request.VatAmountVnd, 0, $"VAT không được khấu trừ: {request.Reason}");
            transaction.AddLine("1331", 0, request.VatAmountVnd, "Giảm VAT đầu vào");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán thuế TNDN hoãn lại tài sản (X05)
        /// </summary>
        /// <param name="request">Yêu cầu thuế hoãn lại</param>
        /// <returns>Bút toán thuế hoãn lại tài sản</returns>
        public Transaction CreateDeferredTaxAssetEntry(DeferredTaxRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RecognitionDate,
                Description = $"Ghi nhận thuế TNDN hoãn lại tài sản - Năm {request.FiscalYearId}",
            };

            transaction.AddLine("243", request.DeferredTaxAssetVnd, 0, "Tài sản thuế TNDN hoãn lại");
            transaction.AddLine("8212", 0, request.DeferredTaxAssetVnd, "Chi phí thuế TNDN hoãn lại");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán thuế TNDN hoãn lại nợ phải trả (X05)
        /// </summary>
        /// <param name="request">Yêu cầu thuế hoãn lại</param>
        /// <returns>Bút toán thuế hoãn lại nợ phải trả</returns>
        public Transaction CreateDeferredTaxLiabilityEntry(DeferredTaxRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.RecognitionDate,
                Description = $"Ghi nhận thuế TNDN hoãn lại nợ phải trả - Năm {request.FiscalYearId}",
            };

            transaction.AddLine("8212", request.DeferredTaxAssetVnd, 0, "Chi phí thuế TNDN hoãn lại");
            transaction.AddLine("347", 0, request.DeferredTaxAssetVnd, "Thuế TNDN hoãn lại phải trả");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán đảo thuế TNDN hoãn lại
        /// </summary>
        /// <param name="request">Yêu cầu đảo thuế hoãn lại</param>
        /// <returns>Bút toán đảo thuế</returns>
        public Transaction CreateDeferredTaxReversalEntry(DeferredTaxReversalRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.ReversalDate,
                Description = $"Đảo thuế TNDN hoãn lại - {request.Reason}",
            };

            transaction.AddLine("8212", request.ReversalAmountVnd, 0, "Đảo chi phí thuế hoãn lại");
            transaction.AddLine(request.OriginalDeferredTaxCode, 0, request.ReversalAmountVnd, "Giảm thuế hoãn lại");

            return transaction;
        }

        /// <summary>
        /// Tạo bút toán hóa đơn điện tử (FCT)
        /// </summary>
        /// <param name="request">Yêu cầu hóa đơn điện tử</param>
        /// <returns>Bút toán FCT</returns>
        public Transaction CreateFctInvoiceEntry(FctInvoiceRequest request)
        {
            var transaction = new Transaction
            {
                Id = Guid.NewGuid().ToString(),
                Date = request.InvoiceDate,
                Description = $"Hóa đơn điện tử {request.InvoiceId}",
            };

            decimal totalWithVat = request.TotalBeforeVatVnd + request.VatAmountVnd;

            transaction.AddLine("131", totalWithVat, 0, $"Phải thu từ FCT {request.InvoiceId}");
            transaction.AddLine("5111", 0, request.TotalBeforeVatVnd, "Doanh thu bán hàng");
            transaction.AddLine("33311", 0, request.VatAmountVnd, "VAT đầu ra");

            return transaction;
        }
    }
}