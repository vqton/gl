"""Views for Phân Tích Tài Chính."""

import json
from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from .services import PhanTichTaiChinhService


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "phan_tich/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tu_ngay = self.request.GET.get("tu_ngay")
        den_ngay = self.request.GET.get("den_ngay")

        if tu_ngay and den_ngay:
            tu = date.fromisoformat(tu_ngay)
            den = date.fromisoformat(den_ngay)
        else:
            den = date.today()
            tu = date(den.year, 1, 1)

        service = PhanTichTaiChinhService(tu_ngay=tu, den_ngay=den)
        context["data"] = service.get_bang_tong_hop()
        context["trend"] = service.get_trend_data()
        context["tu_ngay"] = tu.isoformat()
        context["den_ngay"] = den.isoformat()
        return context


def api_tong_hop(request):
    """JSON API endpoint for financial ratios summary."""
    tu_ngay = request.GET.get("tu_ngay")
    den_ngay = request.GET.get("den_ngay")

    if not tu_ngay or not den_ngay:
        den = date.today()
        tu = date(den.year, 1, 1)
    else:
        tu = date.fromisoformat(tu_ngay)
        den = date.fromisoformat(den_ngay)

    service = PhanTichTaiChinhService(tu_ngay=tu, den_ngay=den)
    data = service.get_bang_tong_hop()

    return JsonResponse(data, json_dumps_params={"default": str})


def api_trend(request):
    """JSON API endpoint for multi-period trend data."""
    so_ky = int(request.GET.get("so_ky", 4))
    den_ngay = request.GET.get("den_ngay")

    if den_ngay:
        den = date.fromisoformat(den_ngay)
    else:
        den = date.today()

    tu = date(den.year, 1, 1)
    service = PhanTichTaiChinhService(tu_ngay=tu, den_ngay=den)
    data = service.get_trend_data(so_ky=so_ky)

    return JsonResponse(data, json_dumps_params={"default": str})
