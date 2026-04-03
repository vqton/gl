"""Views for Luong (Payroll) module."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from apps.luong.models import BangLuong, NhanVien


class SalaryAccessMixin(UserPassesTestMixin):
    """Mixin to restrict payroll access to chief accountant only."""

    def test_func(self):
        """Check if user is chief accountant or system admin."""
        return self.request.user.is_ke_toan_truong

    def handle_no_permission(self):
        """Return 403 with Vietnamese message."""
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden(
            "Bạn không có quyền truy cập thông tin lương. "
            "Chỉ Kế toán trưởng mới có quyền này."
        )


class NhanVienListView(LoginRequiredMixin, SalaryAccessMixin, ListView):
    model = NhanVien
    template_name = "luong/nhanvien_list.html"
    context_object_name = "nhanvien_list"


class BangLuongListView(LoginRequiredMixin, SalaryAccessMixin, ListView):
    model = BangLuong
    template_name = "luong/bangluong_list.html"
    context_object_name = "bangluong_list"
    ordering = ["-nam", "-thang"]
