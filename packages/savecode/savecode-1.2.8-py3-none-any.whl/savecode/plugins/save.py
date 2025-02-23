"""
savecode/plugins/save.py - Plugin to save code from Python files into a single output file with enhanced error handling.
"""

import os
import sys
import logging
from typing import Any, Dict, List
from savecode.manager.manager import register_plugin

logger = logging.getLogger(__name__)

@register_plugin
class SavePlugin:
    """
    Plugin that reads Python files and writes their content to a designated output file with enhanced error handling.
    
    Fatal error:
      - If the output file cannot be written, the process will terminate with a nonzero exit code.
      
    Non-fatal error:
      - If individual files cannot be read, the error is logged and processing continues.
    """
    def run(self, context: Dict[str, Any]) -> None:
        """
        Execute the saving process.
        
        Expects the following keys in context:
          - 'all_py_files': list of Python file paths gathered by the GatherPlugin.
          - 'output': the output file path where the combined code should be saved.
        """
        all_py_files: List[str] = context.get('all_py_files', [])
        output_file: str = context.get('output', "./temp.txt")
        try:
            with open(output_file, 'w', encoding='utf-8') as out:
                # Write a summary header at the beginning of the file.
                summary = "Files saved:\n"
                for file in all_py_files:
                    rel_path = os.path.relpath(file, os.getcwd())
                    summary += f"- {rel_path}\n"
                summary += "\n\n"
                out.write(summary)
                
                # Now write the contents of each file.
                for file in all_py_files:
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            header = f"\nFile: {file}\n\n"
                            out.write(header)
                            out.write(f.read())
                            out.write("\n\n")
                    except (OSError, UnicodeDecodeError) as e:
                        logger.error("Error reading %s: %s", file, e)
        except OSError as e:
            logger.error("Error writing to output file %s: %s", output_file, e)
            sys.exit(1)  # Terminate the program if the output file cannot be written