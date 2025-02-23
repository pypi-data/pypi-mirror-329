"""
savecode/utils/logger.py - Centralized logging configuration for savecode.
This module sets up the logging level and format for the application.
"""

import logging

def configure_logging() -> None:
    """
    Configures the logging settings for the savecode application.
    
    Sets the log level to WARNING to suppress info messages by default and
    specifies a consistent format and date format.
    """
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )