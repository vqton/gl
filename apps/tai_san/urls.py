"""URL configuration for TaiSan module."""

from django.urls import path

from apps.tai_san import views

app_name = "tai_san"

urlpatterns = [
    path("", views.TaiSanListView.as_view(), name="taisan_list"),
]
