"""URL routing for Phân Tích Tài Chính."""

from django.urls import path

from . import views

app_name = "phan_tich"

urlpatterns = [
    path(
        "dashboard/",
        views.DashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "api/tong-hop/",
        views.api_tong_hop,
        name="api_tong_hop",
    ),
    path(
        "api/trend/",
        views.api_trend,
        name="api_trend",
    ),
]
