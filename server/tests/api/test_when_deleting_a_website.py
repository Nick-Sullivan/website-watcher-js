
import pytest

from .endpoints import (
    create_website,
    delete_website,
    get_scrapes,
    get_websites,
    scrape_website,
)


@pytest.fixture(scope='module')
def setup():
    create_req = {'name': 'website_one', 'url': 'https://google.com'}
    create_res = create_website(create_req)
    website_id = create_res.json()['website_id']

    scrape_req = {'website_id': website_id}
    scrape_res = scrape_website(scrape_req)
    scrape_id = scrape_res.json()['scrape_id']

    yield {'website_id': website_id, 'scrape_id': scrape_id}


@pytest.fixture(scope='module')
def response(setup):
    delete_req = {'website_id': setup['website_id']}
    delete_res = delete_website(delete_req)
    yield delete_res


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


@pytest.fixture(scope='module')
def get_websites_response_body(setup, response):
    response = get_websites()
    yield response.json()


@pytest.fixture(scope='module')
def get_scrapes_response_body(setup, response):
    request = {'website_id': setup['website_id']}
    response = get_scrapes(request)
    yield response.json()


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_deleted_the_website(setup, get_websites_response_body):
    matching = [
        w for w in get_websites_response_body['websites']
        if w['website_id'] == setup['website_id']]
    assert len(matching) == 0


def test_it_deleted_the_scrapes(setup, get_scrapes_response_body):
    matching = [
        s for s in get_scrapes_response_body['scrapes']
        if s['scrape_id'] == setup['scrape_id']]
    assert len(matching) == 0