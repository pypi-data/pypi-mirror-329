# -*- coding: utf-8 -*-
"""
Test parity with the standard library’s tabnanny module

"""

import contextlib
import io
import itertools
import logging
import sys
import tabnanny
import unittest

from typing import Any, Callable
from unittest.mock import patch

from supertabnanny import frontend

from . import commons


ALL_EXAMPLES = commons.AllSources()

NORMAL = "normal"
VERBOSE = "verbose"
QUIET = "quiet"
OUTPUT_LEVELS = NORMAL, VERBOSE, QUIET
STDOUT = "stdout"
STDERR = "stderr"
STREAM_NAMES: list[str] = [
    f"{prefix}_{suffix}"
    for prefix, suffix in itertools.product(OUTPUT_LEVELS, (STDOUT, STDERR))
]

RETURNCODE = "returncode"
RETURNVALUE = "returnvalue"
STN_ONLY_RETURNCODE = f"stn_only_{RETURNCODE}"

EMPTY = ""
NOTHING = object()

TABNANNY = "tabnanny"
SUPERTABNANNY = "supertabnanny"


@contextlib.contextmanager
def captured_output(stream_name):
    """Return a context manager used by captured_stdout/stdin/stderr
    that temporarily replaces the sys stream *stream_name* with a StringIO."""
    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, io.StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)


def captured_stdout():
    """Capture the output of sys.stdout:

    with captured_stdout() as stdout:
        print("hello")
    self.assertEqual(stdout.getvalue(), "hello\\n")
    """
    return captured_output("stdout")


def captured_stderr():
    """Capture the output of sys.stderr:

    with captured_stderr() as stderr:
        print("hello", file=sys.stderr)
    self.assertEqual(stderr.getvalue(), "hello\\n")
    """
    return captured_output("stderr")


def wrap_func(func: Callable, *args, **kwargs) -> tuple[int | None, Any, str, str]:
    """Execute func(*args, **kwargs) and return
    returncode, returnvalue, stdout and stderr in a tuple
    """
    verbose = int(kwargs.pop("verbose", 0))
    filename_only = int(kwargs.pop("filename_only", 0))
    returncode: int | None = None
    returnvalue: Any = None
    with (
        patch("sys.exit") as mock_exit,
        captured_stdout() as stdout,
        captured_stderr() as stderr,
    ):
        with (
            patch("tabnanny.verbose", verbose),
            patch("tabnanny.filename_only", filename_only),
        ):
            returnvalue = func(*args, **kwargs)
    #
    if mock_exit.called:
        exit_args = mock_exit.call_args.args
        returncode = int(exit_args[0])
    #
    # pylint: disable=no-member ; streams temoporarily replaced by StringIO
    return returncode, returnvalue, stdout.getvalue(), stderr.getvalue()


def get_example(name: str, offending_line_number: int | None = None) -> tuple[str, str]:
    """Get an example, return a tuple containing the full filename as string
    and offending line content (offending_line_number as 1-based index)
    """
    cached_example = ALL_EXAMPLES[name]
    full_filename = str(cached_example.file_path)
    if offending_line_number is None:
        return full_filename, EMPTY
    #
    return full_filename, cached_example.get_line(offending_line_number)


