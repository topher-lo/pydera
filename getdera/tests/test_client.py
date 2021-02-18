import os
import pytest
import responses
import shutil

from requests_toolbelt import sessions
from getdera import utils

from getdera.scrapper.client import _get
from getdera.scrapper.client import get_DERA


# TESTCASES
TEST_SESSION_URL = "https://www.testingsec.gov/files/dera/data/dir"
TEST_URL = "https://www.testingsec.gov/files/dera/data"
DERA_URLS = {
    'statements': 'https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets',
    'risk': 'https://www.sec.gov/files/dera/data/mutual-fund-prospectus-risk/return-summary-data-sets'
}

# SESSION SET-UP
test_http = sessions.BaseUrlSession(base_url=TEST_SESSION_URL)
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
    '403': [{'url': f'{TEST_URL}/2019q1_rr1.zip',
             'method': 'GET',
             'status': 403}],
    '500': [{'url': f'{TEST_URL}/2019q2_rr1.zip',
             'method': 'GET',
             'status': 500}],
    '200_risk': [
        {'url': '{}/2020q2_rr1.zip'.format(DERA_URLS['risk']),
         'method': 'GET',
         'status': 200},
        {'url': '{}/2020q3_rr1.zip'.format(DERA_URLS['risk']),
         'method': 'GET',
         'status': 200},
        {'url': '{}/2020q4_rr1.zip'.format(DERA_URLS['risk']),
         'method': 'GET',
         'status': 200},
    ],
    '200_statements': [
        {'url': '{}/2020q2_notes.zip'.format(DERA_URLS['statements']),
         'method': 'GET',
         'status': 200},
        {'url': '{}/2020q3_notes.zip'.format(DERA_URLS['statements']),
         'method': 'GET',
         'status': 200},
        {'url': '{}/2020_10_notes.zip'.format(DERA_URLS['statements']),
         'method': 'GET',
         'status': 200},
        {'url': '{}/2020_11_notes.zip'.format(DERA_URLS['statements']),
         'method': 'GET',
         'status': 200},
    ]
}

TESTCASES = {
    '_get': [
        {'kwargs': {'urls': [r['url'].split('/')[-1] for r
                             in TEST_RESPONSES['200']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': [r for r in TEST_RESPONSES['200']]},
    ],
    '_get_error': [
        {'kwargs': {'urls': [r['url'].split('/')[-1] for r
                             in TEST_RESPONSES['403']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': [r for r in TEST_RESPONSES['403']]},
        {'kwargs': {'urls': [r['url'].split('/')[-1] for r
                             in TEST_RESPONSES['500']],
                    'dir': 'TEMPORARY',
                    'session': test_http,
                    'chunk_size': 3,
                    'timeout': 1,
                    'retry': 2,
                    'delay': 1},
         'expected': [r for r in TEST_RESPONSES['500']]},
    ],
    'get_mock': [
        {'args': ('risk', '31-03-2020', '01-10-2020'),
         'expected': ([r for r in TEST_RESPONSES['200_risk']],
                      ['2020q2_rr1.zip', '2020q3_rr1.zip', '2020q4_rr1.zip'])},
        {'args': ('statements', '31-03-2020', '15-11-2020'),
         'expected': ([r for r in TEST_RESPONSES['200_statements']],
                      ['2020q2_notes.zip', '2020q3_notes.zip',
                       '2020_10_notes.zip', '2020_11_notes.zip'])},
    ],
    'get_live': [
        {'args': ('risk', '01-05-2019', '15-12-2019'),
         'expected': ['2019q3_rr1.zip', '2019q4_rr1.zip']},
    ],
}


# FIXTURES

def register_mock_responses(mocks):
    for r in mocks:
        responses.add(responses.Response(**r))


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

    args = request.param['args']
    rsps = request.param['expected'][0]
    file_names = request.param['expected'][1]
    return args, rsps, file_names


@pytest.fixture(scope='function', params=TESTCASES['get_live'])
def get_live_params(request):

    args = request.param['args']
    expected = request.param['expected']
    return args, expected


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

    # Mock responses content
    rsps = _get_params[1]
    contents = [r['body'] for r in rsps]
    register_mock_responses(rsps)
    _get(**kwargs)  # Test _get

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

    kwargs = _get_error_params[0]
    # Create tmpdir and set in kwargs
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)
    kwargs['dir'] = tmpdir

    # Register mock response
    rsps = _get_error_params[1]
    register_mock_responses(rsps)

    _get(**kwargs)  # Test _get

    shutil.rmtree(str(tmpdir))
    assert all([str(r['status']) in caplog.text for r in rsps])


@responses.activate
def test_get_mock(get_mock_params, tmp_data_directory):
    """(Mock test) Downloads and saves every relevant DERA
    dataset between start_date and end_date.
    """

    dataset, *args = get_mock_params[0]
    # Create tmpdir
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)

    # Register mock response
    rsps = get_mock_params[1]
    register_mock_responses(rsps)

    get_DERA(dataset, tmpdir, *args)  # Test get_DERA

    saved = [os.path.isfile(f'{tmpdir}/{f}') for f in get_mock_params[2]]
    shutil.rmtree(str(tmpdir))
    assert all(saved)


@pytest.mark.webtest
def test_get_live(get_live_params, tmp_data_directory):
    """(Live test) Downloads and saves every relevant DERA dataset
    between start_date and end_date.
    """

    dataset, *args = get_live_params[0]
    tmpdir = tmp_data_directory
    utils.make_path(tmpdir)

    get_DERA(dataset, tmpdir, *args)  # Test get_DERA

    saved = [os.path.isfile(f'{tmpdir}/{f}') for f in get_live_params[1]]
    shutil.rmtree(str(tmpdir))
    assert all(saved)


if __name__ == "__main__":
    pass
