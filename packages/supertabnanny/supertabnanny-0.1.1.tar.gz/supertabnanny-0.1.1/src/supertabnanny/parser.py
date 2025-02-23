# -*- coding: utf-8 -*-

"""
supertabnanny.parser - indent parser
"""

import dataclasses
import json
import logging
import pathlib
import shlex
import tokenize

from typing import TextIO

from .console import ROOT_LOGGER
from .whitespace import WitnessesGroup, LeadingWhitespace


EMPTY = ""
SPACE = " "
ZERO_WHITESPACE = LeadingWhitespace(EMPTY)


class NannyNag(Exception):
    """
    Raised by process_tokens() if detecting an ambiguous indent.
    Captured and handled in check().
    """

    def __init__(self, lineno: int, witnesses: WitnessesGroup, full_line: str) -> None:
        r"""Initialization arguments:

        *   _lineno_: line number where the error occurred
        *   _witnesses_: a whitespace.WitnessesGroup instance
        *   _full\_line_: the full line causing the error
        """
        self.lineno, self.witnesses, self.full_line = (
            lineno,
            witnesses,
            full_line,
        )


@dataclasses.dataclass
class Diagnosis:
    """Diagnosis base class"""

    filename: str
    _: dataclasses.KW_ONLY
    lineno: int = dataclasses.field(init=False, default=-1)
    message: str = dataclasses.field(init=False, default=EMPTY)
    detail: str = dataclasses.field(init=False, default=EMPTY)
    success: bool = dataclasses.field(init=False, default=False)
    tabsizes: list[int] = dataclasses.field(init=False, default_factory=list)

    @property
    def quoted_filename(self) -> str:
        """return shlex.quoted filename"""
        return shlex.quote(self.filename)

    def compatible_output(self) -> str:
        """Return output compatible to the original tabnanny"""
        return f"{self.filename!r}: {self.message}: {self.detail}"

    def json_output(self) -> str:
        """Return output as JSON"""
        return json.dumps(dataclasses.asdict(self))

    def normal_output(self) -> str:
        """Return normal human-readable output"""
        message = (
            f"{self.message}: {self.detail}"
            if self.detail and ROOT_LOGGER.level < logging.WARNING
            else self.message
        )
        return f"{self.quoted_filename}: {message}"


@dataclasses.dataclass
class CleanDiagnosis(Diagnosis):
    """Successful Diagnosis initialized with _filename_ and _message_"""

    message: str
    success: bool = dataclasses.field(init=False, default=True)

    def compatible_output(self) -> str:
        """Return output compatible to the original tabnanny if verbose"""
        if ROOT_LOGGER.level < logging.WARNING:
            return f"{self.filename!r}: {self.message}"
        #
        return EMPTY

    def normal_output(self) -> str:
        """Return normal human-readable output if not set to quiet mode"""
        if ROOT_LOGGER.level < logging.ERROR:
            return super().normal_output()
        #
        return EMPTY


@dataclasses.dataclass
class ErrorDiagnosis(Diagnosis):
    """Error Diagnosis base class"""


@dataclasses.dataclass
class ExceptionDiagnosis(ErrorDiagnosis):
    """Exception Diagnosis initialized with _filename_, and _exc_"""

    exc: dataclasses.InitVar[Exception] = dataclasses.InitVar(Exception)

    def __post_init__(self, exc: Exception):
        """Determine message by exception Type"""
        match exc:
            case OSError():
                self.message = "I/O Error"
            case tokenize.TokenError():
                self.message = "Token Error"
            case IndentationError():
                self.message = "Indentation Error"
            case SyntaxError():
                self.message = "Syntax Error"
            case _:
                self.message = f"{exc.__class__.__name__}"
            #
        #
        self.lineno = int(getattr(exc, "lineno", -1))
        self.detail = str(exc)


@dataclasses.dataclass
class NagDiagnosis(ErrorDiagnosis):
    """Nag Diagnosis class initialized with _filename_ and _nag_"""

    nag: dataclasses.InitVar[NannyNag] = dataclasses.InitVar(NannyNag)
    full_line: str = dataclasses.field(init=False)

    def __post_init__(self, nag: NannyNag):
        r"""Derive _message_, _detail_, _lineno_, and _full\_line_
        from  _nag_
        """
        self.message = f"Line {nag.lineno}"
        self.detail = str(nag.witnesses)
        self.lineno = nag.lineno
        self.full_line = nag.full_line
        self.tabsizes = nag.witnesses.tabsizes

    def compatible_output(self) -> str:
        """Return output compatible to the original tabnanny"""
        if ROOT_LOGGER.level < logging.WARNING:
            return (
                f"{self.filename!r}: *** {self.message}: trouble in tab city! ***\n"
                f"offending line: {self.full_line!r}\n{self.detail}"
            )
        #
        filename = self.filename
        if SPACE in filename:
            filename = f'"{self.filename}"'
        #
        if ROOT_LOGGER.level > logging.WARNING:
            return filename
        #
        return f"{filename} {self.lineno} {self.full_line!r}"


