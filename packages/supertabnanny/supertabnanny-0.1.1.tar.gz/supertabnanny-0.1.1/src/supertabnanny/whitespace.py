# -*- coding: utf-8 -*-

"""
supertabnanny.whitespace - whitespace analysis module
"""

import collections
import dataclasses
import unicodedata

from typing import ClassVar, Iterator, Type

from .console import (
    CYAN,
    EMPTY,
    SPACE_SYMBOL,
    END_FORMAT,
    arrow,
    escape_sequence_start,
)


_SP = "\x20"
_TAB = "\x09"
_LF = "\x0a"
_CR = "\x0d"

_COMMA_BLANK = ", "


@dataclasses.dataclass
class LineFragment:
    """Fragment of a line"""

    source: str

    def __str__(self) -> str:
        """String value"""
        return self.source

    def __eq__(self, other) -> bool:
        """String value"""
        return self.__class__ == other.__class__ and self.source == other.source


@dataclasses.dataclass
class WhitespaceFragment(LineFragment):
    """Whitespace fragment of a line: a single whitespace character"""

    source: str = EMPTY
    allow: ClassVar[str] = EMPTY

    def __post_init__(self) -> None:
        """check for valid source"""
        self.source = self.source or self.allow
        if len(self.source) > 1:
            raise ValueError(
                f"{self.__class__.__name__} instances must always contain"
                " a single character"
            )
        #
        if self.allow and self.source != self.allow:
            raise ValueError(
                f"{self.__class__.__name__} instances must always contain"
                f" {self.allow!r}, not {self.source!r}"
            )
        #
        if unicodedata.category(self.source) not in ("Cc", "Cf", "Zl", "Zp", "Zs"):
            raise ValueError(
                f"{self.source!r} does not appear to be a whitespace character"
            )
        #

    def __str__(self) -> str:
        """String value"""
        return repr(self.source)[1:-1]


@dataclasses.dataclass
class SpaceFragment(WhitespaceFragment):
    """Fragment of a line containing only spaces"""

    allow: ClassVar[str] = _SP

    def __str__(self) -> str:
        """String value"""
        return SPACE_SYMBOL


@dataclasses.dataclass
class TabFragment(WhitespaceFragment):
    """Fragment of a line containing a single Tab character"""

    allow: ClassVar[str] = _TAB

    def expanded_arrow(self, tabsize: int = 4, offset: int = 0) -> str:
        """expand the tab and replace it by an arrow of the expanded length"""
        expanded_size = tabsize - (offset % tabsize)
        return arrow(size=expanded_size)


@dataclasses.dataclass
class LineFeedFragment(WhitespaceFragment):
    """Fragment of a line containing a single line feed character"""

    allow: ClassVar[str] = _LF


@dataclasses.dataclass
class CarriageReturnFragment(WhitespaceFragment):
    """Fragment of a line containing a single carriage return character"""

    allow: ClassVar[str] = _CR


@dataclasses.dataclass
class Calculator:
    """Caculate indent characteristics"""

    source: str
    total: int = dataclasses.field(init=False, default=0)
    trailing_spaces: int = dataclasses.field(init=False, default=0)
    spaces_preceding_tabs: tuple[int, ...] = dataclasses.field(init=False, default=())
    frequencies: tuple[int, ...] = dataclasses.field(init=False, default=())

    def __post_init__(self) -> None:
        """Analyze source and store the analysis results"""
        if self.source:
            # current trailing spaces
            current_trailing_spaces: int = 0
            # collector for number spaces directly before tabs
            spaces_before_tabs: list[int] = []
            for position, character in enumerate(self.source):
                if character == _SP:
                    current_trailing_spaces += 1
                elif character == _TAB:
                    spaces_before_tabs.append(current_trailing_spaces)
                    current_trailing_spaces = 0
                else:
                    self.total = position
                    break
                #
            else:
                self.total = position + 1
            #
            self.trailing_spaces = current_trailing_spaces
            self.spaces_preceding_tabs = tuple(spaces_before_tabs)
        #
        if self.spaces_preceding_tabs:
            freq_counter = collections.Counter(self.spaces_preceding_tabs)
            freq: list[int] = []
            for runlength in range(max(freq_counter) + 1):
                freq.append(freq_counter[runlength])
            #
            self.frequencies = tuple(freq)
        #


