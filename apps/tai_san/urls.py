"""URL configuration for TaiSan module."""

from django.urls import path

from apps.tai_san import views

app_name = "tai_san"

urlpatterns = [
    path("", views.TaiSanListView.as_view(), name="taisan_list"),
    # Biên bản giao nhận TSCĐ
    path(
        "bien-ban-giao-nhan/",
        views.BienBanGiaoNhanTSCDListView.as_view(),
        name="bien_ban_giao_nhan_list",
    ),
    path(
        "bien-ban-giao-nhan/tao-moi/",
        views.BienBanGiaoNhanTSCDCreateView.as_view(),
        name="bien_ban_giao_nhan_create",
    ),
    # Biên bản thanh lý TSCĐ
    path(
        "bien-ban-thanh-ly/",
        views.BienBanThanhLyTSCDListView.as_view(),
        name="bien_ban_thanh_ly_list",
    ),
    path(
        "bien-ban-thanh-ly/tao-moi/",
        views.BienBanThanhLyTSCDCreateView.as_view(),
        name="bien_ban_thanh_ly_create",
    ),
    # Bảng khấu hao
    path(
        "khau-hao/",
        views.BangKhauHaoListView.as_view(),
        name="bang_khau_hao_list",
    ),
    path(
        "khau-hao/tao-moi/",
        views.BangKhauHaoCreateView.as_view(),
        name="bang_khau_hao_create",
    ),
]
