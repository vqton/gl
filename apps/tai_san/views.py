"""Views for TaiSan (Fixed Assets) module."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.tai_san.models import TaiSanCoDinh


class TaiSanListView(LoginRequiredMixin, ListView):
    model = TaiSanCoDinh
    template_name = "tai_san/taisan_list.html"
    context_object_name = "taisan_list"
