import json

import pytest
from domain_models.domain import Scrape, create_unique_key, now
from handler.get_scrapes import get_scrapes
from infrastructure import scrape_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    scrape_store.create(Scrape(user_id=user_id, website_id='1', scrape_id='1', scraped_at=now()))
    scrape_store.create(Scrape(user_id=user_id, website_id='1', scrape_id='2', scraped_at=now()))
    scrape_store.create(Scrape(user_id=user_id, website_id='2', scrape_id='3', scraped_at=now()))
    try:
        yield {'user_id': user_id, 'website_id': '1'}
    finally:
        scrape_store.delete(user_id, '1', '1')
        scrape_store.delete(user_id, '1', '2')
        scrape_store.delete(user_id, '2', '3')


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield get_scrapes({
        'body': json.dumps(request),
        'requestContext': context,
        'pathParameters': {'website_id': setup['website_id']}})


@pytest.fixture
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_scrapes_for_this_user(response_body):
    assert 'scrapes' in response_body
    assert len(response_body['scrapes']) == 2
    assert response_body['scrapes'][0]['scrape_id'] == '1'
    assert response_body['scrapes'][1]['scrape_id'] == '2'


def test_it_returns_scrape_id(response_body):
    assert response_body['scrapes'][0]['scrape_id'] == '1'
    assert response_body['scrapes'][1]['scrape_id'] == '2'


def test_it_returns_website_id(response_body):
    assert response_body['scrapes'][0]['website_id'] == '1'
    assert response_body['scrapes'][1]['website_id'] == '1'


def test_it_returns_scraped_at(response_body):
    assert response_body['scrapes'][0]['scraped_at'] is not None
    assert response_body['scrapes'][1]['scraped_at'] is not None