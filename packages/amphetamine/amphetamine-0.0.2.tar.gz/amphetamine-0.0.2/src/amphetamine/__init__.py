"""
amphetamine

Conveniences for faster prototyping and more enjoyable interactive sessions.
"""
import logging
import os
import platform
import sys
import tomllib

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsRead

from platformdirs import user_data_dir

from . import algorithms, utils
from .algorithms import *
from .utils import *
from .utils import Color, EnhancedPrettyPrinter, ppe, ppi, ppw
from .utils import watch_modules, watch_modules_context, stop_watching

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# Reading `pyproject.toml` into `CONFIG`
with open(Path(__file__).parents[2] / "pyproject.toml", "rb") as f:
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


@dataclass
class Constants(Enum):
    """
    Constants

    Package-level constants.
    """
    AMP_DATA_DIR = os.getenv("AMP_DATA_DIR") or (
        user_data_dir(
            appname="amphetamine",
            appauthor="K. LeBryce",
            version=__version__,
            ensure_exists=True
        )
    )
    AMP_IMAGES_DIR = os.getenv("AMP_IMAGES_DIR") or Path("~/Library/Mobile Documents/com~apple~CloudDocs/garter/images").expanduser()
    LLM_DATA_DIR = os.getenv("LLM_DATA_DIR") or AMP_DATA_DIR / "llm"
    CLAUDE_CONVERSATIONS_DIR = os.getenv("CLAUDE_CONVERSATIONS_DIR") or LLM_DATA_DIR / "claude/conversations"
    CHATGPT_CONVERSATIONS_DIR = os.getenv("CHATGPT_CONVERSATIONS_DIR") or LLM_DATA_DIR / "chatgpt/conversations"
    PLATFORM = platform.platform()
    SYSTEM = platform.system()

    try:
        # Ensure data directories exist
        if not Path(AMP_DATA_DIR).exists():
            Path(AMP_DATA_DIR).mkdir(parents=True, exist_ok=True)

        if not Path(AMP_IMAGES_DIR).exists():
            Path(AMP_IMAGES_DIR).mkdir(parents=True, exist_ok=True)

        if not Path(LLM_DATA_DIR).exists():
            Path(LLM_DATA_DIR).mkdir(parents=True, exist_ok=True)

        if not Path(CLAUDE_CONVERSATIONS_DIR).exists():
            Path(CLAUDE_CONVERSATIONS_DIR).mkdir(parents=True, exist_ok=True)

        if not Path(CHATGPT_CONVERSATIONS_DIR).exists():
            Path(CHATGPT_CONVERSATIONS_DIR).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)


# Export package-level constants
AMP_DATA_DIR = Constants.AMP_DATA_DIR.value
AMP_IMAGES_DIR = Constants.AMP_IMAGES_DIR.value
LLM_DATA_DIR = Constants.LLM_DATA_DIR.value
CLAUDE_CONVERSATIONS_DIR = Constants.CLAUDE_CONVERSATIONS_DIR.value
CHATGPT_CONVERSATIONS_DIR = Constants.CHATGPT_CONVERSATIONS_DIR.value

__all__ = [
    "ANTHROPIC_API_KEY",
    "CHATGPT_CONVERSATIONS_DIR",
    "CLAUDE_CONVERSATIONS_DIR",
    "AMP_DATA_DIR",
    "AMP_IMAGES_DIR",
    "LLM_DATA_DIR",
    "OPENAI_API_KEY",
    "ChatGPT",
    "ChatGPTModel",
    "Claude",
    "ClaudeModel",
    "Color",
    "Notable",
    "Note",
    "algorithms",
    "claude",
    "hot_reload",
    "ppe",
    "ppi",
    "pprint",
    "ppw",
    "stop_watching",
    "llm",
    "manacher",
    "note",
    "watch_modules",
    "watch_modules_context"
]

