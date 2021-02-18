import os
import pytest
import responses
import shutil

from requests_toolbelt import sessions
from getdera import utils

from getdera.scrapper.client import _get
from getdera.scrapper.client import get_DERA


# TESTCASES

BASE_URL = "https://www.testingsec.gov/dera/data"
TEST_ENDPOINT = "testing-data-sets"
TEST_SESSION_URL = f'{BASE_URL}/{TEST_ENDPOINT}/zipfile'
TEST_URL = f'{BASE_URL}/{TEST_ENDPOINT}'

# SESSION SET-UP
test_http = sessions.BaseUrlSession(base_url=f'{TEST_SESSION_URL}')
assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
test_http.hooks["response"] = [assert_status_hook]

CONTENT = ['1'*3,
           '2'*6,
           '3'*13]

TEST_RESPONSES = {
    '200': [
        {'url': f'{TEST_URL}/2019q1_rr1.zip',
         'method': 'GET',
         'body': CONTENT[0],
         'status': 200},
        {'url': f'{TEST_URL}/2019q2_rr1.zip',
         'method': 'GET',
         'body': CONTENT[1],
         'status': 200},
        {'url': f'{TEST_URL}/2019q3_rr1.zip',
         'method': 'GET',
         'body': CONTENT[2],
         'status': 200},
    ],
    '403': {'url': f'{TEST_URL}/2019q1_rr1.zip',
            'method': 'GET',
            'status': 403},
    '500': {'url': f'{TEST_URL}/2019q2_rr2.zip',
            'method': 'GET',
            'status': 500},
    '200_statements': [
        {'url': f'{TEST_URL}/2020q2_notes.zip',
         'method': 'GET',
         'status': 200},
        {'url': f'{TEST_URL}/2020q3_notes.zip',
         'method': 'GET',
         'status': 200},
        {'url': f'{TEST_URL}/2020_10_notes.zip',
         'method': 'GET',
         'status': 200},
        {'url': f'{TEST_URL}/2020_11_notes.zip',
         'method': 'GET',
         'status': 200},
    ]
}

TESTCASES = {
    '_get': [
        {'kwargs': {'urls': [r['url'] for r in TEST_RESPONSES['200']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': [r for r in TEST_RESPONSES['200']]},
    ],
    '_get_error': [
        {'kwargs': {'urls': [r['url'] for r in TEST_RESPONSES['403']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': TEST_RESPONSES['403']},
        {'kwargs': {'urls': [r['url'] for r in TEST_RESPONSES['500']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': TEST_RESPONSES['500']},
    ],
    'get_mock': [
        {'args': ('risk', '01-05-2020', '15-11-2020'),
         'expected': [r for r in TEST_RESPONSES['200_risk']]},
        {'args': ('statements', '01-05-2020', '15-11-2020'),
         'expected': [r for r in TEST_RESPONSES['200_statements']]},
    ],
    'get_live': [
        {'args': ('risk', '01-05-2019', '15-12-2019'),
         'expected': ['2019q2_rr1.zip', '2019q3_rr1.zip', '2019q4_rr1.zip']},
    ]
}


# FIXTURES

@pytest.fixture(scope='function', params=TESTCASES['_get'])
def _get_params(request):

    kwargs = request.param['kwargs']
    rsps = request.param['expected']
    return kwargs, rsps


@pytest.fixture(scope='function', params=TESTCASES['_get_error'])
def _get_error_params(request):

    kwargs = request.param['kwargs']
    rsps = request.param['expected']
    return kwargs, rsps


@pytest.fixture(scope='function', params=TESTCASES['get_mock'])
def get_mock_params(request):

    kwargs = request.param['kwargs']
    rsps = request.param['expected']
    return kwargs, rsps


@pytest.fixture(scope='function', params=TESTCASES['get_live'])
def get_live_params(request):

    dataset, *args = request.param['args']
    expected = request.param['expected']
    return (dataset, *args), expected


# UNIT TESTS

@responses.activate
def test_get_(_get_params, tmp_data_directory):
    """Downloads and saves body content from test urls.
    """
    kwargs = _get_params[0]
    # Create tmpdir and set in kwargs
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    kwargs['dir'] = tmpdir

    rsps = _get_params[1]
    contents = [r['body'] for r in rsps]
    for r in rsps:
        responses.add(responses.Response(**r))
    _get(**kwargs)

    saved = []
    for filename in os.listdir(tmpdir):
        with open(os.path.join(tmpdir, filename), 'r') as f:
            saved.append(f.read())
    result = sorted(''.join(saved))
    expected = sorted(''.join(contents))

    shutil.rmtree(str(tmpdir))
    assert result == expected


@responses.activate
def test_get_error(_get_error_params, tmp_data_directory, caplog):
    """Captures HTTPError and MaxRetryError exceptions.
    """
    kwargs = _get_params[0]
    # Create tmpdir and set in kwargs
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    kwargs['dir'] = tmpdir

    rsps = _get_error_params[1]
    responses.add(responses.Response(**rsps))

    _get(**kwargs)

    shutil.rmtree(str(tmpdir))
    assert str(rsps['status']) in caplog.text


@responses.activate
def test_get_mock(get_mock_params):
    """(Mock test) Downloads and saves every relevant DERA
    dataset between start_date and end_date.
    """




@pytest.mark.webtest
def test_get_live(get_params, tmp_data_directory):
    """(Live test) Downloads and saves every relevant DERA dataset
    between start_date and end_date.
    """

    dataset, *args = get_params[0]
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)

    get_DERA(dataset, tmpdir, *args)
    saved = [os.path.isfile(f'{tmpdir}/{f}') for f in get_params[1]]

    shutil.rmtree(str(tmpdir))
    assert all(saved)


if __name__ == "__main__":
    pass
