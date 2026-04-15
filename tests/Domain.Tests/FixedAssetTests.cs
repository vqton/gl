using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;
using GL.Application.Services;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Unit tests cho FixedAssetService (A01-A06)
    /// </summary>
    public class FixedAssetTests
    {
        private readonly InMemoryFixedAssetRepository _repo;
        private readonly FixedAssetService _service;

        public FixedAssetTests()
        {
            _repo = new InMemoryFixedAssetRepository();
            _service = new FixedAssetService(_repo);
        }

        [Fact]
        public void A01_AddAsset_ValidAsset_ReturnsSuccess()
        {
            var result = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính Dell",
                AssetType = FixedAssetType.Tangible,
                OriginalCost = 50_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine,
                DepartmentId = "KD"
            });

            Assert.True(result.Success);
            Assert.NotNull(result.Asset);
            Assert.Equal("TSC001", result.Asset.AssetCode);
        }

        [Fact]
        public void A01_AddAsset_DuplicateCode_ReturnsFalse()
        {
            _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính",
                OriginalCost = 50_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine
            });

            var result = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính 2",
                OriginalCost = 30_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine
            });

            Assert.False(result.Success);
        }

        [Fact]
        public void A02_CalculateDepreciation_StraightLine_ReturnsCorrect()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính",
                AssetType = FixedAssetType.Tangible,
                OriginalCost = 60_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine
            }).Asset;

            var monthly = _service.CalculateMonthlyDepreciation(asset.Id);

            Assert.Equal(1_000_000m, monthly); // 60tr / 5 năm / 12 tháng = 1tr
        }

        [Fact]
        public void A02_CalculateDepreciation_DoubleDeclining_ReturnsCorrect()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC002",
                AssetName = "Xe hơi",
                AssetType = FixedAssetType.Tangible,
                OriginalCost = 600_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.DoubleDecliningBalance
            }).Asset;

            var monthly = _service.CalculateMonthlyDepreciation(asset.Id);

            // Rate = 2/5 = 40%
            // Annual = 600tr * 40% = 240tr
            // Monthly = 240tr / 12 = 20tr
            Assert.Equal(20_000_000m, monthly);
        }

        [Fact]
        public void A02_RecordDepreciation_UpdatesAccumulated()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính",
                OriginalCost = 60_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine
            }).Asset;

            _service.RecordDepreciation(asset.Id, 2026, 1);
            _service.RecordDepreciation(asset.Id, 2026, 2);

            var updated = _service.GetById(asset.Id);
            Assert.Equal(2_000_000m, updated.AccumulatedDepreciation);
        }

        [Fact]
        public void A03_TransferAsset_ChangesDepartment()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính",
                OriginalCost = 50_000_000m,
                PurchaseDate = new DateTime(2026, 1, 1),
                UsefulLifeYears = 5,
                DepreciationMethod = DepreciationMethod.StraightLine,
                DepartmentId = "KD"
            }).Asset;

            var result = _service.TransferAsset(asset.Id, "KT");

            Assert.True(result.Success);
            var updated = _service.GetById(asset.Id);
            Assert.Equal("KT", updated.DepartmentId);
        }

        [Fact]
        public void A04_DisposeAsset_ReturnsCorrectJournalEntry()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Máy tính",
                OriginalCost = 60_000_000m,
                PurchaseDate = new DateTime(2024, 1, 1),
                UsefulLifeYears = 2,
                DepreciationMethod = DepreciationMethod.StraightLine
            }).Asset;

            // Record 24 months depreciation = 60tr
            for (int m = 1; m <= 12; m++)
                _service.RecordDepreciation(asset.Id, 2024, m);
            for (int m = 1; m <= 12; m++)
                _service.RecordDepreciation(asset.Id, 2025, m);

            var journal = _service.DisposeAsset(asset.Id, 5_000_000m);

            Assert.True(journal.Success);
            Assert.NotNull(journal.Entry);
            // Has 3 lines: 811, 214, 211
            Assert.True(journal.Entry.Lines.Count >= 2);
        }

        [Fact]
        public void A05_Revaluation_UpdatesAssetValue()
        {
            var asset = _service.AddAsset(new AddAssetInput
            {
                AssetCode = "TSC001",
                AssetName = "Nhà xưởng",
                OriginalCost = 1_000_000_000m,
                PurchaseDate = new DateTime(2020, 1, 1),
                UsefulLifeYears = 10,
                DepreciationMethod = DepreciationMethod.StraightLine
            }).Asset;

            var result = _service.RevaluateAsset(asset.Id, 1_500_000_000m);

            Assert.True(result.Success);
            var updated = _service.GetById(asset.Id);
            Assert.Equal(1_500_000_000m, updated.OriginalCost);
        }

        [Fact]
        public void GetAllAssets_ReturnsAll()
        {
            _service.AddAsset(new AddAssetInput { AssetCode = "A", AssetName = "A", OriginalCost = 10, PurchaseDate = DateTime.Now, UsefulLifeYears = 1, DepreciationMethod = DepreciationMethod.StraightLine });
            _service.AddAsset(new AddAssetInput { AssetCode = "B", AssetName = "B", OriginalCost = 20, PurchaseDate = DateTime.Now, UsefulLifeYears = 1, DepreciationMethod = DepreciationMethod.StraightLine });

            var assets = _service.GetAll();

            Assert.Equal(2, assets.Count());
        }
    }

    public class InMemoryFixedAssetRepository : IFixedAssetRepository
    {
        private readonly List<FixedAsset> _assets = new();

        public void Add(FixedAsset asset)
        {
            _assets.Add(asset);
        }

        public FixedAsset GetById(string id)
        {
            return _assets.FirstOrDefault(a => a.Id == id);
        }

        public FixedAsset GetByCode(string code)
        {
            return _assets.FirstOrDefault(a => a.AssetCode == code);
        }

        public void Update(FixedAsset asset)
        {
            var index = _assets.FindIndex(a => a.Id == asset.Id);
            if (index >= 0) _assets[index] = asset;
        }

        public IEnumerable<FixedAsset> GetAll()
        {
            return _assets;
        }

        public void Delete(string id)
        {
            _assets.RemoveAll(a => a.Id == id);
        }
    }
}