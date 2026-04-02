"""Custom user model for Vietnamese SME Accounting System."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    ADMIN = "admin", _("Quản trị hệ thống")
    ACCOUNTANT = "accountant", _("Kế toán")
    VIEWER = "viewer", _("Người xem")


class NguoiDung(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds user type classification, company association, and system admin flag.
    """

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.VIEWER,
        verbose_name=_("Loại người dùng"),
    )
    company = models.ForeignKey(
        "danh_muc.DonVi",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nhan_vien",
        verbose_name=_("Đơn vị"),
    )
    is_system_admin = models.BooleanField(
        default=False,
        verbose_name=_("Quản trị viên hệ thống"),
        help_text=_("Người dùng có quyền quản trị toàn bộ hệ thống"),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name=_("Số điện thoại"),
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name=_("Phòng ban"),
    )

    class Meta:
        verbose_name = _("Người dùng")
        verbose_name_plural = _("Người dùng")
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_admin_user(self):
        """Check if user is admin type."""
        return self.user_type == UserType.ADMIN

    @property
    def is_accountant_user(self):
        """Check if user is accountant type."""
        return self.user_type == UserType.ACCOUNTANT

    @property
    def is_viewer_user(self):
        """Check if user is viewer type."""
        return self.user_type == UserType.VIEWER
