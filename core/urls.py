"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.accounting.urls')),
    path('admin/', admin.site.urls),
    path('nghiep-vu/', include('apps.nghiep_vu.urls')),
    path('danh-muc/', include('apps.danh_muc.urls')),
    path('kho/', include('apps.kho.urls')),
    path('tai-san/', include('apps.tai_san.urls')),
    path('luong/', include('apps.luong.urls')),
    path('bao-cao/', include('apps.bao_cao.urls')),
    path('ngan-hang/', include('apps.ngan_hang.urls')),
    path('cong-no/', include('apps.cong_no.urls')),
    path('so-sach/', include('apps.so_sach.urls')),
    path('ccdc/', include('apps.ccdc.urls')),
    path('thue/', include('apps.thue.urls')),
    path('mua-hang/', include('apps.mua_hang.urls')),
    path('gia-thanh/', include('apps.gia_thanh.urls')),
    path('thu-quy/', include('apps.thu_quy.urls')),
    path('phan-tich/', include('apps.phan_tich.urls')),
]
