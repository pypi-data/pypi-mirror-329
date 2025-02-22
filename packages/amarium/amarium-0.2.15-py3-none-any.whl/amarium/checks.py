"""Module to provide sanity checks for user inputs and other routine quality
checks during execution.

:author: Julian M. Kleber
"""

import os
from collections.abc import Iterable
from typing import List, Any
import shutil


import logging

LOGGER = logging.getLogger(__name__)


def check_header_and_data(data: List[Any], header: List[Any]) -> None:
    """The check_header_and_data function checks that the length of the data
    and header lists are equal. If they are not, it raises a RuntimeError with
    an appropriate message.

    :param data: List[Any]: Used to Pass in the data to be written.
    :param header: List[Any]: Used to Ensure that the header and data
        have the same number of fields.
    :return: A boolean value.  :doc-author: Julian M. Kleber
    """

    if len(data) == len(header):
        pass
    else:
        raise RuntimeError(
            "Input data and input header do not have the "
            "same number of fields. "
            "Please ensure an appropriate data structure."
        )


def check_make_file_name_suffix(file_name: str, suffix: str = "") -> str:
    """The check_name_plot function checks that the file_name ends with .png.
    If it does not, then check_name_plot appends .png to the end of the
    file_name.

    :param file_name: Used to Specify the name of the file to be
        plotted.
    :return: The file_name with the correct file extension. :doc-
        author: Trelent
    """
    name = file_name
    ext = os.path.splitext(file_name)[1]
    if not ext:
        if not suffix.startswith("."):
            suffix = "." + suffix
        name += suffix
    return name


def check_make_subdirs(dir_names: Iterable[str]) -> str:
    from .utils import attach_slash

    final_dir = ""
    for directory in dir_names:
        final_dir += attach_slash(directory)

    check_make_dir(final_dir)
    logging.info("Created dir " + final_dir)
    return final_dir


def check_delete_dir(dir_name: str) -> None:
    """The check_delete_dir function checks if a directory exists and deletes
    it.

    :param dir_name: str: Used to Specify the directory name.
    :return: None. :doc-author: Julian M. Kleber
    """

    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)


def check_make_dir(dir_name: str) -> None:
    """The check_make_dir function checks if a directory exists. If it does not
    exist, the function creates it.

    :param dir_name: str: Used to Specify the folder name.
    :return: None.  :doc-author: Trelent
    """

    if dir_name == "":
        return None

    check_folder = os.path.isdir(dir_name)
    logging.info("Checked the directory %s", dir_name)

    if not check_folder:
        os.makedirs(dir_name)
        logging.info("Created folder : %s", dir_name)

    else:
        logging.info("%s folder already exists.", dir_name)
