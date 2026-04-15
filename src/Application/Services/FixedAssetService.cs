using System;
using System.Linq;
using GL.Domain.Entities;
using GL.Domain.Interfaces;

namespace GL.Application.Services
{
    /// <summary>
    /// Service quản lý TSCĐ - A01-A06
    /// Theo Thông tư 99/2025/TT-BTC
    /// </summary>
    public class FixedAssetService
    {
        private readonly IFixedAssetRepository _repository;

        public FixedAssetService(IFixedAssetRepository repository)
        {
            _repository = repository;
        }

        /// <summary>
        /// A01: Thêm TSCĐ mới
        /// </summary>
        public (bool Success, string Message, FixedAsset Asset) AddAsset(AddAssetInput input)
        {
            if (string.IsNullOrWhiteSpace(input.AssetCode))
            {
                return (false, "Mã TSCĐ không được để trống", null);
            }

            var existing = _repository.GetByCode(input.AssetCode);
            if (existing != null)
            {
                return (false, $"Mã TSCĐ {input.AssetCode} đã tồn tại", null);
            }

            if (input.OriginalCost <= 0)
            {
                return (false, "Nguyên giá phải > 0", null);
            }

            if (input.UsefulLifeYears <= 0)
            {
                return (false, "Thời gian sử dụng phải > 0", null);
            }

            var asset = new FixedAsset
            {
                Id = Guid.NewGuid().ToString(),
                AssetCode = input.AssetCode,
                AssetName = input.AssetName,
                Description = input.Description,
                AssetAccountCode = input.AssetType == FixedAssetType.Tangible ? "211" : 
                               input.AssetType == FixedAssetType.Intangible ? "213" : "217",
                AssetType = input.AssetType,
                OriginalCost = input.OriginalCost,
                AccumulatedDepreciation = 0,
                PurchaseDate = input.PurchaseDate,
                DeploymentDate = input.DeploymentDate ?? input.PurchaseDate,
                UsefulLifeYears = input.UsefulLifeYears,
                DepreciationRate = input.DepreciationMethod == DepreciationMethod.StraightLine 
                    ? 1.0m / input.UsefulLifeYears 
                    : 2.0m / input.UsefulLifeYears,
                DepreciationMethod = input.DepreciationMethod,
                DepartmentId = input.DepartmentId,
                DepartmentName = input.DepartmentName,
                Status = FixedAssetStatus.Active,
                CreatedAt = DateTime.Now,
                CreatedBy = input.CreatedBy ?? "System"
            };

            _repository.Add(asset);
            return (true, "Thêm TSCĐ thành công", asset);
        }

        /// <summary>
        /// A02: Tính khấu hao hàng tháng
        /// </summary>
        public decimal CalculateMonthlyDepreciation(string assetId)
        {
            var asset = _repository.GetById(assetId);
            if (asset == null) return 0;

            decimal annualDepreciation;
            
            switch (asset.DepreciationMethod)
            {
                case DepreciationMethod.StraightLine:
                    annualDepreciation = asset.OriginalCost * asset.DepreciationRate;
                    break;
                    
                case DepreciationMethod.DoubleDecliningBalance:
                    // Số dư giảm dần: Rate = 2/năm
                    // Tháng = (Giá trị còn lại * Rate) / 12
                    annualDepreciation = asset.NetBookValue * asset.DepreciationRate;
                    break;
                    
                case DepreciationMethod.UnitsOfProduction:
                    // Tính theo công suất - default = straight line
                    annualDepreciation = asset.OriginalCost * asset.DepreciationRate;
                    break;
                    
                default:
                    annualDepreciation = asset.OriginalCost * asset.DepreciationRate;
                    break;
            }
            
            return Math.Round(annualDepreciation / 12, 0);
        }

