"""
Core utilities for the Kosmo package.

This module provides basic utility functions for file operations, directory navigation,
and terminal output manipulation. It includes enhanced versions of common shell commands
and custom printing functionality.

Environment Variables:
    HOME (str): User's home directory path
    USER (str): Current username
    PYTHONHOME (str): Python installation directory
    PYTHONPATH (str): Python module search path
"""

import json
import os
import shutil
import sys
from pathlib import Path
from time import sleep

# Environment variables
HOME = os.environ.get("HOME")
USER = os.environ.get("USER")
PYTHONHOME = os.environ.get("PYTHONHOME")
PYTHONPATH = os.environ.get("PYTHONPATH")

# ANSI Color Constants
# Reset sequence
RESET = "\033[0m"

# Standard ANSI Colors (0-7)
BLACK = "\033[38;5;0m"
MAROON = "\033[38;5;1m"
GREEN = "\033[38;5;2m"
OLIVE = "\033[38;5;3m"
NAVY = "\033[38;5;4m"
PURPLE = "\033[38;5;5m"
TEAL = "\033[38;5;6m"
SILVER = "\033[38;5;7m"

# Bright ANSI Colors (8-15)
GRAY = "\033[38;5;8m"
RED = "\033[38;5;9m"
LIME = "\033[38;5;10m"
YELLOW = "\033[38;5;11m"
BLUE = "\033[38;5;12m"
MAGENTA = "\033[38;5;13m"
CYAN = "\033[38;5;14m"
WHITE = "\033[38;5;15m"

