import json

import pytest
from domain_models.domain import Scrape, create_unique_key, now
from handler.get_screenshot import get_screenshot
from infrastructure import scrape_store, screenshot_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    scrape = Scrape(user_id=user_id, website_id='wid', scrape_id='sid', scraped_at=now())
    scrape_store.create(scrape)
    screenshot_store.save(scrape, screenshot='screenshot')
    try:
        yield {'user_id': user_id, 'website_id': 'wid', 'scrape_id': 'sid'}
    finally:
        screenshot_store.delete(scrape)
        scrape_store.delete(scrape.user_id, scrape.website_id, scrape.scrape_id)


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id'], 'website_id': setup['website_id'], 'scrape_id': setup['scrape_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    path_params= {'website_id': setup['website_id'], 'scrape_id': setup['scrape_id']}
    yield get_screenshot({
        'body': json.dumps(request),
        'pathParameters': path_params,
        'requestContext': context})


@pytest.fixture
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_scrape_id(response_body):
    assert 'scrape_id' in response_body


def test_it_returns_screenshot_url(response_body):
    assert 'screenshot_url' in response_body