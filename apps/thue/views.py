"""Thuế views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.thue.models import BangKeHoaDonBanRa, BangKeHoaDonMuaVao, ToKhaiGTGT, ToKhaiTNCN, ToKhaiTNDNTamTinh


class BangKeMuaVaoListView(LoginRequiredMixin, ListView):
    model = BangKeHoaDonMuaVao
    template_name = "thue/bang_ke_mua_vao_list.html"
    context_object_name = "bang_ke_list"
    paginate_by = 20


class BangKeBanRaListView(LoginRequiredMixin, ListView):
    model = BangKeHoaDonBanRa
    template_name = "thue/bang_ke_ban_ra_list.html"
    context_object_name = "bang_ke_list"
    paginate_by = 20


class ToKhaiGTGTListView(LoginRequiredMixin, ListView):
    model = ToKhaiGTGT
    template_name = "thue/to_khai_gtgt_list.html"
    context_object_name = "to_khai_list"
    paginate_by = 20


class ToKhaiGTGTCreateView(LoginRequiredMixin, CreateView):
    model = ToKhaiGTGT
    template_name = "thue/to_khai_gtgt_form.html"
    fields = ["thang", "nam", "tong_doanh_so_ban", "thue_gtgt_dau_ra", "tong_gia_tri_mua_vao", "thue_gtgt_dau_vao"]
    success_url = reverse_lazy("thue:to_khai_gtgt_list")


class ToKhaiGTGTDetailView(LoginRequiredMixin, DetailView):
    model = ToKhaiGTGT
    template_name = "thue/to_khai_gtgt_detail.html"
    context_object_name = "to_khai"


class ToKhaiTNDNListView(LoginRequiredMixin, ListView):
    model = ToKhaiTNDNTamTinh
    template_name = "thue/to_khai_tndn_list.html"
    context_object_name = "to_khai_list"
    paginate_by = 20


class ToKhaiTNCNListView(LoginRequiredMixin, ListView):
    model = ToKhaiTNCN
    template_name = "thue/to_khai_tncn_list.html"
    context_object_name = "to_khai_list"
    paginate_by = 20
