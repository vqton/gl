"""Signals to protect master data from modification."""

import logging

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from apps.danh_muc.models import TaiKhoanKeToan

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=TaiKhoanKeToan)
def protect_immutable_account(sender, instance, **kwargs):
    """
    Prevent modification of immutable (seeded) accounting accounts.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix II - Chart of Accounts
        - Master data must remain consistent with legal standard
    """
    if instance.pk:
        try:
            original = TaiKhoanKeToan.objects.get(pk=instance.pk)
            if original.is_immutable:
                immutable_fields = [
                    "ma_tai_khoan",
                    "ten_tai_khoan",
                    "cap_do",
                    "loai_tai_khoan",
                ]
                for field in immutable_fields:
                    if getattr(original, field) != getattr(instance, field):
                        raise ValidationError(
                            f"Không thể sửa tài khoản bất biến: "
                            f"{original.ma_tai_khoan} - {field}"
                        )
        except TaiKhoanKeToan.DoesNotExist:
            pass


@receiver(pre_delete, sender=TaiKhoanKeToan)
def prevent_immutable_account_deletion(sender, instance, **kwargs):
    """
    Prevent deletion of immutable (seeded) accounting accounts.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix II - Chart of Accounts
        - Seeded accounts are part of the legal accounting framework
    """
    if instance.is_immutable:
        raise ValidationError(
            f"Không thể xóa tài khoản bất biến: "
            f"{instance.ma_tai_khoan} - {instance.ten_tai_khoan}"
        )
