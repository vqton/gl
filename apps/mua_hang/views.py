"""Mua hàng views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from apps.mua_hang.models import DeXuatMuaHang, DonDatHang, TraHangNCC


class DeXuatMuaHangListView(LoginRequiredMixin, ListView):
    model = DeXuatMuaHang
    template_name = "mua_hang/de_xuat_list.html"
    context_object_name = "de_xuat_list"
    paginate_by = 20


class DeXuatMuaHangCreateView(LoginRequiredMixin, CreateView):
    model = DeXuatMuaHang
    template_name = "mua_hang/de_xuat_form.html"
    fields = ["so_de_xuat", "ngay", "nguoi_de_xuat", "ly_do"]
    success_url = reverse_lazy("mua_hang:de_xuat_list")


class DeXuatMuaHangDetailView(LoginRequiredMixin, DetailView):
    model = DeXuatMuaHang
    template_name = "mua_hang/de_xuat_detail.html"
    context_object_name = "de_xuat"


class DonDatHangListView(LoginRequiredMixin, ListView):
    model = DonDatHang
    template_name = "mua_hang/don_dat_hang_list.html"
    context_object_name = "don_hang_list"
    paginate_by = 20


class DonDatHangCreateView(LoginRequiredMixin, CreateView):
    model = DonDatHang
    template_name = "mua_hang/don_dat_hang_form.html"
    fields = ["so_don_hang", "ngay", "nha_cung_cap", "ngay_giao_du_kien"]
    success_url = reverse_lazy("mua_hang:don_hang_list")


class DonDatHangDetailView(LoginRequiredMixin, DetailView):
    model = DonDatHang
    template_name = "mua_hang/don_dat_hang_detail.html"
    context_object_name = "don_hang"


class DonDatHangDeleteView(LoginRequiredMixin, DeleteView):
    model = DonDatHang
    template_name = "mua_hang/don_dat_hang_confirm_delete.html"
    success_url = reverse_lazy("mua_hang:don_hang_list")


class TraHangNCCListView(LoginRequiredMixin, ListView):
    model = TraHangNCC
    template_name = "mua_hang/tra_hang_list.html"
    context_object_name = "tra_hang_list"
    paginate_by = 20


class TraHangNCCCreateView(LoginRequiredMixin, CreateView):
    model = TraHangNCC
    template_name = "mua_hang/tra_hang_form.html"
    fields = ["so_chung_tu", "ngay", "nha_cung_cap", "ly_do_tra", "tong_tien"]
    success_url = reverse_lazy("mua_hang:tra_hang_list")


class TraHangNCCDetailView(LoginRequiredMixin, DetailView):
    model = TraHangNCC
    template_name = "mua_hang/tra_hang_detail.html"
    context_object_name = "tra_hang"
