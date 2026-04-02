"""Custom admin site for Vietnamese SME Accounting System."""

from django.contrib import admin
from django.contrib.auth.models import Group, User

from apps.users.models import NguoiDung


class AccountingAdminSite(admin.AdminSite):
    """Custom admin site with permission-based model filtering."""

    site_header = 'Hệ thống Kế toán SME - Thông tư 99/2025/TT-BTC'
    site_title = 'Kế toán SME'
    index_title = 'Quản lý hệ thống kế toán'

    def get_app_list(self, request, app_label=None):
        """Filter available models based on user permissions."""
        app_list = super().get_app_list(request, app_label)

        if request.user.is_superuser:
            return app_list

        permission_map = {
            'danh_muc': ['view_taikhoanketoan', 'view_donvi', 'view_khachhang', 'view_nhacungcap'],
            'nghiep_vu': ['view_buttoan', 'view_hoadon', 'view_nhapkho', 'view_xuatkho'],
            'kho': ['view_khoentry', 'view_vattuhanghoa', 'view_kholot'],
            'tai_san': ['view_taisancodinh'],
            'luong': ['view_nhanvien', 'view_bangluong'],
        }

        user_perms = set()
        for perms in permission_map.values():
            for p in perms:
                if request.user.has_perm(p):
                    user_perms.add(p)

        filtered_app_list = []
        for app in app_list:
            app_name = app['app_label']
            if app_name in permission_map:
                required_perms = set(permission_map[app_name])
                if required_perms & user_perms:
                    filtered_app_list.append(app)
            elif app_name in ['auth', 'users']:
                if request.user.is_staff:
                    filtered_app_list.append(app)
        return filtered_app_list

    def index(self, request, extra_context=None):
        """Check if user has access to admin."""
        if not request.user.is_staff:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Bạn không có quyền truy cập trang quản trị.')
        return super().index(request, extra_context)


class AccountingSite(AccountingAdminSite):
    """Alias for backward compatibility."""
    pass


admin_site = AccountingAdminSite(name='accounting_admin')