# -*- coding: utf-8 -*-

"""
frontend checks
"""

import logging
import pathlib
import sys
import textwrap

from enum import Enum
from typing import Iterator

from .console import LF, BLACK, WHITE, GREEN, RED, ROOT_LOGGER, colorized, bright
from .parser import IndentParser, Diagnosis, CleanDiagnosis, ExceptionDiagnosis
from .whitespace import LineFormatter


class OutputMode(Enum):
    """Output modes"""

    JSON = "JSON"
    COMPATIBILITY = "tabnanny-compatibility"
    NORMAL = "normal"


def frequent_tabsizes_iter() -> Iterator[int]:
    """Iterate over the most frequent tabsizes
    (own guess, not backed by any statistical data):
    4, 8, 2, 1, 6, 3, 5, 7, 9, 10, 11, …, 99
    """
    yield from (4, 8, 2, 1, 6, 3, 5, 7)
    yield from range(9, 100)


def iter_with_lineno(
    source_lines: list[str],
    lineno: int,
    max_lines: int = 3,
) -> Iterator[tuple[int, str]]:
    """Get a part of a source file"""
    start_line = 0
    if max_lines > 0:
        start_line = lineno - max_lines
        start_line = max(start_line, 0)
    #
    for index, line in enumerate(source_lines[start_line:lineno], start=start_line + 1):
        yield index, line
    #


# pylint: disable=too-many-locals ; refactoring candidate
def collect_samples(
    file_path: pathlib.Path,
    diagnosis: Diagnosis,
    max_lines: int = 3,
    samples_limit: int = 3,
) -> Iterator[tuple[int, str]]:
    """Collect samples from a file, each being max_lines long
    before and including line #lineno,
    and replace whitespace by symbols
    """
    if diagnosis.lineno < 1:
        return
    #
    source_lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    sample_formatters: list[tuple[int, LineFormatter]] = [
        (lineno, LineFormatter(line))
        for (lineno, line) in iter_with_lineno(
            source_lines, diagnosis.lineno, max_lines=max_lines
        )
    ]
    total_tabs = sum(formatter.ntabs for (_, formatter) in sample_formatters)
    if not total_tabs:
        samples_limit = 1
        logging.info(
            "No tabs in the sample, so it will not expand differently"
            " at varying tab sizes."
        )
    #
    frequent_tab_sizes = list(frequent_tabsizes_iter())
    remaining_tabsizes = set(diagnosis.tabsizes or frequent_tab_sizes)
    found_samples = 0
    for current_ts in frequent_tab_sizes:
        if found_samples >= samples_limit or not remaining_tabsizes:
            break
        #
        try:
            remaining_tabsizes.remove(current_ts)
        except KeyError:
            continue
        #
        found_samples += 1
        collected: list[str] = []
        for line_number, formatter in sample_formatters:
            lineno_prefix = colorized(f"{line_number:4d}: ", fg=bright(BLACK), bg=WHITE)
            collected.append(f"  {lineno_prefix}{formatter.format(tabsize=current_ts)}")
        #
        yield current_ts, LF.join(collected)
    #


def compatible_check_impl(
    file_path: str | pathlib.Path,
    fail_fast: bool = False,
) -> bool:
    """Check a file and produce the exacttly same output
    as the standard library tabnanny module
    """
    if isinstance(file_path, pathlib.Path):
        path_obj = file_path
    else:
        path_obj = pathlib.Path(file_path)
    #
    indent_parser = IndentParser(compatibility_mode=True)
    diagnosis = indent_parser.parse_file(path_obj)
    output = diagnosis.compatible_output()
    if output:
        if isinstance(diagnosis, ExceptionDiagnosis):
            sys.stderr.write(f"{output}\n")
        else:
            print(output)
        #
    #
    if fail_fast and isinstance(diagnosis, ExceptionDiagnosis):
        sys.exit(1)
    #
    return isinstance(diagnosis, CleanDiagnosis)


def compatible_walk_impl(
    file_or_directory: str | pathlib.Path,
) -> Iterator[pathlib.Path]:
    """Yield file names from the path, descending into directories only
    if they are not symbolic links
    """
    if isinstance(file_or_directory, pathlib.Path):
        path_obj = file_or_directory
    else:
        path_obj = pathlib.Path(file_or_directory)
    #
    if path_obj.is_file() and path_obj.suffix == ".py":
        yield path_obj
    elif path_obj.is_dir() and not path_obj.is_symlink():
        if ROOT_LOGGER.level < logging.WARNING:
            print(f"{str(path_obj)}: listing directory")
        #
        for sub_path in path_obj.glob("*"):
            if sub_path.is_dir() and not sub_path.is_symlink() or sub_path.is_file():
                yield from compatible_walk_impl(sub_path)
            #
        #
    #


