# pydera
[![codecov](https://codecov.io/gh/topher-lo/pydera/branch/main/graph/badge.svg?token=MURPG4B3J0)](https://codecov.io/gh/topher-lo/pydera)

Dowloading aggregated textual data from the SEC's Division of Economic and Risk Analysis.

## Features
- Webscrapes structured datasets from SEC DERA data library website (https://www.sec.gov/dera/data)
- Bulk downloads quarterly structured datasets within a specified time period
- Logging module that logs download status (e.g. HTTP status code) for each data set
- Supported datasets and tables:
    - Mutual Fund Prospectus datasets
    - Financial Statement datasets
- Processes tables within the datasets across multiple time periods
- Example NLP pipelines (from data prep to data modelling and visualisation) using `pydera` and `Spacy` in Jupyter notebooks
    - `notebook/risk.ipynb` -- Analysis of risk narratives in mutual fund prospectuses

## Install
pydera depends on the following packages:
- `pandas`
- `requests`
- `requests-toolbelt`
- `responses`
- `zipfile`

## A quick example
```python
import tempfile

from getdera import dera

from getdera.scrapper import client
from tqdm import tqdm

# GLOBAL VARIABLES
DATASET = "risk"
DIR = tempfile.gettempdir()
START_DATE = "01/01/2018"
END_DATE = "30/12/2019"

DATA = {} # Data dictionary

# Extract mutual fund prospectus datasets from sec.gov

with tempfile.TemporaryDirectory(dir=DIR) as tmpdir:
    # Download data and save in tempdir
    client.get_DERA(DATASET, tmpdir, START_DATE, END_DATE)
    # Process SUB data in tempdir
    DATA['sub'] = dera.process(tmpdir, 'sub', START_DATE, END_DATE)
    # Process TXT data in tempdir
    DATA['txt'] = dera.process(tmpdir, 'txt', START_DATE, END_DATE, dtype = {'document': str, 'txtlen': int})
```

## Background
There are packages to download company filings via the EDGAR API (e.g. `sec-edgar`). These packages download multiple reports / filings in their entirety. The SEC's Division of Economic and Risk Analysis (DERA), however, has "provided access to aggregated data from public filings for research and analysis" found ![here](https://www.sec.gov/dera/data). 

`pydera` downloads from this library of aggregated datasets, which I believe are more suitable for data analysis.

The aggregated data from DERA is structured, cleaned, and provides columns of data (including financials and textual information) for all filings quarter by quarter. The datasets are also well documentated and contain fields (e.g. e city of the registrant's business address) relevant for data analysis. 

In particular, I believe the `TXT` tables (from the mutual fund prospectus dataset and financial statements datasets) provide a large corpus of textual financial information. This corpus can be immediately usable for natural language processing (NLP) tasks.

## Roadmap
- Build visualisation of data relationships between tables within DERA datasets
    - To support data processing
    - To improve clarity of the information provided by DERA