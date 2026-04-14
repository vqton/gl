using GL.Domain.Entities;
using System;
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
    }
}
