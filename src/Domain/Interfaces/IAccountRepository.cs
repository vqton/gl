using GL.Domain.Entities;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GL.Domain.Interfaces
{
    /// <summary>
    /// Định nghĩa hợp đồng cho repository truy cập dữ liệu tài khoản
    /// </summary>
    public interface IAccountRepository
    {
        /// <summary>
        /// Lấy tất cả tài khoản từ database
        /// </summary>
        Task<IEnumerable<Account>> GetAllAsync();

        /// <summary>
        /// Lấy tài khoản theo mã
        /// </summary>
        Task<Account> GetByCodeAsync(string code);

        /// <summary>
        /// Thêm tài khoản mới
        /// </summary>
        Task AddAsync(Account account);

        /// <summary>
        /// Cập nhật tài khoản tồn tại
        /// </summary>
        Task UpdateAsync(Account account);

        /// <summary>
        /// Xóa tài khoản
        /// </summary>
        Task DeleteAsync(string code);

        /// <summary>
        /// Kiểm tra tài khoản có tồn tại không
        /// </summary>
        Task<bool> ExistsAsync(string code);
    }
}