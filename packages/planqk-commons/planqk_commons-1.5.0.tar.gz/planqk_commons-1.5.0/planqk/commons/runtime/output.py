import os

from planqk.commons.file import write_str_to_file


def write_to_output_directory(file_name: str, content: str,
                              output_directory: str = os.environ.get("OUTPUT_DIRECTORY", "/var/runtime/output")):
    write_str_to_file(output_directory, file_name, content)
