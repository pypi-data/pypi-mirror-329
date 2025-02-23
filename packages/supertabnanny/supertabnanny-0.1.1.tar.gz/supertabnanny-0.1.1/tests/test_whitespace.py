# -*- coding: utf-8 -*-
"""
Test the supertabnanny.whitespace module
"""

# import itertools
import secrets

from unittest import TestCase

from supertabnanny import whitespace

EMPTY = ""
SP = " "
TAB = "\t"
SP_TAB = f"{SP}{TAB}"
LETTER_S = "S"
LETTER_T = "T"
LETTERS_ST = f"{LETTER_S}{LETTER_T}"
SYMBOLIZE = str.maketrans(SP_TAB, LETTERS_ST)
DESYMBOLIZE = str.maketrans(LETTERS_ST, SP_TAB)

KW_NUMBER_OF_TABS = "number of tabs"
KW_TOTAL_NUMBER_OF_CHARS = "total number"
KW_NO_TABS = "not tabs"
KW_TABS_ONLY = "tabs only"
KW_LONGEST_RUN_OF_SPACES = "longest run of spaces"
KW_INDENT_LEVEL = "index level"
KW_NO_SBT = "no spaces before tabs"
KW_EXPANDED_SIZE = "expanded size"
KW_ATTRIBUTE = "attribute"
KW_FREQUENCIES = "frequencies"
KW_TRAILING_SPACES = "trailing spaces"

WG_GE_COMPATIBILITY = "indent not greater e.g. "
WG_GE_NEWSTYLE = "expanded size greater or equal "
WG_NE_COMPATIBILITY = "indent not equal e.g. "
WG_NE_NEWSTYLE = "expanded size different "


FUZZ_ITERATIONS = 500

#
# Helper functions
#


def get_random_prefix(min_length: int = 2, max_length: int = 80) -> str:
    """Return a random combination of tabs and spaces between the two lengths"""
    length = min_length + secrets.randbelow(max_length + 1 - min_length)
    collector = [secrets.choice(SP_TAB) for _ in range(length)]
    return EMPTY.join(collector)


def sym2ws(symbolic: str) -> str:
    """Convert symbols S and T for spaces and tabs in a string to whitespace"""
    return symbolic.translate(DESYMBOLIZE)


def ws2sym(preceding_whitespace: str) -> str:
    """Convert whitespace in a string to symbols S and T for spaces and Tabs"""
    return preceding_whitespace.translate(SYMBOLIZE)


#
# Test cases
#


class LineFragment(TestCase):
    """LineFragment class"""

    def test_str(self) -> None:
        """Initialization and string representation"""
        for source in ("Ole", "Dole", "Doffen"):
            with self.subTest("str", source=source):
                self.assertEqual(str(whitespace.LineFragment(source)), source)
            #
        #

    def test_eq(self) -> None:
        """equality"""
        with self.subTest("equal"):
            self.assertEqual(
                whitespace.LineFragment("Ole"),
                whitespace.LineFragment("Ole"),
            )
        #
        with self.subTest("equal"):
            self.assertNotEqual(
                whitespace.LineFragment("Dole"),
                whitespace.LineFragment("Doffen"),
            )
        #


class WhitespaceFragment(TestCase):
    """WhitespaceFragment class"""

    def test_postinit_errors(self) -> None:
        """__post_init__() method"""
        for source, expected_error_message_re in (
            (
                "  ",
                "^WhitespaceFragment instances must always contain a single character$",
            ),
            (
                "x",
                "^'x' does not appear to be a whitespace character",
            ),
        ):
            with self.subTest("__post_init__", source=source):
                self.assertRaisesRegex(
                    ValueError,
                    expected_error_message_re,
                    whitespace.WhitespaceFragment,
                    source,
                )
            #
        #

    def test_str(self) -> None:
        """Initialization and string representation"""
        testcases: list[tuple[str, str]] = [
            ("\t", "\\t"),
            ("\n", "\\n"),
            ("\r", "\\r"),
            ("\x0b", "\\x0b"),
            ("\x0c", "\\x0c"),
        ]
        for codepoint in (
            0x85,
            0xA0,
            0x1680,
            0x180E,
            *(range(0x2000, 0x200E)),
            0x2028,
            0x2029,
            0x202F,
            0x205F,
            0x2060,
            0x3000,
            0xFEFF,
        ):
            character = chr(codepoint)
            testcases.append(
                (
                    character,
                    character.encode("ascii", errors="backslashreplace").decode(
                        "utf-8"
                    ),
                )
            )
        for source, expected_value in testcases:
            with self.subTest("str", source=source):
                self.assertEqual(
                    str(whitespace.WhitespaceFragment(source)), expected_value
                )
            #
        #


