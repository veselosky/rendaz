"Test features of the DazFile model"
from pathlib import Path

from production.models import DazFile


TEST_DIR = Path(__file__).parent


def test_dson_compressed():
    "Test reading compressed DSON files"
    fname = TEST_DIR / "Sphere-compressed.duf"
    duf = DazFile(name="Sphere", raw_path=str(fname))
    assert duf.path.name == "Sphere-compressed.duf"
    dson = duf.read_dson()
    assert "asset_info" in dson


def test_dson_uncompressed():
    "Test reading uncompressed DSON files"
    fname = TEST_DIR / "Sphere-uncompressed.duf"
    duf = DazFile(name="Sphere", raw_path=str(fname))
    assert duf.path.name == "Sphere-uncompressed.duf"
    dson = duf.read_dson()
    assert "asset_info" in dson
