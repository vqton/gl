using System;
using System.Collections.Generic;
using GL.Domain.Entities;

namespace GL.Domain.Interfaces
{
    public interface IContractRepository
    {
        LaborContract GetById(string id);
        IEnumerable<LaborContract> GetByEmployeeId(string employeeId);
        IEnumerable<LaborContract> GetByStatus(ContractStatus status);
        IEnumerable<LaborContract> GetActiveContracts();
        void Add(LaborContract contract);
        void Update(LaborContract contract);
        void Delete(string id);
        bool Exists(string contractNumber);
    }

    public interface IPayrollRepository
    {
        Payroll GetById(string id);
        Payroll GetByPeriod(int year, int month);
        IEnumerable<Payroll> GetAll();
        void Add(Payroll payroll);
        void Update(Payroll payroll);
        void Delete(string id);
    }

    public interface IPayrollLineRepository
    {
        PayrollLine GetById(string id);
        IEnumerable<PayrollLine> GetByPayrollId(string payrollId);
        void Add(PayrollLine line);
        void AddRange(IEnumerable<PayrollLine> lines);
        void Update(PayrollLine line);
        void Delete(string id);
    }
}