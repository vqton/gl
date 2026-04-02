"""URL configuration for nghiep_vu app."""

from django.urls import path

from apps.nghiep_vu import views

app_name = "nghiep_vu"

urlpatterns = [
    path("", views.index, name="index"),
    # Phieu Thu
    path("phieu-thu/", views.PhieuThuListView.as_view(), name="phieu_thu_list"),
    path(
        "phieu-thu/tao-moi/",
        views.PhieuThuCreateView.as_view(),
        name="phieu_thu_create",
    ),
    path(
        "phieu-thu/<int:pk>/",
        views.PhieuThuDetailView.as_view(),
        name="phieu_thu_detail",
    ),
    path(
        "phieu-thu/<int:pk>/xoa/",
        views.PhieuThuDeleteView.as_view(),
        name="phieu_thu_delete",
    ),
    # Phieu Chi
    path("phieu-chi/", views.PhieuChiListView.as_view(), name="phieu_chi_list"),
    path(
        "phieu-chi/tao-moi/",
        views.PhieuChiCreateView.as_view(),
        name="phieu_chi_create",
    ),
    path(
        "phieu-chi/<int:pk>/",
        views.PhieuChiDetailView.as_view(),
        name="phieu_chi_detail",
    ),
    path(
        "phieu-chi/<int:pk>/xoa/",
        views.PhieuChiDeleteView.as_view(),
        name="phieu_chi_delete",
    ),
    # Hoa Don
    path("hoa-don/", views.HoaDonListView.as_view(), name="hoa_don_list"),
    path("hoa-don/tao-moi/", views.HoaDonCreateView.as_view(), name="hoa_don_create"),
    path("hoa-don/<int:pk>/", views.HoaDonDetailView.as_view(), name="hoa_don_detail"),
    path(
        "hoa-don/<int:pk>/xoa/", views.HoaDonDeleteView.as_view(), name="hoa_don_delete"
    ),
]
