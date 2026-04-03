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
    # Giấy tạm ứng (03-TT)
    path(
        "giay-tam-ung/",
        views.GiayTamUngListView.as_view(),
        name="giay_tam_ung_list",
    ),
    path(
        "giay-tam-ung/tao-moi/",
        views.GiayTamUngCreateView.as_view(),
        name="giay_tam_ung_create",
    ),
    path(
        "giay-tam-ung/<int:pk>/",
        views.GiayTamUngDetailView.as_view(),
        name="giay_tam_ung_detail",
    ),
    # Giấy thanh toán tạm ứng (04-TT)
    path(
        "tam-ung-thanh-toan/",
        views.TamUngSettlementListView.as_view(),
        name="tam_ung_settlement_list",
    ),
    path(
        "tam-ung-thanh-toan/tao-moi/",
        views.TamUngSettlementCreateView.as_view(),
        name="tam_ung_settlement_create",
    ),
]
