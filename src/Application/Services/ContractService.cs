using System;
using System.Collections.Generic;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý hợp đồng lao động
    /// </summary>
    public class ContractService
    {
        private readonly IContractRepository _contractRepository;

        public ContractService(IContractRepository contractRepository)
        {
            _contractRepository = contractRepository;
        }

        public LaborContract GetContract(string id)
        {
            return _contractRepository.GetById(id);
        }

        public IEnumerable<LaborContract> GetEmployeeContracts(string employeeId)
        {
            return _contractRepository.GetByEmployeeId(employeeId);
        }

        public IEnumerable<LaborContract> GetActiveContracts()
        {
            return _contractRepository.GetActiveContracts();
        }

        public (bool Success, string Message) CreateContract(LaborContract contract)
        {
            if (!contract.IsValid())
            {
                return (false, "Dữ liệu hợp đồng không hợp lệ");
            }

            if (_contractRepository.Exists(contract.ContractNumber))
            {
                return (false, $"Số hợp đồng {contract.ContractNumber} đã tồn tại");
            }

            contract.Id = Guid.NewGuid().ToString();
            contract.Status = ContractStatus.HoạtĐộng;
            contract.CreatedAt = DateTime.Now;
            
            _contractRepository.Add(contract);
            return (true, "Tạo hợp đồng thành công");
        }

        public (bool Success, string Message) UpdateContract(LaborContract contract)
        {
            if (!contract.IsValid())
            {
                return (false, "Dữ liệu hợp đồng không hợp lệ");
            }

            var existing = _contractRepository.GetById(contract.Id);
            if (existing == null)
            {
                return (false, "Không tìm thấy hợp đồng");
            }

            contract.UpdatedAt = DateTime.Now;
            _contractRepository.Update(contract);
            return (true, "Cập nhật hợp đồng thành công");
        }

        public (bool Success, string Message) TerminateContract(string contractId, DateTime terminationDate)
        {
            var contract = _contractRepository.GetById(contractId);
            if (contract == null)
            {
                return (false, "Không tìm thấy hợp đồng");
            }

            if (contract.Status == ContractStatus.ChấmDứt)
            {
                return (false, "Hợp đồng đã chấm dứt");
            }

            contract.Status = ContractStatus.ChấmDứt;
            contract.EndDate = terminationDate;
            contract.UpdatedAt = DateTime.Now;
            
            _contractRepository.Update(contract);
            return (true, "Chấm dứt hợp đồng thành công");
        }

        public (bool Success, string Message) DeleteContract(string contractId)
        {
            var contract = _contractRepository.GetById(contractId);
            if (contract == null)
            {
                return (false, "Không tìm thấy hợp đồng");
            }

            if (contract.Status == ContractStatus.HoạtĐộng)
            {
                return (false, "Không thể xóa hợp đồng đang hoạt động");
            }

            _contractRepository.Delete(contractId);
            return (true, "Xóa hợp đồng thành công");
        }

        public IEnumerable<LaborContract> GetExpiringContracts(int daysAhead = 30)
        {
            var activeContracts = _contractRepository.GetActiveContracts();
            var cutoffDate = DateTime.Now.AddDays(daysAhead);
            
            var result = new List<LaborContract>();
            foreach (var contract in activeContracts)
            {
                if (contract.EndDate.HasValue && 
                    contract.EndDate.Value <= cutoffDate && 
                    contract.EndDate.Value > DateTime.Now)
                {
                    result.Add(contract);
                }
            }
            return result;
        }
    }
}