from time import sleep

import pytest

from .endpoints import create_website, delete_website, get_scrapes
from .eventbridge import publish_scrape_schedule_event


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
    yield publish_scrape_schedule_event()


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


def test_it_successfully_added_the_event(response):
    assert len(response['Entries']) == 1


def test_it_triggered_scraping(setup, get_scrape_response_body):
    assert len(get_scrape_response_body['scrapes']) == 1
    assert get_scrape_response_body['scrapes'][0]['website_id'] == setup['website_id']
