# -*- coding: utf-8 -*-

"""
Unit test the supertabnanny.parser module

"""

import io
import logging
import re
import sys
import tokenize

from unittest import TestCase, skipIf
from unittest.mock import patch

from supertabnanny import parser
from supertabnanny.whitespace import Witness, WitnessesGroup

from . import commons

ALL_EXAMPLES = commons.AllSources()

KW_ATTRIBUTE = "attribute"
KW_OUTPUT = "output"
KW_REDUCED_OUTPUT = "reduced output"

PARSER_ROOT_LOGGER = "supertabnanny.parser.ROOT_LOGGER"

# Python major and minor version as a 2-int tuple
PYTHON_MMVERSION = tuple(sys.version_info[:2])


def get_nannynag_re_pattern(
    lineno: int = 1,
    error_message: str = commons.EMPTY,
    tabsizes: str = commons.EMPTY,
    offending_line: str = commons.EMPTY,
):
    """Return a regular expression pattern for mathing a NannyNag exception"""
    return re.escape(
        f"""({lineno}, WitnessesGroup({error_message!r}) with tabsizes"""
        f""" [{tabsizes}], {offending_line!r})"""
    )


class NannyNag(TestCase):
    """NannyNag exception"""

    def test_attributes(self) -> None:
        """Initialization and attributes"""
        lineno, wg, full_line = 7, WitnessesGroup("dummy"), "\t   1 tab and 3 spaces"
        nag = parser.NannyNag(lineno, wg, full_line)
        with self.subTest(KW_ATTRIBUTE, name="lineno"):
            self.assertEqual(nag.lineno, lineno)
        #
        with self.subTest(KW_ATTRIBUTE, name="witnesses group"):
            self.assertEqual(repr(nag.witnesses), repr(wg))
        #
        with self.subTest(KW_ATTRIBUTE, name="full_line"):
            self.assertEqual(nag.full_line, full_line)
        #


class Diagnosis(TestCase):
    """Diagnosis base class"""

    def test_init_attrs(self) -> None:
        """Initialization and attributes"""
        filename = "test/example.py"
        diagnosis = parser.Diagnosis(filename)
        with self.subTest(KW_ATTRIBUTE, filename=filename):
            self.assertEqual(diagnosis.filename, filename)
        #
        with self.subTest(KW_ATTRIBUTE, lineno=-1):
            self.assertEqual(diagnosis.lineno, -1)
        #
        with self.subTest(KW_ATTRIBUTE, message=commons.EMPTY):
            self.assertEqual(diagnosis.message, commons.EMPTY)
        #
        with self.subTest(KW_ATTRIBUTE, detail=commons.EMPTY):
            self.assertEqual(diagnosis.detail, commons.EMPTY)
        #
        with self.subTest(KW_ATTRIBUTE, success=False):
            self.assertFalse(diagnosis.success)
        #
        with self.subTest(KW_ATTRIBUTE, tabsizes=[]):
            self.assertEqual(diagnosis.tabsizes, [])
        #

    def test_qf_property(self) -> None:
        """.quoted_filename property"""
        filename = "test/example with whitespace.py"
        expected_qf = "'test/example with whitespace.py'"
        diagnosis = parser.Diagnosis(filename)
        with self.subTest(KW_ATTRIBUTE, expected_qf=expected_qf):
            self.assertEqual(diagnosis.quoted_filename, expected_qf)
        #

    def test_compatible_output(self) -> None:
        """.compatible_output() function"""
        for filename, expected_result in (
            ("test/example.py", "'test/example.py': : "),
            (
                "test/example with whitespace.py",
                "'test/example with whitespace.py': : ",
            ),
        ):
            with self.subTest(KW_OUTPUT, expected_result=expected_result):
                diagnosis = parser.Diagnosis(filename)
                self.assertEqual(diagnosis.compatible_output(), expected_result)
            #
        #

    def test_json_output(self) -> None:
        """.json_output() function"""
        for filename, expected_result in (
            (
                "test/example.py",
                '{"filename": "test/example.py", "lineno": -1, "message": "",'
                ' "detail": "", "success": false, "tabsizes": []}',
            ),
            (
                "test/example with whitespace.py",
                '{"filename": "test/example with whitespace.py", "lineno": -1,'
                ' "message": "", "detail": "", "success": false, "tabsizes": []}',
            ),
        ):
            with self.subTest(KW_OUTPUT, expected_result=expected_result):
                diagnosis = parser.Diagnosis(filename)
                self.assertEqual(diagnosis.json_output(), expected_result)
            #
        #

    def test_normal_output(self) -> None:
        """.normal_output() function"""
        for filename, expected_result in (
            ("test/example.py", "test/example.py: "),
            (
                "test/example with whitespace.py",
                "'test/example with whitespace.py': ",
            ),
        ):
            with self.subTest(KW_OUTPUT, expected_result=expected_result):
                diagnosis = parser.Diagnosis(filename)
                self.assertEqual(diagnosis.normal_output(), expected_result)
            #
        #