class CheckFunctions(unittest.TestCase):
    """check() functions in tabnanny and supertabnanny"""

    def setUp(self) -> None:
        """Full diff"""
        # pylint: disable=invalid-name ; defined in unittest.TestCase
        self.maxDiff = None

    def _consistency_checked_results(
        self,
        results: dict[str, tuple[Any, Any]],
        backend: str = SUPERTABNANNY,
    ) -> dict[str, Any]:
        """check result data
        (ie. returncode and returnvalue tuples for each output mode)
        for consistency between all output modes
        """
        for first, second in itertools.combinations(OUTPUT_LEVELS, 2):
            with self.subTest(
                "return(code|value) consistency",
                backend=backend,
                first=first,
                second=second,
            ):
                self.assertEqual(results[first], results[second])
            #
        #
        normal_values = results[NORMAL]
        return {RETURNCODE: normal_values[0], RETURNVALUE: normal_values[1]}

    def _complete_checked_results(
        self,
        streams: dict[str, Any],
        results: dict[str, Any],
        backend: str = SUPERTABNANNY,
        **expected_results,
    ) -> dict[str, Any]:
        """check streams and returned data
        and return a dict containing all
        """
        checked_results = self._consistency_checked_results(results, backend=backend)
        for key in RETURNCODE, RETURNVALUE:
            expected: Any = expected_results.get(key, NOTHING)
            if NOTHING is expected:
                continue
            #
            with self.subTest("returned", backend=backend, key=key, expected=expected):
                self.assertEqual(checked_results[key], expected)
            #
        #
        for key in STREAM_NAMES:
            expected = expected_results.get(key, EMPTY)
            if NOTHING is expected:
                continue
            #
            with self.subTest(
                "stream contents", backend=backend, key=key, expected=expected
            ):
                self.assertEqual(streams[key], expected)
            #
        #
        return streams | checked_results

    def _tabnanny_check_file(
        self,
        file_name: str,
        **expected_results,
    ) -> dict[str, Any]:
        """..."""
        # tabnanny never provides a return value,
        # so put a possibly expected one aside and add it again after the check.
        # If a returncode for the supertabnanny only was specified with
        # stn_only_returncode, put that aside as well
        # and add it as expected returncode after the check
        expected_stn_results = {
            RETURNCODE: expected_results.pop(
                STN_ONLY_RETURNCODE, expected_results.get(RETURNCODE, NOTHING)
            ),
            RETURNVALUE: expected_results.pop(RETURNVALUE, NOTHING),
        }
        results: dict[str, tuple[Any, Any]] = {}
        streams: dict[str, Any] = {}
        for output_level in OUTPUT_LEVELS:
            verbose = 1 if output_level == VERBOSE else 0
            filename_only = 1 if output_level == QUIET else 0
            rc, rv, out, err = wrap_func(
                tabnanny.check, file_name, verbose=verbose, filename_only=filename_only
            )
            results.update({output_level: (rc, rv)})
            streams.update(
                {f"{output_level}_{STDOUT}": out, f"{output_level}_{STDERR}": err}
            )
        #
        return (
            self._complete_checked_results(
                streams, results, backend=TABNANNY, **expected_results
            )
            | expected_stn_results
        )

    def _stn_check_file_compatible(
        self,
        file_name: str,
        **expected_results,
    ) -> dict[str, Any]:
        """..."""
        results: dict[str, tuple[Any, Any]] = {}
        streams: dict[str, Any] = {}
        for output_level in OUTPUT_LEVELS:
            loglevel = logging.WARNING
            if output_level == VERBOSE:
                loglevel = logging.INFO
            elif output_level == QUIET:
                loglevel = logging.ERROR
            #
            with patch(
                "supertabnanny.parser.ROOT_LOGGER",
                new=commons.MockLogger(level=loglevel),
            ):
                rc, rv, out, err = wrap_func(
                    frontend.check_compatible,
                    file_name,
                    fail_fast=True,
                )
            #
            results.update({output_level: (rc, rv)})
            streams.update(
                {f"{output_level}_{STDOUT}": out, f"{output_level}_{STDERR}": err}
            )
        #
        return self._complete_checked_results(
            streams, results, backend=SUPERTABNANNY, **expected_results
        )

    def test_error_free_file(self) -> None:
        """test with the error free file
        that triggers an IndentationError exception
        """
        file_name = get_example(commons.ERROR_FREE)[0]
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            verbose_stdout=f"{file_name!r}: Clean bill of health.\n",
            returnvalue=True,
            returncode=None,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_incomplete_expression_file_up_to_311(self) -> None:
        """test with the incomplete-expression file
        that triggers a TokenError exception
        """
        file_name = get_example(commons.INCOMPLETE_EXPRESSION)[0]
        expected_message = (
            f"{file_name!r}: Token Error: ('EOF in multi-line statement', (9, 0))\n"
        )
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stderr=expected_message,
            verbose_stderr=expected_message,
            quiet_stderr=expected_message,
            returnvalue=False,
            stn_only_returncode=1,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_incomplete_expression_file_from_312(self) -> None:
        """test with the incomplete-expression file
        that triggers a TokenError exception
        """
        file_name = get_example(commons.INCOMPLETE_EXPRESSION)[0]
        expected_message = (
            f"{file_name!r}: Token Error:"
            " ('unexpected EOF in multi-line statement', (8, 0))\n"
        )
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stderr=expected_message,
            verbose_stderr=expected_message,
            quiet_stderr=expected_message,
            returnvalue=False,
            returncode=1,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_wrong_indented_file_up_to_311(self) -> None:
        """test with the wrong-indented file
        that triggers an IndentationError exception
        """
        offending_line_number = 3
        file_name = get_example(commons.WRONG_INDENTED)[0]
        err_loc = "tokenize"
        expected_message = (
            f"{file_name!r}: Indentation Error: unindent does not match any"
            f" outer indentation level (<{err_loc}>, line {offending_line_number})\n"
        )
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stderr=expected_message,
            verbose_stderr=expected_message,
            quiet_stderr=expected_message,
            returnvalue=False,
            stn_only_returncode=1,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_wrong_indented_file_from_312(self) -> None:
        """test with the wrong-indented file
        that triggers an IndentationError exception
        """
        offending_line_number = 3
        file_name = get_example(commons.WRONG_INDENTED)[0]
        err_loc = "string"
        expected_message = (
            f"{file_name!r}: Indentation Error: unindent does not match any"
            f" outer indentation level (<{err_loc}>, line {offending_line_number})\n"
        )
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stderr=expected_message,
            verbose_stderr=expected_message,
            quiet_stderr=expected_message,
            returnvalue=False,
            returncode=1,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_inequal_indent_file_up_to_311(self) -> None:
        """test with the not-equal file that triggers a NannyNag exception"""
        offending_line_number = 3
        file_name, offending_line = get_example(
            commons.NOT_EQUAL, offending_line_number=offending_line_number
        )
        verbose_reason = "indent not equal e.g. at tab sizes 1, 2, 3, 4, 5"
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} 3 {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line 3: trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_inequal_indent_file_from_312(self) -> None:
        """test with the not-equal file that triggers a NannyNag exception"""
        offending_line_number = 3
        file_name, offending_line = get_example(
            commons.NOT_EQUAL, offending_line_number=offending_line_number
        )
        verbose_reason = commons.TAB_ERROR_MESSAGE
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} 3 {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line 3: trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_nannynag_errored_file_up_to_311(self) -> None:
        """test with the nannaynag-errorred file that triggers a NannyNag exception"""
        offending_line_number = 3
        file_name, offending_line = get_example(
            commons.NANNYNAG_ERRORED, offending_line_number=offending_line_number
        )
        verbose_reason = "indent not equal e.g. at tab size 1"
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} 3 {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line 3: trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_nannynag_errored_file_from_312(self) -> None:
        """test with the nannaynag-errorred file that triggers a NannyNag exception"""
        offending_line_number = 3
        file_name, offending_line = get_example(
            commons.NANNYNAG_ERRORED, offending_line_number=offending_line_number
        )
        verbose_reason = commons.TAB_ERROR_MESSAGE
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} 3 {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line 3: trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_tab_space_error_file_1_up_to_311(self) -> None:
        """test with the ...  that triggers a NannyNag exception"""
        offending_line_number = 4
        file_name, offending_line = get_example(
            commons.TAB_SPACE_ERRORED_1, offending_line_number=offending_line_number
        )
        verbose_reason = "indent not greater e.g. at tab sizes 1, 2"
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} {offending_line_number} {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line {offending_line_number}:"
                " trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_tab_space_error_file_1_from_312(self) -> None:
        """test with the ... that triggers a NannyNag exception"""
        offending_line_number = 4
        file_name, offending_line = get_example(
            commons.TAB_SPACE_ERRORED_1, offending_line_number=offending_line_number
        )
        verbose_reason = commons.TAB_ERROR_MESSAGE
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} {offending_line_number} {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line {offending_line_number}:"
                " trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] >= (3, 12), "up to 3.11 only")
    def test_tab_space_error_file_2_up_to_311(self) -> None:
        """test with the ...  that triggers a NannyNag exception"""
        offending_line_number = 4
        file_name, offending_line = get_example(
            commons.TAB_SPACE_ERRORED_2, offending_line_number=offending_line_number
        )
        verbose_reason = "indent not equal e.g. at tab sizes 1, 2, 3, 4, 5, 6, 7, 9"
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} {offending_line_number} {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line {offending_line_number}:"
                " trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)

    @unittest.skipIf(sys.version_info[:2] <= (3, 11), "from 3.12 only")
    def test_tab_space_error_file_2_from_312(self) -> None:
        """test with the ... that triggers a NannyNag exception"""
        offending_line_number = 4
        file_name, offending_line = get_example(
            commons.TAB_SPACE_ERRORED_2, offending_line_number=offending_line_number
        )
        verbose_reason = commons.TAB_ERROR_MESSAGE
        tn_results = self._tabnanny_check_file(
            file_name,
            # Expected results:
            normal_stdout=f"{file_name} {offending_line_number} {offending_line!r}\n",
            verbose_stdout=(
                f"{file_name!r}: *** Line {offending_line_number}:"
                " trouble in tab city! ***\n"
                f"offending line: {offending_line!r}\n{verbose_reason}\n"
            ),
            quiet_stdout=f"{file_name}\n",
            returncode=None,
            stn_only_returnvalue=False,
        )
        # Compare tn_results to supertabnanny results
        self._stn_check_file_compatible(file_name, **tn_results)
