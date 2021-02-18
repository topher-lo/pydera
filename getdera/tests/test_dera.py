import pytest

import pandas as pd

from getdera import utils

from pandas.testing import assert_frame_equal
from getdera.dera import process


# TESTCASES

TEST_DATA_PATH = 'getdera/tests/data'

TESTCASES = {
    'process_tag': [
        {'args': (f'{TEST_DATA_PATH}',
                  'risk',
                  'tag',
                  '01-01-2020',
                  '01-03-2020'),
         'expected': pd.DataFrame({
             'tag': ['AcquiredFundFeesAndExpensesBasedOnEstimates',
                     'AmendmentFlag',
                     'AmendmentFlag',
                     'AnnualFundOperatingExpensesTableTextBlock',
                     'AnnualReturn2006'],
             'version': ['rr/2012',
                         'dei/2012',
                         'dei/2014',
                         'rr/2012',
                         'rr/2012'],
             'dummy_value': ['lorem2020q1',
                             'ipsum2020q1',
                             'dolor2020q1',
                             'sit2020q1',
                             'amet2020q1']}).set_index(['tag', 'version'])}
    ],
    'process_sub': [
        {'args': (f'{TEST_DATA_PATH}',
                  'risk',
                  'sub',
                  '01-10-2019',
                  '15-12-2019'),
         'expected': pd.DataFrame({
             'adsh': ['0000000001-01-000001',
                      '0000000001-01-000002',
                      '0000000001-01-000003'],
             'dummy_val': ['lorem2019q4',
                           None,
                           'dolor2019q4']}).set_index('adsh')}
    ],
    'process': [
        {'args': (f'{TEST_DATA_PATH}',
                  'risk',
                  'txt',
                  '01-07-2019',
                  '15-12-2019'),
         'expected': pd.DataFrame({
             'adsh': ['0000000001-01-000001',
                      '0000000001-01-000002',
                      '0000000001-01-000003']*2,
             'dummy_val': ['lorem2019q3', None, 'ipsum2019q3',
                           'lorem2019q4', None, 'ipsum2019q4']})},
        {'args': (f'{TEST_DATA_PATH}',
                  'risk',
                  'txt',
                  '01-10-2019',
                  '15-01-2020'),
         'expected': pd.DataFrame({
             'adsh': ['0000000001-01-000001',
                      '0000000001-01-000002',
                      '0000000001-01-000003']*2,
             'dummy_val': ['lorem2020q1', None, 'ipsum2020q1',
                           'lorem2019q4', None, 'ipsum2019q4']})}
    ],
}

# FIXTURES

@pytest.fixture(scope='function', params=TESTCASES['process_tag'])
def process_tag_params(request, tmp_data_directory):
    args = request.param['args']
    expected = request.param['expected']
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    return args, expected


@pytest.fixture(scope='function', params=TESTCASES['process_sub'])
def process_sub_params(request, tmp_data_directory):
    args = request.param['args']
    expected = request.param['expected']
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    return args, expected


@pytest.fixture(scope='function', params=TESTCASES['process'])
def process_params(request, tmp_data_directory):
    args = request.param['args']
    expected = request.param['expected']
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    return args, expected


# UNIT TESTS

def test_process_tag(process_tag_params):
    result = process(*process_tag_params[0])
    expected = process_tag_params[1]
    assert_frame_equal(result, expected)


def test_process_sub(process_sub_params):
    result = process(*process_sub_params[0])
    expected = process_sub_params[1]
    assert_frame_equal(result, expected)


def test_process(process_params):
    result = process(*process_params[0]).sort_values('dummy_val')\
                                        .reset_index(drop=True)
    expected = process_params[1].sort_values('dummy_val')\
                                .reset_index(drop=True)
    assert_frame_equal(result, expected)
