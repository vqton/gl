"""Management command to execute year-end closing."""

from datetime import date

from django.core.management.base import BaseCommand, CommandError

from apps.nghiep_vu.ket_chuyen import ket_chuyen_cuoi_ky


class Command(BaseCommand):
    help = "Execute year-end closing (Kết chuyển TK 911)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tu-ngay",
            type=str,
            help="Start date (YYYY-MM-DD). Default: Jan 1 of current year",
        )
        parser.add_argument(
            "--den-ngay",
            type=str,
            help="End date (YYYY-MM-DD). Default: Dec 31 of current year",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be closed without creating entries",
        )

    def handle(self, *args, **options):
        tu_ngay_str = options.get("tu_ngay")
        den_ngay_str = options.get("den_ngay")

        if tu_ngay_str:
            tu_ngay = date.fromisoformat(tu_ngay_str)
        else:
            tu_ngay = date(date.today().year, 1, 1)

        if den_ngay_str:
            den_ngay = date.fromisoformat(den_ngay_str)
        else:
            den_ngay = date(date.today().year, 12, 31)

        self.stdout.write(self.style.WARNING(f"Kết chuyển kỳ {tu_ngay} đến {den_ngay}"))

        if options["dry_run"]:
            self.stdout.write("DRY RUN - Không tạo bút toán")
            from apps.nghiep_vu.ket_chuyen import (
                DOANH_THU_ACCOUNTS,
                CHI_PHI_ACCOUNTS,
                get_tong_phatsinh,
            )

            for tk in DOANH_THU_ACCOUNTS:
                no, co = get_tong_phatsinh(tk, tu_ngay, den_ngay)
                if co > 0:
                    self.stdout.write(f"  {tk}: Nợ {no} / Có {co}")
            for tk in CHI_PHI_ACCOUNTS:
                no, co = get_tong_phatsinh(tk, tu_ngay, den_ngay)
                if no > 0:
                    self.stdout.write(f"  {tk}: Nợ {no} / Có {co}")
            return

        try:
            result = ket_chuyen_cuoi_ky(tu_ngay, den_ngay)
            self.stdout.write(
                self.style.SUCCESS(f'Doanh thu: {result["doanh_thu"]:,.0f} VND')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Chi phí: {result["chi_phi"]:,.0f} VND')
            )
            if result["loi_nhuan"] >= 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Lợi nhuận: {result["loi_nhuan"]:,.0f} VND')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Lỗ: {abs(result["loi_nhuan"]):,.0f} VND')
                )
            self.stdout.write(f'Số bút toán: {len(result["but_toan_list"])}')
        except Exception as e:
            raise CommandError(f"Kết chuyển thất bại: {e}")
