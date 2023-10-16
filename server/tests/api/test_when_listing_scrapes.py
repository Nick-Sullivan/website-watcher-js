
import pytest

from .endpoints import create_website, delete_website, get_scrapes, scrape_website


@pytest.fixture(scope='module')
def setup():

    create_req = {'name': 'website_one', 'url': 'https://google.com'}
    create_res = create_website(create_req)
    website_id = create_res.json()['website_id']

    scrape_req = {'website_id': website_id}
    scrape_res = scrape_website(scrape_req)
    scrape_id = scrape_res.json()['scrape_id'] 

    try:    
        yield {'website_id': website_id, 'scrape_id': scrape_id}
    finally:
        delete_req = {'website_id': website_id}
        delete_website(delete_req)


@pytest.fixture(scope='module')
def response(setup):
    get_scrapes_req = {'website_id': setup['website_id']}
    yield get_scrapes(get_scrapes_req)


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


@pytest.fixture(scope='module')
def response_scrape(setup, response_body):
    matching = [s for s in response_body['scrapes'] if s['scrape_id'] == setup['scrape_id']]
    assert len(matching) == 1
    yield matching[0]


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_scrape_id(setup, response_scrape):
    assert response_scrape['scrape_id'] == setup['scrape_id']


def test_it_returns_website_id(setup, response_scrape):
    assert response_scrape['website_id'] == setup['website_id']


def test_it_returns_scraped_at(response_scrape):
    assert response_scrape['scraped_at'] is not None
