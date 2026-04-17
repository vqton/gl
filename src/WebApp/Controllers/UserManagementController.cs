using GL.Domain.Entities;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace GL.WebApp.Controllers
{
    /// <summary>
    /// User Management API - ASP.NET Core Identity
    /// </summary>
    [ApiController]
    [Route("api/v1/[controller]")]
    [Authorize(Policy = "FullAccess")]
    public class UserManagementController : ControllerBase
    {
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly RoleManager<ApplicationRole> _roleManager;

        public UserManagementController(
            UserManager<ApplicationUser> userManager,
            RoleManager<ApplicationRole> roleManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
        }

        /// <summary>
        /// Lấy danh sách users
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetUsers()
        {
            var users = await _userManager.Users
                .Select(u => new
                {
                    u.Id,
                    u.UserName,
                    u.Email,
                    u.FullName,
                    u.IsActive,
                    u.LastLoginAt,
                    u.Department
                })
                .ToListAsync();

            return Ok(users);
        }

        /// <summary>
        /// Lấy user theo ID
        /// </summary>
        [HttpGet("{id}")]
        public async Task<IActionResult> GetUser(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            var roles = await _userManager.GetRolesAsync(user);

            return Ok(new
            {
                user.Id,
                user.UserName,
                user.Email,
                user.FullName,
                user.IsActive,
                user.LastLoginAt,
                user.Department,
                roles
            });
        }

        /// <summary>
        /// Tạo user mới
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest request)
        {
            var existingUser = await _userManager.FindByNameAsync(request.Username);
            if (existingUser != null)
                return BadRequest(new { error = "Username already exists" });

            var user = new ApplicationUser
            {
                UserName = request.Username,
                Email = request.Email,
                FullName = request.FullName,
                Department = request.Department,
                IsActive = true
            };

            var result = await _userManager.CreateAsync(user, request.Password);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            if (request.Roles?.Length > 0)
            {
                await _userManager.AddToRolesAsync(user, request.Roles);
            }

            return Created($"/api/v1/usermanagement/{user.Id}", new
            {
                user.Id,
                user.UserName,
                user.Email
            });
        }

        /// <summary>
        /// Cập nhật user
        /// </summary>
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateUser(string id, [FromBody] UpdateUserRequest request)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            if (!string.IsNullOrEmpty(request.FullName))
                user.FullName = request.FullName;

            if (!string.IsNullOrEmpty(request.Department))
                user.Department = request.Department;

            if (request.IsActive.HasValue)
                user.IsActive = request.IsActive.Value;

            var result = await _userManager.UpdateAsync(user);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "User updated successfully" });
        }

        /// <summary>
        /// Đổi mật khẩu
        /// </summary>
        [HttpPost("{id}/change-password")]
        public async Task<IActionResult> ChangePassword(string id, [FromBody] UserChangePasswordRequest request)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            var result = await _userManager.ChangePasswordAsync(user, request.OldPassword, request.NewPassword);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "Password changed successfully" });
        }

        /// <summary>
        /// Reset mật khẩu (admin only)
        /// </summary>
        [HttpPost("{id}/reset-password")]
        public async Task<IActionResult> ResetPassword(string id, [FromBody] UserResetPasswordRequest request)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            var token = await _userManager.GeneratePasswordResetTokenAsync(user);
            var result = await _userManager.ResetPasswordAsync(user, token, request.NewPassword);

            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "Password reset successfully" });
        }

        /// <summary>
        /// Gán role cho user
        /// </summary>
        [HttpPost("{id}/assign-role")]
        public async Task<IActionResult> AssignRole(string id, [FromBody] AssignRoleRequest request)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            var roleExists = await _roleManager.RoleExistsAsync(request.Role);
            if (!roleExists)
                return BadRequest(new { error = "Role not found" });

            var result = await _userManager.AddToRoleAsync(user, request.Role);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "Role assigned successfully" });
        }

        /// <summary>
        /// Xóa role khỏi user
        /// </summary>
        [HttpDelete("{id}/remove-role")]
        public async Task<IActionResult> RemoveRole(string id, [FromBody] AssignRoleRequest request)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            var result = await _userManager.RemoveFromRoleAsync(user, request.Role);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "Role removed successfully" });
        }

        /// <summary>
        /// Lấy danh sách roles
        /// </summary>
        [HttpGet("roles")]
        public async Task<IActionResult> GetRoles()
        {
            var roles = await _roleManager.Roles
                .Select(r => new
                {
                    r.Id,
                    r.Name,
                    r.Description
                })
                .ToListAsync();

            return Ok(roles);
        }

        /// <summary>
        /// Tạo role mới
        /// </summary>
        [HttpPost("roles")]
        public async Task<IActionResult> CreateRole([FromBody] CreateRoleRequest request)
        {
            var roleExists = await _roleManager.RoleExistsAsync(request.Name);
            if (roleExists)
                return BadRequest(new { error = "Role already exists" });

            var role = new ApplicationRole
            {
                Name = request.Name,
                Description = request.Description
            };

            var result = await _roleManager.CreateAsync(role);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Created($"/api/v1/usermanagement/roles/{role.Id}", new
            {
                role.Id,
                role.Name
            });
        }

        /// <summary>
        /// Xóa user
        /// </summary>
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteUser(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound(new { error = "User not found" });

            // Prevent self-deletion
            var currentUserId = _userManager.GetUserId(User);
            if (id == currentUserId)
                return BadRequest(new { error = "Cannot delete yourself" });

            var result = await _userManager.DeleteAsync(user);
            if (!result.Succeeded)
                return BadRequest(new { errors = result.Errors.Select(e => e.Description) });

            return Ok(new { message = "User deleted successfully" });
        }
    }

    public class CreateUserRequest
    {
        public string Username { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public string FullName { get; set; }
        public string Department { get; set; }
        public string[] Roles { get; set; }
    }

    public class UpdateUserRequest
    {
        public string FullName { get; set; }
        public string Department { get; set; }
        public bool? IsActive { get; set; }
    }

    public class UserChangePasswordRequest
    {
        public string OldPassword { get; set; }
        public string NewPassword { get; set; }
    }

    public class UserResetPasswordRequest
    {
        public string NewPassword { get; set; }
    }

    public class AssignRoleRequest
    {
        public string Role { get; set; }
    }

    public class CreateRoleRequest
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }
}