@dataclasses.dataclass
class Witness:
    """Witness of indent sizes at a given tabsize"""

    tabsize: int
    own_level: int
    other_level: int


class LineFormatter:
    """Formatter for a line"""

    fragment_types: dict[str, Type[WhitespaceFragment]] = {
        _SP: SpaceFragment,
        _TAB: TabFragment,
        _LF: LineFeedFragment,
        _CR: CarriageReturnFragment,
    }

    def __init__(self, source: str) -> None:
        """Split the line into fragments"""
        self.fragments: tuple[LineFragment, ...] = tuple(self.__iter_fragments(source))
        # total number of tabs in the line
        self.ntabs = len(
            [
                fragment
                for fragment in self.fragments
                if isinstance(fragment, TabFragment)
            ]
        )

    def __iter_fragments(self, source: str) -> Iterator[LineFragment]:
        """Build the fragments"""
        collected: list[str] = []
        for character in source:
            if character == _SP or not character.isprintable():
                if collected:
                    yield LineFragment(EMPTY.join(collected))
                    collected.clear()
                #
                try:
                    yield self.fragment_types[character]()
                except KeyError:
                    yield WhitespaceFragment(character)
                #
            else:
                collected.append(character)
            #
        #
        if collected:
            yield LineFragment(EMPTY.join(collected))
        #

    @staticmethod
    def get_replacement(
        fragment: LineFragment, tabsize: int = 4, offset: int = 0
    ) -> str:
        """Return the replacement for a fragment"""
        if isinstance(fragment, TabFragment):
            return fragment.expanded_arrow(tabsize=tabsize, offset=offset)
        #
        return str(fragment)

    def iter_chunks(self, tabsize: int = 4) -> Iterator[tuple[bool, str]]:
        """Iterate over replacement chunks calculated for the given tabsize"""
        collected: list[str] = []
        last_whitespace = False
        current_whitespace = False
        offset = 0
        for fragment in self.fragments:
            current_whitespace = isinstance(fragment, WhitespaceFragment)
            if current_whitespace != last_whitespace:
                if collected:
                    yield last_whitespace, EMPTY.join(collected)
                    collected.clear()
                #
                last_whitespace = current_whitespace
            #
            replacement = self.get_replacement(fragment, tabsize=tabsize, offset=offset)
            collected.append(replacement)
            match fragment:
                case LineFeedFragment() | CarriageReturnFragment():
                    offset = 0
                case SpaceFragment():
                    offset += 1
                case _:
                    offset += len(replacement)
                #
            #
        #
        yield current_whitespace, EMPTY.join(collected)

    def format(
        self, tabsize: int = 4, fg: int | None = CYAN, bg: int | None = None
    ) -> str:
        """Return the line with whitespace characters replaced
        by their visualizations (spaces by middle dots, tabs by arrows,
        line feeds by \n, carriage return by \r, other whitespace
        characters by their backslash representation),
        and highlighted using ANSI escapes if fg and or bg are not None.
        """
        highlight_start = escape_sequence_start(fg=fg, bg=bg)
        highlight_end = END_FORMAT if highlight_start else EMPTY
        last_whitespace = False
        output_parts: list[str] = []
        for current_whitespace, chunk in self.iter_chunks(tabsize=tabsize):
            if current_whitespace and not last_whitespace:
                output_parts.append(f"{highlight_start}")
            elif last_whitespace and not current_whitespace:
                output_parts.append(f"{highlight_end}")
            #
            output_parts.append(chunk)
            last_whitespace = current_whitespace
        #
        if last_whitespace:
            output_parts.append(highlight_end)
        #
        return EMPTY.join(output_parts)


