import os
import pytest

import pandas as pd

from pandas.testing import assert_frame_equal

from getgar.utils import unzip
from getgar.dera import zip_to_tags

### TESTCASES

TEST_DATA_PATH = 'getgar/tests/data'

TESTCASES = {
    'zip_to_tags': [
        {'args': (f'{TEST_DATA_PATH}/mutual_fund',
                  '01-05-2019',
                  '15-12-2019')}
    ],
    # 'display_tags': [
    #     [],
    #     {'kwargs': {'custom':True}},
    #     {'kwargs': {'dtype':True}},
    #     {'kwargs': {'detailed':True}},
    #     {'kwargs': {'detailed':True}},
    #     {'kwargs': {'numerical':0}},
    #     {'kwargs': {'detailed':True}},

    # ],
}

### FIXTURES


@pytest.fixture(scope='function', params=TESTCASES['zip_to_tags'])
def zip_to_tags_params(request, tmp_data_directory):
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


### UNIT TESTS

def test_zip_to_tags(zip_to_tags_params):
    result = zip_to_tags(*zip_to_tags_params[0])
    expected = zip_to_tags_params[1]
    assert_frame_equal(result, expected)