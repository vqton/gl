using System.Globalization;
using System.IO;

namespace GL.Application.Services
{
    /// <summary>
    /// Data Import Service - CSV import cho accounting data
    /// Supports: Chart of Accounts, Customers, Suppliers, Opening Balances
    /// </summary>
    public class DataImportService
    {
        public class ImportResult
        {
            public string EntityType { get; set; }
            public int Total { get; set; }
            public int Imported { get; set; }
            public int Failed { get; set; }
            public List<string> Errors { get; set; } = new();
            public bool Success => Failed == 0;
        }

        /// <summary>
        /// Import Chart of Accounts from CSV
        /// CSV Format: Code,Name,Level,Type,NormalBalance,ParentCode
        /// </summary>
        public ImportResult ImportChartOfAccountsCsv(string csvContent)
        {
            var result = new ImportResult { EntityType = "ChartOfAccounts" };
            var lines = csvContent.Split('\n', StringSplitOptions.RemoveEmptyEntries);

            for (int i = 1; i < lines.Length; i++) // Skip header
            {
                try
                {
                    var fields = ParseCsvLine(lines[i]);
                    if (fields.Length < 4) continue;

                    // Validation: Code must not be empty
                    if (string.IsNullOrWhiteSpace(fields[0]))
                    {
                        result.Errors.Add($"Line {i + 1}: Code is empty");
                        result.Failed++;
                        continue;
                    }

                    result.Imported++;
                }
                catch (Exception ex)
                {
                    result.Errors.Add($"Line {i + 1}: {ex.Message}");
                    result.Failed++;
                }
            }

            result.Total = lines.Length - 1;
            return result;
        }

        /// <summary>
        /// Import Customers from CSV
        /// CSV Format: Code,Name,TaxCode,Address,Phone,Email
        /// </summary>
        public ImportResult ImportCustomersCsv(string csvContent)
        {
            var result = new ImportResult { EntityType = "Customers" };
            var lines = csvContent.Split('\n', StringSplitOptions.RemoveEmptyEntries);

            for (int i = 1; i < lines.Length; i++)
            {
                try
                {
                    var fields = ParseCsvLine(lines[i]);
                    if (fields.Length < 2) continue;

                    // Validate required fields
                    if (string.IsNullOrWhiteSpace(fields[0]) || string.IsNullOrWhiteSpace(fields[1]))
                    {
                        result.Errors.Add($"Line {i + 1}: Code and Name are required");
                        result.Failed++;
                        continue;
                    }

                    // Validate tax code format (10 digits for Vietnam)
                    if (fields.Length > 2 && !string.IsNullOrWhiteSpace(fields[2]))
                    {
                        var taxCode = fields[2].Trim();
                        if (taxCode.Length != 10 || !taxCode.All(char.IsDigit))
                        {
                            result.Errors.Add($"Line {i + 1}: Tax code must be 10 digits");
                            result.Failed++;
                            continue;
                        }
                    }

                    result.Imported++;
                }
                catch (Exception ex)
                {
                    result.Errors.Add($"Line {i + 1}: {ex.Message}");
                    result.Failed++;
                }
            }

            result.Total = lines.Length - 1;
            return result;
        }

        /// <summary>
        /// Import Suppliers from CSV
        /// </summary>
        public ImportResult ImportSuppliersCsv(string csvContent)
        {
            var result = new ImportResult { EntityType = "Suppliers" };
            var lines = csvContent.Split('\n', StringSplitOptions.RemoveEmptyEntries);

            for (int i = 1; i < lines.Length; i++)
            {
                try
                {
                    var fields = ParseCsvLine(lines[i]);
                    if (fields.Length < 2) continue;

                    if (string.IsNullOrWhiteSpace(fields[0]) || string.IsNullOrWhiteSpace(fields[1]))
                    {
                        result.Errors.Add($"Line {i + 1}: Code and Name are required");
                        result.Failed++;
                        continue;
                    }

                    result.Imported++;
                }
                catch (Exception ex)
                {
                    result.Errors.Add($"Line {i + 1}: {ex.Message}");
                    result.Failed++;
                }
            }

            result.Total = lines.Length - 1;
            return result;
        }

        /// <summary>
        /// Import Opening Balances from CSV
        /// CSV Format: AccountCode,DebitAmount,CreditAmount
        /// </summary>
        public ImportResult ImportOpeningBalancesCsv(string csvContent)
        {
            var result = new ImportResult { EntityType = "OpeningBalances" };
            var lines = csvContent.Split('\n', StringSplitOptions.RemoveEmptyEntries);

            for (int i = 1; i < lines.Length; i++)
            {
                try
                {
                    var fields = ParseCsvLine(lines[i]);
                    if (fields.Length < 3) continue;

                    var accountCode = fields[0].Trim();
                    
                    // Parse amounts
                    if (!decimal.TryParse(fields[1].Trim(), out var debitAmount) && 
                        !decimal.TryParse(fields[2].Trim(), out var creditAmount))
                    {
                        result.Errors.Add($"Line {i + 1}: Invalid amount format");
                        result.Failed++;
                        continue;
                    }

                    result.Imported++;
                }
                catch (Exception ex)
                {
                    result.Errors.Add($"Line {i + 1}: {ex.Message}");
                    result.Failed++;
                }
            }

            result.Total = lines.Length - 1;
            return result;
        }

        private string[] ParseCsvLine(string line)
        {
            var fields = new List<string>();
            var current = "";
            var inQuotes = false;

            foreach (var c in line)
            {
                if (c == '"')
                {
                    inQuotes = !inQuotes;
                }
                else if (c == ',' && !inQuotes)
                {
                    fields.Add(current.Trim());
                    current = "";
                }
                else if (c != '\r')
                {
                    current += c;
                }
            }
            fields.Add(current.Trim());

            return fields.ToArray();
        }

        /// <summary>
        /// Generate sample CSV template
        /// </summary>
        public string GenerateTemplate(string templateType)
        {
            return templateType switch
            {
                "ChartOfAccounts" => "Code,Name,Level,Type,NormalBalance,ParentCode\n111,Tiền mặt,1,Asset,Debit,\n1111,Tiền mặt tại quỹ,2,Asset,Debit,111",
                "Customers" => "Code,Name,TaxCode,Address,Phone,Email\nKH001,Công ty ABC,0123456789,123 Đường Nguyễn Trãi,0123456789,abc@example.com",
                "Suppliers" => "Code,Name,TaxCode,Address,Phone,Email\nNCC001,Công ty XYZ,9876543210,456 Đường Lê Lợi,0987654321,xyz@example.com",
                "OpeningBalances" => "AccountCode,DebitAmount,CreditAmount\n1111,10000000,0\n3311,0,5000000",
                _ => ""
            };
        }
    }
}