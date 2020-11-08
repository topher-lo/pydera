import os
import pytest

import pandas as pd

from pandas.testing import assert_frame_equal

from getgar.utils import unzip
from getgar.dera import Reports

### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data'

TESTCASES = {
    'reports_init': [
        {'args': ('09/30/2018', '06/19/2019'),
         'expected': ('30-09-2018', '19-06-2019')},
        {'args': ('2018-09-30', '2019-06-19'),
         'expected': ('30-09-2018', '19-06-2019')}
    ],
    'reports_tag_setter': [
        {'args': f'{TEST_DATA_PATH}/mutual_fund'}
    ],
    'reports_display_tags_err': None,
    'reports_display_tags': [
        [],
        {'kwargs': {'custom':True}},
        {'kwargs': {'dtype':True}},
        {'kwargs': {'detailed':True}},
        {'kwargs': {'detailed':True}},
        {'kwargs': {'numerical':0}},
        {'kwargs': {'detailed':True}},

    ],
}

### FIXTURES

@pytest.fixture(scope='function')
def get_testreports_cls():
    """Returns TestReports class.
    """
    class TestReports(Reports):
        def get(self, dir: str) -> None:
            pass
    return TestReports


@pytest.fixture(scope='function')
def get_testreports():
    """Returns TestReports instance with start_date = "01-05-2019"
    and end_date = "15-12-2019"
    """
    class TestReports(Reports):
        def get(self, dir: str) -> None:
            pass
    return TestReports("01-05-2019", "15-12-2019")


@pytest.fixture(scope='function', params=TESTCASES['reports_init'])
def reports_init_params(request):
    args = request.param['args']
    expected = request.param['expected']
    return args, expected


@pytest.fixture(scope='function', params=TESTCASES['reports_tag_setter'])
def reports_tag_setter_params(request, tmp_data_directory):
    args = request.param['args']

    tmpdir = tmp_data_directory + '/reports'

    unzip(f'{TEST_DATA_PATH}/mutual_fund/2019q2_rr1.zip', 'tag.tsv', tmpdir)
    os.rename(f'{tmpdir}/tag.tsv', f'{tmpdir}/2019q2.tsv') 

    unzip(f'{TEST_DATA_PATH}/mutual_fund/2019q3_rr1.zip', 'tag.tsv', tmpdir)
    os.rename(f'{tmpdir}/tag.tsv', f'{tmpdir}/2019q3.tsv') 

    unzip(f'{TEST_DATA_PATH}/mutual_fund/2019q4_rr1.zip', 'tag.tsv', tmpdir)
    os.rename(f'{tmpdir}/tag.tsv', f'{tmpdir}/2019q4.tsv') 

    q2_2019 = pd.read_csv(f'{tmpdir}/2019q2.tsv', sep='\t').set_index(['tag', 'version'])
    q3_2019 = pd.read_csv(f'{tmpdir}/2019q3.tsv', sep='\t').set_index(['tag', 'version'])
    q4_2019 = pd.read_csv(f'{tmpdir}/2019q4.tsv', sep='\t').set_index(['tag', 'version'])

    expected = pd.concat([q2_2019, q3_2019, q4_2019], axis=0)
    expected = expected[~expected.index.duplicated(keep='first')].sort_index()

    return args, expected


@pytest.fixture(scope='function')
def mutualfunds():
    """Returns MutualFunds instance with start_date = "01-05-2019"
    and end_date = "01-12-2019"
    """
    return MutualFunds(start_date="01-05-2019", end_date="01-12-2019")


### UNIT TESTS

def test_reports_init(reports_init_params, 
                      get_testreports_cls):
    instance = get_testreports_cls(*reports_init_params[0])
    result = (instance.start_date, instance.end_date)
    expected = reports_init_params[1]
    assert result == expected


def test_reports_tag_setter(reports_tag_setter_params, 
                            get_testreports):
    instance = get_testreports
    instance.TAG = reports_tag_setter_params[0]
    result = instance.TAG
    expected = reports_tag_setter_params[1]
    assert_frame_equal(result, expected)


def test_reports_display_tags_err(get_testreports):
    instance = get_testreports
    with pytest.raises(Exception) as ValueError:
        instance.display_tags()