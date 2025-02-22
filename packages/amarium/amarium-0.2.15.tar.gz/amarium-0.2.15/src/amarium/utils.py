"""Collection of utitly functions for file I/O operations. The purpose is
especially for scientific computing, thus numpy is involved in some functions.
Copyright (C) 2022 Julian M. Kleber This program comes with ABSOLUTELY NO
WARRANTY.".

author: Julian M. Kleber
"""

import os
import json
import time
import logging
import tarfile
import base64
from typing import Tuple, List, Dict, Any, Optional, Union, Type

import shutil

import numpy as np
import numpy.typing as npt

from .checks import check_make_file_name_suffix, check_make_dir

LOGGER = logging.getLogger(__name__)


def remove_all_files_from_dir(dir: str) -> None:
    """Removes all files in the specified directory without deleting the directory

    Args:
        dir (str): Path to the directory that shall be cleared
    """
    files = os.listdir(dir)

    for file in files:
        file_name = make_full_filename(prefix=dir, file_name=file)
        if os.path.isdir(file_name):
            continue
        else:
            delete_file(file_name)


def read_file(file_name: str, encoding="ISO-8859-1") -> str:
    with open(file_name, "r", encoding=encoding) as f:
        content = f.read()
    return content


def write_file(content: str, file_name: str, encoding: str = "ISO-8859-1"):
    file_name = prepare_file_name_saving(file_name=file_name)
    with open(file_name, "w", encoding=encoding) as txt_file:
        txt_file.write(content)
    logging.info("Wrote file to " + file_name)


def prepare_file_name_saving(
    file_name: str,
    prefix: Optional[str | Type[None]] = None,
    suffix: Optional[str | Type[None]] = None,
) -> str:
    """The prepare_file_name_saving function takes a prefix and file name as
    input. It checks to see if the directory exists, and makes it if not. Then
    it returns the full path of the file.

    :param prefix: str: Used to specify the folder where the file will
        be saved.
    :param file_name: str: Used to specify the name of the file to be
        saved.
    :return: The full path of the file name. :doc-author: Julian M.
        Kleber
    """
    if suffix == "" or suffix is None:
        file_name, suffix = os.path.splitext(file_name)

    if prefix == "" or prefix is None:
        prefix, file_name = os.path.split(file_name)

    check_make_dir(prefix)
    file_name = make_full_filename(prefix, file_name)
    file_name = check_make_file_name_suffix(file_name, suffix)
    return file_name


def insert_string_in_file_name(file_name: str, insertion: str, suffix: str) -> str:
    """The insert_string_in_file_name function takes a file_name and inserts a
    string into the name. The insertion is placed before the extension of the
    file_name, or if there is no extension, it will be placed at the end of the
    file_name with an suffix specified by you.

    :param file_name: str: Used to Specify the file name that you want
        to insert a string into.
    :param insertion: str: Used to Specify the string that will be
        inserted into the file name.
    :param suffix: str: Used to Specify the file suffix.
    :return: A string.  :doc-author: Julian M. Kleber
    """

    root, ext = os.path.splitext(file_name)

    if suffix is None and not ext:
        raise ValueError(
            "You must either specify an suffix in the file_name or pass an suffix through the\
            suffix argument. For example the file_name could be 'foo.bar' or you pass\
            file_name'foo' with suffix = '.bar'"
        )
    if suffix is not None:
        if not suffix.startswith("."):
            suffix = "." + suffix

    if not ext:
        file_name = file_name + "_" + insertion + suffix
    else:
        file_name = root + "_" + insertion + ext
    return file_name


def make_full_filename(prefix: str, file_name: str) -> str:
    """
    The make_full_filename function takes a prefix and a file_name as input.
    If the prefix is None, then the file_name is returned unchanged.
    Otherwise, if the file name starts with 'http://' or 'ftp://', then it's assumed to be an URL
    and the full_filename will contain both the prefix and file_name; otherwise,
    only return full_filename = file_name.

    :param prefix: Used to Add a prefix to the file_name.
    :param file_name: Used to Create a full file_name for the file to be downloaded.
    :return: The full file_name with the prefix added to the beginning of the file_name.

    :doc-author: Trelent
    """
    if prefix is None:
        return file_name
    if prefix.endswith("/") and file_name.startswith("/"):
        file_name = prefix + file_name[1:]
    elif prefix.endswith("/") or file_name.startswith("/"):
        file_name = prefix + file_name
    else:
        file_name = prefix + "/" + file_name
    return file_name


