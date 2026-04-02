"""Bank views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from apps.ngan_hang.models import DoiChieuNganHang, GiayBaoCo, GiayBaoNo, UyNhiemChi


class GiayBaoNoListView(LoginRequiredMixin, ListView):
    model = GiayBaoNo
    template_name = "ngan_hang/giay_bao_no_list.html"
    context_object_name = "giay_bao_no_list"
    paginate_by = 20


class GiayBaoNoCreateView(LoginRequiredMixin, CreateView):
    model = GiayBaoNo
    template_name = "ngan_hang/giay_bao_no_form.html"
    fields = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "so_tien", "dien_giai"]
    success_url = reverse_lazy("ngan_hang:giay_bao_no_list")


class GiayBaoNoDetailView(LoginRequiredMixin, DetailView):
    model = GiayBaoNo
    template_name = "ngan_hang/giay_bao_no_detail.html"
    context_object_name = "giay_bao_no"


class GiayBaoNoDeleteView(LoginRequiredMixin, DeleteView):
    model = GiayBaoNo
    template_name = "ngan_hang/giay_bao_no_confirm_delete.html"
    success_url = reverse_lazy("ngan_hang:giay_bao_no_list")


class GiayBaoCoListView(LoginRequiredMixin, ListView):
    model = GiayBaoCo
    template_name = "ngan_hang/giay_bao_co_list.html"
    context_object_name = "giay_bao_co_list"
    paginate_by = 20


class GiayBaoCoCreateView(LoginRequiredMixin, CreateView):
    model = GiayBaoCo
    template_name = "ngan_hang/giay_bao_co_form.html"
    fields = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "so_tien", "dien_giai"]
    success_url = reverse_lazy("ngan_hang:giay_bao_co_list")


class GiayBaoCoDetailView(LoginRequiredMixin, DetailView):
    model = GiayBaoCo
    template_name = "ngan_hang/giay_bao_co_detail.html"
    context_object_name = "giay_bao_co"


class GiayBaoCoDeleteView(LoginRequiredMixin, DeleteView):
    model = GiayBaoCo
    template_name = "ngan_hang/giay_bao_co_confirm_delete.html"
    success_url = reverse_lazy("ngan_hang:giay_bao_co_list")


class UyNhiemChiListView(LoginRequiredMixin, ListView):
    model = UyNhiemChi
    template_name = "ngan_hang/uy_nhiem_chi_list.html"
    context_object_name = "uy_nhiem_chi_list"
    paginate_by = 20


class UyNhiemChiCreateView(LoginRequiredMixin, CreateView):
    model = UyNhiemChi
    template_name = "ngan_hang/uy_nhiem_chi_form.html"
    fields = ["so_chung_tu", "ngay", "tai_khoan_ngan_hang", "nha_cung_cap", "so_tien", "noi_dung"]
    success_url = reverse_lazy("ngan_hang:uy_nhiem_chi_list")


class UyNhiemChiDetailView(LoginRequiredMixin, DetailView):
    model = UyNhiemChi
    template_name = "ngan_hang/uy_nhiem_chi_detail.html"
    context_object_name = "uy_nhiem_chi"


class DoiChieuNganHangListView(LoginRequiredMixin, ListView):
    model = DoiChieuNganHang
    template_name = "ngan_hang/doi_chieu_ngan_hang_list.html"
    context_object_name = "doi_chieu_list"
    paginate_by = 20


class DoiChieuNganHangCreateView(LoginRequiredMixin, CreateView):
    model = DoiChieuNganHang
    template_name = "ngan_hang/doi_chieu_ngan_hang_form.html"
    fields = ["tai_khoan_ngan_hang", "thang", "nam", "so_du_so_sach", "so_du_ngan_hang", "ghi_chu"]
    success_url = reverse_lazy("ngan_hang:doi_chieu_list")


class DoiChieuNganHangDetailView(LoginRequiredMixin, DetailView):
    model = DoiChieuNganHang
    template_name = "ngan_hang/doi_chieu_ngan_hang_detail.html"
    context_object_name = "doi_chieu"
