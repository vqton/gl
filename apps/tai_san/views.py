"""Views for TaiSan (Fixed Assets) module."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from apps.nghiep_vu.models import BienBanGiaoNhanTSCD, BienBanThanhLyTSCD
from apps.tai_san.models import BangKhauHao, TaiSanCoDinh


class TaiSanListView(LoginRequiredMixin, ListView):
    model = TaiSanCoDinh
    template_name = "tai_san/taisan_list.html"
    context_object_name = "taisan_list"


# ==================== BIÊN BẢN GIAO NHẬN TSCĐ ====================


class BienBanGiaoNhanTSCDListView(LoginRequiredMixin, ListView):
    model = BienBanGiaoNhanTSCD
    template_name = "tai_san/bien_ban_giao_nhan_list.html"
    context_object_name = "bien_ban_list"
    ordering = ["-ngay_lap"]
    paginate_by = 20


class BienBanGiaoNhanTSCDCreateView(LoginRequiredMixin, CreateView):
    model = BienBanGiaoNhanTSCD
    template_name = "tai_san/bien_ban_giao_nhan_form.html"
    fields = [
        "so_chung_tu",
        "ngay_lap",
        "loai",
        "tai_san",
        "nguoi_giao",
        "nguoi_nhan",
        "bo_phan_su_dung",
        "nguyen_gia",
        "so_luong",
        "dien_giai",
    ]
    success_url = reverse_lazy("tai_san:bien_ban_giao_nhan_list")


# ==================== BIÊN BẢN THANH LÝ TSCĐ ====================


class BienBanThanhLyTSCDListView(LoginRequiredMixin, ListView):
    model = BienBanThanhLyTSCD
    template_name = "tai_san/bien_ban_thanh_ly_list.html"
    context_object_name = "bien_ban_list"
    ordering = ["-ngay_lap"]
    paginate_by = 20


class BienBanThanhLyTSCDCreateView(LoginRequiredMixin, CreateView):
    model = BienBanThanhLyTSCD
    template_name = "tai_san/bien_ban_thanh_ly_form.html"
    fields = [
        "so_chung_tu",
        "ngay_lap",
        "tai_san",
        "nguyen_gia",
        "khau_hao_luy_ke",
        "gia_tri_con_lai",
        "loai_xu_ly",
        "so_tien_thu",
        "chiet_khau",
        "ly_do",
        "nguoi_lap",
        "nguoi_duyet",
    ]
    success_url = reverse_lazy("tai_san:bien_ban_thanh_ly_list")


# ==================== BẢNG KHẤU HAO ====================


class BangKhauHaoListView(LoginRequiredMixin, ListView):
    model = BangKhauHao
    template_name = "tai_san/bang_khau_hao_list.html"
    context_object_name = "bang_khau_hao_list"
    ordering = ["-nam", "-thang"]
    paginate_by = 20


class BangKhauHaoCreateView(LoginRequiredMixin, CreateView):
    model = BangKhauHao
    template_name = "tai_san/bang_khau_hao_form.html"
    fields = [
        "tai_san",
        "thang",
        "nam",
        "so_tien_khau_hao",
        "khau_hao_luy_ke_dau_thang",
        "khau_hao_luy_ke_cuoi_thang",
    ]
    success_url = reverse_lazy("tai_san:bang_khau_hao_list")
