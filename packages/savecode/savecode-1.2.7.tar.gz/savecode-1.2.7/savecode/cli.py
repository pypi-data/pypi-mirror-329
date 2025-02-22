"""
cli.py - Entry point for savecode system. Aggregates plugins to gather and save Python code.
"""

import argparse
import os
from savecode import __version__
# Import the plugins package to ensure all plugins are registered.
import savecode.plugins
from savecode.manager.manager import run_plugins
from savecode.utils.output_manager import configure_output_path

def main():
    """
    Main entry point for the savecode CLI.
    Parses command-line arguments, builds a shared context, and runs the plugins.
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
    # Add version flag.
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit."
    )
    # Allow additional unknown arguments for future expansion.
    args, extra_args = parser.parse_known_args()
    
    # Build a shared context for all plugins.
    context = {
        'roots': args.roots,
        'files': args.files,
        'skip': args.skip,
        'output': configure_output_path(args.output),
        'extra_args': extra_args
    }
    
    run_plugins(context)
    
    # After plugins run, display a summary.
    all_py_files = context.get('all_py_files', [])
    green = "\033[1;32m"
    blue = "\033[1;34m"
    cyan = "\033[1;36m"
    reset = "\033[0m"
    print(f"\n{cyan}Saved code from {len(all_py_files)} files to {context['output']}{reset}")
    print(f"\n{green}Files saved:{reset}")
    for f in all_py_files:
        # Convert each absolute file path to a relative path from the current working directory.
        rel_path = os.path.relpath(f, os.getcwd())
        print(f"{blue}- {rel_path}{reset}")
    print("\n")
    
if __name__ == "__main__":
    main()
   
   # RELEASE PROCESS:
# ----------------
# 1. Update the version in setup.py and savecode/__init__.py.
#
# 2. Commit your changes.
#
# 3. Create a release tag with a 'v' prefix (e.g., "v*.*.*"):
#      git tag v*.*.*
#
# 4. Push your tags (if your remote isn't named 'origin', use its name):
#      git push origin --tags
#
# 5. The GitHub Actions workflow (in .github/workflows/publish.yml) is triggered by
#    tag pushes (tags matching "v*") to automatically build and publish your package to PyPI.
#
# Note: Regular commits don't trigger the release workflow—only pushing a new tag does.

# -----------

# Clear Dist: rm -rf dist/

# Clear Build: rm -rf build/

# Build: python -m build

# Add Tag: git tag v*.*.*

#Git Push Origin

# Push: git push origin --tags

# -----------