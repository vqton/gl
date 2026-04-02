"""Công nợ views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.cong_no.models import BienBanDoiChieuCongNo, CongNoPhaiThu, CongNoPhaiTra


class CongNoPhaiThuListView(LoginRequiredMixin, ListView):
    model = CongNoPhaiThu
    template_name = "cong_no/cong_no_phai_thu_list.html"
    context_object_name = "cong_no_list"
    paginate_by = 20


class CongNoPhaiThuDetailView(LoginRequiredMixin, DetailView):
    model = CongNoPhaiThu
    template_name = "cong_no/cong_no_phai_thu_detail.html"
    context_object_name = "cong_no"


class CongNoPhaiTraListView(LoginRequiredMixin, ListView):
    model = CongNoPhaiTra
    template_name = "cong_no/cong_no_phai_tra_list.html"
    context_object_name = "cong_no_list"
    paginate_by = 20


class CongNoPhaiTraDetailView(LoginRequiredMixin, DetailView):
    model = CongNoPhaiTra
    template_name = "cong_no/cong_no_phai_tra_detail.html"
    context_object_name = "cong_no"


class BienBanDoiChieuCongNoListView(LoginRequiredMixin, ListView):
    model = BienBanDoiChieuCongNo
    template_name = "cong_no/bien_ban_doi_chieu_list.html"
    context_object_name = "bien_ban_list"
    paginate_by = 20


class BienBanDoiChieuCongNoCreateView(LoginRequiredMixin, CreateView):
    model = BienBanDoiChieuCongNo
    template_name = "cong_no/bien_ban_doi_chieu_form.html"
    fields = ["doi_tuong_content_type", "doi_tuong_object_id", "loai", "thang", "nam", "so_dau_ky", "phat_sinh_no", "phat_sinh_co"]
    success_url = reverse_lazy("cong_no:bien_ban_list")


class BienBanDoiChieuCongNoDetailView(LoginRequiredMixin, DetailView):
    model = BienBanDoiChieuCongNo
    template_name = "cong_no/bien_ban_doi_chieu_detail.html"
    context_object_name = "bien_ban"
