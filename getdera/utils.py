"""The `utils` module contains the helper functions used in `getdera`.
"""

import os
import pandas as pd
import dateutil.parser

from datetime import date
from zipfile import ZipFile

from typing import Union
from typing import List
from typing import Tuple


STRFTIME_FORMATS = {
    'date': '%d-%m-%Y',
    'year_quarter': '%Yq%q',
    'year_month': '%Y_%m',
}  # Striftime formats used in getdera


def get_start_end_strftimes(
        start_date: str,
        end_date: str,
        format: str = STRFTIME_FORMATS['date']) -> Tuple[str]:
    """Returns start_date and end_date as formatted strings for internal use.
    If end_date is not specified, returns end_date as current day's
    formatted strftime.
    """
    # Convert datetime string to %d-%m-$Y format
    start_date = dateutil.parser\
                         .parse(start_date)\
                         .strftime(format)
    if not(end_date):
        end_date = date.today().strftime(format)
    else:
        end_date = dateutil.parser\
                           .parse(end_date)\
                           .strftime(format)
    return start_date, end_date


def get_quarters(start_date: str,
                 end_date: Union[None, str],
                 format: str = STRFTIME_FORMATS['year_quarter']) -> List[str]:
    """Returns list of quarters (as formatted strings) between start_end
    and end_date. Uses quarter start frequency such that the list includes
    end_date's quarter.
    """
    # Get list of quarters between start_date and end_date
    quarters = pd.date_range(start_date, end_date,
                             freq='QS').to_period('Q')\
                                       .strftime(format)\
                                       .to_list()
    return quarters


def get_year_months(
        start_date: str,
        end_date: Union[None, str],
        format: str = STRFTIME_FORMATS['year_month']) -> List[str]:
    """Returns list of months (as formatted strings) between start_end
    and end_date. Uses month start frequency such that the list
    includes end_date's month.
    """
    # Get list of months by year between start_date and end_date
    year_months = pd.date_range(start_date, end_date,
                                freq='MS').to_period('M')\
                                          .strftime(format)\
                                          .to_list()
    return year_months


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


if __name__ == "__main__":
    pass
