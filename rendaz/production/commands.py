"""Command routines for this app."""
import logging
from pathlib import Path

from rendaz.daztools import DSONFile

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