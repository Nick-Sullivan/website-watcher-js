import json
from time import sleep

import pytest
from domain_models.domain import Frequency, Scrape, Website, create_unique_key, now
from handler.schedule_scrapes import schedule_scrapes
from infrastructure import scrape_queue, scrape_store, website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    website_store.create(Website(user_id=user_id, website_id='1', name='One', url='https://one.com', frequency=Frequency.DAILY))
    website_store.create(Website(user_id=user_id, website_id='2', name='Two', url='https://two.com', frequency=Frequency.DAILY))
    scrape_store.create(Scrape(user_id=user_id, website_id='2', scrape_id='2', scraped_at=now()))
    try:
        yield {'user_id': user_id, 'website_id': '1', 'other_website_id': '2'}
    finally:
        website_store.delete(user_id, '1')
        website_store.delete(user_id, '2')


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield schedule_scrapes({'body': json.dumps(request), 'requestContext': context})


@pytest.fixture(scope='module')
def response_body(response):
    body = json.loads(response['body'])
    yield body


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_websites_that_were_added_to_scrape_queue(setup, response_body):
    for website in response_body['websites']:
        record = scrape_queue.get_record(
            user_id=website['user_id'],
            website_id=website['website_id'])
        assert record is not None


def test_it_adds_websites_to_scrape_queue(setup, response_body):
    updated_website_ids = [w['website_id'] for w in response_body['websites']]
    assert setup['website_id'] in updated_website_ids


def test_it_doesnt_add_websites_that_have_recently_been_scraped(setup, response_body):
    updated_website_ids = [w['website_id'] for w in response_body['websites']]
    assert setup['other_website_id'] not in updated_website_ids
