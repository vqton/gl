"""Views for Luong (Payroll) module."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.luong.models import BangLuong, NhanVien


class NhanVienListView(LoginRequiredMixin, ListView):
    model = NhanVien
    template_name = "luong/nhanvien_list.html"
    context_object_name = "nhanvien_list"


class BangLuongListView(LoginRequiredMixin, ListView):
    model = BangLuong
    template_name = "luong/bangluong_list.html"
    context_object_name = "bangluong_list"
    ordering = ["-nam", "-thang"]
