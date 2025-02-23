"""
setup.py - Packaging configuration for the savecode tool with enhanced long description from README.
"""

from setuptools import setup, find_packages
from savecode import __version__
import os

# Read the contents of README.md for a long description.
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='savecode',
    version=__version__,
    description='Save Python code from directories and files into one output file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Austin Wagner',
    author_email='austinwagner@msn.com',
    url='https://github.com/wagner-austin',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'savecode=savecode.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)