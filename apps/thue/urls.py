"""URL configuration for Thuế app."""

from django.urls import path

from apps.thue import views

app_name = "thue"

urlpatterns = [
    path("bang-ke-mua-vao/", views.BangKeMuaVaoListView.as_view(), name="bang_ke_mua_vao"),
    path("bang-ke-ban-ra/", views.BangKeBanRaListView.as_view(), name="bang_ke_ban_ra"),
    path("to-khai-gtgt/", views.ToKhaiGTGTListView.as_view(), name="to_khai_gtgt_list"),
    path("to-khai-gtgt/tao-moi/", views.ToKhaiGTGTCreateView.as_view(), name="to_khai_gtgt_create"),
    path("to-khai-gtgt/<int:pk>/", views.ToKhaiGTGTDetailView.as_view(), name="to_khai_gtgt_detail"),
    path("to-khai-tndn/", views.ToKhaiTNDNListView.as_view(), name="to_khai_tndn_list"),
    path("to-khai-tncn/", views.ToKhaiTNCNListView.as_view(), name="to_khai_tncn_list"),
]
