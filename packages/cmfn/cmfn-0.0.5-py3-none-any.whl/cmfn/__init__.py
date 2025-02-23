# SPDX-FileCopyrightText: 2024-present Hao Wu <haowu@dataset.sh>
#
# SPDX-License-Identifier: MIT
import bz2
import gzip
import os
import json
from typing import Union


def listdir(folder):
    """
    list files under the current folder.

    :param folder: The path of the folder for which the list of files and directories is needed.
    :return: A list of file and directory paths within the specified folder.
    """
    return [os.path.join(folder, x) for x in os.listdir(folder)]


def listdir_recursively(folder):
    """
    list all files under the current folder recursively.

    :param folder: The path of the folder for which the list of files and directories is needed.
    :return: A list of file and directory paths within the specified folder.
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path


def chunk_it(iterator, chunk_size=50):
    """
    Yield successive chunks of a given size from an iterator.

    :param iterator: The input iterator.
    :param chunk_size: The number of items per chunk.
    :yield: A list containing the chunk of items.
    """
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk  # Yield the last chunk if it's not empty


def read_file(fn):
    """
    read content of a file.

    :param fn: The file path of the file to be read.
    :return: The content of the file as a string.
    """
    with smart_open(fn) as fd:
        return fd.read()


def iter_jsonl(fn):
    """
    :param fn: The file path of the JSONL file to be read
    :return: A generator object that yields each valid JSON object from the file
    """
    with smart_open(fn) as fd:
        for line in fd:
            line = line.strip()
            if line:
                yield json.loads(line)


def iter_folder_of_jsonl(folder, postfix='.jsonl'):
    """
    :param folder: the directory containing the JSONL files to iterate over
    :param postfix: the file extension suffix to filter the files in the folder
    :return: a generator that yields each JSON record from the files in the specified folder
    """
    file_list = listdir(folder)
    file_list = [f for f in file_list if f.endswith(postfix)]
    file_list = sorted(file_list)
    for f in file_list:
        for item in iter_jsonl(f):
            yield item


def ensure_folder_exists(p):
    """
    ensure the specified folder exists and return the resolved path using os.path.expanduser.

    :param p: A string representing the path of the folder to ensure existence.
    :return: The input path after expanding and creating the folder if it doesn't already exist.
    """
    p = os.path.expanduser(p)
    os.makedirs(p, exist_ok=True)
    return p


def smart_open(file_path, mode='r'):
    """
    :param file_path: Path to the file to be open.
    :param mode: The mode in which the file should be opened. Default is 'r'.
    :return: The file object for reading or writing.
    """
    if file_path.endswith('.gz'):
        return gzip.open(file_path, mode + 't') if 'b' not in mode else gzip.open(file_path, mode)
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, mode + 't') if 'b' not in mode else bz2.open(file_path, mode)
    else:
        return open(file_path, mode)


def pick_fields(dict_data: dict, fields: list[Union[str | tuple(str, str)]]) -> dict:
    """
    Extracts specified fields from a dictionary, with optional renaming.

    Args:
        dict_data (dict): The input dictionary.
        fields (list[str | tuple(str, str)]):
            List of fields to extract.
            Use a string to keep the original key or a tuple (original_key, new_key) to rename it.

    Returns:
        dict: A new dictionary with only the selected fields, renamed if specified.
    """
    result = {}

    for field in fields:
        if isinstance(field, str):
            if field in dict_data:
                result[field] = dict_data[field]
        elif isinstance(field, tuple) and len(field) == 2:
            original_key, new_key = field
            if original_key in dict_data:
                result[new_key] = dict_data[original_key]
    return result
