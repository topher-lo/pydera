"""
The `dera` module contains the `Reports` abstract base class.
`Reports`'s concrete implementations are associated certain types of 
structured datasets produced by the SEC's Divison of Economic 
and Risk Analysis. In particular, `Reports` is associated
with datasets derived from report-like SEC submissions. 
Each concrete class contains methods to download and process its 
associated dataset scope.

Supported scopes for the Reports class include: 
    - Mutual Fund Prospectus Risk / Return Summary
    - Financial Statements

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

class Reports(ABC):
    """Abstract base class containing methods to 
    download and extract DERA datasets associated
    with report-like SEC submissions.
    
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
        """Inits Reports abstract base class.
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

    @property
    def TAG(self):
        return self._TAG
    
    @TAG.setter
    def TAG(self, dir: str) -> None:
        """SQL UNIONS all TAG tables in dataset zipfiles
        between start_date and end_date.

        Sets frequency table of tags in LABEL tables in 
        dataset zipfiles between start_date and end_date.

        The TAG (Tags) table contains all standard taxonomy tags
        (as of the date) and custom tags.

        References:
        https://www.sec.gov/info/edgar/edgartaxonomies.shtml
        """
        # Get list of quarters between start_date and end_date
        start_end_dates = pd.to_datetime([self.start_date, self.end_date])
        date_range = pd.date_range(*(start_end_dates) + pd.offsets.QuarterEnd(), freq='Q')\
                       .to_period('Q')\
                       .strftime('%Yq%q')\
                       .to_list()
        # Create tmp dir
        with tempfile.TemporaryDirectory(dir=tempfile.gettempdir()) as tmpdir:
            # Unzip TAG tables into tmp dir
            for f in os.listdir(dir):
                path = os.path.join(dir, f)
                if any(q in path for q in date_range):
                    unzip(f'{path}', 'tag.tsv', tmpdir)
                    dataset_name = f.split('.')[0]
                    os.rename(f'{tmpdir}/tag.tsv', 
                              f'{tmpdir}/{dataset_name}_tag.tsv')
            
            # UNION all TAG tables on columns
            table_paths = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
            tables = [pd.read_csv(t, sep='\t')
                        .set_index(['tag', 'version']) for t in table_paths]
            data = pd.concat(tables, axis=0)
            data = data[~data.index.duplicated(keep='first')]

            # Sort TAG tables rows by tag index
            data = data.sort_index()

        # Set UNIONED TAG tables
        self._TAG = data


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
    def SUB(self, dir: str) -> None:
        """SQL UNIONS all SUB tables in dataset zipfiles
        between start_date and end_date.
        """

    @abstractmethod
    def get(self, dir: str, *args, **kwargs) -> None:
        """Retrieves all dataset zipfiles between start_date 
        and end_date. Saves zipfiles in dir.
        """


### CONCRETE CLASSES

class MutualFunds(Reports):
    """Concrete implementation of Reports.
    Download and process Reports's "Mutual Fund Prospectus Risk / Return 
    Summary" Datasets.
    
    Datasets are found at:
    https://www.sec.gov/dera/data/mutual-fund-prospectus-risk-return-summary-data-sets
    """

    def get(self, dir: str) -> None:
        """Retrieves all dataset zipfiles between start_date 
        and end_date. Saves zipfiles in dir.
        """
        pass


class FinancialStatements(Reports):
    """Concrete implementation of Reports.
    Download and process Reports's "Financial Statement and Notes" Datasets.
    
    Datasets are found at:
    https://www.sec.gov/dera/data/mutual-fund-prospectus-risk-return-summary-data-sets
    """

    def get(self, path: str) -> None:
        """Retrieves all dataset zipfiles between start_date 
        and end_date. Saves zipfiles in path.
        """
        pass