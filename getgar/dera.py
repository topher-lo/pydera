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
import numpy as np
import pandas as pd 
import urllib.error as urlerr
import tempfile

import dateutil.parser

from abc import ABC
from abc import abstractmethod
from datetime import date
from urllib import request
from typing import Union
from typing import List

from getgar.utils import unzip

### ABSTRACT BASE CLASS

class DERA(ABC):
    """Abstract base class containing methods to 
    download and extract DERA datasets.
    
    Attributes:
        start_date: str
            Fetch all datasets after start_date
            (includes start_date's quarter even if start_date is after the
            start of the quarter).

            Date must be written in some ordered DateTime string format 
            e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD

        end_date: Union[None, str]
            Optional; if end_date = None, feteches all datasets 
            before today (UTC) and after start_end.
            (includes end_date's quarter even if end_date is before the
            end of the quarter).

            Date must be written in some ordered DateTime string format 
            e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD

        TAG: Pandas DataFrame
            Optional;


    """
    
    def __init__(self,
                 start_date: str,
                 end_date: Union[None, str] = None,
                 *args, **kwargs
    ) -> None:
        """Inits DERA abstract base class.
        Dates stored as %d-%m-%Y time format strings.
        """
        self.start_date = dateutil.parser\
                                  .parse(start_date)\
                                  .strftime('%d-%m-%Y')
        if not(end_date):
            end_date = date.today().strftime('%d-%m-%Y')
        else:
            end_date = dateutil.parser\
                               .parse(end_date)\
                               .strftime('%d-%m-%Y')
        self.end_date = end_date
        self.TAG = None
        self.SUB = None

    @property
    def TAG(self):
        return self._TAGS
    
    @TAG.setter
    def TAG(self, path: str) -> None:
        """SQL JOINS all TAG tables in dataset zipfiles
        between start_date and end_date.

        The TAG (Tags) table contains all standard taxonomy tags
        (as of the date) and custom tags.

        References:
        https://www.sec.gov/info/edgar/edgartaxonomies.shtml
        """
        # Get list of quarters between start_date and end_date
        date_range = pd.date_range(self.start_date, 
                                   self.end_date, 
                                   freq='Q')\
                                   .to_period('Q')\
                                   .strftime('%Yq%q')\
                                   .to_list()
        tags = []


    def display_tags(self, 
                     custom=False, 
                     dtype=False,
                     detailed=False,
                     numerical=2
    ) -> str:
        tags = self.TAG
        if not(tags):
            raise ValueError(
                "No TAG table found."
        )
        else:
            if custom:
                tags = tags[tags['custom'] == 1]
            else:
                tags = tags[tags['custom'] == 0]
            full_desc = ''
            for i in range(len(tags)):
                entry = tags.iloc[i]
                attr = (entry['tag'], entry['version'], entry['tlabel'])
                tag_desc = f'\nTag: {attr[0]} \
                             \nVersion: {attr[1]} \
                             \nLabel: {attr[2]}'
                if dtype:
                    attr = entry['datatype']
                    tag_desc = tag_desc + f'\nDatatype: {attr}'
                if detailed:
                    attr = entry['doc']
                    tag_desc = tag_desc + f'\nDefinition: {attr}'
                full_desc = full_desc + tag_desc
            return full_desc

    @property
    def SUB(self):
        return self._sub
    
    @SUB.setter
    def SUB(self, path: str) -> None:
        """SQL JOINS all SUB tables in dataset zipfiles
        between start_date and end_date.
        """

    @abstractmethod
    def get(self, path: str, *args, **kwargs) -> None:
        """Retrieves all dataset zipfiles between start_date 
        and end_date. Saves zipfiles in path.
        """


### CONCRETE CLASSES

class MutualFunds(DERA):
    """Concrete implementation of DERA.
    Download and process DERA's "Mutual Fund Prospectus Risk / Return 
    Summary" Datasets.
    
    Datasets are found at:
    https://www.sec.gov/dera/data/mutual-fund-prospectus-risk-return-summary-data-sets
    """

    def get(self, path: str) -> None:
        """Retrieves all dataset zipfiles between start_date 
        and end_date. Saves zipfiles in path.
        """
        pass
