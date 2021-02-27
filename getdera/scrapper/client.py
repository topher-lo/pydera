"""The `client` module contains functions to webscape the
SEC website. Designed for parallelised
webscrapping within the SEC EDGAR's Fair Access policy.

Datasets are found at https://www.sec.gov/files/dera/data

Paths to specific datasets:\n
1. Financial Statements and Notes -- `financial-statement-and-notes-data-sets/zipfile`
2. Mutual Fund Prospectuses -- `mutual-fund-prospectus-risk/return-summary-data-sets/zipfile`

References:
https://www.sec.gov/developer
"""

import os
import logging
import requests

from datetime import datetime
from typing import List

from requests_toolbelt import sessions
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from getdera.utils import get_start_end_strftimes
from getdera.utils import get_quarters
from getdera.utils import get_year_months

from requests.packages.urllib3.util.retry import Retry


# Logging
logger = logging.getLogger(__name__)  

# Set log level
logger.setLevel(logging.INFO)

# Define file handler and set formatter
file_handler = logging.FileHandler('scrapper.log')
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s',
                              datefmt='%d-%b-%y %H:%M')
file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)

# Path to certificate
PATH_TO_CERT = 'getdera/scrapper/certs/secgov.cer'

# Base URLs and paths to datasets
# Last Update: 7th November 2020

DERA_DATA_URL = "https://www.sec.gov/files/dera/data"
DERA_DATA_PATHS = {
    'risk': 'mutual-fund-prospectus-risk/return-summary-data-sets/zipfile',
    'statements': 'financial-statement-and-notes-data-sets/zipfile',
}
DERA_DATA_EXT = {
    'risk': '_rr1.zip',
    'statements': '_notes.zip',
}  # DERA dataset identifier and extension


# CLIENT

def _response_raise_status(response, *args, **kwargs):
    return response.raise_for_status()


class _TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def _get(urls: List[str],
         dir: str,
         session: sessions.BaseUrlSession,
         chunk_size: int = 128,
         timeout: int = 5,
         retry: int = 2,
         delay: int = 5,
         path_to_cert=PATH_TO_CERT) -> None:
    """Downloads the given URLs and saves the contents to dir.

    Args:
        urls (list): 
            List of URLs with files at their endpoints to download.

        dir (str): 
            Directory path to save downloaded files in.

        session (BaseUrlSession): 
            BaseUrlSession instance to use.

        chunk_size (int): 
            Optional; chunk size for streaming files.

        timeout (int): 
            Optional; timeout before closing connection.

        retry (int): 
            Optional; number of times to retry a request
            after a ConnectTimeout error.

        delay (int): 
            Optional; backoff factor. Determines number of seconds
            processes will sleep between failed requests.
            {delay} * (2 ** ({number of total retries} - 1))

        path_to_cert (str): 
            Optional; path to server SSL certificate.

    Effects: 
        Downloaded files are saved in dir. Exceptions raised by requests
        module are logged and saved.

    Returns: 
        None
    """

    def _save_content(path, r, chunk_size):
        with open(path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
        # Check if downloaded
        if os.path.isfile(path):
            logger.info(f'Downloaded {url}')
        else:
            logger.warning(f'{url} not found!')

    retry_strategy = Retry(
        total=retry,
        backoff_factor=delay,
        # requests should incrementally backoff on common 5xx server errors
        # and 429 rate exceeded client error
        status_forcelist=[429, 500, 502, 503, 504],
        # Only have GET requests in getdera
        allowed_methods=['GET']
    )
    session.mount('https://', _TimeoutHTTPAdapter(max_retries=retry_strategy,
                  timeout=timeout))
    session.verify = True  # Verify session
    for url in urls:
        try:
            r = session.get(url, stream=True)
        except MaxRetryError as err:
            logger.warning(err)
            continue
        except requests.exceptions.HTTPError as err:
            logger.warning(err)
            continue
        except requests.exceptions.SSLError as err:
            logger.warning(err)
            continue
        else:
            base_url = session.base_url
            full_url = '{}/{}'.format(base_url[:base_url.rfind('/')], url)
            logger.info(f'Successful access to url: {full_url}')
            path = f'{dir}/{url}'
            _save_content(path, r, chunk_size)


def get_DERA(dataset: str,
             dir: str,
             start_date: str,
             end_date: str,
             chunk_size: int = 128,
             timeout: int = 120,
             retry: int = 2,
             delay: int = 1) -> None:
    """Downloads and saves DERA dataset zipfiles for quarters between
    start_date and end_date.

    Args:
        dataset (str): 
            DERA dataset to download.
            Supported datasets include:
                - 'statements': Financial Statements and Notes
                - 'risk': Mutual Fund Prospectus Risk and Return Summary
 
        dir (str): 
            Directory path to save downloaded files in.

        start_date (str): 
            Fetch all datasets after start_date.
            Includes start_date's quarter even if start_date is after the
            start of the quarter. Cannot be in the same month as end_date.

            Date must be written in some ordered DateTime string format
            (e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD)

        end_date (Union[None, str]): 
            Optional; if end_date = None, feteches all datasets
            before today (UTC) and after start_end.
            (includes end_date's quarter even if end_date is before the
            end of the quarter). Cannot be in the same month as start_date.

            Date must be written in some ordered DateTime string format
            e.g. DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD, YYYY-MM-DD

        chunk_size (int): 
            Optional; chunk size for streaming files.

        timeout (int): 
            Optional; timeout before closing connection.

        retry (int): 
            Optional; number of times to retry a request
            after a ConnectTimeout error.

        delay (int): 
            Optional; backoff factor. Determines number of seconds
            processes will sleep between failed requests, where
            sleep seconds = delay * (2 ** ({number of total retries} - 1)).

    Effects:
        Downloaded files are saved in dir.

    Returns:
        None
    """

    # SET-UP
    endpoint = DERA_DATA_PATHS[dataset]
    dera_http = sessions.BaseUrlSession(base_url=f'{DERA_DATA_URL}/{endpoint}')
    assert_status_hook = _response_raise_status
    dera_http.hooks["response"] = [assert_status_hook]
    # Dataset identifier and extension
    ext = DERA_DATA_EXT[dataset]

    # Start date and end date strftimes
    start_date, end_date = get_start_end_strftimes(start_date, end_date)

    # If statements dataset and end_date on or after 2020-10-01
    if dataset == 'statements' and\
            datetime.strptime(end_date, '%Y-%m-%d') >= datetime(2020, 10, 1):
        quarters_range = get_quarters(start_date, '2020-09-01')
        months_range = get_year_months('2020-10-01', end_date)
        date_range = quarters_range + months_range
    else:
        # Get list of quarters between start_date and end_date
        date_range = get_quarters(start_date, end_date)

    # If no date range
    if not(date_range):
        raise ValueError('Improperly specified start and end dates.')

    # Create list of urls
    urls = [f'{date}{ext}' for date in date_range]
    # GET and save datasets in dir
    _get(urls, dir, dera_http, chunk_size, timeout, retry, delay)

    return None


if __name__ == "__main__":
    pass
