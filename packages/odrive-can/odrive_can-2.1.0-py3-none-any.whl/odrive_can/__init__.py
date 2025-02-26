from importlib.metadata import version, PackageNotFoundError
from .utils import get_axis_id, get_dbc, extract_ids, LOG_FORMAT, TIME_FORMAT
from .odrive import ODriveCAN, CanMsg

# Specify the public API of the module
__all__ = [
    "get_axis_id",
    "get_dbc",
    "extract_ids",
    "LOG_FORMAT",
    "TIME_FORMAT",
    "ODriveCAN",
    "CanMsg",
]

try:
    __version__ = version("odrive_can")
except PackageNotFoundError:
    # Package is not installed, and therefore, version is unknown.
    __version__ = "0.0.0+unknown"
