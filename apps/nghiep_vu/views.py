"""Views for nghiep_vu app (M4: Tiền tệ, M1/M8: Mua/Bán)."""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView

from apps.danh_muc.models import KhachHang, NhaCungCap
from apps.nghiep_vu.models import (
    ButToan,
    HoaDon,
    HoaDonChiTiet,
    PhieuChi,
    PhieuThu,
)
from apps.nghiep_vu.services import tao_hoa_don, tao_phieu_chi, tao_phieu_thu


def index(request):
    """Nghiệp vụ dashboard."""
    return render(request, "nghiep_vu/index.html")


# ==================== PHIEU THU ====================


class PhieuThuListView(LoginRequiredMixin, ListView):
    model = PhieuThu
    template_name = "nghiep_vu/phieu_thu_list.html"
    context_object_name = "phieu_thu_list"
    ordering = ["-ngay_chung_tu"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        trang_thai = self.request.GET.get("trang_thai", "")
        tu_ngay = self.request.GET.get("tu_ngay", "")
        den_ngay = self.request.GET.get("den_ngay", "")

        if search:
            qs = qs.filter(so_chung_tu__icontains=search)
        if trang_thai:
            qs = qs.filter(trang_thai=trang_thai)
        if tu_ngay:
            qs = qs.filter(ngay_chung_tu__gte=tu_ngay)
        if den_ngay:
            qs = qs.filter(ngay_chung_tu__lte=den_ngay)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        context["trang_thai"] = self.request.GET.get("trang_thai", "")
        context["tu_ngay"] = self.request.GET.get("tu_ngay", "")
        context["den_ngay"] = self.request.GET.get("den_ngay", "")
        return context


class PhieuThuCreateView(LoginRequiredMixin, CreateView):
    model = PhieuThu
    template_name = "nghiep_vu/phieu_thu_form.html"
    fields = [
        "khach_hang",
        "so_tien",
        "ty_gia",
        "hinh_thuc_thanh_toan",
        "tk_co",
        "ngay_chung_tu",
        "dien_giai",
    ]
    success_url = reverse_lazy("nghiep_vu:phieu_thu_list")

    def form_valid(self, form):
        try:
            tao_phieu_thu(
                khach_hang=form.cleaned_data.get("khach_hang"),
                so_tien=form.cleaned_data["so_tien"],
                tk_co=form.cleaned_data.get("tk_co", "131"),
                hinh_thuc_thanh_toan=form.cleaned_data.get(
                    "hinh_thuc_thanh_toan", "tien_mat"
                ),
                ngay_chung_tu=form.cleaned_data.get("ngay_chung_tu"),
                dien_giai=form.cleaned_data.get("dien_giai", ""),
                ty_gia=form.cleaned_data.get("ty_gia", Decimal("1")),
                nguoi_tao=self.request.user.username,
            )
            messages.success(self.request, "Phiếu thu đã được tạo thành công.")
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class PhieuThuDetailView(LoginRequiredMixin, DetailView):
    model = PhieuThu
    template_name = "nghiep_vu/phieu_thu_detail.html"
    context_object_name = "phieu"


class PhieuThuDeleteView(LoginRequiredMixin, DeleteView):
    model = PhieuThu
    template_name = "nghiep_vu/phieu_confirm_delete.html"
    success_url = reverse_lazy("nghiep_vu:phieu_thu_list")


# ==================== PHIEU CHI ====================


class PhieuChiListView(LoginRequiredMixin, ListView):
    model = PhieuChi
    template_name = "nghiep_vu/phieu_chi_list.html"
    context_object_name = "phieu_chi_list"
    ordering = ["-ngay_chung_tu"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        trang_thai = self.request.GET.get("trang_thai", "")
        tu_ngay = self.request.GET.get("tu_ngay", "")
        den_ngay = self.request.GET.get("den_ngay", "")

        if search:
            qs = qs.filter(so_chung_tu__icontains=search)
        if trang_thai:
            qs = qs.filter(trang_thai=trang_thai)
        if tu_ngay:
            qs = qs.filter(ngay_chung_tu__gte=tu_ngay)
        if den_ngay:
            qs = qs.filter(ngay_chung_tu__lte=den_ngay)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        context["trang_thai"] = self.request.GET.get("trang_thai", "")
        context["tu_ngay"] = self.request.GET.get("tu_ngay", "")
        context["den_ngay"] = self.request.GET.get("den_ngay", "")
        return context


class PhieuChiCreateView(LoginRequiredMixin, CreateView):
    model = PhieuChi
    template_name = "nghiep_vu/phieu_chi_form.html"
    fields = [
        "nha_cung_cap",
        "so_tien",
        "ty_gia",
        "hinh_thuc_thanh_toan",
        "tk_no",
        "ngay_chung_tu",
        "dien_giai",
    ]
    success_url = reverse_lazy("nghiep_vu:phieu_chi_list")

    def form_valid(self, form):
        try:
            tao_phieu_chi(
                nha_cung_cap=form.cleaned_data.get("nha_cung_cap"),
                so_tien=form.cleaned_data["so_tien"],
                tk_no=form.cleaned_data.get("tk_no", "331"),
                hinh_thuc_thanh_toan=form.cleaned_data.get(
                    "hinh_thuc_thanh_toan", "tien_mat"
                ),
                ngay_chung_tu=form.cleaned_data.get("ngay_chung_tu"),
                dien_giai=form.cleaned_data.get("dien_giai", ""),
                ty_gia=form.cleaned_data.get("ty_gia", Decimal("1")),
                nguoi_tao=self.request.user.username,
            )
            messages.success(self.request, "Phiếu chi đã được tạo thành công.")
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class PhieuChiDetailView(LoginRequiredMixin, DetailView):
    model = PhieuChi
    template_name = "nghiep_vu/phieu_chi_detail.html"
    context_object_name = "phieu"


class PhieuChiDeleteView(LoginRequiredMixin, DeleteView):
    model = PhieuChi
    template_name = "nghiep_vu/phieu_confirm_delete.html"
    success_url = reverse_lazy("nghiep_vu:phieu_chi_list")


# ==================== HOA DON ====================


class HoaDonListView(LoginRequiredMixin, ListView):
    model = HoaDon
    template_name = "nghiep_vu/hoa_don_list.html"
    context_object_name = "hoa_don_list"
    ordering = ["-ngay_hoa_don"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        trang_thai = self.request.GET.get("trang_thai", "")
        tu_ngay = self.request.GET.get("tu_ngay", "")
        den_ngay = self.request.GET.get("den_ngay", "")

        if search:
            qs = qs.filter(so_hoa_don__icontains=search)
        if trang_thai:
            qs = qs.filter(trang_thai=trang_thai)
        if tu_ngay:
            qs = qs.filter(ngay_hoa_don__gte=tu_ngay)
        if den_ngay:
            qs = qs.filter(ngay_hoa_don__lte=den_ngay)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        context["trang_thai"] = self.request.GET.get("trang_thai", "")
        context["tu_ngay"] = self.request.GET.get("tu_ngay", "")
        context["den_ngay"] = self.request.GET.get("den_ngay", "")
        return context


class HoaDonCreateView(LoginRequiredMixin, CreateView):
    model = HoaDon
    template_name = "nghiep_vu/hoa_don_form.html"
    fields = [
        "khach_hang",
        "ngay_hoa_don",
        "hinh_thuc_thanh_toan",
        "ky_hieu",
    ]
    success_url = reverse_lazy("nghiep_vu:hoa_don_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        form.instance.trang_thai = "draft"
        return super().form_valid(form)


class HoaDonDetailView(LoginRequiredMixin, DetailView):
    model = HoaDon
    template_name = "nghiep_vu/hoa_don_detail.html"
    context_object_name = "hoa_don"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chi_tiet_list"] = self.object.chi_tiet.all()
        return context


class HoaDonDeleteView(LoginRequiredMixin, DeleteView):
    model = HoaDon
    template_name = "nghiep_vu/hoa_don_confirm_delete.html"
    success_url = reverse_lazy("nghiep_vu:hoa_don_list")
