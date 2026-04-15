using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho SalaryScaleService
    /// </summary>
    public class SalaryScaleTests
    {
        private readonly InMemorySalaryScaleRepository _repo;
        private readonly SalaryScaleService _service;

        public SalaryScaleTests()
        {
            _repo = new InMemorySalaryScaleRepository();
            _service = new SalaryScaleService(_repo);
        }

        [Fact]
        public void CreateSalaryScale_ValidScale_ReturnsSuccess()
        {
            var result = _service.CreateSalaryScale("A", "Thang A", 2026, 1);

            Assert.True(result.Success);
            Assert.NotNull(result.Scale);
            Assert.Equal("A", result.Scale.ScaleCode);
        }

        [Fact]
        public void CreateSalaryScale_DuplicateCode_ReturnsFalse()
        {
            _service.CreateSalaryScale("A", "Thang A", 2026, 1);
            var result = _service.CreateSalaryScale("A", "Thang A", 2026, 1);

            Assert.False(result.Success);
        }

        [Fact]
        public void AddGrade_ToScale_ReturnsSuccess()
        {
            var scale = _service.CreateSalaryScale("A", "Thang A", 2026, 1).Scale;

            var result = _service.AddGrade(scale.Id, 1, 1.0m, 5_000_000m);

            Assert.True(result.Success);
        }

        [Fact]
        public void CalculateSalary_ValidGrade_ReturnsCorrectSalary()
        {
            var scale = _service.CreateSalaryScale("A", "Thang A", 2026, 1).Scale;
            // Thêm bậc với lương cơ sở là 5tr, hệ số 1.0 và 1.5
            _service.AddGrade(scale.Id, 1, 1.0m, 5_000_000m);
            _service.AddGrade(scale.Id, 2, 1.5m, 5_000_000m); // Bậc 2 = 5tr * 1.5 = 7.5tr

            var salary = _service.CalculateSalary(scale.Id, 2);

            Assert.Equal(7_500_000m, salary);
        }

        [Fact]
        public void CalculateSalary_InvalidGrade_ThrowsException()
        {
            var scale = _service.CreateSalaryScale("A", "Thang A", 2026, 1).Scale;
            _service.AddGrade(scale.Id, 1, 1.0m, 5_000_000m);

            var salary = _service.CalculateSalary(scale.Id, 99);

            Assert.Equal(0, salary);
        }

        [Fact]
        public void GetGrade_Count_ReturnsCorrect()
        {
            var scale = _service.CreateSalaryScale("A", "Thang A", 2026, 1).Scale;
            _service.AddGrade(scale.Id, 1, 1.0m, 5_000_000m);
            _service.AddGrade(scale.Id, 2, 1.5m, 7_500_000m);
            _service.AddGrade(scale.Id, 3, 2.0m, 10_000_000m);

            var grades = _service.GetGrades(scale.Id);

            Assert.Equal(3, grades.Count());
        }
    }

    public class InMemorySalaryScaleRepository : ISalaryScaleRepository
    {
        private readonly List<SalaryScale> _scales = new();

        public void Add(SalaryScale scale)
        {
            _scales.Add(scale);
        }

        public SalaryScale GetById(string id)
        {
            return _scales.FirstOrDefault(s => s.Id == id);
        }

        public SalaryScale GetByCode(string code)
        {
            return _scales.FirstOrDefault(s => s.ScaleCode == code);
        }

        public void Update(SalaryScale scale)
        {
            var index = _scales.FindIndex(s => s.Id == scale.Id);
            if (index >= 0) _scales[index] = scale;
        }

        public IEnumerable<SalaryScale> GetAll()
        {
            return _scales;
        }

        public void Delete(string id)
        {
            _scales.RemoveAll(s => s.Id == id);
        }
    }
}