"""Views for BaoCao (Reports) module - TT 99/2025/TT-BTC."""

from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.bao_cao.services import (
    get_so_cai_tai_khoan,
    get_tong_hop_so_cai,
    lap_bang_can_doi_ke_toan,
    lap_bang_can_doi_so_phat_sinh,
    lap_bao_cao_kq_kinh_doanh,
    lap_bao_cao_luu_chuyen_tien_te,
    lap_thuyet_minh_bctc,
)


class BangCanDoiKeToanView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/bang_cdk.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ngay = self.request.GET.get("ngay")
        if ngay:
            from datetime import datetime
            ngay = datetime.strptime(ngay, "%Y-%m-%d").date()
        else:
            ngay = date.today()
        context["report"] = lap_bang_can_doi_ke_toan(ngay)
        context["ngay_bao_cao"] = ngay
        return context


class BaoCaoKQKDView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/kqkd.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu = self.request.GET.get("tu")
        den = self.request.GET.get("den")
        if tu and den:
            from datetime import datetime
            tu = datetime.strptime(tu, "%Y-%m-%d").date()
            den = datetime.strptime(den, "%Y-%m-%d").date()
        else:
            tu = date(date.today().year, 1, 1)
            den = date.today()
        context["report"] = lap_bao_cao_kq_kinh_doanh(tu, den)
        context["tu_ngay"] = tu
        context["den_ngay"] = den
        return context


class BangCanDoiSoPhatSinhView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/bcd_sps.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu = self.request.GET.get("tu")
        den = self.request.GET.get("den")
        if tu and den:
            from datetime import datetime
            tu = datetime.strptime(tu, "%Y-%m-%d").date()
            den = datetime.strptime(den, "%Y-%m-%d").date()
        else:
            tu = date(date.today().year, 1, 1)
            den = date.today()
        context["report"] = lap_bang_can_doi_so_phat_sinh(tu, den)
        context["tu_ngay"] = tu
        context["den_ngay"] = den
        return context


class BaoCaoLuuChuyenTienTeView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/lctt.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu = self.request.GET.get("tu")
        den = self.request.GET.get("den")
        if tu and den:
            from datetime import datetime
            tu = datetime.strptime(tu, "%Y-%m-%d").date()
            den = datetime.strptime(den, "%Y-%m-%d").date()
        else:
            tu = date(date.today().year, 1, 1)
            den = date.today()
        context["report"] = lap_bao_cao_luu_chuyen_tien_te(tu, den)
        context["tu_ngay"] = tu
        context["den_ngay"] = den
        return context


class ThuyetMinhBCTCView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/thuyet_minh.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ngay = self.request.GET.get("ngay")
        if ngay:
            from datetime import datetime
            ngay = datetime.strptime(ngay, "%Y-%m-%d").date()
        else:
            ngay = date.today()
        context["report"] = lap_thuyet_minh_bctc(ngay)
        context["ngay_bao_cao"] = ngay
        return context


class SoCaiTaiKhoanView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/so_cai_chi_tiet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ma_tai_khoan = kwargs.get("ma_tai_khoan")
        tu = self.request.GET.get("tu")
        den = self.request.GET.get("den")
        if tu and den:
            from datetime import datetime
            tu = datetime.strptime(tu, "%Y-%m-%d").date()
            den = datetime.strptime(den, "%Y-%m-%d").date()
        else:
            tu = date(date.today().year, 1, 1)
            den = date.today()
        context["report"] = get_so_cai_tai_khoan(ma_tai_khoan, tu, den)
        context["ma_tai_khoan"] = ma_tai_khoan
        context["tu_ngay"] = tu
        context["den_ngay"] = den
        return context


class TongHopSoCaiView(LoginRequiredMixin, TemplateView):
    template_name = "bao_cao/tong_hop_so_cai.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu = self.request.GET.get("tu")
        den = self.request.GET.get("den")
        if tu and den:
            from datetime import datetime
            tu = datetime.strptime(tu, "%Y-%m-%d").date()
            den = datetime.strptime(den, "%Y-%m-%d").date()
        else:
            tu = date(date.today().year, 1, 1)
            den = date.today()
        context["report"] = get_tong_hop_so_cai(tu, den)
        context["tu_ngay"] = tu
        context["den_ngay"] = den
        return context
