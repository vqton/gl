"""URL configuration for Luong module."""

from django.urls import path

from apps.luong import views

app_name = "luong"

urlpatterns = [
    path("", views.NhanVienListView.as_view(), name="nhanvien_list"),
    path("bang-luong/", views.BangLuongListView.as_view(), name="bangluong_list"),
]