class CleanDiagnosis(TestCase):
    """CleanDiagnosis class"""

    def test_init_attrs(self) -> None:
        """Initialization and attributes"""
        filename = "test/example.py"
        message = "good"
        diagnosis = parser.CleanDiagnosis(filename, message)
        with self.subTest(KW_ATTRIBUTE, filename=filename):
            self.assertEqual(diagnosis.filename, filename)
        #
        with self.subTest(KW_ATTRIBUTE, lineno=-1):
            self.assertEqual(diagnosis.lineno, -1)
        #
        with self.subTest(KW_ATTRIBUTE, message=message):
            self.assertEqual(diagnosis.message, message)
        #
        with self.subTest(KW_ATTRIBUTE, detail=commons.EMPTY):
            self.assertEqual(diagnosis.detail, commons.EMPTY)
        #
        with self.subTest(KW_ATTRIBUTE, success=True):
            self.assertTrue(diagnosis.success)
        #
        with self.subTest(KW_ATTRIBUTE, tabsizes=[]):
            self.assertEqual(diagnosis.tabsizes, [])
        #

    def test_compatible_output(self) -> None:
        """.compatible_output() function"""
        for filename, message, expected_result in (
            ("test/example.py", "good", "'test/example.py': good"),
            (
                "test/example with whitespace.py",
                "clean",
                "'test/example with whitespace.py': clean",
            ),
        ):
            diagnosis = parser.CleanDiagnosis(filename, message)
            with patch(PARSER_ROOT_LOGGER, new=commons.MockLogger(level=logging.INFO)):
                with self.subTest(
                    KW_OUTPUT,
                    filename=filename,
                    message=message,
                    expected_result=expected_result,
                ):
                    self.assertEqual(diagnosis.compatible_output(), expected_result)
                #
            #
            with self.subTest(KW_REDUCED_OUTPUT, filename=filename, message=message):
                self.assertEqual(diagnosis.compatible_output(), commons.EMPTY)
            #
        #

    def test_normal_output(self) -> None:
        """.normal_output() function"""
        for filename, message, expected_result in (
            ("test/example.py", "good", "test/example.py: good"),
            (
                "test/example with whitespace.py",
                "clean",
                "'test/example with whitespace.py': clean",
            ),
        ):
            diagnosis = parser.CleanDiagnosis(filename, message)
            with patch(PARSER_ROOT_LOGGER, new=commons.MockLogger(level=logging.ERROR)):
                with self.subTest(
                    KW_REDUCED_OUTPUT, filename=filename, message=message
                ):
                    self.assertEqual(diagnosis.normal_output(), commons.EMPTY)
                #
            #
            with self.subTest(
                KW_OUTPUT,
                filename=filename,
                message=message,
                expected_result=expected_result,
            ):
                self.assertEqual(diagnosis.normal_output(), expected_result)
            #
        #


class ExceptionDiagnosis(TestCase):
    """ExceptionDiagnosis class"""

    def test_init_attrs(self) -> None:
        """Initialization and attributes"""
        filename = "test/example.py"
        syntax_error = SyntaxError("invalid", (filename, 7, 8, "pnirt", 7, 13))
        for exception, expected_lineno, expected_message, expected_detail in (
            (OSError("access forbidden"), -1, "I/O Error", "access forbidden"),
            (syntax_error, 7, "Syntax Error", str(syntax_error)),
            (ValueError("whatever"), -1, "ValueError", "whatever"),
        ):
            exc = str(exception)
            diagnosis = parser.ExceptionDiagnosis(filename, exc=exception)
            with self.subTest(KW_ATTRIBUTE, exc=exc, filename=filename):
                self.assertEqual(diagnosis.filename, filename)
            #
            with self.subTest(KW_ATTRIBUTE, exc=exc, expected_lineno=expected_lineno):
                self.assertEqual(diagnosis.lineno, expected_lineno)
            #
            with self.subTest(KW_ATTRIBUTE, exc=exc, expected_message=expected_message):
                self.assertEqual(diagnosis.message, expected_message)
            #
            with self.subTest(KW_ATTRIBUTE, exc=exc, detail=expected_detail):
                self.assertEqual(diagnosis.detail, expected_detail)
            #
            with self.subTest(KW_ATTRIBUTE, exc=exc, success=False):
                self.assertFalse(diagnosis.success)
            #
            with self.subTest(KW_ATTRIBUTE, exc=exc, tabsizes=[]):
                self.assertEqual(diagnosis.tabsizes, [])
            #
        #


