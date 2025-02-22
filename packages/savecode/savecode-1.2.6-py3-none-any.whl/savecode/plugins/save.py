"""
savecode/plugins/save.py - Plugin to save code from Python files into a single output file.
Version: 1.2.1
"""

import os
from savecode.manager.manager import register_plugin

@register_plugin
class SavePlugin:
    """
    Plugin that reads Python files and writes their content to a designated output file.
    """
    def run(self, context):
        """
        Execute the saving process.
        
        Expects the following keys in context:
          - 'all_py_files': list of Python file paths gathered by the GatherPlugin.
          - 'output': the output file path where the combined code should be saved.
        """
        all_py_files = context.get('all_py_files', [])
        output_file = context.get('output', "./temp.txt")
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
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
        except Exception as e:
            print(f"Error writing to output file {output_file}: {e}")