class SpaceFragment(TestCase):
    """SpaceFragment class"""

    def test_postinit_errors(self) -> None:
        """__post_init__() method"""
        for source, expected_error_message_re in (
            (
                "\t",
                "^SpaceFragment instances must always contain ' ', not '\\\\t'$",
            ),
            (
                "y",
                "^SpaceFragment instances must always contain ' ', not 'y'$",
            ),
        ):
            with self.subTest("__post_init__", source=source):
                self.assertRaisesRegex(
                    ValueError,
                    expected_error_message_re,
                    whitespace.SpaceFragment,
                    source,
                )
            #
        #

    def test_str(self) -> None:
        """Initialization and string representation"""
        self.assertEqual(str(whitespace.SpaceFragment()), "·")


class TabFragment(TestCase):
    """TabFragment class"""

    def test_postinit_errors(self) -> None:
        """__post_init__() method"""
        self.assertRaisesRegex(
            ValueError,
            "^TabFragment instances must always contain '\\\\t', not '\\\\n'$",
            whitespace.TabFragment,
            "\n",
        )

    def test_str(self) -> None:
        """Initialization and string representation"""
        self.assertEqual(str(whitespace.TabFragment()), "\\t")

    def test_expanded_arrow(self) -> None:
        """expanded_arrow() method"""
        tab_fragment = whitespace.TabFragment()
        for arrow_data, expected_result in (
            ({"tabsize": 4, "offset": 0}, "———⇥"),
            ({"tabsize": 5, "offset": 7}, "——⇥"),
            ({"tabsize": 1, "offset": 0}, "⇥"),
            ({"tabsize": 8, "offset": 1}, "——————⇥"),
        ):
            with self.subTest("expanded_arror", expected_result=expected_result):
                self.assertEqual(
                    tab_fragment.expanded_arrow(**arrow_data), expected_result
                )
            #
        #


class LineFeedFragment(TestCase):
    """LineFeedFragment class"""

    def test_postinit_errors(self) -> None:
        """__post_init__() method"""
        self.assertRaisesRegex(
            ValueError,
            "^LineFeedFragment instances must always contain '\\\\n', not '\\\\r'$",
            whitespace.LineFeedFragment,
            "\r",
        )

    def test_str(self) -> None:
        """Initialization and string representation"""
        self.assertEqual(str(whitespace.LineFeedFragment()), "\\n")


class CarriageReturnFragment(TestCase):
    """CarriageReturnFragment class"""

    def test_postinit_errors(self) -> None:
        """__post_init__() method"""
        self.assertRaisesRegex(
            ValueError,
            "^CarriageReturnFragment instances must always contain"
            " '\\\\r', not '\\\\t'$",
            whitespace.CarriageReturnFragment,
            "\t",
        )

    def test_str(self) -> None:
        """Initialization and string representation"""
        self.assertEqual(str(whitespace.CarriageReturnFragment()), "\\r")


