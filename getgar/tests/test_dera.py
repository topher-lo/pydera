import pytest

from getgar.dera import DERA


### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data/'

TESTCASES = {
    'dera_init': [
        {'args': ('09/30/2018', '06/19/2019'),
         'expected': ('30-09-2018', '19-06-2019')},
        {'args': ('2018-09-30', '2019-06-19'),
         'expected': ('30-09-2018', '19-06-2019')}
    ]
}

### FIXTURES

@pytest.fixture(scope='session')
def testdera():
    """Returns MutualFunds instance with start_date = "01-05-2019"
    and end_date = "01-12-2019"
    """
    class TestDERA(DERA):
        def get(self, path: str) -> None:
            pass
    return TestDERA


@pytest.fixture(scope='session', params=TESTCASES['dera_init'])
def dera_init_params(request):
    args = request.param['args']
    expected = request.param['expected']
    return args, expected


@pytest.fixture(scope='session')
def mutualfunds():
    """Returns MutualFunds instance with start_date = "01-05-2019"
    and end_date = "01-12-2019"
    """
    return MutualFunds(start_date="01-05-2019", end_date="01-12-2019")


### UNIT TESTS

def test_dera_init(dera_init_params, testdera):
    instance = testdera(*dera_init_params[0])
    result = (instance.start_date, instance.end_date)
    expected = dera_init_params[1]
    assert result == expected