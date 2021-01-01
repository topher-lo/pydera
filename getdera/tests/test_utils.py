import os

import pytest
import tempfile

from getdera.utils import unzip
from getdera.utils import make_path


### TESTCASES

TEST_DATA_PATH = 'getdera/tests/data/'

TESTCASES = {
    'unzip': [
        {'args': (f'{TEST_DATA_PATH}/2019q3_rr1.zip', 'sub.tsv'),
         'expected': 'sub.tsv'},
        {'args': (f'{TEST_DATA_PATH}/2019q3_rr1.zip',
                  ['tag.tsv', 'sub.tsv']),
         'expected': ['tag.tsv', 'sub.tsv']}],
    'make_path': [
        {'args': False},
        {'args': str(TEST_DATA_PATH)}
    ]
}


### FIXTURES

@pytest.fixture(scope='function', params=TESTCASES['unzip'])
def unzip_params(request):
    args = request.param['args']
    expected = sorted(''.join(request.param['expected']))
    return args, expected


@pytest.fixture(scope='function', params=TESTCASES['make_path'])
def make_path_params(request):
    args = request.param['args']
    return args


### UNIT TESTS

def test_make_path(make_path_params):
    """If directory path exists, returns path.
    Else creates directory and returns path.
    """

    test_path = make_path_params

    if not(test_path):
        tmpdir = tempfile.gettempdir()
        path = f'{tmpdir}/getdera/tests/'
        result = make_path(path)
    else:
        path = test_path
        result = make_path(path)

    assert result == path and os.path.exists(path)


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

