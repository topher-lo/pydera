"""
The `dera` module contains functions to process structured datasets
produced by the SEC's Divison of Economic and Risk Analysis.

Supported datasets from DERA include: 
    - Mutual Fund Prospectus Risk and Return Summary
    - Financial Statements and Notes

Note: 
Each dataset from DERA is a zipfile that contains multiple files in 
a tabular format (e.g. tab-separated values file). 
Each file represents a different data table.

You can find DERA datasets at https://www.sec.gov/dera/data
"""

import sys
import os
import numpy as np
import pandas as pd 
import urllib.error as urlerr
import tempfile

import dateutil.parser

from datetime import date
from urllib import request
from typing import Union
from typing import List

from getgar.utils import unzip



def _process_tags(tmpdir: str) -> pd.DataFrame:
    """SQL FULL OUTER JOINS all TAG tables in dataset zipfiles
    found in tmpdir.

    The TAG (Tags) table contains all standard taxonomy tags
    (as of the date) and custom tags.

    References:
    https://www.sec.gov/info/edgar/edgartaxonomies.shtml
    """

    # UNION all TAG tables on columns
    table_paths = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
    tables = [pd.read_csv(t, sep='\t')
                .set_index(['tag', 'version']) for t in table_paths]
    data = pd.concat(tables, axis=0)
    data = data[~data.index.duplicated(keep='first')]

    # Sort TAG tables rows by tag index
    data = data.sort_index()

    return data


def _process_subs(tmpdir: str) -> pd.DataFrame:
    """SQL FULL OUTER JOINS all SUB tables in dataset zipfiles
    found in tmpdir.
    """
    pass


def process(dir: str,
            table: str,
            start_date: str, 
            end_date: Union[None, str]=None) -> pd.DataFrame:
    """Processes DERA dataset zipfiles found in dir for quarters between start_date and end_date. 

    Args:
        dir (str): 
            Path to directory containg DERA datasets as zipfiles.

        table (str): 
            Tables in datasets to process.
            Supported tables (and corresponding datasets) include:

            -  'tag' -- tag.tsv files in:
                1. Mutual Fund Prospectus Risk and Return Summary
                2. Financial Statements and Notes.

            - 'sub' -- sub.tsv files in:
                1. Mutual Fund Prospectus Risk and Return Summary
                2. Financial Statements and Notes.

        start_date (str): 
            Fetch all datasets after start_date. 
            
            Includes start_date's quarter even if start_date is after the
            start of the quarter. Date must be written in some ordered DateTime string format
            (e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD).

        end_date (Union[None, str]): 
            Optional; if end_date = None, fetches all datasets 
            before today (UTC) and after start_end.

            Includes end_date's quarter even if end_date is before the
            end of the quarter. Date must be written in some ordered DateTime string format 
            (e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD)
    """

    # Convert datetime string to %d-%m-$Y format
    start_date = dateutil.parser\
                         .parse(start_date)\
                         .strftime('%d-%m-%Y')
    if not(end_date):
        end_date = date.today().strftime('%d-%m-%Y')
    else:
        end_date = dateutil.parser\
                           .parse(end_date)\
                           .strftime('%d-%m-%Y')
    end_date = end_date

    # Get list of quarters between start_date and end_date
    start_end_dates = pd.to_datetime([start_date, end_date])
    date_range = pd.date_range(*(start_end_dates) + pd.offsets.QuarterEnd(), freq='Q')\
                    .to_period('Q')\
                    .strftime('%Yq%q')\
                    .to_list()

    # Create tmp dir
    with tempfile.TemporaryDirectory(dir=tempfile.gettempdir()) as tmpdir:
        # Unzip tables into tmp dir
        for f in os.listdir(dir):
            path = os.path.join(dir, f)
            if any(q in path for q in date_range):
                unzip(f'{path}', f'{table}.tsv', tmpdir)
                dataset_name = f.split('.')[0]
                os.rename(f'{tmpdir}/{table}.tsv', 
                            f'{tmpdir}/{dataset_name}_{table}.tsv')
        
        # Process specified table
        if table == 'tag':
            data = _process_tags(tmpdir)
        
        elif table == 'sub':
            data = _process_subs(tmpdir)

    return data
