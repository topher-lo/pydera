# pydera
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![codecov](https://codecov.io/gh/topher-lo/pydera/branch/main/graph/badge.svg?token=MURPG4B3J0)](https://codecov.io/gh/topher-lo/pydera)
[![Generic badge](https://img.shields.io/badge/version-v0.01-4B8BBE.svg)]()
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/topher-lo/pydera)
[![Open in nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/topher-lo/pydera)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/)

Downloading and processing aggregated datasets from the SEC's Division of Economic and Risk Analysis.

## Features
- Webscrapes structured datasets from the DERA's data library (https://www.sec.gov/dera/data)
- Bulk downloads quarterly structured datasets within a specified time period
- Logging module that logs download status (e.g. HTTP status code) for each data set
- Supported datasets and tables:
    - Mutual Fund Prospectus datasets
    - Financial Statements and Notes datasets
- Processes tables within the datasets across multiple time periods
- Example NLP pipelines (from data prep to data modelling and visualisation) using `pydera`, `spacy`, `gensim`, and `sklearn` in Jupyter notebooks
    - `notebook/risk.ipynb`: Topic modelling risk narratives from mutual fund prospectuses filed in 2019
- Documentation found [here](https://topher-lo.github.io/pydera/getdera/).

## Install
The latest release can be installed using pip:
```bash
pip install pydera
```
The main branch can be installed locally by cloning the repo and installing its dependencies:
```bash
git clone git@github.com:topher-lo/pydera.git
cd [..path/to/repo]
pip install -r requirements.txt
```

## 🚀 A quick example
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
    client.get_DERA(DATASET,
                    tmpdir,
                    START_DATE,
                    END_DATE)
    # Process SUB data in tempdir
    DATA['sub'] = dera.process(tmpdir,
                               DATASET,
                               'sub',
                               START_DATE,
                               END_DATE)
    # Process TXT data in tempdir
    DATA['txt'] = dera.process(tmpdir,
                               DATASET,
                               'txt',
                               START_DATE,
                               END_DATE,
                               dtype={'document': str, 'txtlen': int})
```

## Background
There are packages to download company filings via the EDGAR API (e.g. `sec-edgar`). These packages download multiple reports / filings in their entirety. The SEC's Division of Economic and Risk Analysis (DERA), however, has "provided access to aggregated data from public filings for research and analysis" found [here](https://www.sec.gov/dera/data). 

`pydera` downloads from this library of aggregated datasets, which I believe are more suitable for data analysis.

The aggregated data from DERA is structured, cleaned, and provides columns of data (including financials and textual information) for all filings quarter by quarter. The datasets are also well documented and contain fields (e.g. e city of the registrant's business address) relevant for data analysis. 

In particular, I believe the `TXT` tables (from the mutual fund prospectus dataset and financial statements datasets) provide a large corpus of textual financial information. This corpus can be immediately usable for natural language processing (NLP) tasks. These tables also present a time-dimension to NLP analysis.

## Roadmap
- Build visualisations of data relationships between tables within DERA datasets
    - To support data processing
    - To improve clarity of the information provided by DERA
    
## Contributing
Found a bug? Wrote a patch? Have an idea on how to use DERA's datasets for a data science project? Please checkout the brief [contribution guide](https://github.com/topher-lo/pydera/blob/main/CONTRIBUTING.md). Any and all contributions are welcome. :heart: :snake: :raised_hands:
