"""
garter.utils.__init__

This package provides various utility modules for file operations, cryptography,
event listening, LLM interactions, and more.
"""

from . import core, cryptex, hot_reload, listen, llm, note, portland, pprint

from .core import (
    # Main functions
    old_print, print, draw_divider, get_terminal_width,
    get_working_dir, goto_home, change_dir,
    make_dir, remove_dir, create_file,
    remove_file, read_file, write_file,
    append_file, read_json, clear_screen,
    go_up,

    # Color utilities
    get_color, get_bg_color,

    # Constants
    HOME, USER, PYTHONHOME, PYTHONPATH,
    DEFAULT_PRINT_DELAY, DEFAULT_TERMINAL_WIDTH,

    # Standard ANSI Colors (0-7)
    BLACK, MAROON, GREEN, OLIVE, NAVY, PURPLE, TEAL, SILVER,

    # Bright ANSI Colors (8-15)
    GRAY, RED, LIME, YELLOW, BLUE, MAGENTA, CYAN, WHITE,

    # 216 Color Cube (16-231)
    BLACK_0, NAVY_0, NAVY_1, NAVY_2, BLUE_0, BLUE_1,
    DARKBLUE_0, DARKBLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GREEN_0, TEAL_0, TEAL_1, TEAL_2, TEAL_3, TEAL_4,
    FOREST_0, GREEN_1, GREEN_2, CYAN_0, CYAN_1, CYAN_2,
    GREEN_3, GREEN_4, GREEN_5, TEAL_5, CYAN_3, CYAN_4,
    BROWN_0, GREEN_6, GREEN_7, SEAFOAM_0, SEAFOAM_1, CYAN_5,
    BROWN_1, MAROON_0, PURPLE_0, PURPLE_1, PURPLE_2, PURPLE_3,
    GREEN_8, OLIVE_0, TEAL_6, STEEL_0, STEEL_1, BLUE_6,
    OLIVE_1, GREEN_9, TEAL_7, STEEL_2, STEEL_3, BLUE_7,
    CHARTREUSE_0, GREEN_10, GREEN_11, TEAL_8, STEEL_4, BLUE_8,
    LIME_0, LIME_1, SEAFOAM_2, SEAFOAM_3, CYAN_6, CYAN_7,
    MAROON_1, MAROON_2, PURPLE_4, PURPLE_5, PURPLE_6, PURPLE_7,
    RED_0, RED_1, MAGENTA_0, MAGENTA_1, MAGENTA_2, VIOLET_0,
    BROWN_2, BROWN_3, MAUVE_0, MAUVE_1, PURPLE_8, PURPLE_9,
    OLIVE_2, OLIVE_3, PURPLE_10, MAUVE_2, PURPLE_11, PURPLE_12,
    LIME_2, GREEN_12, GREEN_13, TEAL_9, STEEL_5, BLUE_9,
    CHARTREUSE_1, LIME_3, GREEN_14, TEAL_10, CYAN_8, CYAN_9,
    RED_2, PINK_0, MAGENTA_3, PINK_1, PINK_2, VIOLET_1,
    RED_3, RED_4, MAGENTA_4, MAGENTA_5, MAGENTA_6, VIOLET_2,
    ORANGE_0, PINK_3, PINK_4, PINK_5, PURPLE_13, PURPLE_14,
    BROWN_4, OLIVE_4, MAUVE_3, MAUVE_4, PURPLE_15, PURPLE_16,
    GOLD_0, KHAKI_0, MAUVE_5, MAUVE_6, PURPLE_17, PURPLE_18,
    LIME_4, LIME_5, GREEN_15, SEAFOAM_4, CYAN_10, CYAN_11,
    ORANGE_1, ORANGE_2, PINK_6, PINK_7, PINK_8, VIOLET_3,
    RED_5, RED_6, MAGENTA_7, MAGENTA_8, MAGENTA_9, VIOLET_4,
    ORANGE_3, SALMON_0, PINK_9, PINK_10, MAGENTA_10, MAGENTA_11,
    ORANGE_4, TAN_0, PINK_11, PINK_12, MAGENTA_12, MAGENTA_13,
    ORANGE_5, KHAKI_1, PINK_13, PINK_14, LILAC_0, LILAC_1,
    YELLOW_0, KHAKI_2, KHAKI_3, KHAKI_4, LILAC_2, LILAC_3,
    ORANGE_6, YELLOW_1, LIME_6, MINT_0, MINT_1, AZURE_0,
    RED_7, RED_8, MAGENTA_14, MAGENTA_15, MAGENTA_16, MAGENTA_17,
    ORANGE_7, SALMON_1, PINK_15, PINK_16, MAGENTA_18, MAGENTA_19,
    ORANGE_8, SALMON_2, PINK_17, PINK_18, PINK_19, PINK_20,
    ORANGE_9, PEACH_0, PINK_21, PINK_22, PINK_23, PINK_24,
    GOLD_1, KHAKI_5, PEACH_1, PINK_25, PINK_26, PINK_27,
    YELLOW_2, YELLOW_3, YELLOW_4, CREAM_0, CREAM_1, WHITE_0,

    # Grayscale Colors (232-255)
    GRAY_0, GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5,
    GRAY_6, GRAY_7, GRAY_8, GRAY_9, GRAY_10, GRAY_11,
    GRAY_12, GRAY_13, GRAY_14, GRAY_15, GRAY_16, GRAY_17,
    GRAY_18, GRAY_19, GRAY_20, GRAY_21, GRAY_22, GRAY_23,

    # Background Colors
    BG_BLACK, BG_MAROON, BG_GREEN, BG_OLIVE, BG_NAVY,
    BG_PURPLE, BG_TEAL, BG_SILVER, BG_GRAY, BG_RED,
    BG_LIME, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN,
    BG_WHITE, BG_BLACK_0, BG_NAVY_0, BG_NAVY_1, BG_GRAY_23,

    # Style modifiers
    BOLD, DIM, ITALIC, UNDERLINE, BLINK,
    REVERSE, HIDDEN, STRIKE,

    # Reset modifiers
    RESET, RESET_ALL, RESET_BOLD, RESET_DIM,
    RESET_ITALIC, RESET_UNDERLINE, RESET_BLINK,
    RESET_REVERSE, RESET_HIDDEN, RESET_STRIKE,

    # Command aliases
    clear, cat, pwd, cd, mkdir, rmdir, touch, rm
)

