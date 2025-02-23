"""
savecode/plugins/gather.py - Plugin to gather Python files from directories and individual file paths with directory validation.
"""

import os
import logging
from typing import Any, Dict, List, Optional
from savecode.manager.manager import register_plugin

logger = logging.getLogger(__name__)

@register_plugin
class GatherPlugin:
    """
    Plugin that recursively gathers all Python (.py) files from specified directories
    and validates individual Python file paths.
    """
    def run(self, context: Dict[str, Any]) -> None:
        """
        Execute the gathering process.
        
        Expects the following keys in context:
          - 'roots': list of root directories to search.
          - 'skip': list of directory names to skip.
          - 'files': list of individual Python file paths.
        
        Populates context with:
          - 'all_py_files': a list of gathered Python file paths.
        """
        all_py_files: List[str] = []
        for root in context.get('roots', []):
            all_py_files.extend(self.gather_py_files(root, context.get('skip', [])))
        # Process individual files
        for file in context.get('files', []):
            if os.path.isfile(file) and file.endswith(".py"):
                all_py_files.append(file)
            else:
                logger.warning("%s is not a valid Python file.", file)
        context['all_py_files'] = all_py_files

    def gather_py_files(self, root_dir: str, skip_dirs: Optional[List[str]] = None) -> List[str]:
        """
        Recursively gather all .py files under the given root_dir, skipping specified directories.
        
        :param root_dir: The directory in which to search.
        :param skip_dirs: Iterable of directory names to skip.
        :return: List of Python file paths. Returns an empty list if the root directory does not exist.
        """
        # Convert the provided root directory to an absolute path.
        root_dir = os.path.abspath(root_dir)
        if not os.path.isdir(root_dir):
            logger.warning("Directory %s does not exist. Skipping.", root_dir)
            return []
        skip_dirs = set(skip_dirs or [])
        py_files: List[str] = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove directories that should be skipped so os.walk won’t traverse them.
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fname in filenames:
                if fname.endswith(".py"):
                    file_path = os.path.join(dirpath, fname)
                    py_files.append(file_path)
        return py_files