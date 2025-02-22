"""
savecode/utils/output_manager.py - Handles configuration of the output file path.
Version: 1.2.1
"""

import os

def configure_output_path(output_arg):
    """
    Configures the output file path.

    If the output_arg is the default ("./temp.txt"), this function returns the absolute path
    to "temp.txt" in the current working directory. Otherwise, it returns the output_arg as provided.

    :param output_arg: The output file path argument.
    :return: The configured output file path.
    """
    if output_arg == "./temp.txt":
        return os.path.join(os.getcwd(), "temp.txt")
    else:
        return output_arg