# 216 Color Cube (16-231)
BLACK_0 = "\033[38;5;16m"
NAVY_0 = "\033[38;5;17m"
NAVY_1 = "\033[38;5;18m"
NAVY_2 = "\033[38;5;19m"
BLUE_0 = "\033[38;5;20m"
BLUE_1 = "\033[38;5;21m"
DARKBLUE_0 = "\033[38;5;22m"
DARKBLUE_1 = "\033[38;5;23m"
BLUE_2 = "\033[38;5;24m"
BLUE_3 = "\033[38;5;25m"
BLUE_4 = "\033[38;5;26m"
BLUE_5 = "\033[38;5;27m"
GREEN_0 = "\033[38;5;28m"
TEAL_0 = "\033[38;5;29m"
TEAL_1 = "\033[38;5;30m"
TEAL_2 = "\033[38;5;31m"
TEAL_3 = "\033[38;5;32m"
TEAL_4 = "\033[38;5;33m"
FOREST_0 = "\033[38;5;34m"
GREEN_1 = "\033[38;5;35m"
GREEN_2 = "\033[38;5;36m"
CYAN_0 = "\033[38;5;37m"
CYAN_1 = "\033[38;5;38m"
CYAN_2 = "\033[38;5;39m"
GREEN_3 = "\033[38;5;40m"
GREEN_4 = "\033[38;5;41m"
GREEN_5 = "\033[38;5;42m"
TEAL_5 = "\033[38;5;43m"
CYAN_3 = "\033[38;5;44m"
CYAN_4 = "\033[38;5;45m"
BROWN_0 = "\033[38;5;46m"
GREEN_6 = "\033[38;5;47m"
GREEN_7 = "\033[38;5;48m"
SEAFOAM_0 = "\033[38;5;49m"
SEAFOAM_1 = "\033[38;5;50m"
CYAN_5 = "\033[38;5;51m"
BROWN_1 = "\033[38;5;52m"
MAROON_0 = "\033[38;5;53m"
PURPLE_0 = "\033[38;5;54m"
PURPLE_1 = "\033[38;5;55m"
PURPLE_2 = "\033[38;5;56m"
PURPLE_3 = "\033[38;5;57m"
GREEN_8 = "\033[38;5;58m"
OLIVE_0 = "\033[38;5;59m"
TEAL_6 = "\033[38;5;60m"
STEEL_0 = "\033[38;5;61m"
STEEL_1 = "\033[38;5;62m"
BLUE_6 = "\033[38;5;63m"
OLIVE_1 = "\033[38;5;64m"
GREEN_9 = "\033[38;5;65m"
TEAL_7 = "\033[38;5;66m"
STEEL_2 = "\033[38;5;67m"
STEEL_3 = "\033[38;5;68m"
BLUE_7 = "\033[38;5;69m"
CHARTREUSE_0 = "\033[38;5;70m"
GREEN_10 = "\033[38;5;71m"
GREEN_11 = "\033[38;5;72m"
TEAL_8 = "\033[38;5;73m"
STEEL_4 = "\033[38;5;74m"
BLUE_8 = "\033[38;5;75m"
LIME_0 = "\033[38;5;76m"
LIME_1 = "\033[38;5;77m"
SEAFOAM_2 = "\033[38;5;78m"
SEAFOAM_3 = "\033[38;5;79m"
CYAN_6 = "\033[38;5;80m"
CYAN_7 = "\033[38;5;81m"
MAROON_1 = "\033[38;5;82m"
MAROON_2 = "\033[38;5;83m"
PURPLE_4 = "\033[38;5;84m"
PURPLE_5 = "\033[38;5;85m"
PURPLE_6 = "\033[38;5;86m"
PURPLE_7 = "\033[38;5;87m"
RED_0 = "\033[38;5;88m"
RED_1 = "\033[38;5;89m"
MAGENTA_0 = "\033[38;5;90m"
MAGENTA_1 = "\033[38;5;91m"
MAGENTA_2 = "\033[38;5;92m"
VIOLET_0 = "\033[38;5;93m"
BROWN_2 = "\033[38;5;94m"
BROWN_3 = "\033[38;5;95m"
MAUVE_0 = "\033[38;5;96m"
MAUVE_1 = "\033[38;5;97m"
PURPLE_8 = "\033[38;5;98m"
PURPLE_9 = "\033[38;5;99m"
OLIVE_2 = "\033[38;5;100m"
OLIVE_3 = "\033[38;5;101m"
PURPLE_10 = "\033[38;5;102m"
MAUVE_2 = "\033[38;5;103m"
PURPLE_11 = "\033[38;5;104m"
PURPLE_12 = "\033[38;5;105m"
LIME_2 = "\033[38;5;106m"
GREEN_12 = "\033[38;5;107m"
GREEN_13 = "\033[38;5;108m"
TEAL_9 = "\033[38;5;109m"
STEEL_5 = "\033[38;5;110m"
BLUE_9 = "\033[38;5;111m"
CHARTREUSE_1 = "\033[38;5;112m"
LIME_3 = "\033[38;5;113m"
GREEN_14 = "\033[38;5;114m"
TEAL_10 = "\033[38;5;115m"
CYAN_8 = "\033[38;5;116m"
CYAN_9 = "\033[38;5;117m"
RED_2 = "\033[38;5;118m"
PINK_0 = "\033[38;5;119m"
MAGENTA_3 = "\033[38;5;120m"
PINK_1 = "\033[38;5;121m"
PINK_2 = "\033[38;5;122m"
VIOLET_1 = "\033[38;5;123m"
RED_3 = "\033[38;5;124m"
RED_4 = "\033[38;5;125m"
MAGENTA_4 = "\033[38;5;126m"
MAGENTA_5 = "\033[38;5;127m"
MAGENTA_6 = "\033[38;5;128m"
VIOLET_2 = "\033[38;5;129m"
ORANGE_0 = "\033[38;5;130m"
PINK_3 = "\033[38;5;131m"
PINK_4 = "\033[38;5;132m"
PINK_5 = "\033[38;5;133m"
PURPLE_13 = "\033[38;5;134m"
PURPLE_14 = "\033[38;5;135m"
BROWN_4 = "\033[38;5;136m"
OLIVE_4 = "\033[38;5;137m"
MAUVE_3 = "\033[38;5;138m"
MAUVE_4 = "\033[38;5;139m"
PURPLE_15 = "\033[38;5;140m"
PURPLE_16 = "\033[38;5;141m"
GOLD_0 = "\033[38;5;142m"
KHAKI_0 = "\033[38;5;143m"
MAUVE_5 = "\033[38;5;144m"
MAUVE_6 = "\033[38;5;145m"
PURPLE_17 = "\033[38;5;146m"
PURPLE_18 = "\033[38;5;147m"
LIME_4 = "\033[38;5;148m"
LIME_5 = "\033[38;5;149m"
GREEN_15 = "\033[38;5;150m"
SEAFOAM_4 = "\033[38;5;151m"
CYAN_10 = "\033[38;5;152m"
CYAN_11 = "\033[38;5;153m"
ORANGE_1 = "\033[38;5;154m"
ORANGE_2 = "\033[38;5;155m"
PINK_6 = "\033[38;5;156m"
PINK_7 = "\033[38;5;157m"
PINK_8 = "\033[38;5;158m"
VIOLET_3 = "\033[38;5;159m"
RED_5 = "\033[38;5;160m"
RED_6 = "\033[38;5;161m"
MAGENTA_7 = "\033[38;5;162m"
MAGENTA_8 = "\033[38;5;163m"
MAGENTA_9 = "\033[38;5;164m"
VIOLET_4 = "\033[38;5;165m"
ORANGE_3 = "\033[38;5;166m"
SALMON_0 = "\033[38;5;167m"
PINK_9 = "\033[38;5;168m"
PINK_10 = "\033[38;5;169m"
MAGENTA_10 = "\033[38;5;170m"
MAGENTA_11 = "\033[38;5;171m"
ORANGE_4 = "\033[38;5;172m"
TAN_0 = "\033[38;5;173m"
PINK_11 = "\033[38;5;174m"
PINK_12 = "\033[38;5;175m"
MAGENTA_12 = "\033[38;5;176m"
MAGENTA_13 = "\033[38;5;177m"
ORANGE_5 = "\033[38;5;178m"
KHAKI_1 = "\033[38;5;179m"
PINK_13 = "\033[38;5;180m"
PINK_14 = "\033[38;5;181m"
LILAC_0 = "\033[38;5;182m"
LILAC_1 = "\033[38;5;183m"
YELLOW_0 = "\033[38;5;184m"
KHAKI_2 = "\033[38;5;185m"
KHAKI_3 = "\033[38;5;186m"
KHAKI_4 = "\033[38;5;187m"
LILAC_2 = "\033[38;5;188m"
LILAC_3 = "\033[38;5;189m"
ORANGE_6 = "\033[38;5;190m"
YELLOW_1 = "\033[38;5;191m"
LIME_6 = "\033[38;5;192m"
MINT_0 = "\033[38;5;193m"
MINT_1 = "\033[38;5;194m"
AZURE_0 = "\033[38;5;195m"
RED_7 = "\033[38;5;196m"
RED_8 = "\033[38;5;197m"
MAGENTA_14 = "\033[38;5;198m"
MAGENTA_15 = "\033[38;5;199m"
MAGENTA_16 = "\033[38;5;200m"
MAGENTA_17 = "\033[38;5;201m"
ORANGE_7 = "\033[38;5;202m"
SALMON_1 = "\033[38;5;203m"
PINK_15 = "\033[38;5;204m"
PINK_16 = "\033[38;5;205m"
MAGENTA_18 = "\033[38;5;206m"
MAGENTA_19 = "\033[38;5;207m"
ORANGE_8 = "\033[38;5;208m"
SALMON_2 = "\033[38;5;209m"
PINK_17 = "\033[38;5;210m"
PINK_18 = "\033[38;5;211m"
PINK_19 = "\033[38;5;212m"
PINK_20 = "\033[38;5;213m"
ORANGE_9 = "\033[38;5;214m"
PEACH_0 = "\033[38;5;215m"
PINK_21 = "\033[38;5;216m"
PINK_22 = "\033[38;5;217m"
PINK_23 = "\033[38;5;218m"
PINK_24 = "\033[38;5;219m"
GOLD_1 = "\033[38;5;220m"
KHAKI_5 = "\033[38;5;221m"
PEACH_1 = "\033[38;5;222m"
PINK_25 = "\033[38;5;223m"
PINK_26 = "\033[38;5;224m"
PINK_27 = "\033[38;5;225m"
YELLOW_2 = "\033[38;5;226m"
YELLOW_3 = "\033[38;5;227m"
YELLOW_4 = "\033[38;5;228m"
CREAM_0 = "\033[38;5;229m"
CREAM_1 = "\033[38;5;230m"
WHITE_0 = "\033[38;5;231m"

