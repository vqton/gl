"""Signals for backdating detection and recalculation triggers."""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.kho.models import KhoEntry, KhoLot
from apps.kho.services import tinh_lai_gia_von

logger = logging.getLogger(__name__)


@receiver(post_save, sender=KhoEntry)
def kho_entry_modified(sender, instance, created, update_fields=None, **kwargs):
    """
    Trigger recalculation when a KhoEntry is modified.

    When a past receipt entry is modified (price change),
    recalculate all subsequent entries for the same item.

    Skips if update_fields only contains recalculation-related fields
    to prevent infinite recursion.
    """
    if created:
        return

    if instance.loai != "NHAP":
        return

    if update_fields and all(
        f in ("gia_von_chinh_thuc", "da_dong_bo", "updated_at") for f in update_fields
    ):
        return

    hang_hoa_id = instance.hang_hoa_id
    start_date = instance.ngay_chung_tu

    logger.info(
        "Signal triggered: KhoEntry %s modified, " "recalculating from %s",
        instance.pk,
        start_date,
    )

    post_save.disconnect(kho_entry_modified, sender=KhoEntry)
    post_save.disconnect(kho_lot_modified, sender=KhoLot)
    try:
        tinh_lai_gia_von(hang_hoa_id, start_date)
    finally:
        post_save.connect(kho_entry_modified, sender=KhoEntry)
        post_save.connect(kho_lot_modified, sender=KhoLot)


@receiver(post_save, sender=KhoLot)
def kho_lot_modified(sender, instance, created, update_fields=None, **kwargs):
    """
    Trigger recalculation when a KhoLot is modified.

    When a lot's price or quantity is changed,
    recalculate all entries from that lot's date onwards.

    Skips if update_fields only contains so_luong_ton to prevent
    infinite recursion during xuat_kho.
    """
    if created:
        return

    if update_fields and set(update_fields) <= {"so_luong_ton", "updated_at"}:
        return

    hang_hoa_id = instance.hang_hoa_id
    start_date = instance.ngay_nhap

    logger.info(
        "Signal triggered: KhoLot %s modified, " "recalculating from %s",
        instance.pk,
        start_date,
    )

    post_save.disconnect(kho_entry_modified, sender=KhoEntry)
    post_save.disconnect(kho_lot_modified, sender=KhoLot)
    try:
        tinh_lai_gia_von(hang_hoa_id, start_date)
    finally:
        post_save.connect(kho_entry_modified, sender=KhoEntry)
        post_save.connect(kho_lot_modified, sender=KhoLot)
