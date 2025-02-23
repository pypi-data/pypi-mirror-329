from enum import Enum
from pprint import PrettyPrinter
import sys
from time import sleep
from typing import Optional, Union


class Color(Enum):
    # Basic colors
    BLACK = 0
    RED = 196
    GREEN = 46
    YELLOW = 226
    BLUE = 33
    MAGENTA = 201
    CYAN = 51
    WHITE = 15

    # Extra shades
    DARK_RED = 160
    DARK_GREEN = 22
    DARK_BLUE = 19
    LIGHT_BLUE = 39
    ORANGE = 208
    PURPLE = 129
    PINK = 218
    GRAY = 242
    DARK_GRAY = 236

    # Special
    SUCCESS = 82
    WARNING = 214
    ERROR = 196
    INFO = 39
    DEBUG = 242


class EnhancedPrettyPrinter(PrettyPrinter):
    def __init__(self,
                 *args,
                 emulate_typing: bool = False,
                 delay: float = 0.005,
                 color: Optional[Union[Color, int]] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.emulate_typing = emulate_typing
        self.delay = delay
        self.color = color.value if isinstance(color, Color) else color

    def _format_with_color(self, text: str) -> str:
        if self.color is None:
            return text
        return f"\033[38;5;{self.color}m{text}\033[0m"

    def _print_text(self, text: str, end: str = '\n') -> None:
        formatted_text = self._format_with_color(text)

        if self.emulate_typing:
            for char in formatted_text:
                sys.stdout.write(char)
                sys.stdout.flush()
                sleep(self.delay)
            sys.stdout.write(end)
        else:
            sys.stdout.write(f"{formatted_text}{end}")
        sys.stdout.flush()

    def pprint(self, object):
        formatted = self.pformat(object)
        self._print_text(formatted)


# Usage examples:
if __name__ == "__main__":
    test_data = {
        "status": "Success",
        "details": {
            "items_processed": 100,
            "errors": []
        }
    }

    # Using enum colors
    pp = EnhancedPrettyPrinter(
        indent=2,
        emulate_typing=True,
        color=Color.SUCCESS
    )
    pp.pprint(test_data)

    error_data = {
        "status": "Error",
        "details": {
            "message": "Connection failed",
            "code": 500
        }
    }

    # Using semantic colors
    pp_error = EnhancedPrettyPrinter(
        indent=2,
        color=Color.ERROR
    )
    pp_error.pprint(error_data)