class IndentParser:
    """Parser for ..."""

    ignored_items = tokenize.COMMENT, tokenize.NL

    def __init__(self, compatibility_mode: bool = False) -> None:
        """Initialization argument:
        compatibility_mode: operate in full tabnanny compatibility mode
        """
        self.__check_for_equal_indent: bool = False
        self.__active: bool = False
        self.__indents: list[LeadingWhitespace] = []
        self.__compatibility_mode = compatibility_mode

    @property
    def is_stopped(self) -> bool:
        """Signal whether the partser is in stopped state"""
        return not self.__active

    @property
    def check_is_required(self) -> bool:
        """Reveal the check flag"""
        return self.__check_for_equal_indent

    @property
    def previous_indent(self) -> LeadingWhitespace:
        """Return the last indent from the indents stack"""
        return self.__indents[-1]

    def reset(self) -> None:
        """Reset internal state and signal readiness"""
        self.avoid_check()
        self.__indents.clear()
        self.push_indent(ZERO_WHITESPACE)
        self.__active = True

    def stop(self) -> None:
        """Stop the parser: clear indents cache and set not-ready"""
        self.__indents.clear()
        self.__active = False

    def avoid_check(self) -> None:
        """Unset the check flag"""
        self.__check_for_equal_indent = False

    def require_check(self) -> None:
        """Set the check flag"""
        self.__check_for_equal_indent = True

    def push_indent(self, leading_whitespace: LeadingWhitespace) -> None:
        """Push leading_whitespace to the indents stack"""
        logging.debug("pushing %r", leading_whitespace.raw)
        logging.debug("frequencies: %r", leading_whitespace.normalization.frequencies)
        self.__indents.append(leading_whitespace)

    def pop_indent(self) -> None:
        """remove the last entry from the indents stack"""
        last_raw_entry = self.__indents.pop().raw
        logging.debug("popped %r", last_raw_entry)

    def feed(self, current_token: tokenize.TokenInfo) -> None:
        """Feed a token to the parser"""
        if self.is_stopped:
            raise ValueError("Parser is stopped and cannot be fed any tokens")
        #
        previous_lw = self.previous_indent
        if current_token.type == tokenize.NEWLINE:
            self.require_check()
        elif current_token.type == tokenize.INDENT:
            self.avoid_check()
            current_lw = LeadingWhitespace(
                current_token.string, compatibility_mode=self.__compatibility_mode
            )
            if previous_lw >= current_lw:
                raise NannyNag(
                    current_token.start[0],
                    previous_lw.greater_or_equal_witnesses(current_lw),
                    current_token.line,
                )
            #
            self.push_indent(current_lw)
        elif current_token.type == tokenize.DEDENT:
            self.require_check()
            self.pop_indent()
        elif self.check_is_required and current_token.type not in self.ignored_items:
            self.avoid_check()
            current_lw = LeadingWhitespace(
                current_token.line, compatibility_mode=self.__compatibility_mode
            )
            if previous_lw != current_lw:
                raise NannyNag(
                    current_token.start[0],
                    previous_lw.not_equal_witnesses(current_lw),
                    current_token.line,
                )
            #
        #

    def parse_io(self, text_io: TextIO) -> bool:
        """Parse TextIO"""
        self.reset()
        try:
            for token_info in tokenize.generate_tokens(text_io.readline):
                self.feed(token_info)
            #
        except TabError as error:
            raise NannyNag(
                error.lineno or -1, WitnessesGroup(error.msg), error.text or "unknown"
            ) from error
        except (tokenize.TokenError, IndentationError, SyntaxError, NannyNag) as error:
            raise error from error
        finally:
            self.stop()
        #
        return True

    def parse_file(
        self,
        file_spec: str | pathlib.Path,
    ) -> Diagnosis:
        """Parse a single file and return a Diagnosis subclass"""
        if isinstance(file_spec, pathlib.Path):
            file_path = file_spec
        else:
            file_path = pathlib.Path(file_spec)
        #
        file_name = str(file_path)
        try:
            with tokenize.open(file_spec) as source_file:
                self.parse_io(source_file)
            #
        except (OSError, tokenize.TokenError, IndentationError, SyntaxError) as exc:
            return ExceptionDiagnosis(file_name, exc=exc)
        except NannyNag as nag:
            return NagDiagnosis(file_name, nag=nag)
        #
        return CleanDiagnosis(file_name, message="Clean bill of health.")
