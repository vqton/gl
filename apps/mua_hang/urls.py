"""URL configuration for Mua hàng app."""

from django.urls import path

from apps.mua_hang import views

app_name = "mua_hang"

urlpatterns = [
    path("de-xuat/", views.DeXuatMuaHangListView.as_view(), name="de_xuat_list"),
    path("de-xuat/tao-moi/", views.DeXuatMuaHangCreateView.as_view(), name="de_xuat_create"),
    path("de-xuat/<int:pk>/", views.DeXuatMuaHangDetailView.as_view(), name="de_xuat_detail"),
    path("don-dat-hang/", views.DonDatHangListView.as_view(), name="don_hang_list"),
    path("don-dat-hang/tao-moi/", views.DonDatHangCreateView.as_view(), name="don_hang_create"),
    path("don-dat-hang/<int:pk>/", views.DonDatHangDetailView.as_view(), name="don_hang_detail"),
    path("don-dat-hang/<int:pk>/xoa/", views.DonDatHangDeleteView.as_view(), name="don_hang_delete"),
    path("tra-hang/", views.TraHangNCCListView.as_view(), name="tra_hang_list"),
    path("tra-hang/tao-moi/", views.TraHangNCCCreateView.as_view(), name="tra_hang_create"),
    path("tra-hang/<int:pk>/", views.TraHangNCCDetailView.as_view(), name="tra_hang_detail"),
]