# Grayscale Colors (232-255)
GRAY_0 = "\033[38;5;232m"
GRAY_1 = "\033[38;5;233m"
GRAY_2 = "\033[38;5;234m"
GRAY_3 = "\033[38;5;235m"
GRAY_4 = "\033[38;5;236m"
GRAY_5 = "\033[38;5;237m"
GRAY_6 = "\033[38;5;238m"
GRAY_7 = "\033[38;5;239m"
GRAY_8 = "\033[38;5;240m"
GRAY_9 = "\033[38;5;241m"
GRAY_10 = "\033[38;5;242m"
GRAY_11 = "\033[38;5;243m"
GRAY_12 = "\033[38;5;244m"
GRAY_13 = "\033[38;5;245m"
GRAY_14 = "\033[38;5;246m"
GRAY_15 = "\033[38;5;247m"
GRAY_16 = "\033[38;5;248m"
GRAY_17 = "\033[38;5;249m"
GRAY_18 = "\033[38;5;250m"
GRAY_19 = "\033[38;5;251m"
GRAY_20 = "\033[38;5;252m"
GRAY_21 = "\033[38;5;253m"
GRAY_22 = "\033[38;5;254m"
GRAY_23 = "\033[38;5;255m"

# Background versions of all colors
BG_BLACK = "\033[48;5;0m"
BG_MAROON = "\033[48;5;1m"
BG_GREEN = "\033[48;5;2m"
BG_OLIVE = "\033[48;5;3m"
BG_NAVY = "\033[48;5;4m"
BG_PURPLE = "\033[48;5;5m"
BG_TEAL = "\033[48;5;6m"
BG_SILVER = "\033[48;5;7m"
BG_GRAY = "\033[48;5;8m"
BG_RED = "\033[48;5;9m"
BG_LIME = "\033[48;5;10m"
BG_YELLOW = "\033[48;5;11m"
BG_BLUE = "\033[48;5;12m"
BG_MAGENTA = "\033[48;5;13m"
BG_CYAN = "\033[48;5;14m"
BG_WHITE = "\033[48;5;15m"
BG_BLACK_0 = "\033[48;5;16m"
BG_NAVY_0 = "\033[48;5;17m"
BG_NAVY_1 = "\033[48;5;18m"
BG_GRAY_23 = "\033[48;5;255m"

