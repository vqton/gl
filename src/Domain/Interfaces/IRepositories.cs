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

    public interface ISocialInsuranceRepository
    {
        SocialInsuranceDeclaration GetById(string id);
        SocialInsuranceDeclaration GetByPeriod(int year, int month);
        IEnumerable<SocialInsuranceDeclaration> GetAll();
        void Add(SocialInsuranceDeclaration declaration);
        void Update(SocialInsuranceDeclaration declaration);
        void Delete(string id);
    }

    public interface ISalaryScaleRepository
    {
        SalaryScale GetById(string id);
        SalaryScale GetByCode(string code);
        IEnumerable<SalaryScale> GetAll();
        void Add(SalaryScale scale);
        void Update(SalaryScale scale);
        void Delete(string id);
    }

    public interface ISalesRepository
    {
        SalesTransaction GetById(string id);
        IEnumerable<SalesTransaction> GetByCustomer(string customerId);
        IEnumerable<SalesTransaction> GetAll();
        void Add(SalesTransaction sale);
        void Update(SalesTransaction sale);
        void Delete(string id);
    }

    public interface IFixedAssetRepository
    {
        FixedAsset GetById(string id);
        FixedAsset GetByCode(string code);
        IEnumerable<FixedAsset> GetAll();
        void Add(FixedAsset asset);
        void Update(FixedAsset asset);
        void Delete(string id);
    }

    public interface IAccountingPeriodRepository
    {
        AccountingPeriod GetByPeriod(int year, int month);
        AccountingPeriod GetByCode(string code);
        IEnumerable<AccountingPeriod> GetAll();
        void Add(AccountingPeriod period);
        void Update(AccountingPeriod period);
        void Delete(string id);
    }
}