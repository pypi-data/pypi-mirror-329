# -*- coding: utf-8 -*-
"""
Test the supertabnanny.console module
"""

import itertools
import secrets

from unittest import TestCase

from supertabnanny import console


DARK_RANGE = range(0, 8)
BRIGHT_RANGE = range(60, 68)
VALID_COLOR_CODES = list(itertools.chain(DARK_RANGE, BRIGHT_RANGE))


class CsiMSequence(TestCase):
    """csi_m_sequence() function"""

    def test_number(self) -> None:
        """CSI-M-Sequence with a number"""
        self.assertEqual(console.csi_m_sequence(0), "\x1b[0m")

    def test_string(self) -> None:
        """CSI-M-Sequence with a string"""
        self.assertEqual(console.csi_m_sequence("31;47"), "\x1b[31;47m")


class CheckedColor(TestCase):
    """checked_color() function"""

    def test_valid(self) -> None:
        """valid values (0–7 or 60–67)"""
        for value in VALID_COLOR_CODES:
            with self.subTest("valid", value=value):
                self.assertEqual(console.checked_color(value), value)
            #
        #

    def test_invalid_fuzzed(self) -> None:
        """invalid values: everything else (fuzzed)"""
        not_inside_limits_re = r"not inside limits \(0, 7\) or \(60, 67\)"
        for iteration in range(100):
            value = 8 + secrets.randbelow(52)
            with self.subTest("invalid midrange", iteration=iteration, value=value):
                self.assertRaisesRegex(
                    ValueError,
                    f"^Color code {value} {not_inside_limits_re}$",
                    console.checked_color,
                    value,
                )
            #
        #
        for iteration in range(100):
            value = 68 + secrets.randbelow(188)
            with self.subTest("invalid high range", iteration=iteration, value=value):
                self.assertRaisesRegex(
                    ValueError,
                    f"^Color code {value} {not_inside_limits_re}$",
                    console.checked_color,
                    value,
                )
            #
        #
        for iteration in range(100):
            value = -1 - secrets.randbelow(2000)
            with self.subTest("invalid low range", iteration=iteration, value=value):
                self.assertRaisesRegex(
                    ValueError,
                    f"^Color code {value} {not_inside_limits_re}$",
                    console.checked_color,
                    value,
                )
            #
        #


class Bright(TestCase):
    """bright() function"""

    def test_valid(self) -> None:
        """valid values (0–7)"""
        for value in DARK_RANGE:
            with self.subTest("valid", value=value):
                self.assertEqual(console.bright(value), value + 60)
            #
        #

    def test_invalid_fuzzed(self) -> None:
        """invalid values: everything else (fuzzed)"""
        not_inside_limits_re = r"not inside limits \(0, 7\)"
        for iteration in range(100):
            value = 8 + secrets.randbelow(248)
            with self.subTest("invalid high range", iteration=iteration, value=value):
                self.assertRaisesRegex(
                    ValueError,
                    f"^Color code {value} {not_inside_limits_re}$",
                    console.bright,
                    value,
                )
            #
        #
        for iteration in range(100):
            value = -1 - secrets.randbelow(2000)
            with self.subTest("invalid low range", iteration=iteration, value=value):
                self.assertRaisesRegex(
                    ValueError,
                    f"^Color code {value} {not_inside_limits_re}$",
                    console.bright,
                    value,
                )
            #
        #


class BackgroudColor(TestCase):
    """background_color() function"""

    def test_none(self) -> None:
        """Test with None parameter"""
        self.assertIsNone(console.background_color(None))

    def test_valid(self) -> None:
        """Test with valid values"""
        for value in VALID_COLOR_CODES:
            with self.subTest("valid", value=value):
                self.assertEqual(console.background_color(value), value + 40)
            #
        #


class ForegroudColor(TestCase):
    """foreground_color() function"""

    def test_none(self) -> None:
        """Test with None parameter"""
        self.assertIsNone(console.foreground_color(None))

    def test_valid(self) -> None:
        """Test with valid values"""
        for value in VALID_COLOR_CODES:
            with self.subTest("valid", value=value):
                self.assertEqual(console.foreground_color(value), value + 30)
            #
        #


