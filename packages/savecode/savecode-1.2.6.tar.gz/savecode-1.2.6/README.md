Python Code Saver

Version: 1.2.1

Python Code Saver is a command-line utility that gathers Python code from specified directories and individual files, then consolidates them into one output file. This tool is especially useful for creating a single aggregated file from multiple Python scripts, for documentation, analysis, or archiving purposes.


---

Features

Recursive File Gathering: Scans directories recursively for all .py files.

Customizable Directory Skipping: Easily exclude specific subdirectories (default: rnn_src).

File Filtering: Automatically skips the script itself (i.e., cli.py) to avoid self-inclusion.

Flexible Input Options: Combine Python files from multiple root directories and individual file paths.

Output Customization: Specify the output file location (defaults to temp.txt in the script's directory).

Enhanced Output Display: After saving, the tool prints a colored list of all the files that were processed.



---

Installation

1. Clone the Repository:

git clone https://github.com/yourusername/python-code-saver.git
cd python-code-saver


2. Ensure Python 3 is Installed:

Verify that you have Python 3 installed on your system:

python3 --version

If not, download and install it from python.org.




---

Usage

Run the script from the command line using Python. Below are the available options:

python cli.py [OPTIONS]

Options

-r or --roots

Specify one or more root directories to search for Python files.

python cli.py -r ./src ./lib

-f or --files

Provide one or more individual Python file paths to include.

python cli.py -f script1.py script2.py

-o or --output

Define the output file path. If not provided, defaults to temp.txt in the same directory as cli.py.

python cli.py -o combined_output.txt

--skip

List subdirectory names to skip during the search (default: rnn_src).

python cli.py --skip tests docs


Example Command

Combine Python files from two directories, exclude certain subdirectories, and specify an output file:

python cli.py -r ./project/src ./project/utils -o all_code.txt --skip __pycache__ migrations


---

How It Works

1. File Discovery:
The script recursively walks through the provided root directories, collecting paths of all .py files while ignoring directories specified by the --skip option and excluding itself (cli.py).


2. File Aggregation:
Each discovered Python file is opened, and its content is read and written into the output file. A header indicating the file path is inserted before each file's content to provide clear separation.


3. Output Confirmation:
Once the aggregation is complete, the script prints a summary that includes the number of files processed and a list of file paths, with colored formatting for improved readability.




---

Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

1. Fork the repository.


2. Create your feature branch: git checkout -b feature/my-new-feature


3. Commit your changes: git commit -am 'Add some feature'


4. Push to the branch: git push origin feature/my-new-feature


5. Open a pull request.




---

License

Specify your license here. For example, MIT License.


---

Acknowledgments

Inspired by the need for a simple yet effective tool to consolidate Python code for documentation and analysis.

Special thanks to all contributors who helped improve the project.



---

Happy coding!

