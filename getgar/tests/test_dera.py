import pytest

from getgar.dera import DERA


### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data/'

TESTCASES = {
    'DERA_to_dataframe': [{'args': None}],
    'MutualFund_get': [{'args': None}],
    'MutualFund_get_error': [{'args': None}],
}

### FIXUTRES

@pytest.fixture(scope='session', params=TESTCASES['DERA_to_dataframe'])
def DERA_to_dataframe_params(request):
    args = request.param['args']
    return args


@pytest.fixture(scope='session', params=TESTCASES['MutualFund_get'])
def MutualFund_get_params(request):
    args = request.param['args']
    return args


@pytest.fixture(scope='session', params=TESTCASES['MutualFund_get_error'])
def MutualFund_get_error_params(request):
    args = request.param['args']
    return args


### UNIT TESTS

def test_DERA_to_dataframe(DERA_to_dataframe_params):
    """
    """
    pass


def test_MutualFund_get(MutualFund_get_params):
    """ 
    """
    pass


def test_MutualFund_get_error(MutualFund_get_error_params):
    """
    """
    pass