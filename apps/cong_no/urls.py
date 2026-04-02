"""URL configuration for Công nợ app."""

from django.urls import path

from apps.cong_no import views

app_name = "cong_no"

urlpatterns = [
    path("phai-thu/", views.CongNoPhaiThuListView.as_view(), name="phai_thu_list"),
    path("phai-thu/<int:pk>/", views.CongNoPhaiThuDetailView.as_view(), name="phai_thu_detail"),
    path("phai-tra/", views.CongNoPhaiTraListView.as_view(), name="phai_tra_list"),
    path("phai-tra/<int:pk>/", views.CongNoPhaiTraDetailView.as_view(), name="phai_tra_detail"),
    path("doi-chieu/", views.BienBanDoiChieuCongNoListView.as_view(), name="bien_ban_list"),
    path("doi-chieu/tao-moi/", views.BienBanDoiChieuCongNoCreateView.as_view(), name="bien_ban_create"),
    path("doi-chieu/<int:pk>/", views.BienBanDoiChieuCongNoDetailView.as_view(), name="bien_ban_detail"),
]
