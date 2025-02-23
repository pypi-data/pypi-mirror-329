"""
savecode/utils/cli_args.py - Module for parsing command-line arguments.

This module provides a function to parse CLI arguments and return the results.
"""

import argparse
from savecode import __version__

def parse_arguments():
    """
    Parse command-line arguments for the savecode tool.

    Returns:
        tuple: A tuple containing:
            - argparse.Namespace: Parsed arguments.
            - list: List of extra arguments not recognized by the parser.
    """
    parser = argparse.ArgumentParser(
        description="Save the full code from Python files in specified directories and individual files to a single output file."
    )
    parser.add_argument(
        '-r', '--roots',
        nargs='*',
        default=[],
        help="One or more root directories to search for Python files."
    )
    parser.add_argument(
        '-f', '--files',
        nargs='*',
        default=[],
        help="One or more individual Python file paths to include."
    )
    parser.add_argument(
        '-o', '--output',
        default="./temp.txt",
        help="Output file path. Defaults to './temp.txt'."
    )
    parser.add_argument(
        '--skip',
        nargs='*',
        default=['rnn_src'],
        help="Subdirectory names to skip (default: ['rnn_src'])."
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit."
    )
    parser.add_argument(
        '--log-level',
        default='WARNING',
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to WARNING."
    )
    args, extra_args = parser.parse_known_args()
    return args, extra_args