"""
savecode/utils/path_utils.py - Utility functions for path manipulation.
"""

import os

def relative_path(path: str) -> str:
    """
    Returns the relative path of the given absolute path relative to the current working directory.

    :param path: The absolute file path.
    :return: The file path relative to the current working directory.
    """
    return os.path.relpath(path, os.getcwd())
