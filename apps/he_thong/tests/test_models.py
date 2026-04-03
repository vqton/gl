"""Tests for he_thong models."""

from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.he_thong.models import AuditLog, CauHinhHeThong, KyKeToan, ThongTinCongTy


@pytest.mark.django_db
class TestThongTinCongTy:
    """Test company info singleton model."""

    def test_singleton_enforcement(self):
        """Test that only one instance can exist with pk=1."""
        company = ThongTinCongTy.objects.create(
            ten_cong_ty="Test Company",
            ma_so_thue="0123456789",
        )
        assert company.pk == 1

        company2 = ThongTinCongTy(
            ten_cong_ty="Another Company",
            ma_so_thue="9876543210",
        )
        company2.save()
        assert company2.pk == 1
        assert ThongTinCongTy.objects.count() == 1

    def test_delete_prevented(self):
        """Test that singleton cannot be deleted."""
        company = ThongTinCongTy.objects.create(
            ten_cong_ty="Test Company",
            ma_so_thue="0123456789",
        )
        with pytest.raises(ValidationError, match="Không được xóa"):
            company.delete()

    def test_get_instance(self):
        """Test get_or_create singleton accessor."""
        instance = ThongTinCongTy.get_instance()
        assert instance.pk == 1

        instance2 = ThongTinCongTy.get_instance()
        assert instance.pk == instance2.pk

    def test_full_fields(self):
        """Test all fields can be set."""
        company = ThongTinCongTy.objects.create(
            ten_cong_ty="Công ty TNHH ABC",
            ma_so_thue="0123456789",
            dia_chi="123 Đường Láng, Hà Nội",
            dien_thoai="02412345678",
            email="info@abc.vn",
            nguoi_dai_dien="Nguyễn Văn A",
            chuc_vu_ndd="Giám đốc",
            ke_toan_truong="Trần Thị B",
            hinh_thuc_ke_toan="nhat_ky_chung",
            phuong_phap_gtgt="khau_tru",
            phuong_phap_ton_kho="binh_quan_lien_hoan",
        )
        assert company.ten_cong_ty == "Công ty TNHH ABC"
        assert company.ma_so_thue == "0123456789"
        assert company.hinh_thuc_ke_toan == "nhat_ky_chung"
        assert company.phuong_phap_gtgt == "khau_tru"
        assert company.phuong_phap_ton_kho == "binh_quan_lien_hoan"


@pytest.mark.django_db
class TestKyKeToan:
    """Test accounting period model."""

    def test_create_open_period(self):
        """Test creating an open accounting period."""
        period = KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="open",
        )
        assert period.is_postable() is True
        assert period.trang_thai == "open"

    def test_lock_period(self):
        """Test locking a period blocks posting."""
        period = KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="open",
        )
        period.lock()
        assert period.trang_thai == "locked"
        assert period.is_postable() is False

    def test_unlock_period(self):
        """Test unlocking a period allows posting."""
        period = KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="locked",
        )
        period.unlock()
        assert period.trang_thai == "open"
        assert period.is_postable() is True

    def test_invalid_date_range(self):
        """Test that end date must be after start date."""
        period = KyKeToan(
            nam=2026,
            ngay_bat_dau=date(2026, 12, 31),
            ngay_ket_thuc=date(2026, 1, 1),
        )
        with pytest.raises(ValidationError, match="Ngày kết thúc"):
            period.full_clean()

    def test_can_post_on_date(self):
        """Test can_post_on_date checks period status."""
        KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="open",
        )
        assert KyKeToan.can_post_on_date(date(2026, 6, 15)) is True

    def test_cannot_post_on_date_locked(self):
        """Test cannot post on date in locked period."""
        KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="locked",
        )
        assert KyKeToan.can_post_on_date(date(2026, 6, 15)) is False

    def test_cannot_post_on_date_no_period(self):
        """Test cannot post on date with no matching period."""
        assert KyKeToan.can_post_on_date(date(2026, 6, 15)) is False

    def test_get_open_periods(self):
        """Test getting all open periods."""
        KyKeToan.objects.create(
            nam=2026,
            ngay_bat_dau=date(2026, 1, 1),
            ngay_ket_thuc=date(2026, 12, 31),
            trang_thai="open",
        )
        KyKeToan.objects.create(
            nam=2025,
            ngay_bat_dau=date(2025, 1, 1),
            ngay_ket_thuc=date(2025, 12, 31),
            trang_thai="closed",
        )
        open_periods = KyKeToan.get_open_periods()
        assert open_periods.count() == 1
        assert open_periods.first().nam == 2026


@pytest.mark.django_db
class TestCauHinhHeThong:
    """Test system configuration model."""

    def test_singleton_enforcement(self):
        """Test that only one config instance exists."""
        config = CauHinhHeThong.objects.create(
            thue_tndn_15=Decimal("15.00"),
        )
        assert config.pk == 1

        config2 = CauHinhHeThong(thue_tndn_15=Decimal("20.00"))
        config2.save()
        assert config2.pk == 1
        assert CauHinhHeThong.objects.count() == 1

    def test_delete_prevented(self):
        """Test that config cannot be deleted."""
        config = CauHinhHeThong.objects.create()
        with pytest.raises(ValidationError, match="Không được xóa"):
            config.delete()

    def test_default_tax_rates(self):
        """Test default tax rates are correct."""
        config = CauHinhHeThong.get_instance()
        assert config.thue_tndn_15 == Decimal("15.00")
        assert config.thue_tndn_20 == Decimal("20.00")
        assert config.thue_vat_0 == Decimal("0.00")
        assert config.thue_vat_5 == Decimal("5.00")
        assert config.thue_vat_8 == Decimal("8.00")
        assert config.thue_vat_10 == Decimal("10.00")

    def test_default_currency(self):
        """Test default currency is VND."""
        config = CauHinhHeThong.get_instance()
        assert config.tien_te_mac_dinh == "VND"


@pytest.mark.django_db
class TestAuditLog:
    """Test audit log model."""

    def test_create_audit_log(self):
        """Test creating an audit log entry."""
        log = AuditLog.objects.create(
            user="admin",
            action="CREATE",
            url="/he-thong/cong-ty/",
            ip_address="127.0.0.1",
            model_name="ThongTinCongTy",
            object_id="1",
            new_value={"ten_cong_ty": "Test Company"},
        )
        assert log.user == "admin"
        assert log.action == "CREATE"
        assert log.model_name == "ThongTinCongTy"

    def test_audit_log_with_old_and_new(self):
        """Test audit log with old and new values."""
        log = AuditLog.objects.create(
            user="admin",
            action="UPDATE",
            model_name="ThongTinCongTy",
            object_id="1",
            old_value={"ten_cong_ty": "Old Name"},
            new_value={"ten_cong_ty": "New Name"},
        )
        assert log.old_value == {"ten_cong_ty": "Old Name"}
        assert log.new_value == {"ten_cong_ty": "New Name"}

    def test_audit_log_ordering(self):
        """Test audit logs are ordered by timestamp descending."""
        log1 = AuditLog.objects.create(
            user="admin",
            action="CREATE",
            model_name="Test",
        )
        log2 = AuditLog.objects.create(
            user="admin",
            action="UPDATE",
            model_name="Test",
        )
        logs = AuditLog.objects.all()
        assert logs[0] == log2
        assert logs[1] == log1
