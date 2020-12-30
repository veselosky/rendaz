"Test features of the DazFile model"
from pathlib import Path
from tempfile import NamedTemporaryFile

from rendaz.daztools import DSONFile


TEST_DIR = Path(__file__).parent


def test_dson_compressed():
    "Test reading compressed DSON files"
    fname = TEST_DIR / "Sphere-compressed.duf"
    duf = DSONFile(path=str(fname))
    assert duf.path.name == "Sphere-compressed.duf"
    assert duf.is_compressed
    assert "asset_info" in duf.dson


def test_dson_uncompressed():
    "Test reading uncompressed DSON files"
    fname = TEST_DIR / "Sphere-uncompressed.duf"
    duf = DSONFile(path=str(fname))
    assert duf.path.name == "Sphere-uncompressed.duf"
    assert duf.is_compressed is False
    assert "asset_info" in duf.dson


def test_save_compressed():
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


def test_save_uncompressed():
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