class NagDiagnosis(TestCase):
    """NagDiagnosis class"""

    def test_init_attrs(self) -> None:
        """Initialization and attributes"""
        filename = "test/example.py"
        lineno = 67
        full_line = "           \t     \t  example content"
        witnesses_group = WitnessesGroup(prefix="multiple witnesses ")
        witnesses_group.add(Witness(4, 5, 6))
        witnesses_group.add(Witness(7, 8, 9))
        witnesses_group.add(Witness(20, 5, 5))
        diagnosis = parser.NagDiagnosis(
            filename, nag=parser.NannyNag(lineno, witnesses_group, full_line)
        )
        with self.subTest(KW_ATTRIBUTE, filename=filename):
            self.assertEqual(diagnosis.filename, filename)
        #
        with self.subTest(KW_ATTRIBUTE, lineno=lineno):
            self.assertEqual(diagnosis.lineno, lineno)
        #
        with self.subTest(KW_ATTRIBUTE, message="Line 67"):
            self.assertEqual(diagnosis.message, "Line 67")
        #
        with self.subTest(KW_ATTRIBUTE, detail=str(witnesses_group)):
            self.assertEqual(diagnosis.detail, str(witnesses_group))
        #
        with self.subTest(KW_ATTRIBUTE, success=False):
            self.assertFalse(diagnosis.success)
        #
        with self.subTest(KW_ATTRIBUTE, full_line=full_line):
            self.assertEqual(diagnosis.full_line, full_line)
        #
        with self.subTest(KW_ATTRIBUTE, tabsizes=[4, 7, 20]):
            self.assertEqual(diagnosis.tabsizes, [4, 7, 20])
        #

    def test_compatible_output(self) -> None:
        """.compatible_output() method"""
        filename = "test/example with spaces.py"
        lineno = 67
        full_line = "           \t     \t  example content"
        witnesses_group = WitnessesGroup(prefix="multiple witnesses ")
        witnesses_group.add(Witness(4, 5, 6))
        witnesses_group.add(Witness(7, 8, 9))
        witnesses_group.add(Witness(20, 5, 5))
        diagnosis = parser.NagDiagnosis(
            filename, nag=parser.NannyNag(lineno, witnesses_group, full_line)
        )
        with patch(PARSER_ROOT_LOGGER, new=commons.MockLogger(level=logging.ERROR)):
            with self.subTest(
                KW_REDUCED_OUTPUT,
                filename=filename,
            ):
                self.assertEqual(diagnosis.compatible_output(), f'"{filename}"')
            #
        #
        with patch(PARSER_ROOT_LOGGER, new=commons.MockLogger(level=logging.INFO)):
            with self.subTest(
                "full output",
                filename=filename,
            ):
                self.assertEqual(
                    diagnosis.compatible_output(),
                    f"{filename!r}: *** Line {lineno}: trouble in tab city! ***\n"
                    f"offending line: {full_line!r}\n"
                    "multiple witnesses at tab sizes 4, 7, 20",
                )
            #
        #
        with self.subTest("default output", filename=filename):
            self.assertEqual(
                diagnosis.compatible_output(), f'"{filename}" {lineno} {full_line!r}'
            )
        #


