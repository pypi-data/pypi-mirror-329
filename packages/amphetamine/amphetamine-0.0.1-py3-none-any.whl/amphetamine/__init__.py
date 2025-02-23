"""
amphetamine

Conveniences for faster prototyping and more enjoyable interactive sessions.
"""
import logging
import os
import platform
import sys
import tomllib

from pathlib import Path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsRead

from platformdirs import user_data_dir

from .pprint import Color, EnhancedPrettyPrinter
pinfo = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.INFO,
    width=79
)
ppi = pinfo.pprint
perror = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.ERROR,
    width=79
)
ppe = perror.pprint
pwarning = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.WARNING,
    width=79
)
ppw = pwarning.pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# Reading `pyproject.toml` into `CONFIG`
with open(Path(__file__).parents[5] / "pyproject.toml", "rb") as f:
    if TYPE_CHECKING:
        f: SupportsRead[bytes]

    CONFIG = tomllib.load(f)

# Package metadata
__author__ = CONFIG["project"]["authors"]
__license__ = CONFIG["project"]["license"]
__version__ = CONFIG["project"]["version"]
__description__ = CONFIG["project"]["description"]

# Constants
AMP_DATA_DIR = os.getenv("AMP_DATA_DIR") or (
    user_data_dir(
        appname="amphetamine",
        appauthor="K. LeBryce",
        version=__version__,
        ensure_exists=True
    )
)
PLATFORM = platform.platform()
SYSTEM = platform.system()

# Load environment variables from `.env`
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    ppe(f"Failed to load environment variables from `.env`: {e}")

# Helper functions
def handle_exception(exc_type):
    if issubclass(exc_type, KeyboardInterrupt):
        print("\nCaught keyboard interrupt, exiting gracefully.")
        sys.exit(1)
    elif issubclass(exc_type, SystemExit):
        print("\nExiting gracefully.")
        sys.exit(0)
    elif issubclass(exc_type, Exception):
        print("\nCaught generic exception.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nUnhandled exception:", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
