# -*- coding: utf-8 -*-

"""
console colors and functions
"""

import logging


EMPTY = ""
LF = "\n"

ARROW_TAIL = chr(0x2014)
ARROW_HEAD = chr(0x21E5)
SPACE_SYMBOL = chr(0xB7)

# ANSI COLOR BASE NUMBERS
BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

_DARK_LIMITS = (BLACK, WHITE)
_BRIGHT_LIMITS = tuple(limit + 60 for limit in _DARK_LIMITS)

# COLOR_OFFSETS
_FOREGROUND_OFFSET = 30
_BACKGROUND_OFFSET = 40

CSI = "\x1b["

ROOT_LOGGER = logging.getLogger()


def initialize_root_logger(loglevel: int) -> None:
    """Initialize the root logger"""
    formatter = logging.Formatter("%(levelname)-8s | %(message)s")
    stream_handlers = [
        handler
        for handler in ROOT_LOGGER.handlers
        if isinstance(handler, logging.StreamHandler)
    ]
    if stream_handlers:
        current_handler = stream_handlers[0]
    else:
        current_handler = logging.StreamHandler()
        ROOT_LOGGER.addHandler(current_handler)
    #
    current_handler.setFormatter(formatter)
    current_handler.setLevel(loglevel)
    ROOT_LOGGER.setLevel(loglevel)


def csi_m_sequence(enclosed: str | int) -> str:
    r"""return a full CSI…m sequence"""
    return f"\x1b[{enclosed}m"


END_FORMAT = csi_m_sequence(0)


def checked_color(color: int) -> int:
    """Allow a dark or bright color"""
    if (
        _DARK_LIMITS[0] <= color <= _DARK_LIMITS[1]
        or _BRIGHT_LIMITS[0] <= color <= _BRIGHT_LIMITS[1]
    ):
        return color
    #
    raise ValueError(
        f"Color code {color} not inside limits {_DARK_LIMITS} or {_BRIGHT_LIMITS}"
    )


def bright(color: int) -> int:
    """bright color"""
    if _DARK_LIMITS[0] <= color <= _DARK_LIMITS[1]:
        return color + 60
    #
    raise ValueError(f"Color code {color} not inside limits {_DARK_LIMITS}")


def background_color(color: int | None) -> int | None:
    """Allow a dark or bright color"""
    if color is None:
        return color
    #
    return checked_color(color) + _BACKGROUND_OFFSET


def foreground_color(color: int | None) -> int | None:
    """Allow a dark or bright color"""
    if color is None:
        return color
    #
    return checked_color(color) + _FOREGROUND_OFFSET


def escape_sequence_start(fg: int | None = None, bg: int | None = None) -> str:
    """Return the escape sequence for setting fg and bg colors"""
    bg_color: int | None = background_color(bg)
    fg_color: int | None = foreground_color(fg)
    if bg_color is None:
        if fg_color is None:
            return EMPTY
        #
        return csi_m_sequence(int(fg_color))
    #
    if fg_color is None:
        return csi_m_sequence(int(bg_color))
    #
    return csi_m_sequence(f"{fg_color};{bg_color}")


def colorized(text: str, fg: int | None = None, bg: int | None = None) -> str:
    """Return text surrounded with ANSI excape sequences for color"""
    start_csi_sequence = escape_sequence_start(fg=fg, bg=bg)
    if not start_csi_sequence:
        return text
    #
    return f"{start_csi_sequence}{text}{END_FORMAT}"


def arrow(size: int = 1, head: str = ARROW_HEAD, tail: str = ARROW_TAIL) -> str:
    """Return a right-pointing console arrow of size _size_"""
    if size < 1:
        raise ValueError("Arrow size must be 1 or greater")
    #
    return EMPTY.join((tail * (size - 1), head))
