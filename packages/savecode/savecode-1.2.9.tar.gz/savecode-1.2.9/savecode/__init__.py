"""
savecode/__init__.py - Initialize the savecode package with centralized version management.
"""

__version__ = "1.2.9"

# Optionally expose plugin manager functions
from .plugin_manager import run_plugins, list_plugins