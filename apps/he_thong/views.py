"""He thong (System) views."""

import csv
import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from apps.he_thong.models import (AuditLog, CauHinhHeThong, KyKeToan,
                                  ThongTinCongTy, VaiTro)

logger = logging.getLogger(__name__)

NguoiDung = get_user_model()


def health_check(request):
    """
    System health endpoint.

    Returns JSON with status, DB integrity, disk space, and connection info.
    """
    data = {
        "status": "ok",
        "db_integrity": "ok",
        "disk_space_mb": 0.0,
        "last_backup": None,
        "active_connections": 1,
    }

    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result and result[0] != "ok":
            data["db_integrity"] = result[0]
            data["status"] = "degraded"
    except Exception as e:
        data["db_integrity"] = str(e)
        data["status"] = "error"

    try:
        db_path = connection.settings_dict["NAME"]
        if os.path.exists(db_path):
            total, used, free = shutil.disk_usage(db_path)
            data["disk_space_mb"] = round(free / (1024 * 1024), 1)
    except Exception:
        data["disk_space_mb"] = 0.0

    return JsonResponse(data)


def cong_ty_view(request):
    """Company information form (singleton CRUD)."""
    company = ThongTinCongTy.get_instance()

    if request.method == "POST":
        company.ten_cong_ty = request.POST.get("ten_cong_ty", "")
        company.ma_so_thue = request.POST.get("ma_so_thue", "")
        company.dia_chi = request.POST.get("dia_chi", "")
        company.dien_thoai = request.POST.get("dien_thoai", "")
        company.email = request.POST.get("email", "")
        company.nguoi_dai_dien = request.POST.get("nguoi_dai_dien", "")
        company.chuc_vu_ndd = request.POST.get("chuc_vu_ndd", "")
        company.ke_toan_truong = request.POST.get("ke_toan_truong", "")
        company.hinh_thuc_ke_toan = request.POST.get(
            "hinh_thuc_ke_toan", "nhat_ky_chung"
        )
        company.phuong_phap_gtgt = request.POST.get("phuong_phap_gtgt", "khau_tru")
        company.phuong_phap_ton_kho = request.POST.get(
            "phuong_phap_ton_kho", "binh_quan_lien_hoan"
        )
        company.save()
        return redirect("he_thong:cong_ty")

    return render(request, "he_thong/cong_ty.html", {"company": company})


def ky_ke_toan_list(request):
    """List all accounting periods."""
    periods = KyKeToan.objects.all()
    return render(
        request,
        "he_thong/ky_ke_toan_list.html",
        {"periods": periods},
    )


def ky_ke_toan_create(request):
    """Create a new accounting period."""
    if request.method == "POST":
        nam = int(request.POST.get("nam", 0))
        ngay_bat_dau = request.POST.get("ngay_bat_dau")
        ngay_ket_thuc = request.POST.get("ngay_ket_thuc")
        trang_thai = request.POST.get("trang_thai", "open")

        period = KyKeToan(
            nam=nam,
            ngay_bat_dau=ngay_bat_dau,
            ngay_ket_thuc=ngay_ket_thuc,
            trang_thai=trang_thai,
        )
        period.full_clean()
        period.save()
        return redirect("he_thong:ky_ke_toan_list")

    return render(request, "he_thong/ky_ke_toan_form.html")


def ky_ke_toan_lock(request, pk):
    """Lock an accounting period."""
    if request.method == "POST":
        period = KyKeToan.objects.get(pk=pk)
        period.lock()
    return redirect("he_thong:ky_ke_toan_list")


def ky_ke_toan_unlock(request, pk):
    """Unlock an accounting period."""
    if request.method == "POST":
        period = KyKeToan.objects.get(pk=pk)
        period.unlock()
    return redirect("he_thong:ky_ke_toan_list")


def cau_hinh_view(request):
    """System configuration form."""
    config = CauHinhHeThong.get_instance()

    if request.method == "POST":
        config.tien_te_mac_dinh = request.POST.get("tien_te_mac_dinh", "VND")
        config.ty_gia = request.POST.get("ty_gia", "1.0000")
        config.thue_tndn_15 = request.POST.get("thue_tndn_15", "15.00")
        config.thue_tndn_20 = request.POST.get("thue_tndn_20", "20.00")
        config.thue_vat_0 = request.POST.get("thue_vat_0", "0.00")
        config.thue_vat_5 = request.POST.get("thue_vat_5", "5.00")
        config.thue_vat_8 = request.POST.get("thue_vat_8", "8.00")
        config.thue_vat_10 = request.POST.get("thue_vat_10", "10.00")
        config.save()
        return redirect("he_thong:cau_hinh")

    return render(request, "he_thong/cau_hinh.html", {"config": config})


