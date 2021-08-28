"""
A file api created only for file operations extracted from Generator
"""
from os import path


def create_file(file_path):
    """
    creates a file
    """
    with open(file_path, "x", encoding="utf8"):
        pass


def wipe_file_content(file_path):
    """
    wipes a file content
    """
    with open(file_path, "r+", encoding="utf8") as file:
        file.truncate(0)


def get_file_content(file_path):
    """
    gets a file content
    """
    with open(file_path, "r+", encoding="utf8") as file:
        return "".join(file.readlines())


def set_file_content(file_path, body):
    """
    sets a file content
    """
    wipe_file_content(file_path)
    with open(file_path, "r+", encoding="utf8") as file:
        file.write(body)


def prepend_file_content(file_path, head):
    """
    prepends a string to file
    """
    body = get_file_content(file_path)
    wipe_file_content(file_path)
    set_file_content(file_path, head + body)


def append_file_content(file_path, tail):
    """
    appends a string to file
    """
    body = get_file_content(file_path)
    wipe_file_content(file_path)
    set_file_content(file_path, body + tail)


def wrap_file_content(file_path, head, tail):
    """
    wraps a file content between two strings and sets the result as the content of the file
    """
    prepend_file_content(file_path, head)
    append_file_content(file_path, tail)


def replace_file_chunk(file_path, chunk, new):
    """
    replaces a string in a file
    """
    body = get_file_content(file_path)
    body = body.replace(chunk, new)
    wipe_file_content(file_path)
    set_file_content(file_path, body)


def is_present_in_file(file_path, string):
    """
    check for string if present in a file
    """
    body = get_file_content(file_path)
    return string in body


def wipe_files(file_paths):
    """
    wipe files
    """
    for file in file_paths:
        wipe_file_content(file)


def create_files(file_paths):
    """
    creates files
    """
    for file in file_paths:
        if not path.isfile(file):
            create_file(file)
