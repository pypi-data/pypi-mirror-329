"""
savecode/utils/logger.py - Centralized logging configuration for savecode.
"""

import logging

def configure_logging() -> None:
    """
    Configures the logging settings for the savecode application.
    
    Sets the log level to INFO and specifies a consistent format and date format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
