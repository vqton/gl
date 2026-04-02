"""Login and auth views for web app."""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    template_name = "accounting/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("accounting:dashboard")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "accounting:dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounting:login")


def dashboard(request):
    """Main dashboard - role-based."""
    if not request.user.is_authenticated:
        return redirect("accounting:login")

    from apps.nghiep_vu.models import HoaDon, PhieuThu, PhieuChi
    from apps.kho.models import KhoEntry

    context = {
        "hoa_don_count": HoaDon.objects.count(),
        "phieu_thu_count": PhieuThu.objects.count(),
        "phieu_chi_count": PhieuChi.objects.count(),
        "kho_entry_count": KhoEntry.objects.count(),
    }

    return render(request, "accounting/dashboard.html", context)


def permission_denied(request, exception=None):
    """403 error page."""
    return render(request, "accounting/403.html", status=403)


def page_not_found(request, exception=None):
    """404 error page."""
    return render(request, "accounting/404.html", status=404)
