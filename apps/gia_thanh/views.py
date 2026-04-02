"""Views for Giá Thành (Product Costing)."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import (
    BangPhanBoChiPhi,
    BangTinhGiaThanh,
    DoiTuongTapHopChiPhi,
    PhieuTapHopChiPhi,
)


class DoiTuongListView(LoginRequiredMixin, ListView):
    model = DoiTuongTapHopChiPhi
    template_name = "gia_thanh/danh_sach_doi_tuong.html"
    context_object_name = "doi_tuong_list"
    paginate_by = 20


class PhieuTapHopChiPhiListView(LoginRequiredMixin, ListView):
    model = PhieuTapHopChiPhi
    template_name = "gia_thanh/tap_hop_chi_phi_form.html"
    context_object_name = "phieu_list"
    paginate_by = 20


class PhanBoChiPhiView(LoginRequiredMixin, TemplateView):
    template_name = "gia_thanh/phan_bo_chi_phi.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bang_phan_bo_list"] = BangPhanBoChiPhi.objects.all().order_by(
            "-nam", "-thang"
        )
        return context


class BangTinhGiaThanhListView(LoginRequiredMixin, ListView):
    model = BangTinhGiaThanh
    template_name = "gia_thanh/bang_tinh_gia_thanh.html"
    context_object_name = "bang_list"
    paginate_by = 20
