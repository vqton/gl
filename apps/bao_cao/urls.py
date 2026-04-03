"""URL configuration for BaoCao module."""

from django.urls import path

from apps.bao_cao import views

app_name = "bao_cao"

urlpatterns = [
    path("bang-cdk/", views.BangCanDoiKeToanView.as_view(), name="bang_cdk"),
    path("kqkd/", views.BaoCaoKQKDView.as_view(), name="kqkd"),
    path("bcd-sps/", views.BangCanDoiSoPhatSinhView.as_view(), name="bcd_sps"),
    path("lctt/", views.BaoCaoLuuChuyenTienTeView.as_view(), name="lctt"),
    path("thuyet-minh/", views.ThuyetMinhBCTCView.as_view(), name="thuyet_minh"),
    path("so-cai/<str:ma_tai_khoan>/", views.SoCaiTaiKhoanView.as_view(), name="so_cai_chi_tiet"),
    path("tong-hop-so-cai/", views.TongHopSoCaiView.as_view(), name="tong_hop_so_cai"),
    path("ban-hang/", views.BaoCaoBanHangView.as_view(), name="ban_hang"),
]
