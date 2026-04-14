using System;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Hợp đồng lao động - quản lý các loại hợp đồng lao động
    /// Theo Bộ luật Lao động 2019
    /// </summary>
    public class LaborContract
    {
        public string Id { get; set; }
        public string EmployeeId { get; set; }
        public string ContractNumber { get; set; }
        public ContractType ContractType { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public decimal BaseSalary { get; set; }
        public string Position { get; set; }
        public string Department { get; set; }
        public ContractStatus Status { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }

        public bool IsValid()
        {
            if (string.IsNullOrEmpty(EmployeeId) || string.IsNullOrEmpty(ContractNumber))
                return false;
            if (BaseSalary <= 0)
                return false;
            if (EndDate.HasValue && EndDate.Value <= StartDate)
                return false;
            return true;
        }

        public bool IsExpired()
        {
            return EndDate.HasValue && EndDate.Value < DateTime.Now;
        }

        public int GetDurationMonths()
        {
            if (!EndDate.HasValue)
                return -1; // Vô hạn
            return ((EndDate.Value.Year - StartDate.Year) * 12) + EndDate.Value.Month - StartDate.Month;
        }
    }

    public enum ContractType
    {
        ThửViệc = 1,
        CóThờiHạn = 2,
        KhôngThờiHạn = 3
    }

    public enum ContractStatus
    {
        HoạtĐộng = 1,
        HếtHạn = 2,
        ChấmDứt = 3
    }
}