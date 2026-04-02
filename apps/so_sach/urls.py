"""URL configuration for Sổ sách app."""

from django.urls import path

from apps.so_sach import views

app_name = "so_sach"

urlpatterns = [
    path("nhat-ky-chung/", views.SoNhatKyChungView.as_view(), name="nhat_ky_chung"),
    path("so-quy/", views.SoQuyView.as_view(), name="so_quy"),
    path("so-ngan-hang/", views.SoNganHangView.as_view(), name="so_ngan_hang"),
]