class Witness(TestCase):
    """Witness class"""

    def test_attributes(self) -> None:
        """Initialization and attributes"""
        tabsize, own_level, other_level = 4, 7, 8
        witness = whitespace.Witness(tabsize, own_level, other_level)
        with self.subTest(KW_ATTRIBUTE, name="tabsize"):
            self.assertEqual(witness.tabsize, tabsize)
        #
        with self.subTest(KW_ATTRIBUTE, name="own_level"):
            self.assertEqual(witness.own_level, own_level)
        #
        with self.subTest(KW_ATTRIBUTE, name="other_level"):
            self.assertEqual(witness.other_level, other_level)
        #


class WitnessesGroup(TestCase):
    """WitnessesGroup class"""

    def test_single(self) -> None:
        """group with only a single witness"""
        witnesses_group = whitespace.WitnessesGroup(prefix="single witness ")
        witnesses_group.add(whitespace.Witness(1, 2, 3))
        self.assertEqual(str(witnesses_group), "single witness at tab size 1")

    def test_multiple(self) -> None:
        """group with muttiple witnesses"""
        witnesses_group = whitespace.WitnessesGroup(prefix="multiple witnesses ")
        witnesses_group.add(whitespace.Witness(4, 5, 6))
        witnesses_group.add(whitespace.Witness(7, 8, 9))
        witnesses_group.add(whitespace.Witness(20, 5, 5))
        self.assertEqual(
            str(witnesses_group), "multiple witnesses at tab sizes 4, 7, 20"
        )


class LineFormatter(TestCase):
    """LineFormatter class"""

    def setUp(self) -> None:
        """Full diff"""
        # pylint: disable=invalid-name ; defined in unittest.TestCase
        self.maxDiff = None

    def test_attributes(self) -> None:
        """Initialization and attributes"""
        for source, expected_ntabs, expected_fragments in (
            (
                " \t print('hello world')\r\n",
                1,
                (
                    whitespace.SpaceFragment(" "),
                    whitespace.TabFragment("\t"),
                    whitespace.SpaceFragment(" "),
                    whitespace.LineFragment("print('hello"),
                    whitespace.SpaceFragment(" "),
                    whitespace.LineFragment("world')"),
                    whitespace.LineFeedFragment("\n"),
                ),
            ),
        ):
            formatter = whitespace.LineFormatter(source)
            with self.subTest(
                "attributes", source=source, expected_ntabs=expected_ntabs
            ):
                self.assertEqual(formatter.ntabs, expected_ntabs)
            #
            with self.subTest(
                "attributes", source=source, expected_fragments=expected_fragments
            ):
                self.assertEqual(formatter.ntabs, expected_ntabs)
            #
        #

    def test_arrow_head_positions(self):
        """.format() method: test if all arrow heads of tab replacements
        are at correct positions (each directly before a tab stop,
        position % tabsize == tabsize - 1)
        """
        for source in (
            " \t print('hello world')\r\n",
            "\t\t\tprint('hello\tworld')\n",
            " \t  \t   \tprint('\thello \t       \t   \tworld\t\u2000')",
        ):
            for tabsize in range(1, 100):
                formatted = whitespace.LineFormatter(source).format(
                    tabsize=tabsize, fg=None, bg=None
                )
                found_at = -1
                while True:
                    found_at = formatted.find(chr(0x21E5), found_at + 1)
                    if found_at == -1:
                        break
                    #
                    with self.subTest(
                        "arrow head", source=source, tabsize=tabsize, found_at=found_at
                    ):
                        self.assertEqual(found_at % tabsize, tabsize - 1)
                    #
                #
            #
        #


