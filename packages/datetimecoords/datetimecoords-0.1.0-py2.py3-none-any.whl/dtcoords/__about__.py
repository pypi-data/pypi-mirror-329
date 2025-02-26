import pathlib

local = pathlib.Path(__file__).parent
version_path = local / "VERSION"

with open(version_path, "r") as version_file:
    __version__ = version_file.read().strip()

__all__ = ["__version__"]
