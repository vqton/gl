namespace GL.Application.Services
{
    /// <summary>
    /// Approval Workflow Service
    /// Quy trình phê duyệt theo TT99/2025
    /// </summary>
    public class ApprovalWorkflowService
    {
        public class ApprovalRequest
        {
            public string Id { get; set; }
            public string EntityType { get; set; } // Transaction, Invoice, Payment, etc.
            public string EntityId { get; set; }
            public decimal Amount { get; set; }
            public string RequestedBy { get; set; }
            public DateTime RequestedAt { get; set; }
            public string Status { get; set; } // Pending, Approved, Rejected
            public List<ApprovalStep> Steps { get; set; } = new();
            public string CurrentStep { get; set; }
        }

        public class ApprovalStep
        {
            public int StepOrder { get; set; }
            public string ApproverRole { get; set; }
            public decimal MinAmount { get; set; }
            public decimal MaxAmount { get; set; }
            public string Status { get; set; } // Pending, Approved, Rejected
            public string ApproverId { get; set; }
            public DateTime? ApprovedAt { get; set; }
            public string Comment { get; set; }
        }

        public class ApprovalRule
        {
            public string Id { get; set; }
            public string EntityType { get; set; }
            public string Name { get; set; }
            public bool IsActive { get; set; } = true;
            public List<ApprovalStep> Steps { get; set; } = new();
        }

        private readonly List<ApprovalRule> _rules = new();

        public ApprovalWorkflowService()
        {
            InitializeDefaultRules();
        }

        /// <summary>
        /// Initialize default approval rules per TT99/2025
        /// </summary>
        private void InitializeDefaultRules()
        {
            // Sales Invoice - requires approval based on amount
            _rules.Add(new ApprovalRule
            {
                Id = "SALES_INVOICE",
                EntityType = "SalesInvoice",
                Name = "Duyệt hóa đơn bán hàng",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, ApproverRole = "BOOKKEEPER", MinAmount = 0, MaxAmount = 10000000 },
                    new() { StepOrder = 2, ApproverRole = "ACCOUNTANT", MinAmount = 10000001, MaxAmount = 50000000 },
                    new() { StepOrder = 3, ApproverRole = "FINANCE_MANAGER", MinAmount = 50000001, MaxAmount = decimal.MaxValue }
                }
            });

            // Purchase Invoice - requires approval
            _rules.Add(new ApprovalRule
            {
                Id = "PURCHASE_INVOICE",
                EntityType = "PurchaseInvoice",
                Name = "Duyệt hóa đơn mua hàng",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, ApproverRole = "BOOKKEEPER", MinAmount = 0, MaxAmount = 10000000 },
                    new() { StepOrder = 2, ApproverRole = "ACCOUNTANT", MinAmount = 10000001, MaxAmount = 50000000 },
                    new() { StepOrder = 3, ApproverRole = "FINANCE_MANAGER", MinAmount = 50000001, MaxAmount = decimal.MaxValue }
                }
            });

            // Payment - requires dual approval for large amounts
            _rules.Add(new ApprovalRule
            {
                Id = "PAYMENT",
                EntityType = "Payment",
                Name = "Duyệt chi tiền",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, ApproverRole = "ACCOUNTANT", MinAmount = 0, MaxAmount = 20000000 },
                    new() { StepOrder = 2, ApproverRole = "FINANCE_MANAGER", MinAmount = 20000001, MaxAmount = 100000000 },
                    new() { StepOrder = 3, ApproverRole = "ADMIN", MinAmount = 100000001, MaxAmount = decimal.MaxValue }
                }
            });

            // Journal Entry - requires approval
            _rules.Add(new ApprovalRule
            {
                Id = "JOURNAL_ENTRY",
                EntityType = "JournalEntry",
                Name = "Duyệt bút toán",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, ApproverRole = "BOOKKEEPER", MinAmount = 0, MaxAmount = 5000000 },
                    new() { StepOrder = 2, ApproverRole = "ACCOUNTANT", MinAmount = 5000001, MaxAmount = decimal.MaxValue }
                }
            });

            // Fixed Asset Disposal
            _rules.Add(new ApprovalRule
            {
                Id = "FA_DISPOSAL",
                EntityType = "FixedAsset",
                Name = "Duyệt thanh lý TSCĐ",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, ApproverRole = "ACCOUNTANT", MinAmount = 0, MaxAmount = 50000000 },
                    new() { StepOrder = 2, ApproverRole = "FINANCE_MANAGER", MinAmount = 50000001, MaxAmount = decimal.MaxValue }
                }
            });
        }

        /// <summary>
        /// Get applicable approval rule for entity type
        /// </summary>
        public ApprovalRule GetRule(string entityType)
        {
            return _rules.FirstOrDefault(r => r.EntityType == entityType && r.IsActive);
        }

        /// <summary>
        /// Get all rules
        /// </summary>
        public List<ApprovalRule> GetAllRules()
        {
            return _rules.ToList();
        }

        /// <summary>
        /// Create approval request based on amount and entity type
        /// </summary>
        public ApprovalRequest CreateRequest(string entityType, string entityId, decimal amount, string requestedBy)
        {
            var rule = GetRule(entityType);
            if (rule == null)
            {
                return null;
            }

            // Determine which step applies based on amount
            var applicableStep = rule.Steps.FirstOrDefault(s => 
                amount >= s.MinAmount && amount <= s.MaxAmount);

            if (applicableStep == null)
            {
                applicableStep = rule.Steps.Last();
            }

            var request = new ApprovalRequest
            {
                Id = Guid.NewGuid().ToString("N")[..8].ToUpper(),
                EntityType = entityType,
                EntityId = entityId,
                Amount = amount,
                RequestedBy = requestedBy,
                RequestedAt = DateTime.Now,
                Status = "Pending",
                CurrentStep = applicableStep.ApproverRole,
                Steps = rule.Steps.Where(s => s.StepOrder <= applicableStep.StepOrder).ToList()
            };

            // Mark applicable step as pending
            foreach (var step in request.Steps)
            {
                step.Status = step.StepOrder <= applicableStep.StepOrder ? "Pending" : "Skipped";
            }

            return request;
        }

        /// <summary>
        /// Approve a step
        /// </summary>
        public ApprovalRequest Approve(string requestId, string approverId, string comment)
        {
            // In real implementation, would fetch from database
            // For now, return success indicator
            return new ApprovalRequest
            {
                Id = requestId,
                Status = "Approved",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, Status = "Approved", ApproverId = approverId, ApprovedAt = DateTime.Now, Comment = comment }
                }
            };
        }

        /// <summary>
        /// Reject a request
        /// </summary>
        public ApprovalRequest Reject(string requestId, string approverId, string reason)
        {
            return new ApprovalRequest
            {
                Id = requestId,
                Status = "Rejected",
                Steps = new List<ApprovalStep>
                {
                    new() { StepOrder = 1, Status = "Rejected", ApproverId = approverId, ApprovedAt = DateTime.Now, Comment = reason }
                }
            };
        }

        /// <summary>
        /// Check if approval is required for amount
        /// </summary>
        public bool IsApprovalRequired(string entityType, decimal amount)
        {
            var rule = GetRule(entityType);
            if (rule == null) return false;

            return rule.Steps.Any(s => amount >= s.MinAmount && amount <= s.MaxAmount);
        }
    }
}