from time import sleep

import pytest

from .endpoints import create_website, delete_website, get_scrapes, schedule_scrapes


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
    schedule_req = {}
    yield schedule_scrapes(schedule_req)


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


@pytest.fixture(scope='module')
def get_scrape_response_body(setup, response):
    wait_for_scraping_to_be_invoked()
    get_scrapes_req = {'website_id': setup['website_id']}
    get_scrapes_res = get_scrapes(get_scrapes_req)
    yield get_scrapes_res.json()


def wait_for_scraping_to_be_invoked():
    sleep(10)


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_websites_for_this_user(setup, response_body):
    assert 'websites' in response_body
    assert len(response_body['websites']) == 1
    assert response_body['websites'][0]['website_id'] == setup['website_id']


def test_it_triggered_scraping(setup, get_scrape_response_body):
    assert len(get_scrape_response_body['scrapes']) == 1
    assert get_scrape_response_body['scrapes'][0]['website_id'] == setup['website_id']
