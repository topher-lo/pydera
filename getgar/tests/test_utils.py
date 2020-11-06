import os

import pytest

from getgar.utils import unzip
from getgar.utils import make_path


### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data/'

TESTCASES = {
    'unzip': [
        {'args': (f'{TEST_DATA_PATH}2020q2_rr1.zip', 'sub.tsv')},
        {'args': (f'{TEST_DATA_PATH}2020q2_rr1.zip', ['tag.tsv', 'sub.tsv'])}],
    'make_path': [
        {'args': False},
        {'args': str(TEST_DATA_PATH)}
    ]
}


### FIXTURES

@pytest.fixture(scope='session', params=TESTCASES['unzip'])
def unzip_params(request):
    args = request.param['args']
    return args


@pytest.fixture(scope='session', params=TESTCASES['make_path'])
def make_path_params(request):
    args = request.param['args']
    return args


### UNIT TESTS

def test_unzip(unzip_params, tmp_data_directory):
    """Unzips zip file and saves content (specified by filename) 
    inside tmp directory.
    """
    unzip(*unzip_params, tmp_data_directory)
    result = sorted(''.join([str(f) for f in os.listdir(tmp_data_directory)]))
    expected = sorted(''.join(unzip_params[1]))
    assert result == expected


def test_make_path(make_path_params, tmp_data_directory):
    """If directory path exists, returns path.
    Else creates directory and returns path.
    """

    test_path = make_path_params

    if not(test_path):
        path = tmp_data_directory
        result = make_path(path)
    else:
        path = test_path
        result = make_path(path)

    assert result == path and os.path.exists(path)