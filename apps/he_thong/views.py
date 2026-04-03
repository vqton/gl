"""He thong (System) views."""

import csv
import logging
import os
import shutil

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from apps.he_thong.models import (
    AuditLog,
    CauHinhHeThong,
    KyKeToan,
    ThongTinCongTy,
    VaiTro,
)

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
