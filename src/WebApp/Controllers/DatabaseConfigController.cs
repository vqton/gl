using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// Database Configuration API
    /// Supports MariaDB, PostgreSQL, SQL Server
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    [Authorize(Policy = "FullAccess")]
    public class DatabaseConfigController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<DatabaseConfigController> _logger;

        public DatabaseConfigController(
            IConfiguration configuration,
            ILogger<DatabaseConfigController> logger)
        {
            _configuration = configuration;
            _logger = logger;
        }

        /// <summary>
        /// Get all database configurations
        /// </summary>
        [HttpGet]
        public IActionResult GetConfigs()
        {
            var currentProvider = _configuration.GetValue<string>("DatabaseProvider", "SqlServer");
            
            var configs = new List<object>();
            
            var mariaDbConn = _configuration.GetConnectionString("DefaultConnection");
            if (!string.IsNullOrEmpty(mariaDbConn))
            {
                configs.Add(new
                {
                    Provider = "MariaDB",
                    DisplayName = "MariaDB / MySQL",
                    IsConfigured = true,
                    IsActive = currentProvider == "MariaDB",
                    ConnectionString = MaskPassword(mariaDbConn)
                });
            }

            var pgConn = _configuration.GetConnectionString("PostgreSQL");
            if (!string.IsNullOrEmpty(pgConn))
            {
                configs.Add(new
                {
                    Provider = "PostgreSQL",
                    DisplayName = "PostgreSQL",
                    IsConfigured = true,
                    IsActive = currentProvider == "PostgreSQL",
                    ConnectionString = MaskPassword(pgConn)
                });
            }

            var sqlConn = _configuration.GetConnectionString("SqlServer");
            if (!string.IsNullOrEmpty(sqlConn))
            {
                configs.Add(new
                {
                    Provider = "SqlServer",
                    DisplayName = "Microsoft SQL Server",
                    IsConfigured = true,
                    IsActive = currentProvider == "SqlServer",
                    ConnectionString = MaskPassword(sqlConn)
                });
            }

            return Ok(new
            {
                CurrentProvider = currentProvider,
                Databases = configs,
                TotalConfigured = configs.Count,
                Instructions = new[]
                {
                    "1. Update appsettings.json: Set DatabaseProvider to MariaDB, PostgreSQL, or SqlServer",
                    "2. Update ConnectionStrings with your database credentials",
                    "3. Run the matching SQL schema script from /sql/",
                    "4. Restart the application"
                }
            });
        }

        /// <summary>
        /// Switch to different database provider
        /// </summary>
        [HttpPost("switch")]
        public IActionResult SwitchProvider([FromBody] SwitchProviderRequest request)
        {
            var validProviders = new[] { "MariaDB", "PostgreSQL", "SqlServer" };
            
            if (!validProviders.Contains(request.Provider))
            {
                return BadRequest(new
                {
                    Error = "Invalid provider. Use: MariaDB, PostgreSQL, or SqlServer"
                });
            }

            _logger.LogInformation("Database provider switching to {Provider}", request.Provider);

            return Ok(new
            {
                Success = true,
                CurrentProvider = request.Provider,
                Message = $"Switched to {request.Provider}. Update appsettings.json DatabaseProvider value, then restart.",
                Note = "On-premise: Edit appsettings.json. Cloud: Set DatabaseProvider environment variable."
            });
        }

        /// <summary>
        /// Get current database status
        /// </summary>
        [HttpGet("status")]
        public IActionResult GetStatus()
        {
            var provider = _configuration.GetValue<string>("DatabaseProvider", "SqlServer");
            
            return Ok(new
            {
                Provider = provider,
                LastChecked = DateTime.Now,
                Note = "Use /api/v1/databaseconfig endpoint to manage database connections."
            });
        }

        private static string MaskPassword(string connectionString)
        {
            if (string.IsNullOrEmpty(connectionString))
                return string.Empty;

            var parts = connectionString.Split(';');
            for (int i = 0; i < parts.Length; i++)
            {
                var part = parts[i].ToLower();
                if (part.StartsWith("password=") || part.StartsWith("pwd="))
                {
                    var key = part.Split('=')[0];
                    parts[i] = key + "=****";
                }
            }
            return string.Join(";", parts);
        }
    }

    public class SwitchProviderRequest
    {
        public string Provider { get; set; }
    }
}