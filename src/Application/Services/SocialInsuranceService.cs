using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý bảo hiểm xã hội - P0
    /// Theo Luật BHXH và các Thông tư hướng dẫn
    /// </summary>
    public class SocialInsuranceService
    {
        private readonly ISocialInsuranceRepository _repository;
        private readonly IPayrollLineRepository _payrollLineRepository;

        // Tỷ lệ BHXH
        private const decimal BHXH_Total = 0.175m;      // 17.5% tổng
        private const decimal BHXH_Employee = 0.035m;   // NLĐ: 3.5%
        private const decimal BHXH_Employer = 0.14m;      // DN: 14%
        
        // Tỷ lệ BHYT
        private const decimal BHYT_Total = 0.03m;      // 3% tổng
        private const decimal BHYT_Employee = 0.01m;    // NLĐ: 1%
        private const decimal BHYT_Employer = 0.02m;      // DN: 2%
        
        // Tỷ lệ BHTN
        private const decimal BHTN_Total = 0.01m;       // 1% tổng
        private const decimal BHTN_Employee = 0.005m;  // NLĐ: 0.5%
        private const decimal BHTN_Employer = 0.005m;  // DN: 0.5%

        // Mức lương tối đa đóng BH
        private const decimal MaxInsuranceSalary = 149_000_000m;

        public SocialInsuranceService(
            ISocialInsuranceRepository repository,
            IPayrollLineRepository payrollLineRepository)
        {
            _repository = repository;
            _payrollLineRepository = payrollLineRepository;
        }

        /// <summary>
        /// Tạo tờ khai BH hàng tháng
        /// </summary>
        public (bool Success, string Message, SocialInsuranceDeclaration Declaration) 
            CreateMonthlyDeclaration(int year, int month)
        {
            var existing = _repository.GetByPeriod(year, month);
            if (existing != null)
            {
                return (false, "Tờ khai đã tồn tại", null);
            }

            var declaration = new SocialInsuranceDeclaration
            {
                Id = Guid.NewGuid().ToString(),
                DeclarationId = $"BH{year}{month:D2}",
                Year = year,
                Month = month,
                Status = SocialInsuranceStatus.Nháp,
                CreatedAt = DateTime.Now
            };

            _repository.Add(declaration);
            return (true, "Tạo tờ khai thành công", declaration);
        }

        /// <summary>
        /// Tính BHXH, BHYT, BHTN (tổng cả hai bên)
        /// </summary>
        public (decimal BHXH, decimal BHYT, decimal BHTN) CalculateSocialInsurance(decimal salary)
        {
            decimal cappedSalary = Math.Min(salary, MaxInsuranceSalary);
            
            decimal bhxh = Math.Round(cappedSalary * BHXH_Total, 0);
            decimal bhyt = Math.Round(cappedSalary * BHYT_Total, 0);
            decimal bhtn = Math.Round(cappedSalary * BHTN_Total, 0);
            
            return (bhxh, bhyt, bhtn);
        }

        /// <summary>
        /// Tính phần DN đóng BH
        /// </summary>
        public (decimal BHXH, decimal BHYT, decimal BHTN) CalculateEmployerContribution(decimal salary)
        {
            decimal cappedSalary = Math.Min(salary, MaxInsuranceSalary);
            
            decimal bhxh = Math.Round(cappedSalary * BHXH_Employer, 0);
            decimal bhyt = Math.Round(cappedSalary * BHYT_Employer, 0);
            decimal bhtn = Math.Round(cappedSalary * BHTN_Employer, 0);
            
            return (bhxh, bhyt, bhtn);
        }

        /// <summary>
        /// Thêm nhân viên vào tờ khai (từ payroll line)
        /// </summary>
        public (bool Success, string Message) AddEmployeeToDeclaration(string declarationId, string employeeId, string employeeName, decimal salary)
        {
            var declaration = _repository.GetById(declarationId);
            if (declaration == null)
            {
                return (false, "Không tìm thấy tờ khai");
            }

            var record = new SocialInsuranceRecord
            {
                Id = Guid.NewGuid().ToString(),
                DeclarationId = declarationId,
                EmployeeId = employeeId,
                EmployeeName = employeeName,
                InsuranceSalary = Math.Min(salary, MaxInsuranceSalary)
            };

            // Tính BH
            record.BHXH_Employee = Math.Round(record.InsuranceSalary * BHXH_Employee, 0);
            record.BHXH_Employer = Math.Round(record.InsuranceSalary * BHXH_Employer, 0);
            record.BHYT_Employee = Math.Round(record.InsuranceSalary * BHYT_Employee, 0);
            record.BHYT_Employer = Math.Round(record.InsuranceSalary * BHYT_Employer, 0);
            record.BHTN_Employee = Math.Round(record.InsuranceSalary * BHTN_Employee, 0);
            record.BHTN_Employer = Math.Round(record.InsuranceSalary * BHTN_Employer, 0);

            declaration.Records.Add(record);
            _repository.Update(declaration);
            
            return (true, "Thêm nhân viên thành công");
        }

        /// <summary>
        /// Tạo báo cáo tờ khai
        /// </summary>
        public SocialInsuranceDeclaration GenerateDeclarationReport(string declarationId)
        {
            return _repository.GetById(declarationId);
        }

        /// <summary>
        /// Xuất tờ khai ra XML theo định dạng BHXH VN
        /// </summary>
        public string ExportToXML(string declarationId)
        {
            var declaration = _repository.GetById(declarationId);
            if (declaration == null)
            {
                return string.Empty;
            }

            var sb = new StringBuilder();
            sb.AppendLine("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            sb.AppendLine("<SoBaoHiem>");
            sb.AppendLine($"  <Nam>{declaration.Year}</Nam>");
            sb.AppendLine($"  <Thang>{declaration.Month}</Thang>");
            sb.AppendLine($"  <TongSoNLĐ>{declaration.TotalEmployees}</TongSoNLĐ>");
            sb.AppendLine($"  <TongQuỹ>{declaration.TotalBHXH + declaration.TotalBHYT + declaration.TotalBHTN}</TongQuỹ>");
            
            foreach (var record in declaration.Records)
            {
                sb.AppendLine("  <ChiTiet>");
                sb.AppendLine($"    <MaNV>{record.EmployeeId}</MaNV>");
                sb.AppendLine($"    <HoTen>{record.EmployeeName}</HoTen>");
                sb.AppendLine($"    <Luong>{record.InsuranceSalary}</Luong>");
                sb.AppendLine($"    <BHXH>{record.BHXH_Employee + record.BHXH_Employer}</BHXH>");
                sb.AppendLine($"    <BHYT>{record.BHYT_Employee + record.BHYT_Employer}</BHYT>");
                sb.AppendLine($"    <BHTN>{record.BHTN_Employee + record.BHTN_Employer}</BHTN>");
                sb.AppendLine("  </ChiTiet>");
            }
            
            sb.AppendLine("</SoBaoHiem>");
            
            return sb.ToString();
        }

        /// <summary>
        /// Duyệt tờ khai
        /// </summary>
        public (bool Success, string Message) ApproveDeclaration(string declarationId, string approvedBy)
        {
            var declaration = _repository.GetById(declarationId);
            if (declaration == null)
            {
                return (false, "Không tìm thấy tờ khai");
            }

            declaration.Status = SocialInsuranceStatus.ĐãDuyệt;
            _repository.Update(declaration);
            
            return (true, "Duyệt tờ khai thành công");
        }

        /// <summary>
        /// Nộp tờ khai
        /// </summary>
        public (bool Success, string Message) SubmitDeclaration(string declarationId, string submittedBy)
        {
            var declaration = _repository.GetById(declarationId);
            if (declaration == null)
            {
                return (false, "Không tìm thấy tờ khai");
            }

            declaration.Status = SocialInsuranceStatus.ĐãNộp;
            declaration.SubmittedAt = DateTime.Now;
            declaration.SubmittedBy = submittedBy;
            _repository.Update(declaration);
            
            return (true, "Nộp tờ khai thành công");
        }
    }
}