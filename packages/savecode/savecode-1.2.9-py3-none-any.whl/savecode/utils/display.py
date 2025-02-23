"""
savecode/utils/display.py - Module for CLI display logic to print the summary output.
"""

from typing import Any, Dict, List
from savecode.utils.colors import GREEN, BLUE, CYAN, RESET
from savecode.utils.path_utils import relative_path

def display_summary(context: Dict[str, Any]) -> None:
    """
    Displays a summary of the saved Python files.
    
    Expects the context to have:
      - 'all_py_files': list of Python file paths.
      - 'output': the output file path.
    
    The function prints the number of files saved and a relative path for each file.
    """
    all_py_files: List[str] = context.get('all_py_files', [])
    output = context.get('output', "./temp.txt")
    
    print(f"\n{CYAN}Saved code from {len(all_py_files)} files to {output}{RESET}")
    print(f"\n{GREEN}Files saved:{RESET}")
    for file in all_py_files:
        # Convert absolute file path to a relative path using the utility function.
        rel_path = relative_path(file)
        print(f"{BLUE}- {rel_path}{RESET}")
    print("\n")