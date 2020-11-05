"""
The `dera` module contains the DERA abstract base class.
DERA's concrete implementations are associated with different 
structured datasets produced by the SEC's Divison of Economic 
and Risk Analysis. Each concrete class contains methods
to download and process its associated dataset scope.
DERA datasets are released on a quarterly basis.

Supported scopes include: 
    - Mutual Fund Prospectus Risk / Return Summary

You can find DERA datasets at https://www.sec.gov/dera/data
"""

import sys
import os

from abc import ABC
from abc import abstractmethod

import numpy as np
import pandas as pd 

import tempfile

from urllib import request
import urllib.error as urlerr

from typing import Union
from typing import List

### ABSTRACT BASE CLASS

class DERA(ABC):
    """Abstract base class containing methods to 
    download and extract DERA datasets.
    
    Attributes:
        start_date: Union[None, str]
            Optional; if start_year = None, fetches all datasets before end_date.
            Date before which not to fetch reports.

            Date must be written in the format year-quarter, 
            where quarter is one of the following four options:
            'q1', 'q2', 'q3', 'q4'.
                e.g. start_date = '2019-q4'

        end_date: Union[None, str]
            Optional; if end_date = None, feteches all datasets 
            before today (UTC) and after start_end.
            Date after which not to fetch reports.

            Date must be written in the format year-quarter, 
            where quarter is one of the following four options:
            'q1', 'q2', 'q3', 'q4'.
                e.g. start_date = '2019-q4'

        table: str
            Each DERA dataset scope has different tables.
            The DERA class only extracts one type of table 
            from each quarter's datasets.

        path: str
            Path to store raw, i.e. directly downloaded from 
            SEC website, datasets in.

        _paths: Union[None, List[str]]
            Paths to raw, i.e. directly downloaded from 
            SEC website, datasets.

        _datasets: Union[None, List[pd.DataFrame]]
            DERA datasets downloaded and stored in memory as
            a list of pandas DataFrames.
    """
    
    def __init__(self,
                 start_date: Union[None, str],
                 end_date: Union[None, str],
                 table: str,
                 *args, **kwargs
    ) -> None:
        """Inits DERA abstract base class"""
        self.start_date = start_date
        self.end_date = end_date
        self.table = table
        self._paths = None
        self._datasets = None

    @classmethod
    def to_dataframe(cls, path: str, sep='\t', table='sub' *args, **kwargs):
        """Converts and concantenates (along index) all datasets with the same
        fields (i.e. all of the same table type e.g. sub.tsv)
        into a single Pandas DataFrame. Returns DataFrame.

        Args:
            path: str
                Path to datasets.

            sep: 
                Defaults to tab regex deliminator '\t'. 
                Delimiter to use to read datasets. 
                See pandas.read_csv() documentation.

            table:
                DERA table type to convert to DataFrame.
                See corresponding docstring in concrete 
                classes for link to documentation
                of the associated DERA dataset.

        Returns:
            DataFrame of concatenated datasets.

        Raises:


        """
        datasets = [pd.read_csv(f'{path}/{f}', sep) for f in os.listdir(path)]
        return pd.concat(datasets)

    @abstractmethod
    def get(self, path: str, *args, **kwargs):
        """Retrieves all datasets between start_date 
        and end_date. Saves 
        """

### CONCRETE CLASSES

class MutualFunds(DERA):
    """Concrete implementation of DERA.
    Download and process DERA's "Mutual Fund Prospectus Risk / Return 
    Summary" Datasets.
    
    Datasets are found at:
    https://www.sec.gov/dera/data/mutual-fund-prospectus-risk-return-summary-data-sets
    """
