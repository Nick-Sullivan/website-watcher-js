
import pytest

from .endpoints import create_website, delete_website, get_websites


@pytest.fixture(scope='module')
def setup():
    website_requests = [
        {'name': 'website_one', 'url': 'https://google.com'},
        {'name': 'website_two', 'url': 'https://google.com'},
    ]
    website_responses = [create_website(req).json() for req in website_requests]
    website_ids = [res['website_id'] for res in website_responses]
    try:
        yield {'website_ids': website_ids}
    finally:
        for website_id in website_ids:
            delete_req = {'website_id': website_id}
            delete_website(delete_req)


@pytest.fixture(scope='module')
def response(setup):
    yield get_websites()


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_websites_for_this_user(setup, response_body):
    assert 'websites' in response_body
    for website_id in setup['website_ids']:
        matching = [w for w in response_body['websites'] if w['website_id'] == website_id]
        assert len(matching) == 1