class WitnessesGroup:
    """Group of witnesses"""

    def __init__(self, prefix: str = "") -> None:
        """Initialization argument:

        *   _prefix_: prefix for the string representation
        """
        self.__prefix = prefix
        self.__witnesses: list[Witness] = []

    @property
    def tabsizes(self) -> list[int]:
        """Return the list of affected tabsizes"""
        return [witness.tabsize for witness in self.__witnesses]

    def add(self, witness: Witness) -> None:
        """Add _witness_"""
        self.__witnesses.append(witness)

    def __repr__(self) -> str:
        """Object representation"""
        return (
            f"{self.__class__.__name__}({self.__prefix!r})"
            f" with tabsizes {self.tabsizes}"
        )

    def __str__(self) -> str:
        """String representation"""
        ts = self.tabsizes
        if not ts:
            return self.__prefix
        #
        plural = "s" if len(ts) > 1 else ""
        return f"{self.__prefix}at tab size{plural} {_COMMA_BLANK.join(map(str, ts))}"


class Normalization:
    """Normalization of leading Whitespace in a string"""

    def __init__(self, source: str) -> None:
        """Determine leading whitespace in _source_,
        and store a normalized representation
        """
        self.__calculator = Calculator(source)
        self.__longest_run_of_spaces = max(
            len(self.frequencies) - 1, self.trailing_spaces
        )
        self.__explicit_tabs = sum(self.frequencies)
        self.__tabs_with_no_preceding_spaces: bool = len(self.frequencies) == 1

    # @staticmethod

    @property
    def explicit_tabs(self) -> int:
        """Number of explicit tab characters"""
        return self.__explicit_tabs

    @property
    def tabs_only(self) -> bool:
        """Special form 'T+': at least one tab, no spaces at all"""
        return self.__tabs_with_no_preceding_spaces and not self.trailing_spaces

    @property
    def tabs_with_no_preceding_spaces(self) -> bool:
        r"""Special form 'T+S\*': at least one tab, but no spaces before tabs"""
        return self.__tabs_with_no_preceding_spaces

    @property
    def longest_run_of_spaces(self) -> int:
        """Longest consecutive run of spaces"""
        return self.__longest_run_of_spaces

    @property
    def frequencies(self) -> tuple[int, ...]:
        r"""Frequencies of spaces directly preceding tabs,
        indexed by number of spaces before the tab character:

        *   frequencies\[0\]: number of tabs
            **not** directly preceded by spaces
        *   frequencies\[1\]: number of tabs
            directly preceded by **exactly 1** space
        *   frequencies\[2\]: number of tabs
            directly preceded by **excatly 2** spaces
        *   (...)
        *   frequencies\[_n_\]: number of tabs
            directly preceded by **excatly _n_** spaces
        """
        return self.__calculator.frequencies

    @property
    def trailing_spaces(self) -> int:
        """Number of trailing spaces"""
        return self.__calculator.trailing_spaces

    def __len__(self) -> int:
        """Total number of leading whitespace characters"""
        return self.__calculator.total

    def __eq__(self, other) -> bool:
        """Rich "equals": compare normalized repreesentation"""
        return (
            self.frequencies == other.frequencies
            and self.trailing_spaces == other.trailing_spaces
        )

    def get_expanded_size(self, tabsize: int) -> int:
        """Calculate expanded size depending on the provided _tabsize_

        1.  Calculate total number of tabs as the sum of explicit tabs
            and tabs inferred from leading spaces.

            *   base formula
                (ls = leading spaces, ts = tabsize, freq = frequencies):

                    tabs = explicit_tabs + sum(ls // ts * freq[ls])

                (the sum is calculated over all freq members)

            *   regarding that `ls // ts == 0` for all `ls < ts`,
                we can start the loop at `freq[ts]` instead of `freq[0]`

            *   An alternative approach would be to lift all indexes by ts
                (`increased_ls = ls + ts)`
                which would simplify the algorithm to

                    tabs = sum(increased_ls // ts * freq[ls])

                but involve more calculations, being less efficient
                than simply adding the known fixed number of explicit tabs

        2.  Calculate the expanded size by multiplying the total number of tabs
            with the tabsize and adding the trailing spaces
        """
        if tabsize < 1:
            raise ValueError("A tabsize of at lest 1 is required")
        #
        over_tabsize_frequencies = self.frequencies[tabsize:]
        additional_tabs = sum(
            leading_spaces // tabsize * frequency
            for leading_spaces, frequency in enumerate(
                over_tabsize_frequencies, start=tabsize
            )
        )
        total_tabs = self.__explicit_tabs + additional_tabs
        return total_tabs * tabsize + self.trailing_spaces


