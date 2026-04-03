from django.db import migrations


def update_account_157_name(apps, schema_editor):
    """Update account 157 name per TT 99/2025/TT-BTC."""
    TaiKhoanKeToan = apps.get_model("danh_muc", "TaiKhoanKeToan")
    TaiKhoanKeToan.objects.filter(ma_tai_khoan="157").update(
        ten_tai_khoan="Hàng gửi đi bán",
        mo_ta="Hàng hóa, thành phẩm gửi bán đại lý, ký gửi"
    )


def reverse_update(apps, schema_editor):
    """Reverse the update."""
    TaiKhoanKeToan = apps.get_model("danh_muc", "TaiKhoanKeToan")
    TaiKhoanKeToan.objects.filter(ma_tai_khoan="157").update(
        ten_tai_khoan="Bất động sản chờ bán",
        mo_ta="Bất động sản đang chờ bán"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("danh_muc", "0005_seed_coa_tt99_full"),
    ]

    operations = [
        migrations.RunPython(update_account_157_name, reverse_update),
    ]