"""
The `utils` module contains the utility functions used in `getgar`.
"""

import os

from zipfile import ZipFile

from typing import Union
from typing import List


def unzip(zipfile: str, filename: Union[str, List[str]], path: str) -> None:
    """Unzip, extract, and save content of a zip file.

    Args:
        zipfile (str): 
            Path to zip file to be unzipped.
        filename (Union[str, List[str]]): 
            File(s) to extract from the zip.
        path (str): 
            Path to save extracted files into.

    Returns: 
        None
    """
    with ZipFile(zipfile, 'r') as zipObj:
        make_path(path)
        if type(filename) == list:
            for f in filename:
                zipObj.extract(f, path)
        else:
            zipObj.extract(filename, path)


def make_path(path: str) -> str:
    """Make directory.

    Args:
        path (str): 
            Path to be made if it doesn't exist.

    Returns:
        path (str)
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path