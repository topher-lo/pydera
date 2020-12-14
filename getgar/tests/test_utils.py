import os

import pytest
import tempfile

from getgar.utils import unzip
from getgar.utils import make_path


### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data/'

TESTCASES = {
    'unzip': [
        {'args': (f'{TEST_DATA_PATH}/mutual_fund/2019q3_rr1.zip', 'sub.tsv')},
        {'args': (f'{TEST_DATA_PATH}/mutual_fund/2019q3_rr1.zip', ['tag.tsv', 'sub.tsv'])}],
    'make_path': [
        {'args': False},
        {'args': str(TEST_DATA_PATH)}
    ]
}


### FIXTURES

@pytest.fixture(scope='function', params=TESTCASES['unzip'])
def unzip_params(request):
    args = request.param['args']
    expected = sorted(''.join(request.param['args'][1]))
    return args, expected


@pytest.fixture(scope='function', params=TESTCASES['make_path'])
def make_path_params(request):
    args = request.param['args']
    return args


### UNIT TESTS

def test_unzip(unzip_params, tmp_data_directory):
    """Unzips zip file and saves content (specified by filename)
    inside tmp directory.
    """
    tmpdir = tmp_data_directory
    make_path(tmpdir)
    unzip(*unzip_params[0], tmpdir)
    result = sorted(''.join([str(f) for f in os.listdir(tmpdir)]))
    expected = unzip_params[1]
    assert result == expected


def test_make_path(make_path_params):
    """If directory path exists, returns path.
    Else creates directory and returns path.
    """

    test_path = make_path_params

    if not(test_path):
        tmpdir = tempfile.gettempdir()
        path = f'{tmpdir}/getgar/tests/'
        result = make_path(path)
    else:
        path = test_path
        result = make_path(path)

    assert result == path and os.path.exists(path)
