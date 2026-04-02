"""URL configuration for CCDC app."""

from django.urls import path

from apps.ccdc import views

app_name = "ccdc"

urlpatterns = [
    path("ccdc/", views.CongCuDungCuListView.as_view(), name="ccdc_list"),
    path("ccdc/tao-moi/", views.CongCuDungCuCreateView.as_view(), name="ccdc_create"),
    path("ccdc/<int:pk>/", views.CongCuDungCuDetailView.as_view(), name="ccdc_detail"),
    path("ccdc/<int:pk>/xoa/", views.CongCuDungCuDeleteView.as_view(), name="ccdc_delete"),
    path("bang-phan-bo/", views.BangPhanBoCCDCListView.as_view(), name="bang_phan_bo_list"),
    path("bang-phan-bo/<int:pk>/", views.BangPhanBoCCDCDetailView.as_view(), name="bang_phan_bo_detail"),
]
