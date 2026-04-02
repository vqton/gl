"""URL routing for Giá Thành (Product Costing)."""

from django.urls import path

from . import views

app_name = "gia_thanh"

urlpatterns = [
    path(
        "doi-tuong/",
        views.DoiTuongListView.as_view(),
        name="doi_tuong_list",
    ),
    path(
        "tap-hop-chi-phi/",
        views.PhieuTapHopChiPhiListView.as_view(),
        name="tap_hop_chi_phi_list",
    ),
    path(
        "phan-bo-chi-phi/",
        views.PhanBoChiPhiView.as_view(),
        name="phan_bo_chi_phi",
    ),
    path(
        "bang-tinh-gia-thanh/",
        views.BangTinhGiaThanhListView.as_view(),
        name="bang_tinh_gia_thanh_list",
    ),
]