class IndentParserParseIO(TestCase):
    """IndentParser class, parse_io() method, tests modified from
    <https://github.com/python/cpython/blob/c501261/Lib/test/test_tabnanny.py>
    """

    def setUp(self) -> None:
        """Provide a parser"""
        self.i_parser = parser.IndentParser()
        # pylint: disable=invalid-name ; defined in unittest.TestCase
        self.maxDiff = None

    def _parse_literal(self, source_code: str) -> bool:
        r"""parse the _source\_code_ literal and return the result"""
        return self.i_parser.parse_io(io.StringIO(source_code))

    def _parse_source_codes(self, key: str) -> bool:
        r"""parse **SOURCE\_CODES\[_key_]** and return the result"""
        return self._parse_literal(ALL_EXAMPLES[key].source)

    def test_correct_source(self) -> None:
        """Python source code without any errors"""
        self.assertTrue(self._parse_source_codes(commons.ERROR_FREE))

    def test_wrong_indented(self) -> None:
        """Python source code eligible for raising an IndentationError"""
        self.assertRaisesRegex(
            IndentationError,
            "^unindent does not match any outer indentation level",
            self._parse_source_codes,
            commons.WRONG_INDENTED,
        )

    @skipIf(PYTHON_MMVERSION >= (3, 12), "up to 3.11 only")
    def test_tokenize_tokenerror_upto_311(self):
        """Python (up to 3.11) source code eligible for raising
        a tokenize.TokenError
        """
        expected_regex = re.escape("('EOF in multi-line statement', (9, 0))")
        self.assertRaisesRegex(
            tokenize.TokenError,
            f"^{expected_regex}$",
            self._parse_source_codes,
            commons.INCOMPLETE_EXPRESSION,
        )

    @skipIf(PYTHON_MMVERSION <= (3, 11), "from 3.12 only")
    def test_tokenize_tokenerror_from_312(self):
        """Python (from 3.12) source code eligible for raising
        a tokenize.TokenError
        """
        expected_regex = re.escape("('unexpected EOF in multi-line statement', (8, 0))")
        self.assertRaisesRegex(
            tokenize.TokenError,
            f"^{expected_regex}$",
            self._parse_source_codes,
            commons.INCOMPLETE_EXPRESSION,
        )

    @skipIf(PYTHON_MMVERSION >= (3, 12), "up to 3.11 only")
    def test_when_nannynag_error_upto_311(self):
        """Python (up to 3.11) source code eligible for raising
        a parser.NannyNag exception
        """
        expected_regex = get_nannynag_re_pattern(
            lineno=3,
            error_message="expanded size different ",
            tabsizes="1",
            offending_line='\tprint("world")\n',
        )
        self.assertRaisesRegex(
            parser.NannyNag,
            f"^{expected_regex}$",
            self._parse_source_codes,
            commons.NANNYNAG_ERRORED,
        )

    @skipIf(PYTHON_MMVERSION <= (3, 11), "from 3.12 only")
    def test_when_nannynag_error_from_312(self):
        """Python (from 3.12) source code eligible for raising
        a parser.NannyNag exception
        """
        expected_regex = get_nannynag_re_pattern(
            lineno=3,
            error_message=commons.TAB_ERROR_MESSAGE,
            tabsizes=commons.EMPTY,
            offending_line='\tprint("world")',
        )
        self.assertRaisesRegex(
            parser.NannyNag,
            f"^{expected_regex}$",
            self._parse_source_codes,
            commons.NANNYNAG_ERRORED,
        )

    @skipIf(PYTHON_MMVERSION >= (3, 12), "up to 3.11 only")
    def test_with_errored_codes_samples_upto311(self):
        """Python source code with whitespace related sampled problems
        with Python 3.11 or lower:

        *   "tab_space_errored_1": matched by the block under

                elif current_token.type == tokenize.INDENT

            in the .feed() method.
        *   "tab space_errored_2": matched block under

                elif self.check_is_required
                and current_token.type not in self.ignored_item

            in the .feed() method`
        """
        for source_key, error_message, tabsizes, offending_line in (
            (
                commons.TAB_SPACE_ERRORED_1,
                "expanded size greater or equal ",
                "1, 2",
                '\t\tprint("If called")\n',
            ),
            (
                commons.TAB_SPACE_ERRORED_2,
                "expanded size different ",
                "1, 2, 3, 4, 5, 6, 7, 9",
                '\t        print("If called")\n',
            ),
        ):
            with self.subTest(
                "NannyNag raised", source_key=source_key, offending_line=offending_line
            ):
                expected_regex = get_nannynag_re_pattern(
                    lineno=4,
                    error_message=error_message,
                    tabsizes=tabsizes,
                    offending_line=offending_line,
                )
                self.assertRaisesRegex(
                    parser.NannyNag,
                    f"^{expected_regex}$",
                    self._parse_source_codes,
                    source_key,
                )
            #
        #

    @skipIf(PYTHON_MMVERSION <= (3, 11), "from 3.12 only")
    def test_with_errored_codes_samples_from312(self):
        """Python source code with whitespace related sampled problems
        with Python 3.12 and up:

        *   "tab_space_errored_1": matched by the block under

                elif current_token.type == tokenize.INDENT

            in the .feed() method.
        *   "tab space_errored_2": matched block under

                elif self.check_is_required
                and current_token.type not in self.ignored_item

            in the .feed() method`
        """
        for source_key, offending_line in (
            (
                commons.TAB_SPACE_ERRORED_1,
                '\t\tprint("If called")',
            ),
            (
                commons.TAB_SPACE_ERRORED_2,
                '\t        print("If called")',
            ),
        ):
            with self.subTest(
                "NannyNag raised", source_key=source_key, offending_line=offending_line
            ):
                expected_regex = get_nannynag_re_pattern(
                    lineno=4,
                    error_message=commons.TAB_ERROR_MESSAGE,
                    tabsizes=commons.EMPTY,
                    offending_line=offending_line,
                )
                self.assertRaisesRegex(
                    parser.NannyNag,
                    f"^{expected_regex}$",
                    self._parse_source_codes,
                    source_key,
                )
            #
        #


