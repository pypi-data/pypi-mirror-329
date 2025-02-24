from gemerald.__main__ import get_dirs
from pathlib import Path


def test_get_dirs():
    _ = get_dirs(Path("gemerald/test_dirs"))
