
import pytest

from .endpoints import create_website, delete_website, scrape_website


@pytest.fixture(scope='module')
def setup():

    create_req = {'name': 'website_one', 'url': 'https://google.com'}
    create_res = create_website(create_req)
    website_id = create_res.json()['website_id']
    
    try:
        yield {'website_id': website_id}
    finally:
        delete_req = {'website_id': website_id}
        delete_website(delete_req)


@pytest.fixture(scope='module')
def response(setup):
    scrape_req = {'website_id': setup['website_id']}
    yield scrape_website(scrape_req)


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_scrape_id(response_body):
    assert 'scrape_id' in response_body


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body
