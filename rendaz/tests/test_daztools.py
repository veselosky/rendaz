"Test handling/parsing of various DAZ Studio files"

from pathlib import Path
from tempfile import NamedTemporaryFile

from django.apps import apps

from rendaz.daztools import (
    DSONFile,
    ProductMeta,
    manifest_files,
    supplement_product_name,
)


TEST_DIR = Path(__file__).parent


def test_read_dson_compressed():
    "Test reading compressed DSON files"
    fname = TEST_DIR / "Sphere-compressed.duf"
    duf = DSONFile(path=str(fname))
    assert duf.path.name == "Sphere-compressed.duf"
    assert duf.is_compressed
    assert "asset_info" in duf.dson


def test_read_dson_uncompressed():
    "Test reading uncompressed DSON files"
    fname = TEST_DIR / "Sphere-uncompressed.duf"
    duf = DSONFile(path=str(fname))
    assert duf.path.name == "Sphere-uncompressed.duf"
    assert duf.is_compressed is False
    assert "asset_info" in duf.dson


def test_save_dson_compressed():
    "Test write round trip, read uncompressed, write compressed, read back"
    fname = TEST_DIR / "Sphere-uncompressed.duf"
    duf = DSONFile(path=str(fname))
    out = NamedTemporaryFile(mode="wt", delete=False)
    tmpname = out.name
    out.close()
    try:
        duf.save(tmpname, compress=True)

        new = DSONFile(tmpname)
        assert new.is_compressed
        assert "asset_info" in new.dson
    finally:
        Path(tmpname).unlink()


def test_save_dson_uncompressed():
    "Test write round trip, read compressed, write uncompressed, read back"
    fname = TEST_DIR / "Sphere-compressed.duf"
    duf = DSONFile(path=str(fname))
    out = NamedTemporaryFile(mode="wt", delete=False)
    tmpname = out.name
    out.close()
    try:
        duf.save(tmpname, compress=False)

        new = DSONFile(tmpname)
        assert new.is_compressed is False
        assert "asset_info" in new.dson
    finally:
        Path(tmpname).unlink()


def test_productmetafile_defaults():
    production = apps.get_app_config("production")
    it = ProductMeta(product_id="THETHING", stem_product_name="THETHING")
    assert it.product_id == "THETHING"
    assert isinstance(it.cms_files, set)
    assert isinstance(it.dim_manifest_files, set)
    assert isinstance(it.included_files, set)


def test_manifest_files():
    expected = [
        "Content/People/Genesis 8 Female/Characters/Aakash.duf",
        "Content/People/Genesis 8 Female/Characters/Aakash.duf.png",
        "Content/Runtime/Support/DAZ_3D_60599_Aakash_HD_for_Kala_8.dsa",
        "Content/Runtime/Support/DAZ_3D_60599_Aakash_HD_for_Kala_8.dsx",
        "Content/Runtime/Support/DAZ_3D_60599_Aakash_HD_for_Kala_8.jpg",
    ]
    fname = TEST_DIR / "Manifest.dsx"
    actual = list(manifest_files(fname))
    assert actual == expected


def test_supplement_product_name():
    expected = "Aakash HD for Kala 8"
    fname = TEST_DIR / "Supplement.dsx"
    actual = supplement_product_name(fname)
    assert actual == expected
