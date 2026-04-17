using GL.Domain.Entities;
using GL.Application.Services;
using System;
using System.Linq;
using Xunit;

namespace GL.Domain.Tests
{
    /// <summary>
    /// Test cases for role-based access control
    /// </summary>
    public class RbacTests
    {
        [Fact]
        public void User_Create_ShouldSetProperties()
        {
            var user = new User
            {
                Id = "USR001",
                Username = "admin",
                Email = "admin@company.com",
                IsActive = true,
                CreatedAt = DateTime.Now
            };

            Assert.Equal("admin", user.Username);
            Assert.True(user.IsActive);
        }

        [Fact]
        public void User_IsValid_ShouldReturnTrue()
        {
            var user = new User
            {
                Id = "USR001",
                Username = "testuser",
                Email = "test@company.com"
            };

            Assert.True(user.IsValid());
        }

        [Fact]
        public void Role_Create_ShouldSetProperties()
        {
            var role = new Role
            {
                Id = "ROLE001",
                Name = "ACCOUNTANT",
                Description = "Kế toán viên",
                Permissions = new string[] { "TRANSACTION_CREATE", "TRANSACTION_VIEW" }
            };

            Assert.Equal("ACCOUNTANT", role.Name);
            Assert.Contains("TRANSACTION_CREATE", role.Permissions);
        }

        [Fact]
        public void Permission_Check_ShouldWorkCorrectly()
        {
            var role = new Role
            {
                Name = "MANAGER",
                Permissions = new string[] { "TRANSACTION_CREATE", "TRANSACTION_APPROVE", "REPORT_VIEW" }
            };

            Assert.True(role.HasPermission("TRANSACTION_CREATE"));
            Assert.True(role.HasPermission("TRANSACTION_APPROVE"));
            Assert.False(role.HasPermission("USER_MANAGE"));
        }

        [Fact]
        public void UserRole_Assign_ShouldTrackUserRoles()
        {
            var userRole = new UserRole
            {
                UserId = "USR001",
                RoleId = "ROLE001",
                AssignedAt = DateTime.Now
            };

            Assert.Equal("USR001", userRole.UserId);
            Assert.Equal("ROLE001", userRole.RoleId);
        }

        [Fact]
        public void UserService_CreateUser_ShouldSucceed()
        {
            var service = new UserService();
            var user = service.CreateUser("testuser", "test@company.com", "Test User");

            Assert.NotNull(user);
            Assert.Equal("testuser", user.Username);
            Assert.Equal("test@company.com", user.Email);
            Assert.True(user.IsActive);
        }

        [Fact]
        public void UserService_CreateUserWithPassword_ShouldHashPassword()
        {
            var service = new UserService();
            var user = service.CreateUserWithPassword("testuser", "test@company.com", "Test User", "password123");

            Assert.NotNull(user);
            Assert.NotNull(user.PasswordHash);
            Assert.NotEqual("password123", user.PasswordHash);
        }

        [Fact]
        public void UserService_Authenticate_ShouldReturnUser()
        {
            var service = new UserService();
            service.CreateUserWithPassword("admin", "admin@company.com", "Admin User", "password123");

            var authenticated = service.Authenticate("admin", "password123");

            Assert.NotNull(authenticated);
            Assert.Equal("admin", authenticated.Username);
        }

        [Fact]
        public void UserService_Authenticate_WrongPassword_ShouldReturnNull()
        {
            var service = new UserService();
            service.CreateUserWithPassword("admin", "admin@company.com", "Admin User", "password123");

            var authenticated = service.Authenticate("admin", "wrongpassword");

            Assert.Null(authenticated);
        }

        [Fact]
        public void UserService_HasPermission_ShouldCheckRolePermissions()
        {
            var service = new UserService();
            var user = service.CreateUser("accountant", "acc@company.com", "Accountant User", new[] { "ACCOUNTANT" });

            var hasPermission = service.HasPermission(user.Id, "TRANSACTION_CREATE");

            Assert.True(hasPermission);
        }

        [Fact]
        public void UserService_AssignRole_ShouldAddRole()
        {
            var service = new UserService();
            var user = service.CreateUser("viewer", "viewer@company.com", "Viewer User");

            service.AssignRole(user.Id, "MANAGER");

            Assert.Contains("MANAGER", user.Roles);
        }

        [Fact]
        public void UserService_DeactivateUser_ShouldSetIsActiveFalse()
        {
            var service = new UserService();
            var user = service.CreateUser("testuser", "test@company.com", "Test User");

            var result = service.DeactivateUser(user.Id);

            Assert.True(result);
            Assert.False(user.IsActive);
        }

        [Fact]
        public void UserService_ChangePassword_ShouldSucceed()
        {
            var service = new UserService();
            var user = service.CreateUserWithPassword("admin", "admin@company.com", "Admin User", "oldpassword");

            var result = service.ChangePassword(user.Id, "oldpassword", "newpassword");

            Assert.True(result);
        }
    }
}
