"""CCDC views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from apps.ccdc.models import BangPhanBoCCDC, CongCuDungCu


class CongCuDungCuListView(LoginRequiredMixin, ListView):
    model = CongCuDungCu
    template_name = "ccdc/ccdc_list.html"
    context_object_name = "ccdc_list"
    paginate_by = 20


class CongCuDungCuCreateView(LoginRequiredMixin, CreateView):
    model = CongCuDungCu
    template_name = "ccdc/ccdc_form.html"
    fields = ["ma_ccdc", "ten_ccdc", "ngay_mua", "so_luong", "gia_mua", "phuong_phap_phan_bo", "so_ky_phan_bo", "ky_phan_bo_bat_dau", "ky_phan_bo_ket_thuc", "tk_chi_phi", "dien_giai"]
    success_url = reverse_lazy("ccdc:ccdc_list")


class CongCuDungCuDetailView(LoginRequiredMixin, DetailView):
    model = CongCuDungCu
    template_name = "ccdc/ccdc_detail.html"
    context_object_name = "ccdc"


class CongCuDungCuDeleteView(LoginRequiredMixin, DeleteView):
    model = CongCuDungCu
    template_name = "ccdc/ccdc_confirm_delete.html"
    success_url = reverse_lazy("ccdc:ccdc_list")


class BangPhanBoCCDCListView(LoginRequiredMixin, ListView):
    model = BangPhanBoCCDC
    template_name = "ccdc/bang_phan_bo_list.html"
    context_object_name = "bang_phan_bo_list"
    paginate_by = 20


class BangPhanBoCCDCDetailView(LoginRequiredMixin, DetailView):
    model = BangPhanBoCCDC
    template_name = "ccdc/bang_phan_bo_detail.html"
    context_object_name = "bang_phan_bo"
