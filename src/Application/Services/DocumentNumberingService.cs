namespace GL.Application.Services
{
    /// <summary>
    /// Document Numbering Service
    /// </summary>
    public class DocumentNumberingService
    {
        public class NumberingRule
        {
            public string Id { get; set; }
            public string DocumentType { get; set; }
            public string Prefix { get; set; }
            public string DateFormat { get; set; }
            public int RunningLength { get; set; }
            public string Separator { get; set; }
        }

        private Dictionary<string, int> _counters = new();
        private List<NumberingRule> _rules = new();

        public DocumentNumberingService()
        {
            InitializeDefaultRules();
        }

        private void InitializeDefaultRules()
        {
            _rules.Add(new NumberingRule
            {
                Id = "JE",
                DocumentType = "JournalEntry",
                Prefix = "JE",
                DateFormat = "YYMM",
                RunningLength = 4,
                Separator = "-"
            });
        }

        public string GenerateNumber(string documentType, int year, int month)
        {
            var rule = _rules.FirstOrDefault(r => r.DocumentType == documentType);
            if (rule == null)
            {
                return GenerateDefault(documentType, year, month);
            }

            var key = $"{documentType}-{year}-{month:D2}";
            if (!_counters.ContainsKey(key))
            {
                _counters[key] = 0;
            }
            _counters[key]++;

            var running = _counters[key].ToString().PadLeft(rule.RunningLength, '0');
            var dateStr = FormatDate(rule.DateFormat, year, month);

            return $"{rule.Prefix}{rule.Separator}{dateStr}{rule.Separator}{running}";
        }

        private string GenerateDefault(string documentType, int year, int month)
        {
            var key = $"{documentType}-{year}-{month:D2}";
            if (!_counters.ContainsKey(key))
            {
                _counters[key] = 0;
            }
            _counters[key]++;

            return $"{documentType.ToUpper()}-{year}{month:D2}-{_counters[key]:D4}";
        }

        private string FormatDate(string format, int year, int month)
        {
            var result = format;
            result = result.Replace("YYYY", year.ToString());
            result = result.Replace("YY", year.ToString()[2..]);
            result = result.Replace("MM", month.ToString("D2"));
            return result;
        }

        public bool ValidateNumber(string documentNumber)
        {
            return !string.IsNullOrWhiteSpace(documentNumber) &&
                   documentNumber.Length >= 6 &&
                   documentNumber.Any(c => c == '-');
        }
    }
}