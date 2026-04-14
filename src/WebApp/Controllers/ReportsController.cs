using GL.Application.Services;
using GL.Domain.Entities;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// Controller quản lý báo cáo tài chính (Phase 3)
    /// </summary>
    public class ReportsController : Controller
    {
        private readonly ReportService _reportService;

        public ReportsController()
        {
            _reportService = new ReportService();
        }

        /// <summary>
        /// Trang chủ báo cáo
        /// </summary>
        public IActionResult Index()
        {
            return View();
        }

        /// <summary>
        /// Báo cáo Bảng cân đối kế toán (BCĐKT)
        /// </summary>
        public IActionResult BalanceSheet(string periodCode, DateTime? reportDate)
        {
            var period = periodCode ?? $"{DateTime.Now.Year}-{DateTime.Now.Month:D2}";
            var date = reportDate ?? DateTime.Now;

            var sampleTransactions = GetSampleTransactions();
            var report = _reportService.GenerateBalanceSheetReport(sampleTransactions, period, date);

            ViewBag.PeriodCode = period;
            ViewBag.ReportDate = date.ToString("dd/MM/yyyy");

            return View(report);
        }

        /// <summary>
        /// Báo cáo Kết quả hoạt động kinh doanh (BCKQHĐKD)
        /// </summary>
        public IActionResult IncomeStatement(string periodCode, DateTime? reportDate)
        {
            var period = periodCode ?? $"{DateTime.Now.Year}-{DateTime.Now.Month:D2}";
            var date = reportDate ?? DateTime.Now;

            var sampleTransactions = GetSampleTransactions();
            var report = _reportService.GenerateIncomeStatementReport(sampleTransactions, period, date);

            ViewBag.PeriodCode = period;
            ViewBag.ReportDate = date.ToString("dd/MM/yyyy");

            return View(report);
        }

        /// <summary>
        /// Lấy danh sách giao dịch mẫu (demo)
        /// </summary>
        private List<Transaction> GetSampleTransactions()
        {
            var transactions = new List<Transaction>();

            var txn1 = new Transaction
            {
                Id = "TX001",
                Date = new DateTime(2026, 1, 5),
                Description = "Bán hàng chưa thu tiền"
            };
            txn1.AddLine("131", 110000000, 0, "Phải thu khách hàng");
            txn1.AddLine("511", 0, 100000000, "Doanh thu bán hàng");
            txn1.AddLine("3331", 0, 10000000, "VAT đầu ra");
            transactions.Add(txn1);

            var txn2 = new Transaction
            {
                Id = "TX002",
                Date = new DateTime(2026, 1, 10),
                Description = "Thu tiền khách hàng"
            };
            txn2.AddLine("112", 110000000, 0, "Tiền gửi ngân hàng");
            txn2.AddLine("131", 0, 110000000, "Phải thu khách hàng");
            transactions.Add(txn2);

            var txn3 = new Transaction
            {
                Id = "TX003",
                Date = new DateTime(2026, 1, 15),
                Description = "Mua hàng hóa"
            };
            txn3.AddLine("156", 70000000, 0, "Hàng hóa");
            txn3.AddLine("1331", 7000000, 0, "VAT đầu vào");
            txn3.AddLine("331", 0, 77000000, "Phải trả người bán");
            transactions.Add(txn3);

            var txn4 = new Transaction
            {
                Id = "TX004",
                Date = new DateTime(2026, 1, 20),
                Description = "Chi phí quản lý"
            };
            txn4.AddLine("642", 25000000, 0, "Chi phí quản lý doanh nghiệp");
            txn4.AddLine("112", 0, 25000000, "Tiền gửi ngân hàng");
            transactions.Add(txn4);

            var txn5 = new Transaction
            {
                Id = "TX005",
                Date = new DateTime(2026, 1, 25),
                Description = "Giá vốn hàng bán"
            };
            txn5.AddLine("632", 60000000, 0, "Giá vốn hàng bán");
            txn5.AddLine("156", 0, 60000000, "Hàng hóa");
            transactions.Add(txn5);

            return transactions;
        }
    }
}
