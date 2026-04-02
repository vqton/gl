"""URL configuration for Ngân hàng app."""

from django.urls import path

from apps.ngan_hang import views

app_name = "ngan_hang"

urlpatterns = [
    path("giay-bao-no/", views.GiayBaoNoListView.as_view(), name="giay_bao_no_list"),
    path("giay-bao-no/tao-moi/", views.GiayBaoNoCreateView.as_view(), name="giay_bao_no_create"),
    path("giay-bao-no/<int:pk>/", views.GiayBaoNoDetailView.as_view(), name="giay_bao_no_detail"),
    path("giay-bao-no/<int:pk>/xoa/", views.GiayBaoNoDeleteView.as_view(), name="giay_bao_no_delete"),
    path("giay-bao-co/", views.GiayBaoCoListView.as_view(), name="giay_bao_co_list"),
    path("giay-bao-co/tao-moi/", views.GiayBaoCoCreateView.as_view(), name="giay_bao_co_create"),
    path("giay-bao-co/<int:pk>/", views.GiayBaoCoDetailView.as_view(), name="giay_bao_co_detail"),
    path("giay-bao-co/<int:pk>/xoa/", views.GiayBaoCoDeleteView.as_view(), name="giay_bao_co_delete"),
    path("uy-nhiem-chi/", views.UyNhiemChiListView.as_view(), name="uy_nhiem_chi_list"),
    path("uy-nhiem-chi/tao-moi/", views.UyNhiemChiCreateView.as_view(), name="uy_nhiem_chi_create"),
    path("uy-nhiem-chi/<int:pk>/", views.UyNhiemChiDetailView.as_view(), name="uy_nhiem_chi_detail"),
    path("doi-chieu/", views.DoiChieuNganHangListView.as_view(), name="doi_chieu_list"),
    path("doi-chieu/tao-moi/", views.DoiChieuNganHangCreateView.as_view(), name="doi_chieu_create"),
    path("doi-chieu/<int:pk>/", views.DoiChieuNganHangDetailView.as_view(), name="doi_chieu_detail"),
]
