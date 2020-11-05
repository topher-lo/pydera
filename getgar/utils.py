import os

from zipfile import ZipFile

from typing import Union
from typing import List

def unzip(zipfile: Union[ZipFile, str], filename: Union[str, List[str]], path: str) -> None:
    """Unzip, extract, and save content of a zip file.

    Args: 
        zipfile (zip-like object or path-like object): 
            Path to zip file to be unzipped.
        filename (str or list): 
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
    """Make directory based on filing info.
    Args:
        path (str): Path to be made if it doesn't exist.
    Raises:
        OSError: If there is a problem making the path.
    Returns:
        path (str)
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, **kwargs)
        except OSError as e:
            if e.error != error.EXIST:
                raise OSError
    return path