class LeadingWhitespace:
    """Handle leading whitespace

    An attempt to refactor the standard library’s tabnanny.Whitespace class
    """

    def __init__(self, source: str, compatibility_mode: bool = False) -> None:
        """Determine leading whitespace in source,
        assuming it contains only one line
        """
        self.raw = source
        self.__normalization = Normalization(source)
        self.__indent_by_tabsize: dict[int, int] = {}
        self.__compatibility_mode = compatibility_mode

    @property
    def no_spaces_before_tabs(self) -> bool:
        """Special form 'T*S*': no spaces before tabs,
        but maybe tabs and/or trailing spaces
        """
        return (
            self.normalization.tabs_with_no_preceding_spaces
            or not self.normalization.explicit_tabs
        )

    @property
    def longest_run_of_spaces(self) -> int:
        """Longest consecutive run of spaces"""
        return self.normalization.longest_run_of_spaces

    @property
    def normalization(self) -> Normalization:
        """normalization"""
        return self.__normalization

    @property
    def explicit_tabs(self) -> int:
        """number of tab characters"""
        return self.normalization.explicit_tabs

    def __len__(self) -> int:
        """Total number of characters"""
        return len(self.normalization)

    def __eq__(self, other) -> bool:
        """Rich "equals": compare normalized repreesentation"""
        return self.normalization == other.normalization

    def __ge__(self, other) -> bool:
        r"""Rich "greater or equal": at least for one tab size,
        the own expanded size is greater than or equal to the other one.

        This is always true for leading whitespace of the same length
        or greater when assuming a tab size of 1 (shorcut #1)

        In the frequent special case 'T\*S\*', the expanded size
        is always greater than or equal to the other instance
        if the number of tabs is greater (shortcut #2)
        """
        # shoercut #1
        if len(self) >= len(other):
            return True
        #
        if (
            self.normalization.tabs_with_no_preceding_spaces
            and other.normalization.tabs_with_no_preceding_spaces
            and self.explicit_tabs > other.explicit_tabs
        ):
            return True
        #
        for witness in self._iter_witnesses(other):
            if witness.own_level >= witness.other_level:
                return True
            #
        #
        return False

    def _iter_witnesses(self, other, start: int = 1) -> Iterator[Witness]:
        """Return an iterator over Witness instances"""
        max_tabsize = max(self.longest_run_of_spaces, other.longest_run_of_spaces) + 1
        for tabsize in range(start, max_tabsize + 1):
            yield Witness(
                tabsize,
                self.cached_expanded_size(tabsize),
                other.cached_expanded_size(tabsize),
            )
        #

    def greater_or_equal_witnesses(self, other) -> WitnessesGroup:
        """Return an iterator over Witness instances"""
        if self.__compatibility_mode:
            prefix = "indent not greater e.g. "
        else:
            prefix = "expanded size greater or equal "
        #
        group = WitnessesGroup(prefix)
        for witness in self._iter_witnesses(other):
            if witness.own_level >= witness.other_level:
                group.add(witness)
            #
        #
        return group

    def not_equal_witnesses(self, other) -> WitnessesGroup:
        """Return an iterator over Witness instances"""
        if self.__compatibility_mode:
            prefix = "indent not equal e.g. "
        else:
            prefix = "expanded size different "
        #
        group = WitnessesGroup(prefix)
        for witness in self._iter_witnesses(other):
            if witness.own_level != witness.other_level:
                group.add(witness)
            #
        #
        return group

    def cached_expanded_size(self, tabsize: int) -> int:
        """return cached expanded size by tabsize or calculate it"""
        try:
            return self.__indent_by_tabsize[tabsize]
        except KeyError:
            expanded = self.normalization.get_expanded_size(tabsize)
            self.__indent_by_tabsize[tabsize] = expanded
            return expanded
        #
