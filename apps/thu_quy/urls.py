"""URL routing for Thủ Quỹ (Cashier Reconciliation)."""

from django.urls import path

from . import views

app_name = "thu_quy"

urlpatterns = [
    path(
        "kiem-ke-quy/",
        views.KiemKeQuyListView.as_view(),
        name="kiem_ke_quy_list",
    ),
    path(
        "xu-ly-chenh-lech/",
        views.XuLyChenhLechView.as_view(),
        name="xu_ly_chenh_lech",
    ),
    path(
        "so-quy-tien-mat/",
        views.SoQuyTienMatView.as_view(),
        name="so_quy_tien_mat",
    ),
]
