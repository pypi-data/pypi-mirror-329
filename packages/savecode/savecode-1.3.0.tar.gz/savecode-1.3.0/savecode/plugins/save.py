"""
savecode/plugins/save.py - Plugin to save code from Python files with streamlined file iteration.
This module defines a plugin that reads Python files and writes their contents along with a summary
to a designated output file, aggregating any errors encountered during file operations.
"""

import os
import logging
from typing import Any, Dict, List
from savecode.plugin_manager.manager import register_plugin
from savecode.plugin_manager.decorators import handle_plugin_errors
from savecode.utils.path_utils import relative_path
from savecode.utils.error_handler import log_and_record_error

logger = logging.getLogger('savecode.plugins.save')

@register_plugin
class SavePlugin:
    """Plugin that saves the content of Python files to a single output file."""
    
    @handle_plugin_errors
    def run(self, context: Dict[str, Any]) -> None:
        """Execute the saving process in a single pass.

        Expects in context:
          - 'all_py_files': List of Python file paths.
          - 'output': Output file path.

        Aggregates errors in context['errors'].

        Args:
            context (Dict[str, Any]): Shared context containing file lists, output path, etc.

        Returns:
            None
        """
        all_py_files: List[str] = context.get('all_py_files', [])
        output_file: str = context.get('output', "./temp.txt")
        try:
            summary_lines = ["Files saved:"]
            file_contents = []
            for file in all_py_files:
                rel_path = relative_path(file)
                summary_lines.append(f"- {rel_path}")
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    header = f"\nFile: {rel_path}\n\n"
                    file_contents.append(header + content + "\n\n")
                except Exception as e:
                    error_msg = f"Error reading {file}: {e}"
                    log_and_record_error(error_msg, context, logger, exc_info=True)
            
            # Build the complete output by combining the summary and file contents.
            summary_text = "\n".join(summary_lines) + "\n\n"
            complete_output = summary_text + "".join(file_contents)
            
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(complete_output)
        except Exception as e:
            error_msg = f"Error writing to output file {output_file}: {e}"
            log_and_record_error(error_msg, context, logger, exc_info=True)