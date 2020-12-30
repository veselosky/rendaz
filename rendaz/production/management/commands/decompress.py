"Decompress compressed DSON files"
import argparse
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from rendaz.production.commands import decompress_dson_files


class Command(BaseCommand):
    help = "Decompress compressed DSON files"

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="+", type=Path)
        parser.add_argument("--no-backup", action="store_true")

    def handle(self, *args, **options):
        files = []
        for path in options["paths"]:
            if path.is_dir():
                files.extend(list(path.rglob("*.duf")))
            else:
                files.append(path)
        # self.stdout.write(str(files))
        backup = True
        if options["no_backup"]:
            backup = False
        decompress_dson_files(*files, backup=backup)
