import os
import pytest
import requests
import responses
import shutil

from requests_toolbelt import sessions

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from getgar.scrapper.client import _get
from getgar.scrapper.client import get_DERA


### TESTCASES

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

RESPONSES = {
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
}

TESTCASES = {
    '_get': [
        {'args': ([r for r in RESPONSES['200']], '_get', test_http, 3, 1, 2, 1)},
    ],
    '_get_error': [
        {'args': ([RESPONSES['403']], '_get_error', test_http, 3, 1, 2, 1)},
        {'args': ([RESPONSES['500']], '_get_error', test_http, 3, 1, 2, 1)}
    ],
    'get': [
        {'args': ('risk', 'get', '01-05-2019', '15-12-2019'),
         'expected': ['2019q2_rr1.zip', '2019q3_rr1.zip']}
    ]
}


### FIXTURES

@pytest.fixture(scope='function', params=TESTCASES['_get'])
def _get_params(request):

    rsps, *args = request.param['args']
    urls = [r['url'].split('/')[-1] for r in rsps]
    
    return (urls, *args), rsps 


@pytest.fixture(scope='function', params=TESTCASES['_get_error'])
def _get_error_params(request):

    rsps, *args = request.param['args']
    urls = [r['url'].split('/')[-1] for r in rsps]
    
    return (urls, *args), rsps


@pytest.fixture(scope='function', params=TESTCASES['get'])
def get_params(request):

    dataset, dir, *args = request.param['args']
    expected = request.param['expected']

    return (dataset, dir, *args), expected 


### UNIT TESTS

@responses.activate
def test_get_(_get_params, tmp_data_directory):
    """Downloads and saves files from test urls.
    """
    urls, dir, *req = _get_params[0]
    tmpdir = f'{tmp_data_directory}/{dir}'
    os.mkdir(tmpdir)

    rsps = _get_params[1]
    contents = [r['body'] for r in rsps]
    for r in rsps:
        responses.add(responses.Response(**r))
    
    _get(urls, tmpdir, *req)

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

    urls, dir, *req = _get_error_params[0]
    tmpdir = f'{tmp_data_directory}/{dir}'
    os.mkdir(tmpdir)

    rsps = _get_error_params[1][0]
    responses.add(responses.Response(**rsps))

    _get(urls, tmpdir, *req)

    shutil.rmtree(str(tmpdir))
    assert str(rsps['status']) in caplog.text


def test_get(get_params, tmp_data_directory):
    """Downloads and saves files from DERA.
    """

    dataset, dir, *args = get_params[0]
    tmpdir = f'{tmp_data_directory}/{dir}'
    os.mkdir(tmpdir)

    get_DERA(dataset, tmpdir, *args)
    saved = [os.path.isfile(f'{tmpdir}/{f}') for f in get_params[1]]

    print(saved)
    shutil.rmtree(str(tmpdir))
    assert all(saved)