def load_json_from_file(file_name: str) -> Dict[Any, Any]:
    """The load_json_from_file function takes a file name as input and returns
    the contents of that file in JSON format.

    :param file_name: str: Used to Specify the file name of the json
        file to be loaded.
    :return: A dictionary of the data in the file. :doc-author: Julian
        M. Kleber
    """

    with open(file_name, "r", encoding="utf-8") as json_file:
        data = dict(json.load(json_file))
    return data


def save_json_to_file(dictionary: Dict[Any, Any], file_name: str) -> None:
    """The save_json function saves a dictionary to a json file.

    :param dictionary: Used to store the data that will be saved.
    :param file_name: str=None: Used to specify a file name.
    :return: A string with the name of the file that was just created.
        :doc-author: Julian M. Kleber
    """

    def convert(np_data: Union[npt.NDArray[Any], Type[np.generic]]) -> Any:
        """The convert function takes in a numpy object and returns the value
        of that object. If the input is an array, it will return a list of
        values. If it is not an array, it will return just the value.

        :param o: Union[Type(np.ndarray): Used to Specify the type of
            object that will be passed to the function. :param
            Type(np.generic)]: Used to Specify the type of object that
            is being passed into the function.
        :return: The value of the input object.  :doc-author: Trelent
        """

        val = None
        if isinstance(np_data, np.generic):
            val = np_data.item()
        elif isinstance(np_data, np.ndarray):
            val = list(np_data)
        return val

    with open(file_name, "w", encoding="utf-8") as out_file:
        json.dump(dictionary, out_file, default=convert)
        logging.info("Saved json %s", file_name)


def make_date_file_name(prefix: str = "", file_name: str = "", suffix: str = "") -> str:
    """The make_date_file_name function creates a file name with the date and
    time stamp in the format YYYY-MM-DD_HH:MM:SS.out.  The prefix, file_name,
    and suffix are optional arguments that can be used to specify what string
    should precede the date stamp in the file_name (prefix), what string should
    be appended after the date stamp (suffix), or both (file_name).   If no
    arguments are provided, then make_date_file_name will use default values
    for all three arguments.

    :param prefix: str="": Used to ddd a prefix to the file name.
    :param file_name: str="": Used to specify the name of the file.
    :param suffix: str=".out": Used to specify the file extension.
    :return: A string that is the combination of prefix, file_name and
        suffix. :doc-author: Julian M. Kleber
    """
    time_str = time.strftime("%Y%m%d-%H%M%S" + prefix + file_name + suffix)
    return time_str


def delete_all_files_in_dir(dir_name: str) -> None:
    """The function deletes all files within the specified directory.

    :param dir_name: str: Used to specify the directory
    :param file_name: str="": Used to specify the name of the file.
    :param suffix: str=".out": Used to specify the file extension.
    :return: None :suffix: :doc-author: Julian M. Kleber
    """

    for file in os.listdir(dir_name):
        file_name = make_full_filename(dir_name, file)
        delete_file(file_name)


def delete_empty_dir(dir_name: str) -> None:
    """The delete_dir function deletes an empty directory.

    :param file_name: str: Used to Specify the name of the file that
        will be deleted.
    :return: None.  :doc-author: Julian M. Kleber
    """

    if dir_name is None:
        raise RuntimeError("You must specify a directory")
        exit()
    elif not os.path.isdir(dir_name):
        raise RuntimeError(
            "Directory does not exist. You must specify a valid directory."
        )
        exit()
    elif len(os.listdir(dir_name)) != 0:
        raise RuntimeError("You must specify an empty directory.")
        exit()

    os.rmdir(dir_name)
    logging.info("Deleted directory %s", dir_name)


def delete_file(file_name: str) -> None:
    """The delete_file function deletes a file from the local directory.

    :param file_name: str: Used to Specify the name of the file that
        will be deleted.
    :return: None.  :doc-author: Julian M. Kleber
    """

    try:
        os.remove(file_name)
        logging.info("Deleted file %s", file_name)
    except Exception as exc:
        raise exc


def search_subdirs(dir_name: str) -> Tuple[List[str], List[str]]:
    """The search_subdirs function takes a directory name as input and returns
    a tuple of two lists. The first list contains all the files in the
    directory, including those in subdirectories. The second list contains all
    the subdirectories.

    :param dir_name: str: Used to Specify the directory that we want to
        search.
    :return: A tuple of two lists.  :doc-author: Julian M. Kleber
    """
    if not dir_name.endswith("/"):
        dir_name += "/"

    result_files = []
    sub_dirs = []
    for path, subdirs, files in os.walk(dir_name):
        for name in files:
            result_files.append(os.path.join(path, name))
        for subdir in subdirs:
            sub_dirs.append(os.path.join(path, subdir))

    return (result_files, sub_dirs)


