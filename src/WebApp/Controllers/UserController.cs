using GL.Application.Services;
using GL.Domain.Entities;
using Microsoft.AspNetCore.Mvc;
using System.Linq;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// Controller xử lý người dùng và xác thực
    /// Phase 4 - User & Role Management
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    public class UserController : ControllerBase
    {
        private readonly UserService _userService;

        public UserController()
        {
            _userService = new UserService();
        }

        /// <summary>
        /// Đăng nhập
        /// </summary>
        [HttpPost("login")]
        public IActionResult Login([FromBody] LoginRequest request)
        {
            var user = _userService.Authenticate(request.Username, request.Password);
            if (user == null)
                return Unauthorized(new { error = "Invalid username or password" });

            return Ok(new
            {
                userId = user.Id,
                username = user.Username,
                email = user.Email,
                fullName = user.FullName,
                roles = user.Roles,
                lastLogin = user.LastLoginAt
            });
        }

        /// <summary>
        /// Đăng ký người dùng mới
        /// </summary>
        [HttpPost("register")]
        public IActionResult Register([FromBody] RegisterRequest request)
        {
            var existingUser = _userService.GetAllUsers()
                .FirstOrDefault(u => u.Username == request.Username || u.Email == request.Email);

            if (existingUser != null)
                return BadRequest(new { error = "Username or email already exists" });

            var user = _userService.CreateUserWithPassword(
                request.Username,
                request.Email,
                request.FullName,
                request.Password
            );

            return Created($"/api/v1/users/{user.Id}", new
            {
                userId = user.Id,
                username = user.Username,
                email = user.Email
            });
        }

        /// <summary>
        /// Lấy danh sách người dùng
        /// </summary>
        [HttpGet]
        public IActionResult GetUsers()
        {
            var users = _userService.GetAllUsers()
                .Select(u => new
                {
                    userId = u.Id,
                    username = u.Username,
                    email = u.Email,
                    fullName = u.FullName,
                    isActive = u.IsActive,
                    roles = u.Roles
                });

            return Ok(users);
        }

        /// <summary>
        /// Lấy thông tin người dùng theo ID
        /// </summary>
        [HttpGet("{id}")]
        public IActionResult GetUser(string id)
        {
            var user = _userService.GetUserById(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            return Ok(new
            {
                userId = user.Id,
                username = user.Username,
                email = user.Email,
                fullName = user.FullName,
                isActive = user.IsActive,
                roles = user.Roles,
                createdAt = user.CreatedAt,
                lastLogin = user.LastLoginAt
            });
        }

        /// <summary>
        /// Gán vai trò cho người dùng
        /// </summary>
        [HttpPost("{id}/roles")]
        public IActionResult AssignRole(string id, [FromBody] RoleRequest request)
        {
            var user = _userService.GetUserById(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            _userService.AssignRole(id, request.RoleId);

            return Ok(new { message = "Role assigned successfully" });
        }

        /// <summary>
        /// Đổi mật khẩu
        /// </summary>
        [HttpPost("{id}/change-password")]
        public IActionResult ChangePassword(string id, [FromBody] ChangePasswordRequest request)
        {
            var result = _userService.ChangePassword(id, request.OldPassword, request.NewPassword);
            if (!result)
                return BadRequest(new { error = "Failed to change password" });

            return Ok(new { message = "Password changed successfully" });
        }

        /// <summary>
        /// Vô hiệu hóa người dùng
        /// </summary>
        [HttpPost("{id}/deactivate")]
        public IActionResult DeactivateUser(string id)
        {
            var result = _userService.DeactivateUser(id);
            if (!result)
                return NotFound(new { error = "User not found" });

            return Ok(new { message = "User deactivated" });
        }

        /// <summary>
        /// Kích hoạt người dùng
        /// </summary>
        [HttpPost("{id}/activate")]
        public IActionResult ActivateUser(string id)
        {
            var result = _userService.ActivateUser(id);
            if (!result)
                return NotFound(new { error = "User not found" });

            return Ok(new { message = "User activated" });
        }
    }

    public class LoginRequest
    {
        public string Username { get; set; }
        public string Password { get; set; }
    }

    public class RegisterRequest
    {
        public string Username { get; set; }
        public string Email { get; set; }
        public string FullName { get; set; }
        public string Password { get; set; }
    }

    public class RoleRequest
    {
        public string RoleId { get; set; }
    }

    public class ChangePasswordRequest
    {
        public string OldPassword { get; set; }
        public string NewPassword { get; set; }
    }
}