from .hot_reload import watch_modules, watch_modules_context, stop_watching

from .llm import (
    ChatGPT, ChatGPTModel, Claude, ClaudeModel,
    claude, interfaces, models
)

from .llm.models import ANTHROPIC_API_KEY, OPENAI_API_KEY

from .note import Note, Notable

from .pprint import Color, EnhancedPrettyPrinter, ppe, ppi, ppw

__all__ = [
    # Core functions
    "old_print", "print", "draw_divider", "get_terminal_width",
    "get_working_dir", "goto_home", "change_dir",
    "make_dir", "remove_dir", "create_file",
    "remove_file", "read_file", "write_file",
    "append_file", "read_json", "clear_screen",
    "go_up",

    # Color utilities
    "Color", "get_color", "get_bg_color",

    # Constants
    "HOME", "USER", "PYTHONHOME", "PYTHONPATH",
    "DEFAULT_PRINT_DELAY", "DEFAULT_TERMINAL_WIDTH",

    # Standard ANSI Colors
    "BLACK", "MAROON", "GREEN", "OLIVE", "NAVY", "PURPLE", "TEAL", "SILVER",

    # Bright ANSI Colors
    "GRAY", "RED", "LIME", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE",

    # 216 Color Cube
    "BLACK_0", "NAVY_0", "NAVY_1", "NAVY_2", "BLUE_0", "BLUE_1",
    "DARKBLUE_0", "DARKBLUE_1", "BLUE_2", "BLUE_3", "BLUE_4", "BLUE_5",
    "GREEN_0", "TEAL_0", "TEAL_1", "TEAL_2", "TEAL_3", "TEAL_4",
    "FOREST_0", "GREEN_1", "GREEN_2", "CYAN_0", "CYAN_1", "CYAN_2",
    "GREEN_3", "GREEN_4", "GREEN_5", "TEAL_5", "CYAN_3", "CYAN_4",
    "BROWN_0", "GREEN_6", "GREEN_7", "SEAFOAM_0", "SEAFOAM_1", "CYAN_5",
    "BROWN_1", "MAROON_0", "PURPLE_0", "PURPLE_1", "PURPLE_2", "PURPLE_3",
    "GREEN_8", "OLIVE_0", "TEAL_6", "STEEL_0", "STEEL_1", "BLUE_6",
    "OLIVE_1", "GREEN_9", "TEAL_7", "STEEL_2", "STEEL_3", "BLUE_7",
    "CHARTREUSE_0", "GREEN_10", "GREEN_11", "TEAL_8", "STEEL_4", "BLUE_8",
    "LIME_0", "LIME_1", "SEAFOAM_2", "SEAFOAM_3", "CYAN_6", "CYAN_7",
    "MAROON_1", "MAROON_2", "PURPLE_4", "PURPLE_5", "PURPLE_6", "PURPLE_7",
    "RED_0", "RED_1", "MAGENTA_0", "MAGENTA_1", "MAGENTA_2", "VIOLET_0",
    "BROWN_2", "BROWN_3", "MAUVE_0", "MAUVE_1", "PURPLE_8", "PURPLE_9",
    "OLIVE_2", "OLIVE_3", "PURPLE_10", "MAUVE_2", "PURPLE_11", "PURPLE_12",
    "LIME_2", "GREEN_12", "GREEN_13", "TEAL_9", "STEEL_5", "BLUE_9",
    "CHARTREUSE_1", "LIME_3", "GREEN_14", "TEAL_10", "CYAN_8", "CYAN_9",
    "RED_2", "PINK_0", "MAGENTA_3", "PINK_1", "PINK_2", "VIOLET_1",
    "RED_3", "RED_4", "MAGENTA_4", "MAGENTA_5", "MAGENTA_6", "VIOLET_2",
    "ORANGE_0", "PINK_3", "PINK_4", "PINK_5", "PURPLE_13", "PURPLE_14",
    "BROWN_4", "OLIVE_4", "MAUVE_3", "MAUVE_4", "PURPLE_15", "PURPLE_16",
    "GOLD_0", "KHAKI_0", "MAUVE_5", "MAUVE_6", "PURPLE_17", "PURPLE_18",
    "LIME_4", "LIME_5", "GREEN_15", "SEAFOAM_4", "CYAN_10", "CYAN_11",
    "ORANGE_1", "ORANGE_2", "PINK_6", "PINK_7", "PINK_8", "VIOLET_3",
    "RED_5", "RED_6", "MAGENTA_7", "MAGENTA_8", "MAGENTA_9", "VIOLET_4",
    "ORANGE_3", "SALMON_0", "PINK_9", "PINK_10", "MAGENTA_10", "MAGENTA_11",
    "ORANGE_4", "TAN_0", "PINK_11", "PINK_12", "MAGENTA_12", "MAGENTA_13",
    "ORANGE_5", "KHAKI_1", "PINK_13", "PINK_14", "LILAC_0", "LILAC_1",
    "YELLOW_0", "KHAKI_2", "KHAKI_3", "KHAKI_4", "LILAC_2", "LILAC_3",
    "ORANGE_6", "YELLOW_1", "LIME_6", "MINT_0", "MINT_1", "AZURE_0",
    "RED_7", "RED_8", "MAGENTA_14", "MAGENTA_15", "MAGENTA_16", "MAGENTA_17",
    "ORANGE_7", "SALMON_1", "PINK_15", "PINK_16", "MAGENTA_18", "MAGENTA_19",
    "ORANGE_8", "SALMON_2", "PINK_17", "PINK_18", "PINK_19", "PINK_20",
    "ORANGE_9", "PEACH_0", "PINK_21", "PINK_22", "PINK_23", "PINK_24",
    "GOLD_1", "KHAKI_5", "PEACH_1", "PINK_25", "PINK_26", "PINK_27",
    "YELLOW_2", "YELLOW_3", "YELLOW_4", "CREAM_0", "CREAM_1", "WHITE_0",

    # Grayscale Colors
    "GRAY_0", "GRAY_1", "GRAY_2", "GRAY_3", "GRAY_4", "GRAY_5",
    "GRAY_6", "GRAY_7", "GRAY_8", "GRAY_9", "GRAY_10", "GRAY_11",
    "GRAY_12", "GRAY_13", "GRAY_14", "GRAY_15", "GRAY_16", "GRAY_17",
    "GRAY_18", "GRAY_19", "GRAY_20", "GRAY_21", "GRAY_22", "GRAY_23",

    # Background Colors
    "BG_BLACK", "BG_MAROON", "BG_GREEN", "BG_OLIVE", "BG_NAVY",
    "BG_PURPLE", "BG_TEAL", "BG_SILVER", "BG_GRAY", "BG_RED",
    "BG_LIME", "BG_YELLOW", "BG_BLUE", "BG_MAGENTA", "BG_CYAN",
    "BG_WHITE", "BG_BLACK_0", "BG_NAVY_0", "BG_NAVY_1", "BG_GRAY_23",

    # Style modifiers
    "BOLD", "DIM", "ITALIC", "UNDERLINE", "BLINK",
    "REVERSE", "HIDDEN", "STRIKE",

    # Reset modifiers
    "RESET", "RESET_ALL", "RESET_BOLD", "RESET_DIM",
    "RESET_ITALIC", "RESET_UNDERLINE", "RESET_BLINK",
    "RESET_REVERSE", "RESET_HIDDEN", "RESET_STRIKE",

    # Command aliases
    "clear", "cat", "pwd", "cd", "mkdir", "rmdir",
    "touch", "rm",

    # LLM related
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
    "Claude", "ClaudeModel", "ChatGPT", "ChatGPTModel",
    "claude", "interfaces", "llm", "models",

    # Other utilities
    "EnhancedPrettyPrinter", "hot_reload", "Notable", "Note", "note", "ppe", "ppi",
    "pprint", "ppw", "stop_watching", "watch_modules", "watch_modules_context"
]
