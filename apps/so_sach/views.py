"""Sổ sách kế toán views."""

from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.so_sach.services import (
    get_so_ngan_hang,
    get_so_nhat_ky_chung,
    get_so_quy,
)


class SoNhatKyChungView(LoginRequiredMixin, TemplateView):
    template_name = "so_sach/so_nhat_ky_chung.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu_ngay = self.request.GET.get("tu_ngay")
        den_ngay = self.request.GET.get("den_ngay")

        if tu_ngay and den_ngay:
            tu_ngay = date.fromisoformat(tu_ngay)
            den_ngay = date.fromisoformat(den_ngay)
        else:
            today = date.today()
            tu_ngay = date(today.year, 1, 1)
            den_ngay = today

        context.update(get_so_nhat_ky_chung(tu_ngay, den_ngay))
        context["tu_ngay"] = tu_ngay
        context["den_ngay"] = den_ngay
        return context


class SoQuyView(LoginRequiredMixin, TemplateView):
    template_name = "so_sach/so_quy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu_ngay = self.request.GET.get("tu_ngay")
        den_ngay = self.request.GET.get("den_ngay")

        if tu_ngay and den_ngay:
            tu_ngay = date.fromisoformat(tu_ngay)
            den_ngay = date.fromisoformat(den_ngay)
        else:
            today = date.today()
            tu_ngay = date(today.year, 1, 1)
            den_ngay = today

        context.update(get_so_quy(tu_ngay, den_ngay))
        context["tu_ngay"] = tu_ngay
        context["den_ngay"] = den_ngay
        return context


class SoNganHangView(LoginRequiredMixin, TemplateView):
    template_name = "so_sach/so_ngan_hang.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu_ngay = self.request.GET.get("tu_ngay")
        den_ngay = self.request.GET.get("den_ngay")

        if tu_ngay and den_ngay:
            tu_ngay = date.fromisoformat(tu_ngay)
            den_ngay = date.fromisoformat(den_ngay)
        else:
            today = date.today()
            tu_ngay = date(today.year, 1, 1)
            den_ngay = today

        context.update(get_so_ngan_hang(tu_ngay, den_ngay))
        context["tu_ngay"] = tu_ngay
        context["den_ngay"] = den_ngay
        return context
