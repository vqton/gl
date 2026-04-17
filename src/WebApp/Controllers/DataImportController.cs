using GL.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// Data Import API
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    [Authorize(Policy = "FullAccess")]
    public class DataImportController : ControllerBase
    {
        private readonly DataImportService _importService;

        public DataImportController()
        {
            _importService = new DataImportService();
        }

        /// <summary>
        /// Get CSV template
        /// </summary>
        [HttpGet("template/{type}")]
        public IActionResult GetTemplate(string type)
        {
            var template = _importService.GenerateTemplate(type);
            if (string.IsNullOrEmpty(template))
            {
                return BadRequest(new { Error = "Unknown template type" });
            }

            return Ok(new
            {
                Type = type,
                Template = template
            });
        }

        /// <summary>
        /// Import Chart of Accounts
        /// </summary>
        [HttpPost("accounts")]
        public IActionResult ImportAccounts([FromBody] CsvImportRequest request)
        {
            var result = _importService.ImportChartOfAccountsCsv(request.CsvContent);
            return Ok(result);
        }

        /// <summary>
        /// Import Customers
        /// </summary>
        [HttpPost("customers")]
        public IActionResult ImportCustomers([FromBody] CsvImportRequest request)
        {
            var result = _importService.ImportCustomersCsv(request.CsvContent);
            return Ok(result);
        }

        /// <summary>
        /// Import Suppliers
        /// </summary>
        [HttpPost("suppliers")]
        public IActionResult ImportSuppliers([FromBody] CsvImportRequest request)
        {
            var result = _importService.ImportSuppliersCsv(request.CsvContent);
            return Ok(result);
        }

        /// <summary>
        /// Import Opening Balances
        /// </summary>
        [HttpPost("opening-balances")]
        public IActionResult ImportOpeningBalances([FromBody] CsvImportRequest request)
        {
            var result = _importService.ImportOpeningBalancesCsv(request.CsvContent);
            return Ok(result);
        }
    }

    public class CsvImportRequest
    {
        public string CsvContent { get; set; }
    }
}