        /// <summary>
        /// A02: Ghi nhận khấu hao hàng tháng
        /// </summary>
        public (bool Success, string Message) RecordDepreciation(string assetId, int year, int month)
        {
            var asset = _repository.GetById(assetId);
            if (asset == null)
            {
                return (false, "Không tìm thấy TSCĐ");
            }

            if (asset.Status == FixedAssetStatus.FullyDepreciated)
            {
                return (false, "TSCĐ đã khấu hao hết");
            }

            var monthlyDepreciation = CalculateMonthlyDepreciation(assetId);
            
            // Check if this would fully depreciate
            if (asset.AccumulatedDepreciation + monthlyDepreciation >= asset.OriginalCost)
            {
                monthlyDepreciation = asset.OriginalCost - asset.AccumulatedDepreciation;
                asset.Status = FixedAssetStatus.FullyDepreciated;
            }

            asset.AccumulatedDepreciation += monthlyDepreciation;
            _repository.Update(asset);
            
            return (true, $"Ghi nhận khấu hao {monthlyDepreciation:N0} VND");
        }

        /// <summary>
        /// A03: Chuyển giao TSCĐ giữa các bộ phận
        /// </summary>
        public (bool Success, string Message) TransferAsset(string assetId, string newDepartmentId, string newDepartmentName = null)
        {
            var asset = _repository.GetById(assetId);
            if (asset == null)
            {
                return (false, "Không tìm thấy TSCĐ");
            }

            asset.DepartmentId = newDepartmentId;
            asset.DepartmentName = newDepartmentName;
            asset.Status = FixedAssetStatus.Transferred;
            _repository.Update(asset);
            
            return (true, "Chuyển giao TSCĐ thành công");
        }

        /// <summary>
        /// A04: Thanh lý TSCĐ
        /// </summary>
        public (bool Success, string Message, JournalEntry Entry) DisposeAsset(string assetId, decimal proceeds)
        {
            var asset = _repository.GetById(assetId);
            if (asset == null)
            {
                return (false, "Không tìm thấy TSCĐ", null);
            }

            // Tạo bút toán thanh lý
            // Nợ 811: Giá trị còn lại (nếu lỗ) hoặc Giá trị thanh lý (nếu lãi)
            // Nợ 214: Khấu hao lũy kế
            // Có 211: Nguyên giá
            var netBookValue = asset.NetBookValue;
            var journalEntry = new JournalEntry
            {
                Id = Guid.NewGuid().ToString(),
                EntryType = "A04",
                EntryDate = DateTime.Now,
                Description = $"Thanh lý TSCĐ {asset.AssetCode} - {asset.AssetName}",
                Lines = new System.Collections.Generic.List<JournalLine>
                {
                    new JournalLine { AccountCode = "811", Debit = netBookValue, Credit = 0 },
                    new JournalLine { AccountCode = "214", Debit = asset.AccumulatedDepreciation, Credit = 0 },
                    new JournalLine { AccountCode = "211", Debit = 0, Credit = asset.OriginalCost }
                }
            };

            asset.Status = FixedAssetStatus.Disposed;
            _repository.Update(asset);
            
            return (true, "Thanh lý TSCĐ thành công", journalEntry);
        }

        /// <summary>
        /// A05: Đánh giá lại TSCĐ (optional)
        /// </summary>
        public (bool Success, string Message) RevaluateAsset(string assetId, decimal newValue)
        {
            var asset = _repository.GetById(assetId);
            if (asset == null)
            {
                return (false, "Không tìm thấy TSCĐ");
            }

            if (newValue <= 0)
            {
                return (false, "Giá trị mới phải > 0");
            }

            asset.OriginalCost = newValue;
            _repository.Update(asset);
            
            return (true, "Đánh giá lại TSCĐ thành công");
        }

        /// <summary>
        /// Lấy TSCĐ theo ID
        /// </summary>
        public FixedAsset GetById(string id)
        {
            return _repository.GetById(id);
        }

        /// <summary>
        /// Lấy danh sách TSCĐ
        /// </summary>
        public System.Collections.Generic.IEnumerable<FixedAsset> GetAll()
        {
            return _repository.GetAll();
        }
    }

    /// <summary>
    /// Bút toán (Journal Entry)
    /// </summary>
    public class JournalEntry
    {
        public string Id { get; set; }
        public string EntryType { get; set; }  // S01, S02, G01, A04, etc.
        public DateTime EntryDate { get; set; }
        public string Description { get; set; }
        public System.Collections.Generic.List<JournalLine> Lines { get; set; } = new();
    }

    public class JournalLine
    {
        public string AccountCode { get; set; }
        public decimal Debit { get; set; }
        public decimal Credit { get; set; }
    }
}