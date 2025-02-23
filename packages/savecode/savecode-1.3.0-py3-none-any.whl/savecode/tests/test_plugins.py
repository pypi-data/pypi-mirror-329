"""
savecode/tests/test_plugins.py - Unit tests for plugins error handling and edge cases.

Tests for GatherPlugin and SavePlugin, including non-existent directories, invalid file paths,
and output error conditions.
"""

import os
import tempfile
import unittest
from savecode.plugin_manager.manager import run_plugins, clear_registry
from savecode.plugins.save import SavePlugin

class TestPlugins(unittest.TestCase):
    def setUp(self):
        # Reset the plugin registry before each test.
        clear_registry()

    def tearDown(self):
        # Clear the registry after each test to ensure isolation.
        clear_registry()

    def test_nonexistent_directory(self):
        """
        Verify that a non-existent directory in roots records an error and yields no gathered files.
        """
        context = {
            'roots': ["/non/existent/directory"],
            'files': [],
            'skip': [],
            'output': "dummy_output.txt",
            'extra_args': [],
            'errors': []
        }
        run_plugins(context)
        self.assertTrue(len(context['errors']) > 0)
        self.assertEqual(context.get('all_py_files', []), [])
    
    def test_invalid_file_in_files(self):
        """
        Verify that an invalid file in the 'files' list is logged as an error and not gathered.
        """
        # Create temporary invalid file (non-.py) and valid .py file, ensuring they are cleaned up.
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            invalid_file = tmp.name
        self.addCleanup(lambda: os.path.exists(invalid_file) and os.remove(invalid_file))
        
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp2:
            valid_file = tmp2.name
        self.addCleanup(lambda: os.path.exists(valid_file) and os.remove(valid_file))
        
        context = {
            'roots': [],
            'files': [invalid_file, valid_file],
            'skip': [],
            'output': "dummy_output.txt",
            'extra_args': [],
            'errors': []
        }
        run_plugins(context)
        # The valid file should be gathered; the invalid file should generate an error.
        self.assertIn(valid_file, context.get('all_py_files', []))
        self.assertNotIn(invalid_file, context.get('all_py_files', []))
        self.assertTrue(any("is not a valid Python file" in error for error in context['errors']))
    
    def test_valid_directory_gathering(self):
        """
        Verify that a directory containing a Python file is correctly processed,
        and non-Python files are ignored without errors.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w", encoding="utf-8") as f:
                f.write("print('Hello')")
            non_py_file = os.path.join(tmpdir, "readme.txt")
            with open(non_py_file, "w", encoding="utf-8") as f:
                f.write("Not python")
            
            context = {
                'roots': [tmpdir],
                'files': [],
                'skip': [],
                'output': os.path.join(tmpdir, "output.txt"),
                'extra_args': [],
                'errors': []
            }
            run_plugins(context)
            self.assertIn(py_file, context.get('all_py_files', []))
            # No error should be recorded for the non-Python file.
            self.assertFalse(any("readme.txt" in error for error in context['errors']))
    
    def test_saveplugin_output_error(self):
        """
        Verify that SavePlugin records an error when the output file cannot be written to.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set output to a directory to simulate a write error.
            context = {
                'roots': [],
                'files': [],
                'skip': [],
                'output': tmpdir,  # Directory used as file path.
                'extra_args': [],
                'errors': []
            }
            plugin = SavePlugin()
            plugin.run(context)
            self.assertTrue(len(context['errors']) > 0)
            self.assertTrue(any("Error writing to output file" in error for error in context['errors']))

if __name__ == '__main__':
    unittest.main()