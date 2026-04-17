using Microsoft.AspNetCore.Identity;

namespace GL.Domain.Entities
{
    /// <summary>
    /// ASP.NET Core Identity user entity
    /// </summary>
    public class ApplicationUser : IdentityUser
    {
        /// <summary>
        /// Full name of user
        /// </summary>
        public string FullName { get; set; }

        /// <summary>
        /// Is user active
        /// </summary>
        public bool IsActive { get; set; } = true;

        /// <summary>
        /// Last login timestamp
        /// </summary>
        public DateTime? LastLoginAt { get; set; }

        /// <summary>
        /// Department
        /// </summary>
        public string Department { get; set; }
    }

    /// <summary>
    /// Application role
    /// </summary>
    public class ApplicationRole : IdentityRole
    {
        /// <summary>
        /// Role description
        /// </summary>
        public string Description { get; set; }
    }
}