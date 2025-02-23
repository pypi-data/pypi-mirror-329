"""
savecode/__init__.py - Initializes the savecode package with version information.
"""

__version__ = "1.3.0"

# Optionally expose plugin manager functions.
from .plugin_manager import run_plugins, list_plugins