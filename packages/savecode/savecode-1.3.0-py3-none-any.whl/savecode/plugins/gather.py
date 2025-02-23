"""
plugins/gather.py - Plugin to gather Python files from directories and individual file paths.
"""

import os
import logging
from typing import Any, Dict, List, Optional
from savecode.plugin_manager.manager import register_plugin
from savecode.plugin_manager.decorators import handle_plugin_errors
from savecode.utils.path_utils import normalize_path
from savecode.utils.error_handler import log_and_record_error

logger = logging.getLogger('savecode.plugins.gather')

@register_plugin
class GatherPlugin:
    """Plugin for gathering Python files from directories and individual file paths."""
    
    @handle_plugin_errors
    def run(self, context: Dict[str, Any]) -> None:
        """Execute the gathering process.

        Expects in context:
          - 'roots': List of directories to search.
          - 'skip': List of directory names to skip.
          - 'files': List of individual Python file paths.

        Populates context with:
          - 'all_py_files': Deduplicated list of gathered Python file paths.

        Args:
            context (Dict[str, Any]): Shared context containing parameters and data.

        Returns:
            None
        """
        all_py_files: List[str] = []
        for root in context.get('roots', []):
            normalized_root = normalize_path(root)
            if not os.path.isdir(normalized_root):
                error_msg = f"Directory {normalized_root} does not exist. Skipping."
                log_and_record_error(error_msg, context, logger)
            else:
                # Pass the already normalized path to gather_py_files.
                all_py_files.extend(self.gather_py_files(normalized_root, context.get('skip', []), context))
        for file in context.get('files', []):
            normalized_file = normalize_path(file)
            if os.path.isfile(normalized_file) and normalized_file.endswith(".py"):
                all_py_files.append(normalized_file)
            else:
                warning_msg = f"{file} is not a valid Python file."
                log_and_record_error(warning_msg, context, logger)
        # Deduplicate while preserving order.
        deduped_files = list(dict.fromkeys(all_py_files))
        context['all_py_files'] = deduped_files
        logger.info("Gathered %d unique Python files.", len(deduped_files))

    def gather_py_files(self, root_dir: str, skip_dirs: Optional[List[str]] = None, context: Dict[str, Any] = None) -> List[str]:
        """Recursively gather all Python (.py) files from a normalized directory, skipping specified directories.

        Args:
            root_dir (str): Normalized absolute directory path to search for Python files.
            skip_dirs (Optional[List[str]]): List of directory names to skip. Defaults to None.
            context (Optional[Dict[str, Any]]): Optional context for error aggregation. Defaults to None.

        Returns:
            List[str]: List of gathered Python file paths.
        """
        # Assume root_dir is already normalized.
        skip_dirs = set(skip_dirs or [])
        py_files: List[str] = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip specified directories.
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fname in filenames:
                if fname.endswith(".py"):
                    file_path = os.path.join(dirpath, fname)
                    py_files.append(file_path)
        return py_files