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
                 delay: float = 0.001,
                 color: Optional[Union[Color, int]] = None,
                 raw_strings: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.emulate_typing = emulate_typing
        self.delay = delay
        self.color = color.value if isinstance(color, Color) else color
        self.raw_strings = raw_strings

    def _format_with_color(self, text: str) -> str:
        if self.color is None:
            return text
        return f"\033[38;5;{self.color}m{text}\033[0m"

    def _print_text(self, text: str, end: str = '\n') -> None:
        # If dealing with a string and raw_strings is False, print it directly
        if isinstance(text, str) and not self.raw_strings:
            formatted_text = self._format_with_color(text)
        else:
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
        # For strings, we might want to print them directly
        if isinstance(object, str) and not self.raw_strings:
            self._print_text(object)
        else:
            formatted = self.pformat(object)
            self._print_text(formatted)


# Exports
pinfo = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.INFO,
    width=79,
    compact=True
)
ppi = pinfo.pprint
perror = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.ERROR,
    width=79,
    compact=True
)
ppe = perror.pprint
pwarning = EnhancedPrettyPrinter(
    emulate_typing=True,
    indent=2,
    color=Color.WARNING,
    width=79,
    compact=True
)
ppw = pwarning.pprint