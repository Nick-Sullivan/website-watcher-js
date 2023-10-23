
import pytest

from .endpoints import options_website


@pytest.fixture(scope='module')
def response():
    response = options_website('http://localhost:3000')
    yield response


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_allows_localhost_origin(response):
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'


def test_it_allows_auth_headers(response):
    assert 'Authorization' in response.headers['Access-Control-Allow-Headers']


def test_it_allows_get_method(response):
    assert 'GET' in response.headers['Access-Control-Allow-Methods']


def test_it_allows_options_method(response):
    assert 'OPTIONS' in response.headers['Access-Control-Allow-Methods']


def test_it_allows_credentials(response):
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'
