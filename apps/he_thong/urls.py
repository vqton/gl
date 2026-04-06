"""He thong (System) URL configuration."""

from django.urls import path

from apps.he_thong import views

app_name = "he_thong"

urlpatterns = [
    path("setup/", views.setup_wizard, name="setup_wizard"),
    path(
        "setup/test-connection/",
        views.setup_test_connection,
        name="setup_test_connection",
    ),
    path("health/", views.health_check, name="health"),
    path("cong-ty/", views.cong_ty_view, name="cong_ty"),
    path(
        "ky-ke-toan/",
        views.ky_ke_toan_list,
        name="ky_ke_toan_list",
    ),
    path(
        "ky-ke-toan/them/",
        views.ky_ke_toan_create,
        name="ky_ke_toan_create",
    ),
    path(
        "ky-ke-toan/<int:pk>/lock/",
        views.ky_ke_toan_lock,
        name="ky_ke_toan_lock",
    ),
    path(
        "ky-ke-toan/<int:pk>/unlock/",
        views.ky_ke_toan_unlock,
        name="ky_ke_toan_unlock",
    ),
    path("cau-hinh/", views.cau_hinh_view, name="cau_hinh"),
    path("audit-log/", views.audit_log_list, name="audit_log_list"),
    path(
        "audit-log/export/",
        views.audit_log_export,
        name="audit_log_export",
    ),
    path("nguoi-dung/", views.nguoi_dung_list, name="nguoi_dung_list"),
    path(
        "nguoi-dung/<int:pk>/vai-tro/",
        views.nguoi_dung_role_edit,
        name="nguoi_dung_role_edit",
    ),
    # DB Management
    path("quan-ly-csdl/", views.db_management, name="db_management"),
    path("quan-ly-csdl/backup/", views.db_backup, name="db_backup"),
    path("quan-ly-csdl/restore/", views.db_restore, name="db_restore"),
    path("quan-ly-csdl/vacuum/", views.db_vacuum, name="db_vacuum"),
    path("quan-ly-csdl/export/", views.db_export, name="db_export"),
]
