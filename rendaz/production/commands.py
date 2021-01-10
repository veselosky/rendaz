"""Command routines for this app."""
import logging
import re
import typing as T
import zipfile
from pathlib import Path

from django.apps import apps
from django.conf import settings

from rendaz.daztools import DSONFile, ProductMeta, TPathLike

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def compress_dson_files(*args, backup=True):
    """Resave DSON files with compression ON.

    Given a list of file paths as args, will read each in turn to determine whether
    it is compressed. If it is, do nothing. If not, optionally move the file to
    "path.bak", then save the DSON to `path` with compression enabled.
    """
    for name in args:
        the_file = DSONFile(str(name))
        if the_file.is_compressed:
            if backup:
                backup_name = str(name) + ".bak"
                the_file.path.rename(backup_name)
                logger.info(f"Renamed {name} to {backup_name}")
            the_file.save(name, compress=True)
            logger.info(f"Saved {name} uncompressed")
        else:
            logger.info(f"{name} is not compressed, skipping")


def decompress_dson_files(*args, backup=True):
    """Resave DSON files with compression OFF.

    Given a list of file paths as args, will read each in turn to determine whether
    it is compressed. If it is not, do nothing. If yes, optionally move the file to
    "path.gz", then save the DSON to `path` with compression disabled.
    """
    for name in args:
        the_file = DSONFile(str(name))
        if the_file.is_compressed:
            if backup:
                backup_name = str(name) + ".gz"
                the_file.path.rename(backup_name)
                logger.info(f"Renamed {name} to {backup_name}")
            the_file.save(name, compress=False)
            logger.info(f"Saved {name} uncompressed")
        else:
            logger.info(f"{name} is not compressed, skipping")


def dim_inventory(
    dim_downloads_dir: TPathLike, output_dir: T.Optional[TPathLike] = None
):
    """Crawl DIM downloads and generate inventory sheets.

    Given a path to the DAZ Install Manager downloads folder, read each zip file
    and generate a data structure describing its contents. These will be written
    out to .json files in the output directory (by default MEDIA_ROOT/dim_inventory).
    """
    production = apps.get_app_config("production")

    outpath = Path(output_dir) if output_dir else production.inventory_path
    inpath = Path(dim_downloads_dir)

    # glob for zip files
    zipfiles = inpath.glob("*.zip")

    # for each zip file
    for azip in zipfiles:
        if not zipfile.is_zipfile(azip):
            logger.error(f"{azip.name} is not a valid zip archive, skipping")
            continue
        # e.g. IM00000325-01_Camel.zip
        # group 1: IMID; 2: Numeric SKU; 3: CamelCase product name
        dim_pattern = re.compile(r"(IM(\d{8}))-\d{2}_(.*)\.zip")

        # parse the file name for implied product name and id
        # If it's not a DIM package, just use the stem
        if mg := dim_pattern.match(azip.name):
            pkgid, sku, pname = mg.group(1, 2, 3)
        else:
            pkgid = pname = azip.stem
            sku = None

        # Products can be spread over multiple zips, so we need to accumulate and
        # combine with any data from previous zips.
        metapath = (outpath / pkgid).with_suffix(".json")
        product = ProductMeta.from_file(metapath)
        product.stem_product_name = pname
        product.sku = sku or ""
        product.add_zipfile(azip)
        product.dump_json(metapath)