class Normalization(TestCase):
    """LeadingWhitespace class"""

    def test_attributes_fuzzed(self) -> None:
        """initialization with various combinations of spaces and tabs"""
        for iteration in range(FUZZ_ITERATIONS):
            source = get_random_prefix()
            normal = whitespace.Normalization(source)
            display = ws2sym(source)
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_NUMBER_OF_TABS,
            ):
                self.assertEqual(normal.explicit_tabs, source.count(TAB))
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_TOTAL_NUMBER_OF_CHARS,
            ):
                self.assertEqual(len(normal), len(source))
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_TABS_ONLY,
            ):
                self.assertEqual(normal.tabs_only, SP not in source)
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_LONGEST_RUN_OF_SPACES,
            ):
                self.assertEqual(
                    normal.longest_run_of_spaces,
                    max(len(item) for item in source.split(TAB)),
                )
            #
        #

    def test_attributes(self) -> None:
        """initialization and attributes for a selected source"""
        symbolic_prefix = "SSSSSTSSSSSSSSSTSSTSTTTSSTTSSSSSSSSTSSS"
        source = f"{sym2ws(symbolic_prefix)}real_line_content = True"
        normal = whitespace.Normalization(source)
        with self.subTest(
            symbolic_prefix,
            subject=KW_FREQUENCIES,
        ):
            self.assertEqual(normal.frequencies, (3, 1, 2, 0, 0, 1, 0, 0, 1, 1))
        #
        with self.subTest(
            symbolic_prefix,
            subject=KW_TRAILING_SPACES,
        ):
            self.assertEqual(normal.trailing_spaces, 3)
        #
        with self.subTest(
            symbolic_prefix,
            subject=KW_NUMBER_OF_TABS,
        ):
            self.assertEqual(normal.explicit_tabs, symbolic_prefix.count(LETTER_T))
        #
        with self.subTest(
            symbolic_prefix,
            subject=KW_TOTAL_NUMBER_OF_CHARS,
        ):
            self.assertLess(len(normal), len(source))
            self.assertEqual(len(normal), len(symbolic_prefix))
        #
        with self.subTest(
            symbolic_prefix,
            subject=KW_TABS_ONLY,
        ):
            self.assertFalse(normal.tabs_only)
        #
        with self.subTest(
            symbolic_prefix,
            subject=KW_LONGEST_RUN_OF_SPACES,
        ):
            self.assertEqual(
                normal.longest_run_of_spaces,
                max(len(item) for item in symbolic_prefix.split(LETTER_T)),
            )
        #

    def test_frequencies(self) -> None:
        """.frequencies property"""
        for symbolic_source, expected_frequencies in (
            ("SSTTSTSSST", (1, 1, 1, 1)),
            ("STSTSTTTSS", (2, 3)),
        ):
            with self.subTest("norm", symbolic_source=symbolic_source):
                self.assertEqual(
                    whitespace.Normalization(sym2ws(symbolic_source)).frequencies,
                    expected_frequencies,
                )
            #
        #

    def test_expanded_size_error(self) -> None:
        """.get_expanded_size() method, errors with invalid tab sizes"""
        normalization = whitespace.Normalization("example")
        for invalid_tab_size in (-2, -1, 0):
            with self.subTest("invalid tab_size", invalid_tab_size=invalid_tab_size):
                self.assertRaisesRegex(
                    ValueError,
                    "^A tabsize of at lest 1 is required$",
                    normalization.get_expanded_size,
                    invalid_tab_size,
                )
            #
        #

    def test_expanded_size_fuzzed(self) -> None:
        """.get_expanded_size() method, fuzzed"""
        for iteration in range(FUZZ_ITERATIONS):
            source = get_random_prefix()
            normal = whitespace.Normalization(source)
            display = ws2sym(source)
            for tab_size in range(1, normal.longest_run_of_spaces + 1):
                with self.subTest(
                    display,
                    iteration=iteration,
                    subject=KW_EXPANDED_SIZE,
                    tab_size=tab_size,
                ):
                    self.assertEqual(
                        normal.get_expanded_size(tab_size),
                        len(source.expandtabs(tab_size)),
                    )
                #
            #
        #


