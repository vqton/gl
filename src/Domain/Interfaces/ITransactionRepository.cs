using GL.Domain.Entities;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GL.Domain.Interfaces
{
    /// <summary>
    /// Định nghĩa hợp đồng cho repository truy cập dữ liệu giao dịch
    /// </summary>
    public interface ITransactionRepository
    {
        /// <summary>
        /// Lấy tất cả giao dịch từ database
        /// </summary>
        Task<IEnumerable<Transaction>> GetAllAsync();

        /// <summary>
        /// Lấy giao dịch theo ID
        /// </summary>
        Task<Transaction> GetByIdAsync(string id);

        /// <summary>
        /// Thêm giao dịch mới
        /// </summary>
        Task AddAsync(Transaction transaction);

        /// <summary>
        /// Cập nhật giao dịch tồn tại
        /// </summary>
        Task UpdateAsync(Transaction transaction);

        /// <summary>
        /// Xóa giao dịch
        /// </summary>
        Task DeleteAsync(string id);
    }
}