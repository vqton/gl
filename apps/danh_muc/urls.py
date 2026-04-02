"""URL configuration for danh_muc (Master Data) module."""

from django.urls import path

from apps.danh_muc import views

app_name = "danh_muc"

urlpatterns = [
    path("", views.DanhMucDashboardView.as_view(), name="dashboard"),
    # Tai khoan
    path("tai-khoan/", views.TaiKhoanListView.as_view(), name="taikhoan_list"),
    path(
        "tai-khoan/tao-moi/", views.TaiKhoanCreateView.as_view(), name="taikhoan_create"
    ),
    path(
        "tai-khoan/<int:pk>/",
        views.TaiKhoanUpdateView.as_view(),
        name="taikhoan_update",
    ),
    path(
        "tai-khoan/<int:pk>/xoa/",
        views.TaiKhoanDeleteView.as_view(),
        name="taikhoan_delete",
    ),
    # Khach hang
    path("khach-hang/", views.KhachHangListView.as_view(), name="khachhang_list"),
    path(
        "khach-hang/tao-moi/",
        views.KhachHangCreateView.as_view(),
        name="khachhang_create",
    ),
    path(
        "khach-hang/<int:pk>/",
        views.KhachHangUpdateView.as_view(),
        name="khachhang_update",
    ),
    path(
        "khach-hang/<int:pk>/xoa/",
        views.KhachHangDeleteView.as_view(),
        name="khachhang_delete",
    ),
    # Nha cung cap
    path("nha-cung-cap/", views.NhaCungCapListView.as_view(), name="nhacungcap_list"),
    path(
        "nha-cung-cap/tao-moi/",
        views.NhaCungCapCreateView.as_view(),
        name="nhacungcap_create",
    ),
    path(
        "nha-cung-cap/<int:pk>/",
        views.NhaCungCapUpdateView.as_view(),
        name="nhacungcap_update",
    ),
    path(
        "nha-cung-cap/<int:pk>/xoa/",
        views.NhaCungCapDeleteView.as_view(),
        name="nhacungcap_delete",
    ),
    # Hang hoa
    path("hang-hoa/", views.HangHoaListView.as_view(), name="hanghoa_list"),
    path("hang-hoa/tao-moi/", views.HangHoaCreateView.as_view(), name="hanghoa_create"),
    path(
        "hang-hoa/<int:pk>/", views.HangHoaUpdateView.as_view(), name="hanghoa_update"
    ),
    path(
        "hang-hoa/<int:pk>/xoa/",
        views.HangHoaDeleteView.as_view(),
        name="hanghoa_delete",
    ),
    # Ngan hang
    path("ngan-hang/", views.NganHangListView.as_view(), name="nganhang_list"),
    path(
        "ngan-hang/tao-moi/", views.NganHangCreateView.as_view(), name="nganhang_create"
    ),
    path(
        "ngan-hang/<int:pk>/",
        views.NganHangUpdateView.as_view(),
        name="nganhang_update",
    ),
    path(
        "ngan-hang/<int:pk>/xoa/",
        views.NganHangDeleteView.as_view(),
        name="nganhang_delete",
    ),
    # Don vi
    path("don-vi/", views.DonViListView.as_view(), name="donvi_list"),
]