class LeadingWhitespace(TestCase):
    """LeadingWhitespace class"""

    def test_attributes_fuzzed(self) -> None:
        """initialization with various combinations of spaces and tabs"""
        for iteration in range(FUZZ_ITERATIONS):
            source = get_random_prefix()
            leading_whitespace = whitespace.LeadingWhitespace(source)
            display = ws2sym(source)
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_NUMBER_OF_TABS,
            ):
                self.assertEqual(leading_whitespace.explicit_tabs, source.count(TAB))
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_TOTAL_NUMBER_OF_CHARS,
            ):
                self.assertEqual(len(leading_whitespace), len(source))
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_LONGEST_RUN_OF_SPACES,
            ):
                self.assertEqual(
                    leading_whitespace.longest_run_of_spaces,
                    max(len(item) for item in source.split(TAB)),
                )
            #
            with self.subTest(
                display,
                iteration=iteration,
                subject=KW_NO_SBT,
            ):
                self.assertEqual(
                    leading_whitespace.no_spaces_before_tabs,
                    SP_TAB not in source,
                )
            #
        #

    def test_ge(self) -> None:
        """Test "greater or equal" capability"""
        first = "SSS"
        second = "TT"
        with self.subTest("by length (shortcut #1)", first=first, second=second):
            self.assertTrue(
                whitespace.LeadingWhitespace(sym2ws(first))
                >= whitespace.LeadingWhitespace(sym2ws(second))
            )
        #
        first = "TTS"
        second = "TSSS"
        with self.subTest(
            "by tab number if no sbt (shortcut #2)", first=first, second=second
        ):
            self.assertTrue(
                whitespace.LeadingWhitespace(sym2ws(first))
                >= whitespace.LeadingWhitespace(sym2ws(second))
            )
        #
        first = "STT"
        second = "STSS"
        with self.subTest(
            "normal evaluation if sbt (ge case)", first=first, second=second
        ):
            self.assertTrue(
                whitespace.LeadingWhitespace(sym2ws(first))
                >= whitespace.LeadingWhitespace(sym2ws(second))
            )
        #
        first = "ST"
        second = "STT"
        with self.subTest(
            "normal evaluation if sbt (lt resp not ge case)", first=first, second=second
        ):
            self.assertFalse(
                whitespace.LeadingWhitespace(sym2ws(first))
                >= whitespace.LeadingWhitespace(sym2ws(second))
            )
        #

    def test_ge_witnesses(self) -> None:
        """test the .greater_or_equal_witnesses() method"""
        with self.subTest(WG_GE_COMPATIBILITY):
            first = whitespace.LeadingWhitespace(
                sym2ws("SSSTT"), compatibility_mode=True
            )
            second = whitespace.LeadingWhitespace(
                sym2ws("SSSTSS"), compatibility_mode=True
            )
            self.assertEqual(
                str(first.greater_or_equal_witnesses(second)),
                f"{WG_GE_COMPATIBILITY}at tab sizes 2, 3, 4",
            )
        #
        with self.subTest(WG_GE_NEWSTYLE):
            first = whitespace.LeadingWhitespace(sym2ws("SSSTT"))
            second = whitespace.LeadingWhitespace(sym2ws("SSSTSS"))
            self.assertEqual(
                str(first.greater_or_equal_witnesses(second)),
                f"{WG_GE_NEWSTYLE}at tab sizes 2, 3, 4",
            )
        #

    def test_ne_witnesses(self) -> None:
        """test the .not_equal_witnesses() method"""
        with self.subTest(WG_NE_COMPATIBILITY):
            first = whitespace.LeadingWhitespace(
                sym2ws("SSSTT"), compatibility_mode=True
            )
            second = whitespace.LeadingWhitespace(
                sym2ws("SSSTSS"), compatibility_mode=True
            )
            self.assertEqual(
                str(first.not_equal_witnesses(second)),
                f"{WG_NE_COMPATIBILITY}at tab sizes 1, 3, 4",
            )
        #
        with self.subTest(WG_NE_NEWSTYLE):
            first = whitespace.LeadingWhitespace(sym2ws("SSSTT"))
            second = whitespace.LeadingWhitespace(sym2ws("SSSTSS"))
            self.assertEqual(
                str(first.not_equal_witnesses(second)),
                f"{WG_NE_NEWSTYLE}at tab sizes 1, 3, 4",
            )
        #