def write_tar(target_dir: str, file_name: str) -> None:
    """The write_tar function takes a target directory and an output name as
    arguments. It then creates a tar file with the given output name, and adds
    all files in the target directory to it.

    :param target_dir: str: Used to Specify the directory that you want
        to compress.
    :param out_name: str: Used to Specify the name of the tar file that
        will be created.
    :return: None.  :doc-author: Julian M. Kleber
    """

    with tarfile.open(file_name, "w") as tar:
        for root, directory, files in os.walk(target_dir):
            for file in files:
                fullpath = os.path.join(root, file)
                tar.add(fullpath, arcname=file)
            del directory
        tar.close()


def copy_file(file_name: str, destination: str, overwrite: bool = False) -> None:
    """Function to copy a file with implemented checks and overwriting
    functionality.

    :param: file_name: str: specify the file to be copied
    :param: destination: str: specify the destination file name (not
        directory)
    :param: overwrite: bool: Defaults to false. :author: Julian M.
        Kleber
    """

    destination_dir = os.path.dirname(destination)
    base_file_name_original = os.path.basename(file_name)
    destination_is_dir = os.path.isdir(destination)

    if destination_is_dir:
        raise RuntimeError(
            "Destination is a directory. Please specify a file name via the destination parameter."
        )
    elif file_name != destination:
        shutil.copy2(file_name, destination)
    elif file_name == destination and overwrite == True:
        content = read_file = file_name
        destination_to_delete = file_name
        delete_file(destination_to_delete)
        write_file(content, destination)
    else:
        raise RuntimeError("The file already exists. Please choose overwrite = True.")


def copy_dir(old_dir: str, new_dir: str, overwrite=True) -> None:
    """The copy_dir function takes two arguments, old_dir and new_dir. It
    copies all files from the old directory to the new directory. If either of
    these directories do not end with a "/", it will be added.

    :param old_dir: str: Used to Specify the directory that you want to
        copy from.
    :param new_dir: str: Used to Specify the new directory that you want
        to copy your files into.
    :return: None.  :doc-author: Julian M. Kleber
    """

    check_make_dir(new_dir)
    if not old_dir.endswith("/"):
        old_dir += "/"
    if not new_dir.endswith("/"):
        new_dir += "/"
    if overwrite and os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    shutil.copytree(old_dir, new_dir)


def convert_str_to_bool(bool_str: str) -> None:
    """The convert_str_to_bool function takes a string and converts it to a
    boolean. The function is used in the main() function to convert the
    override value from a string to a boolean.

    :param bool_str: str: Used to Specify the type of data that will be
        passed into the function.
    :return: None.  :doc-author: Julian M. Kleber
    """

    if bool_str == "True":
        bool_str = True
    if bool_str == "False":
        bool_str = False
    return bool_str


def attach_slash(raw_string: str) -> str:
    """The attach_slash function takes a string as input and returns the same
    string with a slash appended to it. If the input already ends in a slash,
    then no change is made.

    :param raw_string: str: Used to Specify the type of data that is
        being passed into the function.
    :return: A string with a trailing slash. :doc-author: Julian M.
        Kleber
    """

    if not raw_string.endswith("/"):
        raw_string += "/"
    return raw_string


def combine_dirs(dir_1: str, dir_2: str) -> str:
    """The combine dirs function chains two dir names

    :param dir_1: str: Param for first dir
    :param dir_2: str: Param for second dir

    :return: A string with a trailing slash. :doc-author: Julian M.
        Kleber
    """

    if dir_1.endswith("/"):
        dir_fin = dir_1 + dir_2
    else:
        dir_fin = dir_1 + "/" + dir_2

    return dir_fin


def b64encode_string(input: str) -> str:
    """enocdes string to b64. Useful for APIs

    Args:
        input (str): string to be encoded

    Returns:
        str: encoded input string
    """
    data = base64.b64encode(input.encode())
    return data


def write_list_to_file(list, file_name) -> str:

    prepare_file_name_saving(file_name=file_name)
    with open(file_name, "w") as file:
        for element in list_to_write:
            file.writelines(element)
