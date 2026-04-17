namespace GL.Application.Services
{
    /// <summary>
    /// Bank Reconciliation Service
    /// Đối chiếu ngân hàng - So khớp giữa sổ Quỹ và sao kê ngân hàng
    /// </summary>
    public class BankReconciliationService
    {
        public class ReconciliationResult
        {
            public int TotalLines { get; set; }
            public int Matched { get; set; }
            public int UnmatchedBank { get; set; }
            public int UnmatchedGL { get; set; }
            public decimal BankBalance { get; set; }
            public decimal GLBalance { get; set; }
            public decimal Difference => BankBalance - GLBalance;
            public List<ReconciliationItem> Items { get; set; } = new();
        }

        public class ReconciliationItem
        {
            public string Reference { get; set; }
            public DateTime Date { get; set; }
            public decimal Amount { get; set; }
            public string Description { get; set; }
            public string MatchStatus { get; set; } // "Matched", "Bank only", "GL only"
            public string BankReference { get; set; }
            public string GLReference { get; set; }
        }

        /// <summary>
        /// Perform bank reconciliation
        /// </summary>
        public ReconciliationResult Reconcile(
            List<BankTransaction> bankTransactions,
            List<GLTransaction> glTransactions,
            DateTime startDate,
            DateTime endDate)
        {
            var result = new ReconciliationResult
            {
                TotalLines = bankTransactions.Count + glTransactions.Count
            };

            // Calculate balances
            result.BankBalance = bankTransactions
                .Where(t => t.Date >= startDate && t.Date <= endDate)
                .Sum(t => t.Amount);
            
            result.GLBalance = glTransactions
                .Where(t => t.Date >= startDate && t.Date <= endDate)
                .Sum(t => t.Amount);

            // Match transactions by reference and amount
            var bankMatched = new HashSet<string>();
            var glMatched = new HashSet<string>();

            foreach (var bankTx in bankTransactions)
            {
                var match = glTransactions.FirstOrDefault(gl =>
                    gl.Amount == bankTx.Amount &&
                    gl.Date == bankTx.Date &&
                    !glMatched.Contains(gl.Reference));

                if (match != null)
                {
                    result.Items.Add(new ReconciliationItem
                    {
                        Reference = bankTx.Reference,
                        Date = bankTx.Date,
                        Amount = bankTx.Amount,
                        Description = bankTx.Description,
                        MatchStatus = "Matched",
                        BankReference = bankTx.Reference,
                        GLReference = match.Reference
                    });
                    bankMatched.Add(bankTx.Reference);
                    glMatched.Add(match.Reference);
                    result.Matched++;
                }
                else
                {
                    result.Items.Add(new ReconciliationItem
                    {
                        Reference = bankTx.Reference,
                        Date = bankTx.Date,
                        Amount = bankTx.Amount,
                        Description = bankTx.Description,
                        MatchStatus = "Bank only"
                    });
                    result.UnmatchedBank++;
                }
            }

            // Unmatched GL transactions
            foreach (var glTx in glTransactions.Where(t => !glMatched.Contains(t.Reference)))
            {
                result.Items.Add(new ReconciliationItem
                {
                    Reference = glTx.Reference,
                    Date = glTx.Date,
                    Amount = glTx.Amount,
                    Description = glTx.Description,
                    MatchStatus = "GL only",
                    GLReference = glTx.Reference
                });
                result.UnmatchedGL++;
            }

            return result;
        }

        /// <summary>
        /// Auto-match by amount and date tolerance
        /// </summary>
        public ReconciliationResult AutoMatchWithTolerance(
            List<BankTransaction> bankTransactions,
            List<GLTransaction> glTransactions,
            int dateToleranceDays = 3)
        {
            var result = new ReconciliationResult();
            var bankMatched = new HashSet<string>();
            var glMatched = new HashSet<string>();

            // Sort by amount first
            var bankByAmount = bankTransactions.GroupBy(t => t.Amount).ToDictionary(g => g.Key, g => g.ToList());
            var glByAmount = glTransactions.GroupBy(t => t.Amount).ToDictionary(g => g.Key, g => g.ToList());

            foreach (var bankGroup in bankByAmount)
            {
                if (glByAmount.TryGetValue(bankGroup.Key, out var glGroup))
                {
                    foreach (var bankTx in bankGroup.Value)
                    {
                        var match = glGroup.FirstOrDefault(gl =>
                            Math.Abs((gl.Date - bankTx.Date).Days) <= dateToleranceDays &&
                            !glMatched.Contains(gl.Reference));

                        if (match != null)
                        {
                            result.Items.Add(new ReconciliationItem
                            {
                                Reference = bankTx.Reference,
                                Date = bankTx.Date,
                                Amount = bankTx.Amount,
                                Description = bankTx.Description,
                                MatchStatus = "Matched",
                                BankReference = bankTx.Reference,
                                GLReference = match.Reference
                            });
                            bankMatched.Add(bankTx.Reference);
                            glMatched.Add(match.Reference);
                            result.Matched++;
                            result.BankBalance += bankTx.Amount;
                            result.GLBalance += match.Amount;
                        }
                    }
                }
            }

            // Add unmatched
            foreach (var bankTx in bankTransactions.Where(t => !bankMatched.Contains(t.Reference)))
            {
                result.Items.Add(new ReconciliationItem
                {
                    Reference = bankTx.Reference,
                    Date = bankTx.Date,
                    Amount = bankTx.Amount,
                    Description = bankTx.Description,
                    MatchStatus = "Bank only"
                });
                result.UnmatchedBank++;
                result.BankBalance += bankTx.Amount;
            }

            foreach (var glTx in glTransactions.Where(t => !glMatched.Contains(t.Reference)))
            {
                result.Items.Add(new ReconciliationItem
                {
                    Reference = glTx.Reference,
                    Date = glTx.Date,
                    Amount = glTx.Amount,
                    Description = glTx.Description,
                    MatchStatus = "GL only",
                    GLReference = glTx.Reference
                });
                result.UnmatchedGL++;
                result.GLBalance += glTx.Amount;
            }

            result.TotalLines = result.Items.Count;
            return result;
        }

        public class BankTransaction
        {
            public string Reference { get; set; }
            public DateTime Date { get; set; }
            public decimal Amount { get; set; }
            public string Description { get; set; }
        }

        public class GLTransaction
        {
            public string Reference { get; set; }
            public DateTime Date { get; set; }
            public decimal Amount { get; set; }
            public string Description { get; set; }
        }
    }
}