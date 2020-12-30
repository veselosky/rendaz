"Tools for doing stuff with DAZ files"
import gzip
import json
import zlib
from pathlib import Path, PurePath


class DSONFile:
    """A Daz Studio scene file (or really any DSON file)"""

    def __init__(self, path):
        # underscore attrs are property caches
        self.raw_path = str(path)
        self._path = Path(self.raw_path)
        self._dson = None
        self._is_compressed = None

    def __str__(self):
        return self.path.name

    def _load_dson(self):
        # DSON files can be saved with optional gzip compression, but the extension
        # doesn't change. We'll just have to try opening it both ways and see which
        # works.
        try:
            with gzip.open(self.raw_path) as fh:
                self._dson = json.load(fh)
                self._is_compressed = True
        except (gzip.BadGzipFile, EOFError, zlib.error):
            with open(self.raw_path, mode="rb") as fh:
                self._dson = json.load(fh)
                self._is_compressed = False
        return self._dson

    @property
    def is_compressed(self):
        # Don't know if file is compressed until we read it. _load_dson will set the
        # internal flag once it knows.
        if self._is_compressed is None:
            self._load_dson()
        return self._is_compressed

    @property
    def path(self):
        return self._path

    @property
    def dson(self):
        "Return the DSON data from the file as a Python dict"
        if self._dson:
            return self._dson
        return self._load_dson()

    def save(self, newpath, compress=True):
        "Resave the DSON data with the given compression setting (default true)."
        if compress:
            with gzip.open(newpath, "wt") as outfile:
                json.dump(self.dson, outfile)
            return True
        with open(newpath, "wt") as outfile:
            json.dump(self.dson, outfile, indent=2)
        return True