class IndentParserParseFile(TestCase):
    """IndentParser class, parse_file() method, tests modified from
    <https://github.com/python/cpython/blob/c501261/Lib/test/test_tabnanny.py>
    """

    def setUp(self) -> None:
        """Provide a parser"""
        # self.i_parser = parser.IndentParser()
        self.compatibility_parser = parser.IndentParser(compatibility_mode=True)
        # pylint: disable=invalid-name ; defined in unittest.TestCase
        self.maxDiff = None

    def test_correct_source(self) -> None:
        """Python source code file without any errors"""
        diagnosis = self.compatibility_parser.parse_file(
            ALL_EXAMPLES[commons.ERROR_FREE].file_path
        )
        #
        with self.subTest("type"):
            self.assertIsInstance(diagnosis, parser.CleanDiagnosis)
        #
        with self.subTest("message"):
            self.assertEqual(diagnosis.message, "Clean bill of health.")
        #

    def test_wrong_indented_file(self) -> None:
        """Python source code file with indentation errors"""
        source_path = ALL_EXAMPLES[commons.WRONG_INDENTED].file_path
        diagnosis = self.compatibility_parser.parse_file(source_path)
        #
        with self.subTest("type"):
            self.assertIsInstance(diagnosis, parser.ExceptionDiagnosis)
        #
        with self.subTest("filename"):
            self.assertEqual(diagnosis.filename, str(source_path))
        #
        with self.subTest("message"):
            self.assertEqual(diagnosis.message, "Indentation Error")
        #
        error_source = "tokenize" if PYTHON_MMVERSION <= (3, 11) else "string"
        with self.subTest("detail"):
            self.assertEqual(
                diagnosis.detail,
                "unindent does not match any outer indentation level"
                f" (<{error_source}>, line 3)",
            )
        #

    @patch(PARSER_ROOT_LOGGER, new=commons.MockLogger(level=logging.INFO))
    def test_nannynag_error_verbose(self):
        """A python source code file eligible for raising parser.NannyNag.
        in verbose mode
        """
        example = ALL_EXAMPLES[commons.NANNYNAG_ERRORED]
        line_number = 3
        offending_line = example.get_line(line_number)
        diagnosis = self.compatibility_parser.parse_file(example.file_path)
        #
        reason = (
            "indent not equal e.g. at tab size 1"
            if PYTHON_MMVERSION <= (3, 11)
            else commons.TAB_ERROR_MESSAGE
        )
        self.assertEqual(
            diagnosis.compatible_output(),
            "\n".join(
                (
                    f"{str(example.file_path)!r}: *** Line {line_number}:"
                    " trouble in tab city! ***",
                    f"offending line: {offending_line!r}",
                    reason,
                )
            ),
        )

    def test_nannynag_error_normal(self):
        """A python source code file eligible for raising parser.NannyNag.
        in non-verbose mode
        """
        example = ALL_EXAMPLES[commons.NANNYNAG_ERRORED]
        line_number = 3
        offending_line = example.get_line(line_number)
        diagnosis = self.compatibility_parser.parse_file(example.file_path)
        self.assertEqual(
            diagnosis.compatible_output(),
            f"{example.file_path} {line_number} {offending_line!r}",
        )
