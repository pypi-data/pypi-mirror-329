# -*- coding: utf-8 -*-

"""
Command line script
"""

import argparse
import logging
import pathlib
import sys


from . import __version__
from .console import initialize_root_logger
from .frontend import OutputMode, check_dispatch


def parse_arguments(*test_args: str, test_context: bool = False) -> argparse.Namespace:
    """Parse commandline arguments"""
    main_parser = argparse.ArgumentParser(
        prog="supertabnanny",
        description="Detect ambiguous indentation in Python soure files",
    )
    main_parser.set_defaults(loglevel=logging.WARNING, output_mode=OutputMode.NORMAL)
    main_parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="print version and exit",
    )
    lo_parser = main_parser.add_argument_group(
        "logging options",
        "control log output and partially also affect diagnostic output",
    )
    lo_mutex = lo_parser.add_mutually_exclusive_group()
    lo_mutex.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        dest="loglevel",
        help="debug mode (message overkill)",
    )
    lo_mutex.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.INFO,
        dest="loglevel",
        help="verbose mode (print more messages than default)",
    )
    lo_mutex.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=logging.ERROR,
        dest="loglevel",
        help="quiet mode: print error messages only."
        " In compatibility mode, print the file name only for each indentation error.",
    )
    dof_parser = main_parser.add_argument_group(
        "diagnostics format options", "change the diagnostic output format"
    )
    dof_mutex = dof_parser.add_mutually_exclusive_group()
    dof_mutex.add_argument(
        "-c",
        "--compatibility",
        action="store_const",
        const=OutputMode.COMPATIBILITY,
        dest="output_mode",
        help="same format as the original tabnanny module (compatibility mode)",
    )
    dof_mutex.add_argument(
        "-j",
        "--json",
        action="store_const",
        const=OutputMode.JSON,
        dest="output_mode",
        help="one JSON object per file (json mode)",
    )
    dof_mutex.add_argument(
        "-s",
        "--show-lines",
        type=int,
        nargs="?",
        metavar="NUMBER",
        const=3,
        help="show up to %(metavar)s sample lines before and including"
        " the affected line, with different tab sizes to illustrate the problem."
        " If specified without a number, %(const)s lines are shown.",
    )
    main_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="exit immediately if an exception is encountered",
    )
    main_parser.add_argument(
        "files_and_or_directories",
        type=pathlib.Path,
        metavar="FILE_OR_DIRECTORY",
        nargs="+",
        help="the file(s) or director{y|ies} to analyze",
    )
    args: tuple[str, ...] | None = None
    if test_context or test_args:
        args = test_args
    #
    arguments = main_parser.parse_args(args=args)
    initialize_root_logger(arguments.loglevel)
    return arguments


def main(*test_args: str, test_context: bool = False) -> int:
    """..."""
    arguments = parse_arguments(*test_args, test_context=test_context)
    success = True
    for target_path in arguments.files_and_or_directories:
        success &= check_dispatch(
            target_path,
            output_mode=arguments.output_mode,
            show_lines=arguments.show_lines,
            fail_fast=arguments.fail_fast,
        )
    #
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
