using System;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Tài sản cố định theo TT99
    /// 211: TSCĐ hữu hình
    /// 213: TSCĐ vô hình
    /// 217: Công cụ, dụng cụ
    /// </summary>
    public class FixedAsset
    {
        public string Id { get; set; }
        public string AssetCode { get; set; }
        public string AssetName { get; set; }
        public string Description { get; set; }
        
        // Loại TSCĐ: 211, 213, 217
        public string AssetAccountCode { get; set; }
        public FixedAssetType AssetType { get; set; }
        
        // Nguyên giá
        public decimal OriginalCost { get; set; }
        
        // Khấu hao lũy kế
        public decimal AccumulatedDepreciation { get; set; }
        
        // Giá trị còn lại
        public decimal NetBookValue => OriginalCost - AccumulatedDepreciation;
        
        public DateTime PurchaseDate { get; set; }
        public DateTime? DeploymentDate { get; set; }
        
        // Thời gian sử dụng (năm)
        public int UsefulLifeYears { get; set; }
        
        // Tỷ lệ khấu hao
        public decimal DepreciationRate { get; set; }
        
        public DepreciationMethod DepreciationMethod { get; set; }
        
        // Bộ phận sử dụng
        public string DepartmentId { get; set; }
        public string DepartmentName { get; set; }
        
        public FixedAssetStatus Status { get; set; }
        public DateTime CreatedAt { get; set; }
        public string CreatedBy { get; set; }
    }

    public enum FixedAssetType
    {
        Tangible = 211,     // TSCĐ hữu hình
        Intangible = 213,    // TSCĐ vô hình  
        Tool = 217           // Công cụ dụng cụ
    }

    public enum DepreciationMethod
    {
        StraightLine,           // Khấu hao đường thẳng
        DoubleDecliningBalance,   // Khấu hao theo số dư giảm dần
        UnitsOfProduction      // Khấu hao theo công suất
    }

    public enum FixedAssetStatus
    {
        Draft,
        Active,
        FullyDepreciated,
        Disposed,
        Transferred
    }

    /// <summary>
    /// Input để thêm TSCĐ mới
    /// </summary>
    public class AddAssetInput
    {
        public string AssetCode { get; set; }
        public string AssetName { get; set; }
        public string Description { get; set; }
        public FixedAssetType AssetType { get; set; }
        public decimal OriginalCost { get; set; }
        public DateTime PurchaseDate { get; set; }
        public DateTime? DeploymentDate { get; set; }
        public int UsefulLifeYears { get; set; }
        public DepreciationMethod DepreciationMethod { get; set; }
        public string DepartmentId { get; set; }
        public string DepartmentName { get; set; }
        public string CreatedBy { get; set; }
    }
}