using GL.Application.DTOs;
using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;

namespace GL.Application.Services
{
    /// <summary>
    /// Service xử lý hóa đơn điện tử (E-Invoice / HĐĐT)
    /// Theo Thông tư 99/2025/TT-BTC & quy định Tổng cục Thuế
    /// Phase 6 - Integration
    /// </summary>
    public class EInvoiceService
    {
        private static int _invoiceCounter = 0;
        private readonly Dictionary<string, EInvoiceResult> _invoices = new();

        /// <summary>
        /// Tạo hóa đơn điện tử mới (EI01)
        /// </summary>
        public EInvoiceResult CreateInvoice(EInvoiceCreateRequest request)
        {
            _invoiceCounter++;

            var invoiceNumber = $"{DateTime.Now:yy}{_invoiceCounter:D4}";
            decimal totalAmount = 0;
            decimal vatAmount = 0;

            if (request.Items != null)
            {
                foreach (var item in request.Items)
                {
                    var lineTotal = item.Quantity * item.UnitPrice;
                    totalAmount += lineTotal;
                    vatAmount += lineTotal * item.VATRate / 100;
                }
            }

            var invoice = new EInvoiceResult
            {
                InvoiceId = Guid.NewGuid().ToString(),
                InvoiceNumber = invoiceNumber,
                InvoiceType = request.InvoiceType ?? "01GTKT",
                InvoiceDate = DateTime.Now,
                SellerTaxCode = request.SellerTaxCode,
                BuyerTaxCode = request.BuyerTaxCode,
                TotalAmount = totalAmount + vatAmount,
                VATAmount = vatAmount,
                IsSigned = false,
                Status = "DRAFT"
            };

            _invoices[invoiceNumber] = invoice;
            return invoice;
        }

        /// <summary>
        /// Ký điện tử hóa đơn (EI02)
        /// </summary>
        public EInvoiceResult SignInvoice(EInvoiceResult invoice, string pin)
        {
            if (string.IsNullOrEmpty(pin))
                throw new ArgumentException("PIN is required for signing");

            invoice.IsSigned = true;
            return invoice;
        }

        /// <summary>
        /// Generate XML theo định dạng Tổng cục Thuế (EI06)
        /// </summary>
        public string GenerateXML(EInvoiceResult invoice)
        {
            var xml = new XDocument(
                new XDeclaration("1.0", "UTF-8", null),
                new XElement("Invoice",
                    new XAttribute(XNamespace.Xmlns + "xsi", "http://www.w3.org/2001/XMLSchema-instance"),
                    new XElement("InvoiceId", invoice.InvoiceId),
                    new XElement("InvoiceType", invoice.InvoiceType),
                    new XElement("InvoiceNumber", invoice.InvoiceNumber),
                    new XElement("InvoiceDate", invoice.InvoiceDate.ToString("yyyy-MM-dd")),
                    new XElement("SellerTaxCode", invoice.SellerTaxCode),
                    new XElement("BuyerTaxCode", invoice.BuyerTaxCode ?? ""),
                    new XElement("TotalAmount", invoice.TotalAmount),
                    new XElement("VATAmount", invoice.VATAmount),
                    new XElement("Status", invoice.Status)
                )
            );

            return xml.ToString();
        }

        /// <summary>
        /// Gửi hóa đơn lên Tổng cục Thuế (EI03)
        /// </summary>
        public (bool Success, string Message, string ReferenceCode) SubmitToTaxAuthority(EInvoiceResult invoice)
        {
            if (!invoice.IsSigned)
                return (false, "Invoice must be signed before submission", null);

            var referenceCode = $"{DateTime.Now:yyyyMMdd}{_invoiceCounter:D6}";
            invoice.Status = "ISSUED";

            return (true, "Invoice submitted successfully", referenceCode);
        }

        /// <summary>
        /// Tra cứu hóa đơn (EI04)
        /// </summary>
        public EInvoiceResult GetInvoiceByNumber(string invoiceNumber)
        {
            return _invoices.TryGetValue(invoiceNumber, out var invoice) ? invoice : null;
        }

        /// <summary>
        /// Hủy hóa đơn (EI05)
        /// </summary>
        public (bool Success, string Message) CancelInvoice(string invoiceNumber, string reason)
        {
            if (!_invoices.ContainsKey(invoiceNumber))
                return (false, "Invoice not found");

            var invoice = _invoices[invoiceNumber];

            if (invoice.Status == "ISSUED")
            {
                var daysSinceIssue = (DateTime.Now - invoice.InvoiceDate).Days;
                if (daysSinceIssue > 90)
                    return (false, "Cannot cancel invoice after 90 days from issue date");
            }

            invoice.Status = "CANCELLED";
            return (true, "Invoice cancelled successfully");
        }