def audit_log_list(request):
    """Audit log viewer with filters."""
    logs = AuditLog.objects.all()

    user_filter = request.GET.get("user", "")
    action_filter = request.GET.get("action", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    if user_filter:
        logs = logs.filter(user__icontains=user_filter)
    if action_filter:
        logs = logs.filter(action__icontains=action_filter)
    if date_from:
        logs = logs.filter(timestamp__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__lte=date_to)

    logs = logs[:200]

    return render(
        request,
        "he_thong/audit_log_list.html",
        {
            "logs": logs,
            "user_filter": user_filter,
            "action_filter": action_filter,
            "date_from": date_from,
            "date_to": date_to,
        },
    )


def audit_log_export(request):
    """Export audit logs to CSV."""
    logs = AuditLog.objects.all()[:1000]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="audit_log_export.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Thời gian",
            "Người dùng",
            "Hành động",
            "URL",
            "IP",
            "Model",
            "Object ID",
            "Giá trị cũ",
            "Giá trị mới",
        ]
    )

    for log in logs:
        writer.writerow(
            [
                log.timestamp,
                log.user,
                log.action,
                log.url,
                log.ip_address,
                log.model_name,
                log.object_id,
                json_dumps_safe(log.old_value),
                json_dumps_safe(log.new_value),
            ]
        )

    return response


def json_dumps_safe(value):
    """Safely convert a value to JSON string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        import json

        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


@login_required
def nguoi_dung_list(request):
    """List all users with their roles."""
    users = NguoiDung.objects.select_related("vai_tro").all()
    return render(
        request,
        "he_thong/nguoi_dung_list.html",
        {"users": users},
    )


@login_required
def nguoi_dung_role_edit(request, pk):
    """Edit user role assignment."""
    user = NguoiDung.objects.get(pk=pk)
    roles = VaiTro.objects.all()

    if request.method == "POST":
        role_id = request.POST.get("vai_tro", "")
        if role_id:
            user.vai_tro = VaiTro.objects.get(pk=role_id)
        else:
            user.vai_tro = None
        user.save()
        messages.success(request, "Đã cập nhật vai trò cho người dùng.")
        return redirect("he_thong:nguoi_dung_list")

    return render(
        request,
        "he_thong/user_role_form.html",
        {"user_obj": user, "roles": roles},
    )


DB_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent / "core" / "db_config.json"
)


def is_first_run() -> bool:
    """Check if this is the first run (no valid config exists).

    Returns:
        True if db_config.json is missing, empty, or invalid.
    """
    try:
        if not DB_CONFIG_PATH.exists():
            return True

        content = DB_CONFIG_PATH.read_text(encoding="utf-8")
        if not content.strip():
            return True

        config = json.loads(content)
        return not config or "default" not in config
    except (json.JSONDecodeError, Exception):
        return True


def save_db_config(config_data: dict) -> None:
    """Save database configuration to JSON file with encrypted password.

    Args:
        config_data: Database configuration dictionary.
    """
    import json

    from apps.tien_ich.crypto import encrypt

    engine = config_data.get("database_type", "sqlite")
    db_name = config_data.get("db_name", "")

    config = {
        "default": {
            "engine": engine,
            "name": db_name,
        }
    }

    if engine != "sqlite":
        password = config_data.get("db_password", "")
        if password:
            config["default"]["password"] = encrypt(password)
        config["default"]["user"] = config_data.get("db_user", "")
        config["default"]["host"] = config_data.get("db_host", "localhost")
        config["default"]["port"] = int(config_data.get("db_port", 0))

    DB_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_CONFIG_PATH.write_text(
        json.dumps(config, indent=4, ensure_ascii=False), encoding="utf-8"
    )


def test_db_connection(config_data: dict) -> tuple[bool, str]:
    """Test database connection with provided config.

    Args:
        config_data: Database configuration dictionary.

    Returns:
        Tuple of (success, message).
    """
    engine = config_data.get("database_type", "sqlite")
    db_name = config_data.get("db_name", "")

    try:
        if engine == "sqlite":
            import sqlite3

            conn = sqlite3.connect(db_name)
            conn.close()
            return True, "Kết nối SQLite thành công"
        elif engine == "mysql":
            import pymysql

            conn = pymysql.connect(
                host=config_data.get("db_host", "localhost"),
                port=int(config_data.get("db_port", 3306)),
                user=config_data.get("db_user", ""),
                password=config_data.get("db_password", ""),
                database=db_name,
            )
            conn.close()
            return True, "Kết nối MySQL thành công"
        elif engine == "postgresql":
            import psycopg2

            conn = psycopg2.connect(
                host=config_data.get("db_host", "localhost"),
                port=int(config_data.get("db_port", 5432)),
                user=config_data.get("db_user", ""),
                password=config_data.get("db_password", ""),
                dbname=db_name,
            )
            conn.close()
            return True, "Kết nối PostgreSQL thành công"
        elif engine == "sqlserver":
            import pyodbc

            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={config_data.get('db_host', 'localhost')},"
                f"{config_data.get('db_port', 1433)};"
                f"DATABASE={db_name};"
                f"UID={config_data.get('db_user', '')};"
                f"PWD={config_data.get('db_password', '')}"
            )
            conn = pyodbc.connect(conn_str)
            conn.close()
            return True, "Kết nối SQL Server thành công"
        else:
            return False, f"Loại cơ sở dữ liệu không hỗ trợ: {engine}"
    except ImportError as e:
        return False, f"Thiếu thư viện: {e}"
    except Exception as e:
        return False, f"Không thể kết nối: {e}"


def setup_wizard(request):
    """Setup wizard view for first-run database configuration.

    Redirects to login if already configured.
    """
    if not is_first_run():
        return redirect("accounting:login")

    if request.method == "POST":
        action = request.POST.get("action", "save")

        if action == "test":
            config_data = {
                "database_type": request.POST.get("database_type", "sqlite"),
                "db_name": request.POST.get("db_name", ""),
                "db_host": request.POST.get("db_host", ""),
                "db_port": request.POST.get("db_port", ""),
                "db_user": request.POST.get("db_user", ""),
                "db_password": request.POST.get("db_password", ""),
            }
            success, message = test_db_connection(config_data)
            return JsonResponse({"success": success, "message": message})

        elif action == "save":
            config_data = {
                "database_type": request.POST.get("database_type", "sqlite"),
                "db_name": request.POST.get("db_name", ""),
                "db_host": request.POST.get("db_host", ""),
                "db_port": request.POST.get("db_port", ""),
                "db_user": request.POST.get("db_user", ""),
                "db_password": request.POST.get("db_password", ""),
            }
            save_db_config(config_data)
            messages.success(request, "Đã lưu cấu hình cơ sở dữ liệu.")
            return redirect("accounting:login")

    return render(request, "he_thong/setup_wizard.html")


def setup_test_connection(request):
    """AJAX endpoint for testing database connection.

    Returns:
        JSON response with success status and message.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST

        config_data = {
            "database_type": data.get("database_type", "sqlite"),
            "db_name": data.get("db_name", ""),
            "db_host": data.get("db_host", ""),
            "db_port": data.get("db_port", ""),
            "db_user": data.get("db_user", ""),
            "db_password": data.get("db_password", ""),
        }
        success, message = test_db_connection(config_data)
        return JsonResponse({"success": success, "message": message})

    return JsonResponse({"success": False, "message": "Method not allowed"})


