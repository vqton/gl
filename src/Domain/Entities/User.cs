using System;
using System.Linq;

namespace GL.Domain.Entities
{
    /// <summary>
    /// Đại diện cho người dùng trong hệ thống
    /// </summary>
    public class User
    {
        /// <summary>
        /// Mã người dùng
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Tên đăng nhập
        /// </summary>
        public string Username { get; set; }

        /// <summary>
        /// Email
        /// </summary>
        public string Email { get; set; }

        /// <summary>
        /// Mật khẩu (đã mã hóa)
        /// </summary>
        public string PasswordHash { get; set; }

        /// <summary>
        /// Tên đầy đủ
        /// </summary>
        public string FullName { get; set; }

        /// <summary>
        /// Có đang hoạt động không
        /// </summary>
        public bool IsActive { get; set; }

        /// <summary>
        /// Ngày tạo
        /// </summary>
        public DateTime CreatedAt { get; set; }

        /// <summary>
        /// Lần đăng nhập cuối
        /// </summary>
        public DateTime? LastLoginAt { get; set; }

        /// <summary>
        /// Danh sách vai trò
        /// </summary>
        public string[] Roles { get; set; } = Array.Empty<string>();

        /// <summary>
        /// Kiểm tra tính hợp lệ của người dùng
        /// </summary>
        /// <returns>True nếu hợp lệ</returns>
        public bool IsValid()
        {
            return !string.IsNullOrEmpty(Id) &&
                   !string.IsNullOrEmpty(Username) &&
                   !string.IsNullOrEmpty(Email);
        }
    }

    /// <summary>
    /// Đại diện cho vai trò trong hệ thống
    /// </summary>
    public class Role
    {
        /// <summary>
        /// Mã vai trò
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Tên vai trò
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Mô tả
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Danh sách quyền
        /// </summary>
        public string[] Permissions { get; set; } = Array.Empty<string>();

        /// <summary>
        /// Kiểm tra xem vai trò có quyền cụ thể không
        /// </summary>
        /// <param name="permission">Tên quyền</param>
        /// <returns>True nếu có quyền</returns>
        public bool HasPermission(string permission)
        {
            return Permissions?.Contains(permission) ?? false;
        }
    }

    /// <summary>
    /// Đại diện cho liên kết người dùng - vai trò
    /// </summary>
    public class UserRole
    {
        /// <summary>
        /// Mã người dùng
        /// </summary>
        public string UserId { get; set; }

        /// <summary>
        /// Mã vai trò
        /// </summary>
        public string RoleId { get; set; }

        /// <summary>
        /// Ngày gán
        /// </summary>
        public DateTime AssignedAt { get; set; }
    }
}