# Style modifiers
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
STRIKE = "\033[9m"

# Reset all
RESET_ALL = "\033[0m"
RESET_BOLD = "\033[21m"
RESET_DIM = "\033[22m"
RESET_ITALIC = "\033[23m"
RESET_UNDERLINE = "\033[24m"
RESET_BLINK = "\033[25m"
RESET_REVERSE = "\033[27m"
RESET_HIDDEN = "\033[28m"
RESET_STRIKE = "\033[29m"

# Global settings
DEFAULT_PRINT_DELAY = 0.001
DEFAULT_TERMINAL_WIDTH = shutil.get_terminal_size().columns

def get_color(index: int) -> str:
    """
    Get ANSI color escape sequence by index.

    Args:
        index (int): Color index (0-255)

    Returns:
        str: ANSI escape sequence for the specified color

    Raises:
        ValueError: If index is not between 0 and 255
    """
    if 0 <= index <= 255:
        return f"\033[38;5;{index}m"
    raise ValueError("Color index must be between 0 and 255")

def get_bg_color(index: int) -> str:
    """
    Get ANSI background color escape sequence by index.

    Args:
        index (int): Color index (0-255)

    Returns:
        str: ANSI escape sequence for the specified background color

    Raises:
        ValueError: If index is not between 0 and 255
    """
    if 0 <= index <= 255:
        return f"\033[48;5;{index}m"
    raise ValueError("Color index must be between 0 and 255")