# ==================== DB Management Views ====================

from apps.tien_ich.db_manager import DBManager


@login_required
def db_management(request):
    """Database management dashboard.

    Shows health status, backup list, and management actions.
    """
    manager = DBManager()
    health = manager.health_check()

    # Get backup list
    backup_dir = Path(settings.BASE_DIR) / "data" / "backups"
    backups = []
    if backup_dir.exists():
        for f in sorted(backup_dir.glob("*.zip"), reverse=True):
            backups.append(
                {
                    "name": f.name,
                    "path": str(f),
                    "size_mb": round(f.stat().st_size / 1024 / 1024, 2),
                    "created": datetime.fromtimestamp(f.stat().st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

    context = {
        "health": health,
        "backups": backups,
        "total_backups": len(backups),
    }
    return render(request, "he_thong/db_management.html", context)


@login_required
def db_backup(request):
    """Create database backup.

    POST: Creates backup and returns path.
    """
    if request.method == "POST":
        try:
            manager = DBManager()
            prefix = request.POST.get("prefix", "backup")
            backup_path = manager.backup(prefix=prefix)
            messages.success(request, f"Sao lưu thành công: {Path(backup_path).name}")
            return redirect("he_thong:db_management")
        except Exception as e:
            messages.error(request, f"Lỗi sao lưu: {e}")
            return redirect("he_thong:db_management")
    return redirect("he_thong:db_management")


@login_required
def db_restore(request):
    """Restore database from backup.

    POST: Restores from specified backup file.
    """
    if request.method == "POST":
        backup_path = request.POST.get("backup_path")
        confirmation = request.POST.get("confirmation")
        if not confirmation:
            messages.error(request, "Vui lòng xác nhận khôi phục dữ liệu")
            return redirect("he_thong:db_management")

        try:
            manager = DBManager()
            result = manager.restore(backup_path)
            messages.success(request, "Khôi phục dữ liệu thành công")
            return redirect("he_thong:db_management")
        except Exception as e:
            messages.error(request, f"Lỗi khôi phục: {e}")
            return redirect("he_thong:db_management")
    return redirect("he_thong:db_management")


@login_required
def db_vacuum(request):
    """Run VACUUM to reclaim space.

    POST: Runs VACUUM and shows results.
    """
    if request.method == "POST":
        try:
            manager = DBManager()
            result = manager.vacuum()
            messages.success(
                request,
                f"Tối ưu CSDL: {result['before_mb']} MB → {result['after_mb']} MB",
            )
        except Exception as e:
            messages.error(request, f"Lỗi tối ưu: {e}")
        return redirect("he_thong:db_management")
    return redirect("he_thong:db_management")


@login_required
def db_export(request):
    """Export database to JSON.

    GET/POST: Exports master data to JSON file for download.
    """
    if request.method == "POST":
        try:
            manager = DBManager()
            export_path = manager.export_data(format="json")
            # Return file for download
            with open(export_path, "rb") as f:
                response = HttpResponse(f.read(), content_type="application/json")
                response["Content-Disposition"] = (
                    f'attachment; filename="{Path(export_path).name}"'
                )
            return response
        except Exception as e:
            messages.error(request, f"Lỗi xuất dữ liệu: {e}")
            return redirect("he_thong:db_management")
    return redirect("he_thong:db_management")


# ==================== Client Management Views ====================

from django.db import models

from apps.he_thong.models import Client, ClientUserMapping
from apps.tien_ich.client_manager import ClientManager


@login_required
def client_list(request):
    """Client list for accounting firms."""
    status_filter = request.GET.get("status", "")
    search = request.GET.get("search", "")

    clients = Client.objects.all()
    if status_filter:
        clients = clients.filter(trang_thai=status_filter)
    if search:
        clients = clients.filter(
            models.Q(ten_cong_ty__icontains=search)
            | models.Q(ma_so_thue__icontains=search)
            | models.Q(ma_khach_hang__icontains=search)
        )

    context = {
        "clients": clients,
        "status_filter": status_filter,
        "search": search,
    }
    return render(request, "he_thong/client_list.html", context)


@login_required
def client_onboard(request):
    """Client onboarding wizard."""
    if request.method == "POST":
        try:
            client_data = {
                "ten_cong_ty": request.POST.get("ten_cong_ty"),
                "ma_so_thue": request.POST.get("ma_so_thue"),
                "nganh_nghe": request.POST.get("nganh_nghe", ""),
                "nam": int(request.POST.get("nam", 2026)),
            }
            manager = ClientManager()
            client = manager.onboard(client_data)
            messages.success(
                request,
                f"Khách hàng {client.ma_khach_hang} - {client.ten_cong_ty} đã được tạo thành công",
            )
            return redirect("he_thong:client_list")
        except Exception as e:
            messages.error(request, f"Lỗi tạo khách hàng: {e}")

    return render(request, "he_thong/client_onboard.html")


@login_required
def client_suspend(request, pk):
    """Suspend client access."""
    if request.method == "POST":
        try:
            manager = ClientManager()
            client = manager.suspend(pk)
            messages.success(request, f"Đã tạm khóa khách hàng {client.ma_khach_hang}")
        except Exception as e:
            messages.error(request, f"Lỗi: {e}")
    return redirect("he_thong:client_list")


@login_required
def client_activate(request, pk):
    """Activate suspended client."""
    if request.method == "POST":
        try:
            manager = ClientManager()
            client = manager.activate(pk)
            messages.success(request, f"Đã kích hoạt khách hàng {client.ma_khach_hang}")
        except Exception as e:
            messages.error(request, f"Lỗi: {e}")
    return redirect("he_thong:client_list")


@login_required
def client_archive(request, pk):
    """Archive client."""
    if request.method == "POST":
        try:
            manager = ClientManager()
            archive_path = manager.archive(pk)
            messages.success(request, f"Đã lưu trữ khách hàng: {archive_path}")
        except Exception as e:
            messages.error(request, f"Lỗi: {e}")
    return redirect("he_thong:client_list")


@login_required
def client_batch_backup(request):
    """Backup all active clients."""
    if request.method == "POST":
        try:
            manager = ClientManager()
            results = manager.batch_backup()
            success_count = len(results["success"])
            failed_count = len(results["failed"])
            messages.success(
                request,
                f"Sao lưu hàng loạt: {success_count} thành công, {failed_count} thất bại",
            )
            if results["failed"]:
                for fail in results["failed"]:
                    messages.warning(
                        request,
                        f"Thất bại: {fail['client']} - {fail['error']}",
                    )
        except Exception as e:
            messages.error(request, f"Lỗi sao lưu hàng loạt: {e}")
    return redirect("he_thong:client_list")
