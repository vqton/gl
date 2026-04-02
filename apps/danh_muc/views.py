"""Views for danh_muc (Master Data) module."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.danh_muc.models import (
    DonVi,
    HangHoa,
    KhachHang,
    NganHang,
    NhaCungCap,
    TaiKhoanKeToan,
)

# ==================== TAI KHOAN KE TOAN ====================


class TaiKhoanListView(LoginRequiredMixin, ListView):
    model = TaiKhoanKeToan
    template_name = "danh_muc/taikhoan_list.html"
    context_object_name = "taikhoan_list"
    ordering = ["ma_tai_khoan"]
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        loai = self.request.GET.get("loai", "")
        if search:
            qs = qs.filter(ma_tai_khoan__icontains=search) | qs.filter(
                ten_tai_khoan__icontains=search
            )
        if loai:
            qs = qs.filter(loai_tai_khoan=loai)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("q", "")
        ctx["loai"] = self.request.GET.get("loai", "")
        return ctx


class TaiKhoanCreateView(LoginRequiredMixin, CreateView):
    model = TaiKhoanKeToan
    template_name = "danh_muc/taikhoan_form.html"
    fields = ["ma_tai_khoan", "ten_tai_khoan", "loai_tai_khoan", "cap_do", "tai_khoan_me"]
    success_url = reverse_lazy("danh_muc:taikhoan_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        messages.success(
            self.request, f"Tài khoản {form.instance.ma_tai_khoan} đã được tạo."
        )
        return super().form_valid(form)


class TaiKhoanUpdateView(LoginRequiredMixin, UpdateView):
    model = TaiKhoanKeToan
    template_name = "danh_muc/taikhoan_form.html"
    fields = ["ma_tai_khoan", "ten_tai_khoan", "loai_tai_khoan", "cap_do", "tai_khoan_me"]
    success_url = reverse_lazy("danh_muc:taikhoan_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        messages.success(
            self.request, f"Tài khoản {form.instance.ma_tai_khoan} đã được cập nhật."
        )
        return super().form_valid(form)


class TaiKhoanDeleteView(LoginRequiredMixin, DeleteView):
    model = TaiKhoanKeToan
    template_name = "danh_muc/confirm_delete.html"
    success_url = reverse_lazy("danh_muc:taikhoan_list")


# ==================== KHACH HANG ====================


class KhachHangListView(LoginRequiredMixin, ListView):
    model = KhachHang
    template_name = "danh_muc/khachhang_list.html"
    context_object_name = "kh_list"
    ordering = ["ma_kh"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = (
                qs.filter(ma_kh__icontains=search)
                | qs.filter(ten_kh__icontains=search)
                | qs.filter(ma_so_thue__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("q", "")
        return ctx


class KhachHangCreateView(LoginRequiredMixin, CreateView):
    model = KhachHang
    template_name = "danh_muc/khachhang_form.html"
    fields = [
        "ma_kh",
        "ten_kh",
        "dia_chi",
        "ma_so_thue",
        "dien_thoai",
        "email",
        "so_gioi_thieu_dien_tu",
    ]
    success_url = reverse_lazy("danh_muc:khachhang_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        messages.success(self.request, f"Khách hàng {form.instance.ma_kh} đã được tạo.")
        return super().form_valid(form)


class KhachHangUpdateView(LoginRequiredMixin, UpdateView):
    model = KhachHang
    template_name = "danh_muc/khachhang_form.html"
    fields = [
        "ma_kh",
        "ten_kh",
        "dia_chi",
        "ma_so_thue",
        "dien_thoai",
        "email",
        "so_gioi_thieu_dien_tu",
    ]
    success_url = reverse_lazy("danh_muc:khachhang_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        messages.success(
            self.request, f"Khách hàng {form.instance.ma_kh} đã được cập nhật."
        )
        return super().form_valid(form)


class KhachHangDeleteView(LoginRequiredMixin, DeleteView):
    model = KhachHang
    template_name = "danh_muc/confirm_delete.html"
    success_url = reverse_lazy("danh_muc:khachhang_list")


# ==================== NHA CUNG CAP ====================


class NhaCungCapListView(LoginRequiredMixin, ListView):
    model = NhaCungCap
    template_name = "danh_muc/nhacungcap_list.html"
    context_object_name = "ncc_list"
    ordering = ["ma_ncc"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = (
                qs.filter(ma_ncc__icontains=search)
                | qs.filter(ten_ncc__icontains=search)
                | qs.filter(ma_so_thue__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("q", "")
        return ctx


class NhaCungCapCreateView(LoginRequiredMixin, CreateView):
    model = NhaCungCap
    template_name = "danh_muc/nhacungcap_form.html"
    fields = [
        "ma_ncc",
        "ten_ncc",
        "dia_chi",
        "ma_so_thue",
        "dien_thoai",
        "email",
        "tai_khoan_ngan_hang",
        "ngan_hang",
    ]
    success_url = reverse_lazy("danh_muc:nhacungcap_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        messages.success(
            self.request, f"Nhà cung cấp {form.instance.ma_ncc} đã được tạo."
        )
        return super().form_valid(form)


class NhaCungCapUpdateView(LoginRequiredMixin, UpdateView):
    model = NhaCungCap
    template_name = "danh_muc/nhacungcap_form.html"
    fields = [
        "ma_ncc",
        "ten_ncc",
        "dia_chi",
        "ma_so_thue",
        "dien_thoai",
        "email",
        "tai_khoan_ngan_hang",
        "ngan_hang",
    ]
    success_url = reverse_lazy("danh_muc:nhacungcap_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        messages.success(
            self.request, f"Nhà cung cấp {form.instance.ma_ncc} đã được cập nhật."
        )
        return super().form_valid(form)


class NhaCungCapDeleteView(LoginRequiredMixin, DeleteView):
    model = NhaCungCap
    template_name = "danh_muc/confirm_delete.html"
    success_url = reverse_lazy("danh_muc:nhacungcap_list")


# ==================== HANG HOA ====================


class HangHoaListView(LoginRequiredMixin, ListView):
    model = HangHoa
    template_name = "danh_muc/hanghoa_list.html"
    context_object_name = "hh_list"
    ordering = ["ma_hang_hoa"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = qs.filter(ma_hang_hoa__icontains=search) | qs.filter(
                ten_hang_hoa__icontains=search
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("q", "")
        return ctx


class HangHoaCreateView(LoginRequiredMixin, CreateView):
    model = HangHoa
    template_name = "danh_muc/hanghoa_form.html"
    fields = ["ma_hang_hoa", "ten_hang_hoa", "don_vi_tinh", "gia_mua", "gia_ban", "thue_suat_gtgt"]
    success_url = reverse_lazy("danh_muc:hanghoa_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        messages.success(
            self.request, f"Hàng hóa {form.instance.ma_hang_hoa} đã được tạo."
        )
        return super().form_valid(form)


class HangHoaUpdateView(LoginRequiredMixin, UpdateView):
    model = HangHoa
    template_name = "danh_muc/hanghoa_form.html"
    fields = ["ma_hang_hoa", "ten_hang_hoa", "don_vi_tinh", "gia_mua", "gia_ban", "thue_suat_gtgt"]
    success_url = reverse_lazy("danh_muc:hanghoa_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        messages.success(
            self.request, f"Hàng hóa {form.instance.ma_hang_hoa} đã được cập nhật."
        )
        return super().form_valid(form)


class HangHoaDeleteView(LoginRequiredMixin, DeleteView):
    model = HangHoa
    template_name = "danh_muc/confirm_delete.html"
    success_url = reverse_lazy("danh_muc:hanghoa_list")


# ==================== NGAN HANG ====================


class NganHangListView(LoginRequiredMixin, ListView):
    model = NganHang
    template_name = "danh_muc/nganhang_list.html"
    context_object_name = "nh_list"
    ordering = ["ma_ngan_hang"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = qs.filter(ma_ngan_hang__icontains=search) | qs.filter(
                ten_ngan_hang__icontains=search
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("q", "")
        return ctx


class NganHangCreateView(LoginRequiredMixin, CreateView):
    model = NganHang
    template_name = "danh_muc/nganhang_form.html"
    fields = ["ma_ngan_hang", "ten_ngan_hang", "ma_dien_toan", "dia_chi"]
    success_url = reverse_lazy("danh_muc:nganhang_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        messages.success(
            self.request, f"Ngân hàng {form.instance.ma_ngan_hang} đã được tạo."
        )
        return super().form_valid(form)


class NganHangUpdateView(LoginRequiredMixin, UpdateView):
    model = NganHang
    template_name = "danh_muc/nganhang_form.html"
    fields = ["ma_ngan_hang", "ten_ngan_hang", "ma_dien_toan", "dia_chi"]
    success_url = reverse_lazy("danh_muc:nganhang_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        messages.success(
            self.request, f"Ngân hàng {form.instance.ma_ngan_hang} đã được cập nhật."
        )
        return super().form_valid(form)


class NganHangDeleteView(LoginRequiredMixin, DeleteView):
    model = NganHang
    template_name = "danh_muc/confirm_delete.html"
    success_url = reverse_lazy("danh_muc:nganhang_list")


# ==================== DON VI ====================


class DonViListView(LoginRequiredMixin, ListView):
    model = DonVi
    template_name = "danh_muc/donvi_list.html"
    context_object_name = "dv_list"
    ordering = ["ten_don_vi"]
    paginate_by = 20


# ==================== DASHBOARD ====================


class DanhMucDashboardView(LoginRequiredMixin, ListView):
    model = TaiKhoanKeToan
    template_name = "danh_muc/dashboard.html"
    context_object_name = "taikhoan_list"

    def get_queryset(self):
        return TaiKhoanKeToan.objects.filter(cap_do=1).order_by("ma_tai_khoan")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["kh_count"] = KhachHang.objects.count()
        ctx["ncc_count"] = NhaCungCap.objects.count()
        ctx["hh_count"] = HangHoa.objects.count()
        ctx["nh_count"] = NganHang.objects.count()
        return ctx