class EscapeSequenceStart(TestCase):
    """escape_sequence_start() function"""

    def test_no_color(self) -> None:
        """Test with no colors provided"""
        self.assertEqual(console.escape_sequence_start(), "")

    def test_bg_only(self) -> None:
        """Test with background color only"""
        for bg_color in VALID_COLOR_CODES:
            with self.subTest("valid", bg_color=bg_color):
                self.assertEqual(
                    console.escape_sequence_start(bg=bg_color),
                    f"\x1b[{bg_color + 40}m",
                )
            #
        #

    def test_fg_only(self) -> None:
        """Test with foreground color only"""
        for fg_color in VALID_COLOR_CODES:
            with self.subTest("valid", fg_color=fg_color):
                self.assertEqual(
                    console.escape_sequence_start(fg=fg_color),
                    f"\x1b[{fg_color + 30}m",
                )
            #
        #

    def test_all_combinations(self) -> None:
        """Test all valid foreground/background color combinations"""
        for fg_color, bg_color in itertools.product(
            VALID_COLOR_CODES, VALID_COLOR_CODES
        ):
            with self.subTest("valid", fg_color=fg_color, bg_color=bg_color):
                self.assertEqual(
                    console.escape_sequence_start(fg=fg_color, bg=bg_color),
                    f"\x1b[{fg_color + 30};{bg_color + 40}m",
                )
            #
        #


class Colorized(TestCase):
    """colorized() function"""

    def setUp(self) -> None:
        """Define an instance-wide end sequence"""
        self.end_fmt = "\x1b[0m"

    def test_no_color(self) -> None:
        """Test with no colors provided"""
        text = secrets.token_urlsafe()
        self.assertEqual(console.colorized(text), text)

    def test_bg_only(self) -> None:
        """Test with background color only"""
        text = secrets.token_urlsafe()
        for bg_color in VALID_COLOR_CODES:
            with self.subTest("valid", text=text, bg_color=bg_color):
                self.assertEqual(
                    console.colorized(text, bg=bg_color),
                    f"\x1b[{bg_color + 40}m{text}{self.end_fmt}",
                )
            #
        #

    def test_fg_only(self) -> None:
        """Test with foreground color only"""
        text = secrets.token_urlsafe()
        for fg_color in VALID_COLOR_CODES:
            with self.subTest("valid", text=text, fg_color=fg_color):
                self.assertEqual(
                    console.colorized(text, fg=fg_color),
                    f"\x1b[{fg_color + 30}m{text}{self.end_fmt}",
                )
            #
        #

    def test_all_combinations(self) -> None:
        """Test all valid foreground/background color combinations"""
        text = secrets.token_urlsafe()
        for fg_color, bg_color in itertools.product(
            VALID_COLOR_CODES, VALID_COLOR_CODES
        ):
            with self.subTest("valid", text=text, fg_color=fg_color, bg_color=bg_color):
                self.assertEqual(
                    console.colorized(text, fg=fg_color, bg=bg_color),
                    f"\x1b[{fg_color + 30};{bg_color + 40}m{text}{self.end_fmt}",
                )
            #
        #


class Arrow(TestCase):
    """arrow() function"""

    def test_deault_shape(self) -> None:
        """default shabe in various sizes"""
        tail = "\u2014"
        for size, expected_value in (
            (1, "⇥"),
            (2, f"{tail}⇥"),
            (4, f"{tail * 3}⇥"),
            (5, f"{tail * 4}⇥"),
        ):
            with self.subTest(
                "default shape", size=size, expected_value=expected_value
            ):
                self.assertEqual(console.arrow(size=size), expected_value)
            #
        #

    def test_custom_shape(self) -> None:
        """valid values (0–7)"""
        for size, head, tail, expected_value in (
            (3, ">", "=", "==>"),
            (7, "x", "+", "++++++x"),
        ):
            with self.subTest(
                "default shape",
                size=size,
                head=head,
                tail=tail,
                expected_value=expected_value,
            ):
                self.assertEqual(
                    console.arrow(size=size, head=head, tail=tail), expected_value
                )
            #
        #

    def test_invalid(self) -> None:
        """invalid size: 0 and below"""
        for size in range(-3, 1):
            with self.subTest("invalid", size=size):
                self.assertRaisesRegex(
                    ValueError,
                    "^Arrow size must be 1 or greater$",
                    console.arrow,
                    size=size,
                )
            #
        #
