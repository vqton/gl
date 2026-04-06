"""Management command to create/update template database."""

import logging
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management import call_command

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create or update the template database with all migrations and seed data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="data/template_2026.sqlite3",
            help="Output path for template database",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        output_path.parent.mkdir(parents=True, exist_ok=True)

        self.stdout.write("Creating template database...")

        call_command("migrate", verbosity=1)
        self.stdout.write(self.style.SUCCESS("Migrations applied."))

        try:
            call_command("loaddata", "apps/danh_muc/fixtures/seed_accounts.json")
            self.stdout.write(self.style.SUCCESS("Chart of accounts loaded."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Seed data warning: {e}"))

        db_path = Path("db/accounting_tt99.sqlite3")
        if db_path.exists():
            shutil.copy2(str(db_path), str(output_path))
            self.stdout.write(self.style.SUCCESS(f"Template saved to {output_path}"))
        else:
            self.stdout.write(self.style.WARNING("No source DB found to copy."))
