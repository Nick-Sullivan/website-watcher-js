import json

import pytest
from domain_models.domain import Frequency, Website, create_unique_key
from handler.scrape_website import scrape_website
from infrastructure import scrape_store, screenshot_store, website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    website_store.create(Website(user_id=user_id, website_id='1', name='One', url='https://one.com', frequency=Frequency.DAILY))
    try:
        yield {'user_id': user_id, 'website_id': '1'}
    finally:
        website_store.delete(user_id, '1')


@pytest.fixture(scope='module')
def response(setup):
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield scrape_website({
        'requestContext': context,
        'pathParameters': {'website_id': setup['website_id']}})


@pytest.fixture(scope='module')
def response_body(response):
    body = json.loads(response['body'])
    try:
        yield body
    finally:
        scrape_store.delete(body['user_id'], body['website_id'], body['scrape_id'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body


def test_it_returns_scrape_id(response_body):
    assert 'scrape_id' in response_body


def test_it_saves_website_in_db(response_body):
    scrape = scrape_store.get(
        user_id=response_body['user_id'],
        website_id=response_body['website_id'],
        scrape_id=response_body['scrape_id'])
    
    assert scrape is not None


def test_it_saves_screenshot_in_s3(response_body):
    scrape = scrape_store.get(
        user_id=response_body['user_id'],
        website_id=response_body['website_id'],
        scrape_id=response_body['scrape_id'])
        
    screenshot = screenshot_store.get(scrape)
    
    assert screenshot is not None
    