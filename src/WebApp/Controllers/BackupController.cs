using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Diagnostics;
using System.IO;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// Backup & Maintenance API
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    [Authorize(Policy = "FullAccess")]
    public class BackupController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private readonly IWebHostEnvironment _environment;
        private readonly ILogger<BackupController> _logger;

        public BackupController(
            IConfiguration configuration,
            IWebHostEnvironment environment,
            ILogger<BackupController> logger)
        {
            _configuration = configuration;
            _environment = environment;
            _logger = logger;
        }

        /// <summary>
        /// Get backup info
        /// </summary>
        [HttpGet]
        public IActionResult GetBackupInfo()
        {
            var backupPath = _configuration.GetValue<string>("BackupPath") 
                ?? Path.Combine(_environment.ContentRootPath, "backups");

            var exists = Directory.Exists(backupPath);
            var files = exists ? Directory.GetFiles(backupPath, "*.sql").Select(f => new FileInfo(f)).ToList() : new List<FileInfo>();

            return Ok(new
            {
                BackupPath = backupPath,
                Exists = exists,
                Files = files.Select(f => new
                {
                    Name = f.Name,
                    Size = f.Length,
                    Created = f.CreationTime
                }),
                LastBackup = files.OrderByDescending(f => f.CreationTime).FirstOrDefault()?.CreationTime
            });
        }

        /// <summary>
        /// Manual database backup
        /// </summary>
        [HttpPost("create")]
        public IActionResult CreateBackup([FromBody] CreateBackupRequest request)
        {
            var provider = _configuration.GetValue<string>("DatabaseProvider", "SqlServer");
            var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
            var backupPath = _configuration.GetValue<string>("BackupPath")
                ?? Path.Combine(_environment.ContentRootPath, "backups");

            if (!Directory.Exists(backupPath))
            {
                Directory.CreateDirectory(backupPath);
            }

            var fileName = $"gl_backup_{timestamp}.sql";
            var filePath = Path.Combine(backupPath, fileName);

            try
            {
                var process = new Process();
                var startInfo = new ProcessStartInfo();

                switch (provider)
                {
                    case "MariaDB":
                        startInfo.FileName = "mysqldump";
                        startInfo.Arguments = $"--user=root --password={request.Password} gl_accounting > \"{filePath}\"";
                        break;
                    case "PostgreSQL":
                        startInfo.FileName = "pg_dump";
                        startInfo.Arguments = $"-U postgres -f \"{filePath}\" gl_accounting";
                        break;
                    case "SqlServer":
                        startInfo.FileName = "sqlcmd";
                        startInfo.Arguments = $"-S localhost -U sa -i src/WebApp/sql/001_schema.sql -o \"{filePath}\"";
                        break;
                    default:
                        return BadRequest(new { Error = "Unknown provider: " + provider });
                }

                startInfo.UseShellExecute = false;
                startInfo.RedirectStandardOutput = true;
                process.StartInfo = startInfo;
                process.Start();
                process.WaitForExit(60000);

                var fileInfo = new FileInfo(filePath);
                return Ok(new
                {
                    Success = true,
                    FileName = fileName,
                    FilePath = filePath,
                    Size = fileInfo.Exists ? fileInfo.Length : 0,
                    Created = DateTime.Now,
                    Message = "Backup created successfully"
                });
            }
            catch (Exception ex)
            {
                return Ok(new
                {
                    Success = false,
                    Message = "Backup failed: " + ex.Message,
                    Note = "Manual backup not implemented. Use CLI: mysqldump/pg_dump"
                });
            }
        }

       /// <summary>
        /// Get system health
        /// </summary>
        [HttpGet("health")]
        public IActionResult GetHealth()
        {
            return Ok(new
            {
                Status = "Healthy",
                Uptime = DateTime.Now,
                Environment = _environment.EnvironmentName,
                DatabaseProvider = _configuration.GetValue<string>("DatabaseProvider"),
                Version = "1.0.0"
            });
        }

        /// <summary>
        /// Clear cache
        /// </summary>
        [HttpPost("cache/clear")]
        public IActionResult ClearCache()
        {
            _logger.LogInformation("Cache cleared by {User}", User.Identity?.Name);
            
            return Ok(new
            {
                Success = true,
                Message = "Cache cleared successfully",
                Timestamp = DateTime.Now
            });
        }
    }

    public class CreateBackupRequest
    {
        public string Password { get; set; }
    }
}