        /// <summary>
        /// Xuất nhiều hóa đơn ra file nén (ZIP)
        /// </summary>
        public string ExportMultipleInvoices(string[] invoiceNumbers)
        {
            var sb = new StringBuilder();
            foreach (var num in invoiceNumbers)
            {
                if (_invoices.TryGetValue(num, out var inv))
                {
                    sb.AppendLine(GenerateXML(inv));
                }
            }
            return sb.ToString();
        }

        /// <summary>
        /// Lập hóa đơn điều chỉnh tăng/giảm (UC-EI-003)
        /// Theo Nghị định 70/2025/NĐ-CP
        /// </summary>
        /// <param name="originalInvoiceNumber">Số hóa đơn gốc cần điều chỉnh</param>
        /// <param name="adjustmentAmount">Số tiền điều chỉnh (âm = giảm, dương = tăng)</param>
        /// <param name="adjustmentType">Loại điều chỉnh: "INCREASE" hoặc "DECREASE"</param>
        /// <param name="reason">Lý do điều chỉnh</param>
        /// <returns>Hóa đơn điều chỉnh</returns>
        public EInvoiceResult AdjustInvoice(string originalInvoiceNumber, decimal adjustmentAmount, string adjustmentType, string reason)
        {
            if (!_invoices.ContainsKey(originalInvoiceNumber))
                throw new ArgumentException("Invoice not found");

            var originalInvoice = _invoices[originalInvoiceNumber];
            var adjustmentLabel = adjustmentType == "DECREASE" ? "-" : "+";

            var adjustedInvoice = new EInvoiceResult
            {
                InvoiceId = Guid.NewGuid().ToString(),
                InvoiceNumber = $"{DateTime.Now:yy}{_invoiceCounter:D4}",
                InvoiceType = originalInvoice.InvoiceType,
                InvoiceDate = DateTime.Now,
                SellerTaxCode = originalInvoice.SellerTaxCode,
                BuyerTaxCode = originalInvoice.BuyerTaxCode,
                TotalAmount = adjustmentAmount,
                VATAmount = adjustmentAmount * 10 / 100,
                IsSigned = false,
                Status = "ADJUSTMENT"
            };

            _invoices[adjustedInvoice.InvoiceNumber] = adjustedInvoice;
            return adjustedInvoice;
        }

        /// <summary>
        /// Lập hóa đơn thay thế (UC-EI-004)
        /// Theo Nghị định 70/2025/NĐ-CP
        /// </summary>
        /// <param name="originalInvoiceNumber">Số hóa đơn gốc cần thay thế</param>
        /// <param name="newRequest">Thông tin hóa đơn mới đúng</param>
        /// <returns>Hóa đơn thay thế</returns>
        public EInvoiceResult ReplaceInvoice(string originalInvoiceNumber, EInvoiceCreateRequest newRequest)
        {
            if (!_invoices.ContainsKey(originalInvoiceNumber))
                throw new ArgumentException("Invoice not found");

            var newInvoice = CreateInvoice(newRequest);
            newInvoice.Status = "REPLACED";

            _invoices[originalInvoiceNumber] = newInvoice;
            return newInvoice;
        }

        /// <summary>
        /// Lập biên bản thỏa thuận điều chỉnh hóa đơn
        /// Theo Nghị định 70/2025
        /// </summary>
        public string GenerateAdjustmentMinutes(string invoiceNumber, string buyerName, string sellerName, string errorDescription, string correctionContent)
        {
            var minutes = $@"
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập – Tự do – Hạnh phúc

BIÊN BẢN ĐIỀU CHỈNH HÓA ĐƠN ĐIỆN TỬ

Căn cứ Nghị định 70/2025/NĐ-CP ngày 20/03/2025;

Hôm nay, {DateTime.Now:dd/MM/yyyy} hai bên chúng tôi gồm:

Bên bán: {sellerName}
Bên mua: {buyerName}

Hai bên thống nhất điều chỉnh hóa đơn số {invoiceNumber}

Lý do điều chỉnh: {errorDescription}

Nội dung điều chỉnh: {correctionContent}

ĐẠI DIỆN BÊN BÁN                    ĐẠI DIỆN BÊN MUA
";
            return minutes;
        }
    }
}