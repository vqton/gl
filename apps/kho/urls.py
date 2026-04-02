"""URL configuration for Kho module."""

from django.urls import path

from apps.kho import views

app_name = "kho"

urlpatterns = [
    path("", views.KhoListView.as_view(), name="kho_list"),
    path("nhap-xuat/", views.KhoEntryListView.as_view(), name="kho_entry_list"),
    path("ton-kho/", views.TonKhoListView.as_view(), name="ton_kho_list"),
]
