"Tools for doing stuff with DAZ files"
import gzip
import json
import os
import re
import typing as T
import zipfile
import zlib
from dataclasses import dataclass, asdict, field
from pathlib import Path, PurePath
from xml.etree import ElementTree as ET

from django.apps import apps
from django.conf import settings

TPathLike = T.Union[str, "os.PathLike[str]"]


def camel_case_split(a_string: str) -> str:
    "Given CamelCaseString, return a split Camel Case String"
    matches = re.finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", a_string
    )
    return " ".join([m.group(0) for m in matches])


class DSONFile:
    """A Daz Studio scene file (or really any DSON file)"""

    def __init__(self, path: TPathLike):
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

    def save(self, newpath: TPathLike, compress=True):
        "Resave the DSON data with the given compression setting (default true)."
        if compress:
            with gzip.open(newpath, "wt") as outfile:
                json.dump(self.dson, outfile)
            return True
        with open(newpath, "wt") as outfile:
            json.dump(self.dson, outfile, indent=2)
        return True


def manifest_files(filething):
    "Yields all the files (install paths) listed in the Manifest"
    tree = ET.parse(filething)
    if tree.getroot().tag != "DAZInstallManifest":
        raise ValueError("Not a Manifest file")
    for file_tag in tree.getroot().iter("File"):
        yield file_tag.attrib["VALUE"]


def supplement_product_name(filething):
    "Returns the product name from the Supplement.dsx file"
    tree = ET.parse(filething)
    if tree.getroot().tag != "ProductSupplement":
        raise ValueError("Not a Supplement file")
    return tree.getroot().find("ProductName").attrib["VALUE"]


@dataclass
class ProductMeta:
    """Holds metadata about DAZ store products."""

    product_id: str
    stem_product_name: str

    cms_product_name: str = field(default="", repr=False)
    dim_product_name: str = field(default="", repr=False)
    sku: str = field(default="", repr=False)
    included_files: set = field(default_factory=set, repr=False)
    dim_manifest_files: set = field(default_factory=set, repr=False)
    cms_files: set = field(default_factory=set, repr=False)

    def __post_init__(self):
        # When read from JSON these will be lists, but we want sets
        if isinstance(self.included_files, list):
            self.included_files = set(self.included_files)
        if isinstance(self.dim_manifest_files, list):
            self.dim_manifest_files = set(self.dim_manifest_files)
        if isinstance(self.cms_files, list):
            self.cms_files = set(self.cms_files)

    @classmethod
    def from_file(cls, path: TPathLike):
        inpath = Path(path)
        if not inpath.exists():
            return cls(product_id=inpath.stem, stem_product_name=inpath.stem)
        with inpath.open("r") as fp:
            data = json.load(fp)
            return cls(**data)

    def dump_json(self, outpath: TPathLike, indent=2):
        "Write JSON data to disk"
        with open(outpath, "w") as fp:
            return json.dump(asdict(self), fp, indent=indent)

    def add_zipfile(self, azip: TPathLike):
        # open the zip
        with zipfile.ZipFile(azip) as ozip:
            # Store list of all files in the zip (ignore directories)
            self.included_files.add([x for x in ozip.namelist() if not x.endswith("/")])
            # if manifest.dsx exists (it definitely should)
            if "Manifest.dsx" in self.included_files:
                # read file list from manifest.dsx
                with ozip.open("Manifest.dsx") as manifest:
                    self.dim_manifest_files.add(manifest_files(manifest))
            #   Store list of files in zip but not manifest (buggy product)
            #   Store list of files in manifest but not zip (buggy product)
            # if supplement.dsx exists (it definitely should)
            if "Supplement.dsx" in self.included_files:
                with ozip.open("Supplement.dsx") as supplement:
                    # extract official product name from supplement.dsx
                    self.dim_product_name = supplement_product_name(supplement)

    #   if Content/Runtime/Support/*.dsx exists:
    #       extract meta product name and artist
    #       Store list of files in zip but not meta (buggy product)
    #       Store list of files in meta but not zip (buggy product)
    #       Store list of DSON files in zip but not meta Assets
    #       For each Asset in meta:
    #           store contenttype, categories, compatibilities, Userwords
    #           open the DSON file and store its asset_type

    @property
    def product_name(self) -> str:
        "Product name"
        return (
            self.cms_product_name
            or self.dim_product_name
            or camel_case_split(self.stem_product_name)
        )
