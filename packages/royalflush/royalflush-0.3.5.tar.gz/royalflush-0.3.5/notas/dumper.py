"""
> python .\notas\dumper.py ..\..\Python\nebula\nebula 2300
Done! Check '..\..\Python\nebula\nebula_1.txt' (and subsequent files) for the output.
"""

import os
import sys


def dump_py_files(package_dir, max_lines=None):
    """
    Given a Python package directory, traverse it and dump all .py files
    (ignoring virtual environment folders and common ignore directories)
    into one or more output files.

    If max_lines is None, all output goes to a single <package_dir>.txt file.
    If max_lines is an integer, output is split into multiple files, each
    having at most max_lines lines, e.g. <package_dir>_1.txt, <package_dir>_2.txt, ...
    """
    # Define folder names to ignore during traversal
    ignored_dirs = {
        "venv",
        ".venv",
        "env",
        ".env",
        "__pycache__",
        ".git",
        "build",
        "dist",
    }

    # Resolve package_dir to its absolute path
    package_dir_abs = os.path.abspath(package_dir)

    # Determine the parent directory to build a relative path
    parent_dir = os.path.dirname(package_dir_abs)

    # If max_lines is None, we just write everything into <package_dir>.txt
    if max_lines is None:
        output_filename = f"{package_dir}.txt"
        with open(output_filename, "w", encoding="utf-8") as outfile:
            for root, dirs, files in os.walk(package_dir_abs):
                # Exclude ignored directories in-place
                dirs[:] = [d for d in dirs if d not in ignored_dirs]

                for filename in files:
                    if filename.endswith(".py"):
                        full_path = os.path.join(root, filename)
                        relative_path = os.path.relpath(full_path, parent_dir)
                        # Read file content
                        with open(full_path, "r", encoding="utf-8") as pyfile:
                            content = pyfile.read()
                        # Write path + content, then a blank line
                        outfile.write(f"{relative_path}:\n{content}\n\n")

        print(f"Done! Check '{output_filename}' for the output.")

    else:
        # max_lines is given, so we need to chunk the output
        # We'll maintain a current line count and a current file index
        file_index = 1
        current_line_count = 0

        # Helper function to get the next output filename
        def get_output_filename(index):
            return f"{package_dir}_{index}.txt"

        # Open the first file
        current_output = open(get_output_filename(file_index), "w", encoding="utf-8")

        for root, dirs, files in os.walk(package_dir_abs):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in files:
                if filename.endswith(".py"):
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, parent_dir)

                    # Read file content
                    with open(full_path, "r", encoding="utf-8") as pyfile:
                        content = pyfile.read()

                    # Number of lines this file will occupy in output (path line + file content + blank line)
                    lines_for_this_file = 1 + len(content.splitlines()) + 1

                    # If adding this file surpasses the limit, move to the next file
                    if current_line_count + lines_for_this_file > max_lines:
                        current_output.close()
                        file_index += 1
                        current_output = open(get_output_filename(file_index), "w", encoding="utf-8")
                        current_line_count = 0  # reset line count for the new file

                    # Write path line, content, and a blank line
                    current_output.write(f"{relative_path}:\n{content}\n\n")

                    # Update current line count
                    current_line_count += lines_for_this_file

        # Close the last file
        current_output.close()

        print(f"Done! Check '{package_dir}_1.txt' (and subsequent files) for the output.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dump_py_files.py <package_folder> [<max_lines>]")
        sys.exit(1)

    package_folder = sys.argv[1]

    if not os.path.isdir(package_folder):
        print(f"Error: '{package_folder}' is not a valid directory.")
        sys.exit(1)

    input_max_lines = None
    if len(sys.argv) > 2:
        try:
            input_max_lines = int(sys.argv[2])
        except ValueError:
            print(f"Warning: '{sys.argv[2]}' is not a valid integer. Ignoring.")
            input_max_lines = None

    dump_py_files(package_folder, input_max_lines)
