using GL.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace GL.Application.Services
{
    /// <summary>
    /// Service xử lý người dùng và xác thực
    /// Phase 4 - User & Role Management
    /// </summary>
    public class UserService
    {
        private readonly List<User> _users = new();
        private readonly List<Role> _roles = new();
        private readonly List<UserRole> _userRoles = new();

        public UserService()
        {
            InitializeDefaultRoles();
        }

        private void InitializeDefaultRoles()
        {
            _roles.Add(new Role
            {
                Id = "ADMIN",
                Name = "ADMIN",
                Description = "Quản trị viên",
                Permissions = new string[] { "FULL_ACCESS" }
            });

            _roles.Add(new Role
            {
                Id = "ACCOUNTANT",
                Name = "ACCOUNTANT",
                Description = "Kế toán viên",
                Permissions = new string[] { "TRANSACTION_CREATE", "TRANSACTION_VIEW", "TRANSACTION_EDIT", "REPORT_VIEW" }
            });

            _roles.Add(new Role
            {
                Id = "MANAGER",
                Name = "MANAGER",
                Description = "Quản lý",
                Permissions = new string[] { "TRANSACTION_CREATE", "TRANSACTION_VIEW", "TRANSACTION_APPROVE", "REPORT_VIEW", "REPORT_EXPORT" }
            });

            _roles.Add(new Role
            {
                Id = "VIEWER",
                Name = "VIEWER",
                Description = "Người xem",
                Permissions = new string[] { "TRANSACTION_VIEW", "REPORT_VIEW" }
            });
        }

        /// <summary>
        /// Tạo người dùng mới
        /// </summary>
        public User CreateUser(string username, string email, string fullName, string[] roles = null)
        {
            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                Username = username,
                Email = email,
                FullName = fullName,
                IsActive = true,
                CreatedAt = DateTime.Now,
                Roles = roles ?? new string[] { "VIEWER" }
            };

            _users.Add(user);
            return user;
        }

        /// <summary>
        /// Tạo người dùng với mật khẩu
        /// </summary>
        public User CreateUserWithPassword(string username, string email, string fullName, string password, string[] roles = null)
        {
            var user = CreateUser(username, email, fullName, roles);
            user.PasswordHash = HashPassword(password);
            return user;
        }

        /// <summary>
        /// Xác thực người dùng
        /// </summary>
        public User Authenticate(string username, string password)
        {
            var user = _users.FirstOrDefault(u => 
                u.Username == username && 
                u.IsActive);

            if (user == null)
                return null;

            if (VerifyPassword(password, user.PasswordHash))
            {
                user.LastLoginAt = DateTime.Now;
                return user;
            }

            return null;
        }

        /// <summary>
        /// Kiểm tra quyền truy cập
        /// </summary>
        public bool HasPermission(string userId, string permission)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            if (user == null || !user.IsActive)
                return false;

            foreach (var roleId in user.Roles ?? Array.Empty<string>())
            {
                var role = _roles.FirstOrDefault(r => r.Id == roleId);
                if (role?.HasPermission(permission) == true)
                    return true;
            }

            return false;
        }

        /// <summary>
        /// Gán vai trò cho người dùng
        /// </summary>
        public void AssignRole(string userId, string roleId)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            var role = _roles.FirstOrDefault(r => r.Id == roleId);

            if (user == null || role == null)
                return;

            if (!user.Roles.Contains(roleId))
            {
                user.Roles = user.Roles.Append(roleId).ToArray();
            }

            _userRoles.Add(new UserRole
            {
                UserId = userId,
                RoleId = roleId,
                AssignedAt = DateTime.Now
            });
        }

        /// <summary>
        /// Gỡ vai trò khỏi người dùng
        /// </summary>
        public void RemoveRole(string userId, string roleId)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            if (user == null)
                return;

            user.Roles = user.Roles?.Where(r => r != roleId).ToArray() ?? Array.Empty<string>();
            _userRoles.RemoveAll(ur => ur.UserId == userId && ur.RoleId == roleId);
        }

        /// <summary>
        /// Lấy danh sách người dùng
        /// </summary>
        public List<User> GetAllUsers() => _users.ToList();

        /// <summary>
        /// Lấy người dùng theo ID
        /// </summary>
        public User GetUserById(string id) => _users.FirstOrDefault(u => u.Id == id);

        /// <summary>
        /// Lấy danh sách vai trò
        /// </summary>
        public List<Role> GetAllRoles() => _roles.ToList();

        /// <summary>
        /// Vô hiệu hóa người dùng
        /// </summary>
        public bool DeactivateUser(string userId)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            if (user == null)
                return false;

            user.IsActive = false;
            return true;
        }

        /// <summary>
        /// Kích hoạt người dùng
        /// </summary>
        public bool ActivateUser(string userId)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            if (user == null)
                return false;

            user.IsActive = true;
            return true;
        }

        /// <summary>
        /// Đổi mật khẩu
        /// </summary>
        public bool ChangePassword(string userId, string oldPassword, string newPassword)
        {
            var user = _users.FirstOrDefault(u => u.Id == userId);
            if (user == null)
                return false;

            if (!VerifyPassword(oldPassword, user.PasswordHash))
                return false;

            user.PasswordHash = HashPassword(newPassword);
            return true;
        }

        private static string HashPassword(string password)
        {
            using var sha256 = SHA256.Create();
            var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            return Convert.ToBase64String(bytes);
        }

        private static bool VerifyPassword(string password, string hash)
        {
            return HashPassword(password) == hash;
        }
    }
}