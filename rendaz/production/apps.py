from pathlib import Path

from django.apps import AppConfig
from django.conf import settings


class ProductionConfig(AppConfig):
    name = "rendaz.production"

    @property
    def projects_path(self):
        "Directory to store project output files."
        if hasattr(settings, "PRODUCTION_PATH"):
            return Path(settings.PRODUCTION_PATH)
        return Path(settings.MEDIA_ROOT)

    @property
    def inventory_path(self):
        return self.projects_path / "dim_inventory"
