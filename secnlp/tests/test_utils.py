import os

import pytest

from secnlp.utils import unzip


### TESTCASES

TEST_DATA_PATH = 'secnlp/tests/data/'

TESTCASES = {
    'unzip': [
        {'args': (f'{TEST_DATA_PATH}2020q2_rr1.zip', 'sub.tsv')},
        {'args': (f'{TEST_DATA_PATH}2020q2_rr1.zip', ['tag.tsv', 'sub.tsv'])}]
}


### FIXTURES

@pytest.fixture(scope='session', params=TESTCASES['unzip'])
def unzip_params(request):
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