
import pytest

from .endpoints import create_website, delete_website


@pytest.fixture(scope='module')
def response():
    request = {'name': 'website_one', 'url': 'https://google.com'}
    response = create_website(request)
    yield response


@pytest.fixture(scope='module')
def response_body(response):
    body = response.json()
    try:
        yield body
    finally:
        delete_req = {'website_id': body['website_id']}
        delete_website(delete_req)


def test_it_returns_status_200(response, response_body):
    assert response.status_code == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body