def get_terminal_width() -> int:
    """
    Get current terminal window width.

    Returns:
        int: Width of terminal in columns
    """
    return shutil.get_terminal_size().columns

# Store the inbuilt `print` function in memory
old_print = print

def print(text: str, emulate_typing: bool = False, delay: float = DEFAULT_PRINT_DELAY, end: str = '\n') -> None:
    """
    Enhanced print function with optional typing animation.

    Args:
        text (str): Text to print
        emulate_typing (bool, optional): Whether to animate printing. Defaults to False.
        delay (float, optional): Delay between characters when typing. Defaults to DEFAULT_PRINT_DELAY.
        end (str, optional): String to print at the end. Defaults to '\n'.
    """
    if emulate_typing:
        for char in str(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(delay)
        sys.stdout.write(end)
    else:
        sys.stdout.write(f"{text}{end}")
    sys.stdout.flush()

def draw_divider(length: int = None) -> None:
    """
    Print a horizontal divider line.

    Args:
        length (int, optional): Length of divider. Defaults to terminal width.
    """
    width = length if length is not None else get_terminal_width()
    print(f"\n{'-' * width}\n")

def get_working_dir() -> str:
    """
    Get current working directory.

    Returns:
        str: Current working directory path
    """
    return os.getcwd()

def goto_home() -> None:
    """Navigate to user's home directory."""
    os.chdir(HOME)

def change_dir(path: str) -> None:
    """
    Change current working directory.

    Args:
        path (str): Target directory path
    """
    os.chdir(path)

def make_dir(path: str) -> None:
    """
    Create a new directory.

    Args:
        path (str): Directory path to create
    """
    os.mkdir(path)

def remove_dir(path: str) -> None:
    """
    Remove an empty directory.

    Args:
        path (str): Directory path to remove
    """
    os.rmdir(path)

def create_file(path: str) -> None:
    """
    Create an empty file.

    Args:
        path (str): File path to create
    """
    Path(path).touch()

def remove_file(path: str) -> None:
    """
    Remove a file.

    Args:
        path (str): File path to remove
    """
    os.remove(path)

def read_file(path: str) -> str:
    """
    Read and return file contents.

    Args:
        path (str): File path to read

    Returns:
        str: Contents of the file
    """
    with open(path, 'r') as f:
        return f.read()

def write_file(text: str, path: str) -> None:
    """
    Write text to file (overwrite).

    Args:
        text (str): Content to write
        path (str): Target file path
    """
    with open(path, 'w') as f:
        f.write(text)

def append_file(text: str, path: str) -> None:
    """
    Append text to file.

    Args:
        text (str): Content to append
        path (str): Target file path
    """
    with open(path, 'a') as f:
        f.write(text)

def read_json(path: str) -> dict:
    """
    Read and parse JSON file.

    Args:
        path (str): JSON file path

    Returns:
        dict: Parsed JSON data
    """
    with open(path, 'r') as f:
        return json.load(f)

def clear_screen() -> None:
    """Clear terminal screen."""
    os.system('clear')

def go_up() -> None:
    """Navigate to parent directory."""
    os.chdir('..')

# Aliases for common functions
clear = clear_screen  # Alias for clear_screen
cat = read_file
pwd = get_working_dir
cd = change_dir
mkdir = make_dir
rmdir = remove_dir
touch = create_file
rm = remove_file

def main():
    """Main function placeholder."""
    pass

if __name__ == "__main__":
    main()
