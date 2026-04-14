using GL.Domain.Entities;
using GL.Application.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// API Controller cho các tích hợp bên thứ ba
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    public class ApiController : ControllerBase
    {
        /// <summary>
        /// Lấy danh sách tài khoản
        /// </summary>
        [HttpGet("accounts")]
        public IActionResult GetAccounts()
        {
            return Ok(new { message = "API endpoint for accounts" });
        }

        /// <summary>
        /// Lấy thông tin tài khoản theo mã
        /// </summary>
        [HttpGet("accounts/{code}")]
        public IActionResult GetAccount(string code)
        {
            return Ok(new { code, message = "Account details" });
        }

        /// <summary>
        /// Tạo giao dịch mới
        /// </summary>
        [HttpPost("transactions")]
        public IActionResult CreateTransaction([FromBody] Transaction transaction)
        {
            if (!transaction.IsBalanced)
                return BadRequest(new { error = "Transaction is not balanced" });

            return Created($"/api/v1/transactions/{transaction.Id}", transaction);
        }

        /// <summary>
        /// Lấy danh sách giao dịch
        /// </summary>
        [HttpGet("transactions")]
        public IActionResult GetTransactions([FromQuery] string periodCode = null)
        {
            return Ok(new List<Transaction>());
        }

        /// <summary>
        /// Lấy thông tin giao dịch theo ID
        /// </summary>
        [HttpGet("transactions/{id}")]
        public IActionResult GetTransaction(string id)
        {
            return Ok(new { id, message = "Transaction details" });
        }

        /// <summary>
        /// Lấy danh sách kỳ kế toán
        /// </summary>
        [HttpGet("periods")]
        public IActionResult GetPeriods()
        {
            return Ok(new List<AccountingPeriod>());
        }

        /// <summary>
        /// Lấy thông tin báo cáo tài chính
        /// </summary>
        [HttpGet("reports/{reportType}")]
        public IActionResult GetReport(string reportType, [FromQuery] string periodCode)
        {
            return Ok(new { reportType, periodCode, message = "Report data" });
        }

        /// <summary>
        /// Lấy tỷ giá ngoại tệ
        /// </summary>
        [HttpGet("exchange-rates")]
        public IActionResult GetExchangeRates([FromQuery] string baseCurrency = "VND")
        {
            return Ok(new List<Currency>());
        }

        /// <summary>
        /// Lấy thông tin ngân sách
        /// </summary>
        [HttpGet("budgets")]
        public IActionResult GetBudgets([FromQuery] int? fiscalYear = null)
        {
            return Ok(new List<Budget>());
        }

        /// <summary>
        /// Kiểm tra sức khỏe hệ thống
        /// </summary>
        [HttpGet("health")]
        public IActionResult HealthCheck()
        {
            return Ok(new { status = "healthy", timestamp = DateTime.UtcNow });
        }

        // ========== P0: Lao Động - Tiền Lương ==========

        /// <summary>
        /// Lấy danh sách hợp đồng lao động
        /// </summary>
        [HttpGet("contracts")]
        public IActionResult GetContracts([FromQuery] string? employeeId = null)
        {
            return Ok(new List<LaborContract>());
        }

        /// <summary>
        /// Lấy thông tin hợp đồng lao động theo ID
        /// </summary>
        [HttpGet("contracts/{id}")]
        public IActionResult GetContract(string id)
        {
            return Ok(new { id, message = "Contract details" });
        }

        /// <summary>
        /// Tạo hợp đồng lao động mới
        /// </summary>
        [HttpPost("contracts")]
        public IActionResult CreateContract([FromBody] LaborContract contract)
        {
            if (!contract.IsValid())
                return BadRequest(new { error = "Contract data is invalid" });

            contract.Id = Guid.NewGuid().ToString();
            return Created($"/api/v1/contracts/{contract.Id}", contract);
        }

        /// <summary>
        /// Cập nhật hợp đồng lao động
        /// </summary>
        [HttpPut("contracts/{id}")]
        public IActionResult UpdateContract(string id, [FromBody] LaborContract contract)
        {
            contract.Id = id;
            return Ok(new { id, message = "Contract updated" });
        }

        /// <summary>
        /// Chấm dứt hợp đồng lao động
        /// </summary>
        [HttpDelete("contracts/{id}")]
        public IActionResult TerminateContract(string id)
        {
            return Ok(new { id, message = "Contract terminated" });
        }

        /// <summary>
        /// Lấy bảng lương theo kỳ
        /// </summary>
        [HttpGet("payrolls")]
        public IActionResult GetPayrolls([FromQuery] int year, [FromQuery] int month)
        {
            return Ok(new List<Payroll>());
        }

        /// <summary>
        /// Tạo bảng lương mới
        /// </summary>
        [HttpPost("payrolls")]
        public IActionResult CreatePayroll([FromBody] Payroll payroll)
        {
            payroll.Id = Guid.NewGuid().ToString();
            return Created($"/api/v1/payrolls/{payroll.Id}", payroll);
        }

        /// <summary>
        /// Tính lương
        /// </summary>
        [HttpPost("payrolls/{id}/calculate")]
        public IActionResult CalculatePayroll(string id)
        {
            return Ok(new { id, message = "Payroll calculated" });
        }

        /// <summary>
        /// Duyệt bảng lương
        /// </summary>
        [HttpPost("payrolls/{id}/approve")]
        public IActionResult ApprovePayroll(string id)
        {
            return Ok(new { id, message = "Payroll approved" });
        }

        /// <summary>
        /// Chi trả lương
        /// </summary>
        [HttpPost("payrolls/{id}/pay")]
        public IActionResult PayPayroll(string id)
        {
            return Ok(new { id, message = "Payroll paid" });
        }

        // ========== P1: Tăng ca - Nghỉ phép - Thôi việc ==========

        /// <summary>
        /// Lấy danh sách tăng ca
        /// </summary>
        [HttpGet("overtimes")]
        public IActionResult GetOvertimes([FromQuery] string? employeeId = null, [FromQuery] DateTime? fromDate = null)
        {
            return Ok(new List<OvertimeRecord>());
        }

        /// <summary>
        /// Tạo bản ghi tăng ca
        /// </summary>
        [HttpPost("overtimes")]
        public IActionResult CreateOvertime([FromBody] OvertimeRecord record)
        {
            if (!record.IsValid())
                return BadRequest(new { error = "Invalid overtime record" });

            return Created($"/api/v1/overtimes/{record.Id}", record);
        }

        /// <summary>
        /// Duyệt tăng ca
        /// </summary>
        [HttpPost("overtimes/{id}/approve")]
        public IActionResult ApproveOvertime(string id)
        {
            return Ok(new { id, message = "Overtime approved" });
        }

        /// <summary>
        /// Lấy danh sách nghỉ phép
        /// </summary>
        [HttpGet("leaves")]
        public IActionResult GetLeaves([FromQuery] string? employeeId = null)
        {
            return Ok(new List<LeaveRequest>());
        }

        /// <summary>
        /// Tạo yêu cầu nghỉ phép
        /// </summary>
        [HttpPost("leaves")]
        public IActionResult CreateLeave([FromBody] LeaveRequest request)
        {
            if (!request.IsValid())
                return BadRequest(new { error = "Invalid leave request" });

            return Created($"/api/v1/leaves/{request.Id}", request);
        }

        /// <summary>
        /// Duyệt nghỉ phép
        /// </summary>
        [HttpPost("leaves/{id}/approve")]
        public IActionResult ApproveLeave(string id)
        {
            return Ok(new { id, message = "Leave approved" });
        }

        /// <summary>
        /// Tính trợ cấp thôi việc
        /// </summary>
        [HttpPost("severance/calculate")]
        public IActionResult CalculateSeverance([FromQuery] string employeeId, [FromQuery] DateTime startDate, [FromQuery] DateTime terminationDate, [FromQuery] decimal monthlySalary)
        {
            var calculator = new SeverancePayCalculator();
            var result = calculator.CalculateSeverancePay(startDate, terminationDate, monthlySalary);
            
            return Ok(new { 
                eligible = result.Eligible, 
                message = result.Message, 
                amount = result.Amount,
                eligibleMonths = result.EligibleMonths 
            });
        }

        /// <summary>
        /// Tạo bản ghi trợ cấp thôi việc
        /// </summary>
        [HttpPost("severance")]
        public IActionResult CreateSeveranceRecord([FromBody] SeveranceRecord record)
        {
            return Created($"/api/v1/severance/{record.Id}", record);
        }
    }
}