def check_compatible(
    file_or_directory: str | pathlib.Path,
    fail_fast: bool = False,
) -> bool:
    """Check a file or directory and produce the exactly same output
    as the standard library tabnanny module – wrapper setting the
    verbose and filename_only flags and calling the walk and
    alling the tybnanny compatible walk and check implementations.
    """
    success = True
    for file_path in compatible_walk_impl(file_or_directory):
        success &= compatible_check_impl(
            file_path,
            fail_fast=fail_fast,
        )
    #
    return success


def display_samples(
    file_path: pathlib.Path,
    diagnosis: Diagnosis,
    max_lines: int = 0,
    line_width: int = 72,
) -> None:
    """Print samples of problematic indentation at varying tabsizes"""
    tabsizes_samples = list(collect_samples(file_path, diagnosis, max_lines=max_lines))
    if not tabsizes_samples:
        return
    #
    nsamples = len(tabsizes_samples)
    nlines = len(tabsizes_samples[0][1].splitlines())
    separator = "\u2500" * line_width
    print(f"\u256d{separator}\u256e")
    print(f"  {file_path}:")
    lines_description = (
        f"a {nlines} lines sample" if nlines > 1 else "the affected line"
    )
    if nsamples > 1:
        print(
            textwrap.fill(
                f"Showing {lines_description} expanded at {nsamples} different"
                " tabsizes to illustrate the problem",
                width=line_width,
                initial_indent="  ",
                subsequent_indent="  ",
            )
        )
    else:
        print(f"  Showing {lines_description} to illustrate the problem")
    for tabsize, sample in tabsizes_samples:
        print(f"  {f' expanded at tab size {tabsize} ':⸱^{line_width - 2}}")
        print(sample)
    #
    print(f"\u2570{separator}\u256f")
    # print(separator)


def check_newstyle(
    file_path: pathlib.Path,
    output_mode: OutputMode,
    show_lines: int | None = None,
    fail_fast: bool = False,
) -> bool:
    """check_newstyle(path, output_mode, show_lines)

    If file_or_dir is a directory and not a symbolic link, then recursively
    descend the directory tree named by file_or_dir, checking all .py files
    along the way. If file_or_dir is an ordinary Python source file, it is
    checked for whitespace related problems. The diagnostic messages are
    written to standard output using the print statement.
    """
    diagnostic_messages = ""
    diagnosis = IndentParser().parse_file(file_path)
    match output_mode:
        case OutputMode.JSON:
            print(diagnosis.json_output())
        case OutputMode.NORMAL:
            diagnostic_messages = diagnosis.normal_output()
            if diagnostic_messages:
                if diagnosis.success:
                    status_indicator = colorized(" \u2713 ", bg=GREEN)
                else:
                    status_indicator = colorized(" \u2717 ", bg=RED)
                #
                print(f"{status_indicator} {diagnostic_messages}")
            #
        #
    #
    if fail_fast and isinstance(diagnosis, ExceptionDiagnosis):
        logging.critical("Exiting on first error as requested")
        sys.exit(1)
    #
    if isinstance(show_lines, int):
        display_samples(file_path, diagnosis, max_lines=show_lines)
    #
    return diagnosis.success


def walk(file_or_directory: pathlib.Path) -> Iterator[pathlib.Path]:
    """Yield python file paths"""
    if file_or_directory.is_file() and file_or_directory.suffix.lower() == ".py":
        yield file_or_directory
    elif (
        file_or_directory.is_dir()
        and not file_or_directory.is_symlink()
        and not file_or_directory.name.startswith(".")
    ):
        logging.debug("descending into directory %s", file_or_directory)
        for subpath in file_or_directory.glob("*"):
            yield from walk(subpath)
        #
        logging.debug("back in directory %s", file_or_directory.parent)
    elif file_or_directory.exists():
        reason = " (symbolic link directory)" if file_or_directory.is_symlink() else ""
        logging.debug(
            "%s: ignored, not suitable for checking%s", file_or_directory, reason
        )
    else:
        logging.warning("%s: does not exist", file_or_directory)
    #


def check_dispatch(
    file_or_directory: pathlib.Path,
    output_mode: OutputMode,
    show_lines: int | None = None,
    fail_fast: bool = False,
) -> bool:
    """Dispatch checks to the compatible or newstyle functions"""
    if output_mode == OutputMode.COMPATIBILITY:
        return check_compatible(file_or_directory, fail_fast=fail_fast)
    #
    success = True
    for file_path in walk(file_or_directory):
        success &= check_newstyle(
            file_path,
            output_mode,
            show_lines=show_lines,
            fail_fast=fail_fast,
        )
    #
    return success
