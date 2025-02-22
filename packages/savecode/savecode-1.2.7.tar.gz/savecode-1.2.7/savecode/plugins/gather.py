"""
savecode/plugins/gather.py - Plugin to gather Python files from directories and individual file paths.
"""

import os
from savecode.manager.manager import register_plugin

@register_plugin
class GatherPlugin:
    """
    Plugin that recursively gathers all Python (.py) files from specified directories
    and validates individual Python file paths.
    """
    def run(self, context):
        """
        Execute the gathering process.
        
        Expects the following keys in context:
          - 'roots': list of root directories to search.
          - 'skip': list of directory names to skip.
          - 'files': list of individual Python file paths.
        
        Populates context with:
          - 'all_py_files': a list of gathered Python file paths.
        """
        all_py_files = []
        for root in context.get('roots', []):
            all_py_files.extend(self.gather_py_files(root, context.get('skip', [])))
        # Process individual files
        for file in context.get('files', []):
            if os.path.isfile(file) and file.endswith(".py"):
                # Avoid processing this plugin file (or similar if necessary)
                if os.path.abspath(file) == os.path.abspath(__file__):
                    continue
                all_py_files.append(file)
            else:
                print(f"Warning: {file} is not a valid Python file.")
        context['all_py_files'] = all_py_files

    def gather_py_files(self, root_dir, skip_dirs=None):
        """
        Recursively gather all .py files under the given root_dir, skipping specified directories.
        
        :param root_dir: The directory in which to search.
        :param skip_dirs: Iterable of directory names to skip.
        :return: List of Python file paths.
        """
        # Convert the provided root directory to an absolute path.
        root_dir = os.path.abspath(root_dir)
        skip_dirs = set(skip_dirs or [])
        py_files = []
        current_file = os.path.abspath(__file__)
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove directories that should be skipped so os.walk won’t traverse them.
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fname in filenames:
                if fname.endswith(".py"):
                    file_path = os.path.join(dirpath, fname)
                    # Skip the current plugin file if encountered
                    if os.path.abspath(file_path) == current_file:
                        continue
                    py_files.append(file_path)
        return py_files