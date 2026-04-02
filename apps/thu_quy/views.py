"""Views for Thủ Quỹ (Cashier Reconciliation)."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import KiemKeQuy, XuLyChenhLechQuy


class KiemKeQuyListView(LoginRequiredMixin, ListView):
    model = KiemKeQuy
    template_name = "thu_quy/kiem_ke_quy_form.html"
    context_object_name = "kiem_ke_list"
    paginate_by = 20


class XuLyChenhLechView(LoginRequiredMixin, TemplateView):
    template_name = "thu_quy/xu_ly_chenh_lech.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["xu_ly_list"] = XuLyChenhLechQuy.objects.select_related(
            "kiem_ke", "but_toan"
        ).all()
        return context


class SoQuyTienMatView(LoginRequiredMixin, TemplateView):
    template_name = "thu_quy/so_quy_tien_mat.html"
