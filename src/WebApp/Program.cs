using GL.Domain.Entities;
using GL.Infrastructure.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

var dbProvider = builder.Configuration.GetValue<string>("DatabaseProvider", "SqlServer");
var connectionString = dbProvider switch
{
    "MariaDB" => builder.Configuration.GetConnectionString("DefaultConnection"),
    "PostgreSQL" => builder.Configuration.GetConnectionString("PostgreSQL"),
    "Sqlite" => builder.Configuration.GetConnectionString("Sqlite") ?? "Data Source=gl.db",
    "SqlServer" => builder.Configuration.GetConnectionString("SqlServer"),
    _ => builder.Configuration.GetConnectionString("DefaultConnection")
};

// Configure Identity - supports MariaDB, PostgreSQL, SqlServer, SQLite
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    switch (dbProvider)
    {
        case "MariaDB":
            options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
            break;
        case "PostgreSQL":
            options.UseNpgsql(connectionString);
            break;
        case "Sqlite":
            options.UseSqlite(connectionString);
            break;
        case "SqlServer":
        default:
            options.UseSqlServer(connectionString);
            break;
    }
});

builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    // Password settings
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequiredLength = 8;

    // Lockout settings
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;

    // User settings
    options.User.RequireUniqueEmail = true;
    options.SignIn.RequireConfirmedEmail = false;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();

// Configure Authorization Policies
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("CanCreateTransaction", policy =>
        policy.RequireRole("ADMIN", "ACCOUNTANT", "MANAGER"));
    options.AddPolicy("CanApproveTransaction", policy =>
        policy.RequireRole("ADMIN", "MANAGER"));
    options.AddPolicy("CanViewReports", policy =>
        policy.RequireRole("ADMIN", "ACCOUNTANT", "MANAGER", "VIEWER"));
    options.AddPolicy("FullAccess", policy =>
        policy.RequireRole("ADMIN"));
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();