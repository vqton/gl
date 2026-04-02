"""Views for Kho module."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from apps.kho.models import Kho, KhoEntry, TonKho, VatTuHangHoa


class KhoListView(LoginRequiredMixin, ListView):
    model = Kho
    template_name = "kho/kho_list.html"
    context_object_name = "kho_list"


class KhoEntryListView(LoginRequiredMixin, ListView):
    model = KhoEntry
    template_name = "kho/kho_entry_list.html"
    context_object_name = "entry_list"
    ordering = ["-ngay_chung_tu"]
    paginate_by = 20


class TonKhoListView(LoginRequiredMixin, ListView):
    model = TonKho
    template_name = "kho/ton_kho_list.html"
    context_object_name = "ton_kho_list"
